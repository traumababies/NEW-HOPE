# ONE command to bring up everything the buttons need:
#   MusicGen -> http://127.0.0.1:8002
#   ComfyUI  -> http://127.0.0.1:8188
#   The app  -> http://127.0.0.1:8011   <-- the buttons live here
#
# Run it, keep the window open (minimized is fine), then just push buttons.

# The app package, app/.env, app/ui and app/static are all relative to the
# REPO ROOT, not to this script's folder. (This script used to pass
# -WorkingDirectory $PSScriptRoot, which points inside AI TEAM/ and made the
# app start fail with "No module named app".)
$repoRoot = Split-Path -Parent $PSScriptRoot

# 1) Fire the generators first (they take longest to warm up) ...
. $PSScriptRoot\start-generators.ps1 -Service all

# 2) ... and start the app NOW, in parallel, instead of blocking on them.
Write-Host 'Starting the app on http://127.0.0.1:8011 (parallel with generators)...'
Start-Process -FilePath python -WorkingDirectory $repoRoot -ArgumentList @(
    '-m', 'uvicorn', 'app.main:app', '--port', '8011', '--env-file', 'app/.env'
) -WindowStyle Minimized

# 3) Poll all three concurrently and report as each comes up.
$appUp = $false
$comfy = $false
$music = $false
$deadline = (Get-Date).AddSeconds(180)
do {
    Start-Sleep -Seconds 2
    if (-not $appUp) { $appUp = Test-NetConnection -ComputerName 127.0.0.1 -Port 8011 -InformationLevel Quiet -WarningAction SilentlyContinue }
    if (-not $comfy) { $comfy = Test-NetConnection -ComputerName 127.0.0.1 -Port 8188 -InformationLevel Quiet -WarningAction SilentlyContinue }
    if (-not $music) { $music = Test-NetConnection -ComputerName 127.0.0.1 -Port 8002 -InformationLevel Quiet -WarningAction SilentlyContinue }
} until (($appUp -and $comfy -and $music) -or (Get-Date) -gt $deadline)

if ($appUp -and $comfy -and $music) {
    Write-Host ''
    Write-Host '=== ALL UP ===' -ForegroundColor Green
    Write-Host 'Open http://127.0.0.1:8011/media-editor and push buttons.'
    Write-Host 'Keep this window open (minimized is fine). Close it to stop everything.'
} else {
    Write-Host ''
    Write-Host ("app: {0}   ComfyUI 8188: {1}   MusicGen 8002: {2}" -f $(if ($appUp) { 'UP' } else { 'DOWN' }), $(if ($comfy) { 'UP' } else { 'DOWN' }), $(if ($music) { 'UP' } else { 'DOWN' }))
    Write-Host 'Not everything came up - check the messages above.' -ForegroundColor Yellow
}
