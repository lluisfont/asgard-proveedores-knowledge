param(
  [string]$Root = (Resolve-Path ".").Path,
  [switch]$CopyStandalone
)
$ErrorActionPreference = "Stop"
& (Join-Path $PSScriptRoot "compare-github-local.ps1") -Root $Root
& (Join-Path $PSScriptRoot "verify-audit-coverage.ps1") -Root $Root
& (Join-Path $PSScriptRoot "validate.ps1") -Root $Root
$coverage = Get-Content -LiteralPath (Join-Path $Root "knowledge\snapshots\current\code-db-audit-coverage.json") -Raw | ConvertFrom-Json
if (-not $coverage.code_and_database_covered_by_existing_audit) {
  throw "Knowledge structure is valid, but code/database audit coverage is PARTIAL or unknown. Review coverage evidence before trusting the baseline."
}
Write-Host "Incremental knowledge update PASS"

