# lock-verify.ps1 - the canon intrusion detector (owner directive 2026-09-13).
# Run at the start of every AI session. Exit code 1 = canon changed: report to
# the owner immediately; never repair or "restore" silently.
$ErrorActionPreference = "Stop"
# Portable SHA-256 helper (owner directive 2026-09-17): works identically under
# pwsh 7 AND Windows PowerShell 5.1/older, which may not expose the Get-FileHash
# cmdlet. The .NET API exists on every supported shell. Output format matches
# Get-FileHash exactly (uppercase hex).
function Get-FileSha256([string]$path) {
    $sha = [System.Security.Cryptography.SHA256]::Create()
    try {
        $bytes = [System.IO.File]::ReadAllBytes($path)
        $hash  = $sha.ComputeHash($bytes)
        return ([System.BitConverter]::ToString($hash)).Replace('-', '')
    } finally { $sha.Dispose() }
}
# The manifest file lives beside this script; its ENTRIES are project-root-relative
# (app/ui/..., app/static/...). Self-locate the project root — the folder that
# actually contains app/ui/MediaEditor.dc.html — and resolve entries against it.
$here = Split-Path -Parent $MyInvocation.MyCommand.Path
$projectRoot = $here
foreach ($probe in @((Join-Path $here '..'), $here)) {
    if (Test-Path (Join-Path $probe 'app\ui\MediaEditor.dc.html')) {
        $projectRoot = (Resolve-Path $probe).Path
        break
    }
}
$manifest = Join-Path $here "LOCK-MANIFEST.sha256"
if (-not (Test-Path $manifest)) { Write-Host "LOCK ERROR: manifest missing."; exit 1 }
$failed = $false
foreach ($line in Get-Content $manifest) {
    if ([string]::IsNullOrWhiteSpace($line) -or $line.StartsWith("#")) { continue }
    $parts = $line -split '\s+', 2
    $expected = $parts[0]; $rel = $parts[1].Trim()
    $path = Join-Path $projectRoot $rel
    if (-not (Test-Path $path)) { Write-Host "MISSING : $rel"; $failed = $true; continue }
    $actual = Get-FileSha256 $path
    if ($actual -ne $expected) { Write-Host "CHANGED : $rel"; $failed = $true }
}
if ($failed) {
    Write-Host "CANON VIOLATION - tell the owner now. Do not fix anything yourself."
    exit 1
}
Write-Host "LOCK OK - canon intact."
exit 0
