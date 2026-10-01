param(
  [string]$Root = (Resolve-Path ".").Path,
  [string]$Remote = "origin",
  [string]$Branch = "main",
  [string]$LocalRef = "HEAD"
)
$ErrorActionPreference = "Stop"
function Invoke-GitCommand([string[]]$GitArgs) {
  $r = & git.exe -C $Root @GitArgs 2>$null
  if ($LASTEXITCODE -ne 0) { throw "git $($GitArgs -join ' ') failed" }
  return @($r)
}
function Impact([string]$Path, [object]$Manifest) {
  $p = $Path -replace "\\","/"
  $items = New-Object System.Collections.Generic.List[string]
  foreach ($fp in @($Manifest.repository.functional_paths)) {
    if ($p -eq $fp -or $p.StartsWith("$fp/")) { $items.Add("source-code") }
  }
  if ($p -match "^knowledge/|^scripts/knowledge/|^source-audits/|^QUICK_START\.md$|^README\.md$|^KNOWLEDGE_PACK\.md$|^\.gitignore$") { $items.Add("knowledge") }
  if ($p -match "^\.github/") { $items.Add("ci") }
  if ($items.Count -eq 0) { $items.Add("unclassified") }
  return @($items | Select-Object -Unique)
}
$manifest = Get-Content -LiteralPath (Join-Path $Root "knowledge\manifest.json") -Raw | ConvertFrom-Json
if (Test-Path -LiteralPath (Join-Path $Root ".git")) {
  $remoteUrl = $null
  try { $remoteUrl = @(Invoke-GitCommand @("remote", "get-url", $Remote))[0] } catch {}
  if ($remoteUrl) {
    try { Invoke-GitCommand @("fetch", $Remote, $Branch, "--quiet") | Out-Null } catch {}
  }
}
$remoteRef = "$Remote/$Branch"
$remoteSha = try { @(Invoke-GitCommand @("rev-parse", $remoteRef))[0] } catch { $null }
$localSha = try { @(Invoke-GitCommand @("rev-parse", $LocalRef))[0] } catch { $null }
$changes = @()
if ($remoteSha) {
  $lines = @(Invoke-GitCommand @("diff", "--name-status", $remoteRef))
  foreach ($line in $lines) {
    $parts = $line -split "`t"
    if ($parts.Count -ge 2) {
      $path = $parts[-1]
      $changes += [pscustomobject]@{ source="working-tree-vs-github"; status=$parts[0]; path=$path; impact=@(Impact $path $manifest) }
    }
  }
}
$untracked = try { @(Invoke-GitCommand @("ls-files", "--others", "--exclude-standard")) } catch { @() }
$untracked = @($untracked | Where-Object {
  $_ -and
  $_ -notmatch '^knowledge/' -and
  $_ -notmatch '^scripts/knowledge/' -and
  $_ -notmatch '^source-audits/' -and
  $_ -ne 'KNOWLEDGE_PACK.md'
})
foreach ($path in $untracked) {
  if ($path) { $changes += [pscustomobject]@{ source="untracked-local"; status="??"; path=$path; impact=@(Impact $path $manifest) } }
}
$out = Join-Path $Root "knowledge\snapshots\current"
New-Item -ItemType Directory -Force -Path $out | Out-Null
$impacts = @($changes | ForEach-Object { $_.impact } | Select-Object -Unique | Sort-Object)
$result = [pscustomobject]@{
  generated_at = (Get-Date).ToUniversalTime().ToString("yyyy-MM-ddTHH:mm:ssZ")
  github_ref = $remoteRef
  github_sha = $remoteSha
  local_ref = $LocalRef
  local_sha = $localSha
  changed_path_count = @($changes | Select-Object -ExpandProperty path -Unique).Count
  impacts = $impacts
  changes = $changes
}
$result | ConvertTo-Json -Depth 12 | Set-Content -LiteralPath (Join-Path $out "github-local-diff.json") -Encoding UTF8
$rows = @()
foreach ($c in $changes) { $rows += "| $($c.source) | $($c.status) | ``$($c.path)`` | $(@($c.impact) -join ', ') |" }
if ($rows.Count -eq 0) { $rows += "| none | - | - | - |" }
$md = "# GitHub / Local Diff`n`n| Field | Value |`n| --- | --- |`n| GitHub ref | ``$remoteRef`` |`n| GitHub SHA | ``$remoteSha`` |`n| Local SHA | ``$localSha`` |`n| Changed paths | $($result.changed_path_count) |`n`n## Impacts`n`n$($impacts -join ', ')`n`n## Changes`n`n| Source | Status | Path | Impact |`n| --- | --- | --- | --- |`n$($rows -join "`n")"
Set-Content -LiteralPath (Join-Path $out "github-local-diff.md") -Value $md -Encoding UTF8
Write-Host "GitHub/local comparison written"

