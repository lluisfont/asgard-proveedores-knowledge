param([string]$Root=(Resolve-Path ".").Path); & (Join-Path $PSScriptRoot "validate.ps1") -Root $Root

