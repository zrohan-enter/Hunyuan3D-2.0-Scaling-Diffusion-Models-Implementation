import argparse
import datetime as dt
import json
import platform
import sys
import traceback
from pathlib import Path
import torch
def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")
def write_json(path: Path, data: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False, default=str), encoding="utf-8")
def main():
    parser = argparse.ArgumentParser(description="Hunyuan3D 2.0 research implementation runner")
    parser.add_argument("--image", default="src/Hunyuan3D-2/assets/demo.png", help="Input image path")
    parser.add_argument("--out_dir", default="results", help="Output directory")
    parser.add_argument("--model_path", default="tencent/Hunyuan3D-2", help="HuggingFace model path")
    parser.add_argument("--texture", action="store_true", help="Attempt texture generation")
    args = parser.parse_args()
    start_time = dt.datetime.now()
    stamp = start_time.strftime("%Y%m%d_%H%M%S")
    image_path = Path(args.image)
    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    log_md = out_dir / f"run_log_{stamp}.md"
    metadata_json = out_dir / f"metadata_{stamp}.json"
    metadata = {
        "project": "Hunyuan3D 2.0 Research Paper Implementation",
        "paper": "Hunyuan3D 2.0: Scaling Diffusion Models for High Resolution Textured 3D Assets Generation",
        "start_time": start_time.isoformat(),
        "input_image": str(image_path),
        "output_directory": str(out_dir),
        "model_path": args.model_path,
        "texture_requested": bool(args.texture),
        "python": sys.version,
        "platform": platform.platform(),
        "torch_version": torch.__version__,
        "cuda_available": torch.cuda.is_available(),
        "gpu": torch.cuda.get_device_name(0) if torch.cuda.is_available() else None,
        "outputs": {},
        "status": "started",
        "errors": [],
    }
    write_json(metadata_json, metadata)
    log = []
    log.append("# Hunyuan3D 2.0 Run Log\n")
    log.append(f"- Time: `{start_time}`")
    log.append(f"- Input image: `{image_path}`")
    log.append(f"- Model path: `{args.model_path}`")
    log.append(f"- CUDA available: `{torch.cuda.is_available()}`")
    if torch.cuda.is_available():
        log.append(f"- GPU: `{torch.cuda.get_device_name(0)}`")
    log.append("")
    if not image_path.exists():
        raise FileNotFoundError(f"Input image not found: {image_path}")
    try:
        from hy3dgen.shapegen import Hunyuan3DDiTFlowMatchingPipeline
        log.append("## Step 1: Shape Generation")
        log.append("Loading Hunyuan3D-DiT shape generation pipeline...")
        write_text(log_md, "\n".join(log))
        print("[1/2] Loading Hunyuan3D-DiT shape pipeline...")
        shape_pipeline = Hunyuan3DDiTFlowMatchingPipeline.from_pretrained(args.model_path)
        print("[2/2] Generating bare mesh...")
        mesh = shape_pipeline(image=str(image_path))[0]
        shape_glb = out_dir / f"hunyuan3d_shape_only_{stamp}.glb"
        mesh.export(str(shape_glb))
        print(f"[OK] Shape-only mesh saved: {shape_glb}")
        metadata["outputs"]["shape_glb"] = str(shape_glb)
        metadata["status"] = "shape_generated"
        log.append(f"- Shape-only GLB: `{shape_glb}`")
        log.append("")
        write_json(metadata_json, metadata)
        write_text(log_md, "\n".join(log))
    except Exception:
        error_text = traceback.format_exc()
        metadata["status"] = "shape_failed"
        metadata["errors"].append(error_text)
        log.append("## Shape Generation Failed")
        log.append("```text")
        log.append(error_text)
        log.append("```")
        write_json(metadata_json, metadata)
        write_text(log_md, "\n".join(log))
        print("[FAILED] Shape generation failed.")
        print(error_text)
        raise
    if args.texture:
        try:
            from hy3dgen.texgen import Hunyuan3DPaintPipeline
            log.append("## Step 2: Texture Generation")
            log.append("Loading Hunyuan3D-Paint texture pipeline...")
            write_text(log_md, "\n".join(log))
            print("[Texture] Loading Hunyuan3D-Paint texture pipeline...")
            texture_pipeline = Hunyuan3DPaintPipeline.from_pretrained(args.model_path)
            print("[Texture] Generating textured mesh...")
            textured_mesh = texture_pipeline(mesh, image=str(image_path))
            textured_glb = out_dir / f"hunyuan3d_textured_{stamp}.glb"
            textured_mesh.export(str(textured_glb))
            print(f"[OK] Textured mesh saved: {textured_glb}")
            metadata["outputs"]["textured_glb"] = str(textured_glb)
            metadata["status"] = "shape_and_texture_generated"
            log.append(f"- Textured GLB: `{textured_glb}`")
            log.append("")
        except Exception:
            error_text = traceback.format_exc()
            metadata["status"] = "shape_generated_texture_failed"
            metadata["errors"].append(error_text)
            log.append("## Texture Generation Failed")
            log.append("Shape-only output was still generated successfully.")
            log.append("")
            log.append("```text")
            log.append(error_text)
            log.append("```")
            print("[WARNING] Texture generation failed, but shape-only output is saved.")
            print(error_text)
        finally:
            write_json(metadata_json, metadata)
            write_text(log_md, "\n".join(log))
    end_time = dt.datetime.now()
    metadata["end_time"] = end_time.isoformat()
    metadata["duration_seconds"] = (end_time - start_time).total_seconds()
    write_json(metadata_json, metadata)
    log.append("## Final Status")
    log.append(f"- Status: `{metadata['status']}`")
    log.append(f"- Metadata: `{metadata_json}`")
    log.append(f"- Duration seconds: `{metadata['duration_seconds']}`")
    write_text(log_md, "\n".join(log))
    print("[DONE]")
    print(f"Status: {metadata['status']}")
    print(f"Metadata: {metadata_json}")
    print(f"Log: {log_md}")
if __name__ == "__main__":
    main()
