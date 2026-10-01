param([string]$Root = (Resolve-Path ".").Path)
$ErrorActionPreference = "Stop"
$required = @(
  "knowledge\README.md",
  "knowledge\install.md",
  "knowledge\manifest.json",
  "knowledge\openspec\context.md",
  "knowledge\openspec\guardrails.md",
  "knowledge\openspec\impact-rules.md",
  "knowledge\operations\programmer-branch-runbook.md",
  "scripts\knowledge\validate.ps1",
  "scripts\knowledge\update.ps1",
  "scripts\knowledge\install-knowledge-pack.ps1",
  "scripts\knowledge\verify-audit-coverage.ps1",
  "scripts\knowledge\compare-github-local.ps1"
)
$missing = @()
foreach ($path in $required) {
  if (-not (Test-Path -LiteralPath (Join-Path $Root $path))) { $missing += $path }
}
if ($missing.Count -gt 0) { throw "Missing Knowledge Pack files:`n$($missing -join "`n")" }
Get-Content -LiteralPath (Join-Path $Root "knowledge\manifest.json") -Raw | ConvertFrom-Json | Out-Null
Write-Host "Knowledge Pack validation PASS"

