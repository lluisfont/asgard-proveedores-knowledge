param([string]$Root = (Resolve-Path ".").Path)
$ErrorActionPreference = "Stop"
$manifest = Get-Content -LiteralPath (Join-Path $Root "knowledge\manifest.json") -Raw | ConvertFrom-Json
$audited = $manifest.repository.audited_commit
$head = $null
if (Test-Path -LiteralPath (Join-Path $Root ".git")) {
  $head = (& git.exe -C $Root rev-parse HEAD 2>$null)
  if ($LASTEXITCODE -ne 0) { $head = $null }
}
$changed = @()
$dirty = @()
$codeCovered = $false
$standalone = -not (Test-Path -LiteralPath (Join-Path $Root "index.php"))
$schemaCovered = $false
if ($manifest.coverage -and $manifest.coverage.database_schema -eq "verified_for_audited_commit") {
  $schemaCovered = $true
}
$covered = $false
$action = if ($audited) { "unknown" } else { "no_confirmed_audited_commit_use_hash_comparison_and_refresh_audits" }
if ($standalone) {
  $action = "knowledge_repository_documents_a_pinned_snapshot_use_application_checkout_for_code_coverage"
} elseif ($head -and $audited) {
  & git.exe -C $Root cat-file -e "$audited^{commit}" 2>$null
  $auditedExists = $LASTEXITCODE -eq 0
  if ($auditedExists) {
    $args = @("diff", "--name-only", "$audited..$head", "--") + @($manifest.repository.functional_paths)
    $changed = @(& git.exe -C $Root @args 2>$null | Where-Object { $_ })
    $dirtyLines = @(& git.exe -C $Root status --porcelain -- @($manifest.repository.functional_paths) 2>$null | Where-Object { $_ })
    $dirty = @($dirtyLines)
    $codeCovered = $changed.Count -eq 0 -and $dirty.Count -eq 0
    $covered = $codeCovered -and $schemaCovered
    $action = if (-not $codeCovered) { "refresh_impacted_audits_before_trusting_knowledge" } elseif (-not $schemaCovered) { "provide_and_verify_master_database_schema" } else { "none_for_audited_scope" }
  } else {
    $action = "audited_commit_not_available_in_this_checkout"
  }
}
$out = Join-Path $Root "knowledge\snapshots\current"
New-Item -ItemType Directory -Force -Path $out | Out-Null
$result = [pscustomobject]@{
  generated_at = (Get-Date).ToUniversalTime().ToString("yyyy-MM-ddTHH:mm:ssZ")
  current_head = $head
  audited_commit = $audited
  functional_paths_checked = @($manifest.repository.functional_paths)
  changed_functional_path_count = $changed.Count
  changed_functional_paths = $changed
  uncommitted_functional_changes = $dirty
  source_snapshot_code_matches = $codeCovered
  master_database_schema_verified = $schemaCovered
  standalone_knowledge_repository = $standalone
  code_and_database_covered_by_existing_audit = $covered
  required_action = $action
}
$result | ConvertTo-Json -Depth 10 | Set-Content -LiteralPath (Join-Path $out "code-db-audit-coverage.json") -Encoding UTF8
$verdict = if ($covered) { "PASS - existing audit covers current functional code/database scope." } else { "PARTIAL - source, database or deployment coverage remains unverified; review required_action." }
$rows = @()
foreach ($p in @($manifest.repository.functional_paths)) { $rows += "| ``$p`` | checked |" }
$changedRows = @()
foreach ($p in $changed) { $changedRows += "| ``$p`` | changed |" }
if ($changedRows.Count -eq 0) { $changedRows += "| none reported | This alone does not prove database or deployment coverage |" }
$md = "# Code / Database Audit Coverage`n`n## Verdict`n`n$verdict`n`n| Field | Value |`n| --- | --- |`n| Audited commit | ``$audited`` |`n| Current HEAD | ``$head`` |`n| Changed functional paths | $($changed.Count) |`n| Required action | ``$action`` |`n`n## Checked Scope`n`n| Path | Status |`n| --- | --- |`n$($rows -join "`n")`n`n## Functional Changes`n`n| Path | Status |`n| --- | --- |`n$($changedRows -join "`n")"
Set-Content -LiteralPath (Join-Path $out "code-db-audit-coverage.md") -Value $md -Encoding UTF8
Write-Host $verdict

