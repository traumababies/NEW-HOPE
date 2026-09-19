# Starts the two local generators the Media Editor drives:
#   ComfyUI  -> http://127.0.0.1:8188  (SD 1.5 images, AnimateDiff video, ACE-Step audio)
#   MusicGen -> http://127.0.0.1:8002  (instrumental tracks)
# Both are low-VRAM profiled for the 4 GB GPU. The app's status pill and the
# one-click buttons go live as soon as these are up.
#
# Usage:  .\start-generators.ps1 [-Service comfyui|musicgen|all]
param(
    [ValidateSet('comfyui', 'musicgen', 'all')]
    [string]$Service = 'all'
)
$ErrorActionPreference = 'Stop'

$generatorRoot = 'C:\Users\Bunbunz\Documents\Evolue-Rebuild.worktrees\Media-Generators'
$python = Join-Path $generatorRoot '.venv\Scripts\python.exe'
$comfy = Join-Path $generatorRoot 'ComfyUI'
$musicgenServer = 'C:\Users\Bunbunz\Documents\Evolue-Rebuild.worktrees\best-ai-model-for-databases\DataAnalysisExpert\musicgen_server.py'

if (-not (Test-Path $python)) { throw "Generator environment not found: $python" }
if (-not (Test-Path $musicgenServer)) { throw "MusicGen server not found: $musicgenServer" }

function Start-MusicGen {
    # Idle offload returns the model to RAM after each task so ComfyUI gets
    # the whole GPU while no music is generating. TF32 speeds up the 2060.
    $env:MUSICGEN_PORT = '8002'
    $env:MUSICGEN_IDLE_OFFLOAD = '1'
    $env:PYTORCH_CUDA_ALLOC_CONF = 'expandable_segments:True'
    $env:MUSICGEN_OUTPUT_DIR = Join-Path $PSScriptRoot 'musicgen-output'
    New-Item -ItemType Directory -Force -Path $env:MUSICGEN_OUTPUT_DIR | Out-Null
    Start-Process -FilePath $python -WorkingDirectory (Split-Path $musicgenServer) -ArgumentList @($musicgenServer) -WindowStyle Normal
    Write-Host 'MusicGen starting at http://127.0.0.1:8002 (idle VRAM offload on)'
}

function Start-ComfyUI {
    # Tuned for the RTX 2060: --lowvram keeps the unet streaming,
    # --cpu-vae decodes on CPU, --disable-smart-memory clears VRAM between
    # jobs so the two generators can share the card, and expandable segments
    # stop fragmentation OOMs.
    $env:PYTORCH_CUDA_ALLOC_CONF = 'expandable_segments:True'
    Start-Process -FilePath $python -WorkingDirectory $comfy -ArgumentList @(
        'main.py', '--listen', '127.0.0.1', '--port', '8188', '--lowvram', '--cpu-vae', '--disable-smart-memory'
    ) -WindowStyle Normal
    Write-Host 'ComfyUI starting at http://127.0.0.1:8188 (lowvram + cpu-vae + disable-smart-memory)'
}

switch ($Service) {
    'comfyui' { Start-ComfyUI }
    'musicgen' { Start-MusicGen }
    'all' { Start-MusicGen; Start-ComfyUI }
}
