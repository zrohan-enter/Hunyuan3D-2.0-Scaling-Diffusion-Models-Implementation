# Hunyuan3D 2.0 Research Paper Implementation

## Paper

Hunyuan3D 2.0: Scaling Diffusion Models for High Resolution Textured 3D Assets Generation

## Project Goal

This repository reproduces the practical inference pipeline of the Hunyuan3D 2.0 paper using the official released source code and pretrained models.

This is an implementation/reproduction project, not full training from scratch.

## Main Pipeline

Input Image -> Hunyuan3D-DiT Shape Generation -> Bare Mesh -> Hunyuan3D-Paint Texture Generation -> Textured 3D Asset

## Folder Structure

Documentation/ - paper and project notes
results/ - generated GLB files, metadata, and logs
scripts/ - runners and launch scripts
src/Hunyuan3D-2/ - official source code

## Run Shape Only

powershell -ExecutionPolicy Bypass -File .\scripts\run_shape_only.ps1

## Run Shape + Texture Attempt

powershell -ExecutionPolicy Bypass -File .\scripts\run_shape_texture_attempt.ps1

## Launch Gradio

powershell -ExecutionPolicy Bypass -File .\scripts\launch_gradio_full_lowvram.ps1

## Important Note

Texture generation requires CUDA Toolkit / nvcc, Visual Studio C++ Build Tools, and enough VRAM. Since nvcc was not found, this setup focuses on shape-only generation first.
