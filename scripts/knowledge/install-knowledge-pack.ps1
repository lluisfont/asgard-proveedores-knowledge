param(
  [Parameter(Mandatory = $true)]
  [string]$TargetRepo,
  [string]$KnowledgeRepo = ""
)
$ErrorActionPreference = "Stop"
function Resolve-KnowledgeRoot {
  param([string]$Explicit)
  if ($Explicit) {
    $resolved = (Resolve-Path $Explicit).Path
    if (Test-Path -LiteralPath (Join-Path $resolved "knowledge\manifest.json")) { return $resolved }
    throw "KnowledgeRepo does not contain knowledge\manifest.json: $resolved"
  }
  $candidates = @(
    $PSScriptRoot,
    (Join-Path $PSScriptRoot ".."),
    (Join-Path $PSScriptRoot "..\..")
  )
  foreach ($candidate in $candidates) {
    try {
      $resolved = (Resolve-Path $candidate).Path
      if (Test-Path -LiteralPath (Join-Path $resolved "knowledge\manifest.json")) { return $resolved }
    } catch {}
  }
  throw "Cannot resolve Knowledge repo root. Pass -KnowledgeRepo explicitly."
}
$KnowledgeRepo = Resolve-KnowledgeRoot -Explicit $KnowledgeRepo
$target = (Resolve-Path $TargetRepo).Path
if ($target -eq $KnowledgeRepo) { throw "Knowledge source and application checkout must be different directories" }
foreach ($dir in @("knowledge", "scripts\knowledge", "scripts\audit", "scripts\transfer", "source-audits")) {
  $src = Join-Path $KnowledgeRepo $dir
  if (Test-Path -LiteralPath $src) {
    $dst = Join-Path $target $dir
    $resolvedDestination = [IO.Path]::GetFullPath($dst)
    $resolvedRoot = [IO.Path]::GetFullPath($target).TrimEnd('\', '/') + [IO.Path]::DirectorySeparatorChar
    if (-not $resolvedDestination.StartsWith($resolvedRoot, [StringComparison]::OrdinalIgnoreCase)) {
      throw "Knowledge destination is outside the requested checkout: $resolvedDestination"
    }
    if ((Test-Path -LiteralPath $dst) -and ((Get-Item -LiteralPath $dst -Force).Attributes -band [IO.FileAttributes]::ReparsePoint)) {
      throw "Knowledge destination cannot be a junction or symbolic link: $dst"
    }
    New-Item -ItemType Directory -Force -Path (Split-Path $dst -Parent) | Out-Null
    if (Test-Path -LiteralPath $dst) { Remove-Item -LiteralPath $dst -Recurse -Force }
    Copy-Item -LiteralPath $src -Destination $dst -Recurse -Force
  }
}
$kp = "# Knowledge Pack Installed`n`nRun on every branch:`n`n````powershell`n.\scripts\knowledge\update.ps1`n````"
Set-Content -LiteralPath (Join-Path $target "KNOWLEDGE_PACK.md") -Value $kp -Encoding UTF8
$gitignorePath = Join-Path $target ".gitignore"
$ignoreBlock = @"

# Knowledge Pack local install
knowledge/
scripts/knowledge/
scripts/audit/
scripts/transfer/
source-audits/
KNOWLEDGE_PACK.md
"@
if (Test-Path -LiteralPath $gitignorePath) {
  $existingIgnore = Get-Content -LiteralPath $gitignorePath -Raw
  if ($existingIgnore -notmatch "Knowledge Pack local install") {
    Add-Content -LiteralPath $gitignorePath -Value $ignoreBlock -Encoding UTF8
  }
} else {
  Set-Content -LiteralPath $gitignorePath -Value $ignoreBlock.TrimStart() -Encoding UTF8
}
& (Join-Path $target "scripts\knowledge\validate.ps1") -Root $target
Write-Host "Knowledge Pack installed in $target"

