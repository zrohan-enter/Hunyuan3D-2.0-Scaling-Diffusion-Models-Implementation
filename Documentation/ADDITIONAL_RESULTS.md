# Additional 2D to 3D Results

## Purpose

This folder contains additional test outputs showing that the project can convert 2D input images into 3D mesh outputs using the Hunyuan3D-DiT shape generation pipeline.

## Input Folder

Input images are stored in:

inputs/

## Output Folder

Generated 3D assets are stored in:

results/

## Result Format

- .glb files: generated 3D assets
- .json files: metadata for reproducibility
- .md files: run logs

## Current Status

Shape-only generation is working. Texture generation is optional and may require CUDA Toolkit / nvcc.

## How to Reproduce

Run:

powershell -ExecutionPolicy Bypass -File .\scripts\run_shape_only.ps1

or run custom images using:

.\.venv\Scripts\python.exe .\scripts\generate_result.py --image .\inputs\your_image.png --out_dir .\results
