from pathlib import Path

from smartgallery_core.models import derive_models_root
from smartgallery_core.models import scan_model_library


def test_derive_models_root_uses_comfyui_parent():
    root = derive_models_root("F:/AI/ComfyUI/output")
    assert str(root).replace("\\", "/").endswith("/ComfyUI/models")


def test_scan_model_library_groups_diffusion_models_into_checkpoints(tmp_path: Path):
    checkpoints_dir = tmp_path / "checkpoints"
    diffusion_dir = tmp_path / "diffusion_models"
    loras_dir = tmp_path / "loras"
    embeddings_dir = tmp_path / "embeddings"

    checkpoints_dir.mkdir()
    diffusion_dir.mkdir()
    loras_dir.mkdir()
    embeddings_dir.mkdir()

    (checkpoints_dir / "alpha.safetensors").write_text("a", encoding="utf-8")
    (diffusion_dir / "flux-dev.safetensors").write_text("b", encoding="utf-8")
    (loras_dir / "style-lora.safetensors").write_text("c", encoding="utf-8")
    (embeddings_dir / "neg.pt").write_text("d", encoding="utf-8")

    models = scan_model_library(tmp_path)
    grouped = {section: [model for model in models if model.section == section] for section in ("checkpoints", "loras", "embeddings")}

    assert len(grouped["checkpoints"]) == 2
    assert {model.source_folder for model in grouped["checkpoints"]} == {"checkpoints", "diffusion_models"}
    assert len(grouped["loras"]) == 1
    assert len(grouped["embeddings"]) == 1
