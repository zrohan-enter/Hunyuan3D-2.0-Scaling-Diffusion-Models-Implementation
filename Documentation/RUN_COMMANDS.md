# Run Commands

## Go to project folder

cd "D:\Academic\Research paper\Hunyuan3D 2.0 Scaling Diffusion Models"

## Shape-only generation

powershell -ExecutionPolicy Bypass -File .\scripts\run_shape_only.ps1

## Shape + texture attempt

powershell -ExecutionPolicy Bypass -File .\scripts\run_shape_texture_attempt.ps1

## Gradio full model

powershell -ExecutionPolicy Bypass -File .\scripts\launch_gradio_full_lowvram.ps1
