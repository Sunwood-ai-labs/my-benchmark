param(
    [Parameter(Mandatory = $true)]
    [string]$FixtureId,
    [Parameter(Mandatory = $true)]
    [string]$RunLabel
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

$repoRoot = Split-Path -Parent $PSScriptRoot
$fixtureRoot = Join-Path $repoRoot "benchmark\runtime_fixtures\$FixtureId"

if (-not (Test-Path -LiteralPath $fixtureRoot)) {
    throw "Fixture not found: $fixtureRoot"
}

$workspaceTemplate = Join-Path $fixtureRoot "workspace"
if (-not (Test-Path -LiteralPath $workspaceTemplate)) {
    throw "Workspace template not found: $workspaceTemplate"
}

$stamp = Get-Date -Format "yyyyMMdd-HHmmss"
$safeLabel = ($RunLabel -replace "[^a-zA-Z0-9._-]", "-").Trim("-")
if ([string]::IsNullOrWhiteSpace($safeLabel)) {
    $safeLabel = "manual"
}

$runDirName = "{0}_{1}_{2}" -f $stamp, $FixtureId, $safeLabel
$runRoot = Join-Path $repoRoot "benchmark\validation_runs\$runDirName"

if (Test-Path -LiteralPath $runRoot) {
    throw "Run directory already exists: $runRoot"
}

New-Item -ItemType Directory -Path $runRoot | Out-Null
Copy-Item -LiteralPath $workspaceTemplate -Destination (Join-Path $runRoot "workspace") -Recurse

$promptSource = Join-Path $fixtureRoot "run_prompt.txt"
if (Test-Path -LiteralPath $promptSource) {
    Copy-Item -LiteralPath $promptSource -Destination (Join-Path $runRoot "run_prompt.txt")
}

$manifest = [ordered]@{
    fixture_id = $FixtureId
    run_label = $RunLabel
    created_at = (Get-Date).ToString("o")
    run_root = $runRoot
    workspace = (Join-Path $runRoot "workspace")
}

$manifestPath = Join-Path $runRoot "run_manifest.json"
$manifest | ConvertTo-Json | Set-Content -LiteralPath $manifestPath -Encoding utf8

Write-Output "RUN_ROOT=$runRoot"
Write-Output "WORKSPACE=$(Join-Path $runRoot 'workspace')"
Write-Output "PROMPT=$(Join-Path $runRoot 'run_prompt.txt')"
