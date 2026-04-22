from pathlib import Path
import shutil
import tempfile

from smartgallery_core.renaming import (
    build_sequenced_name,
    build_workflow_name,
    clean_model_name,
    generate_workflow_suggestions,
    preview_batch_renames,
    prompt_keywords,
    rename_with_sidecars,
    sanitize_filename,
)


def test_sanitize_filename_removes_invalid_characters():
    assert sanitize_filename('my:model<>name?/test') == "my_model_name_test"


def test_clean_model_name_strips_runtime_suffixes():
    assert clean_model_name("zavychromaxl_v80.fp16.safetensors") == "zavychromaxl_v80"


def test_prompt_keywords_prefers_meaningful_subject_terms():
    prompt = "masterpiece, best quality, australian shepherd puppy sleeping on pink blanket"
    assert prompt_keywords(prompt) == "australian_shepherd_puppy_sleeping"


def test_build_workflow_name_defaults_to_model_first():
    meta = {
        "model": "juggernautXL_v9.safetensors",
        "positive_prompt_clean": "close portrait of a leather jacket woman in city lights",
    }
    assert build_workflow_name(meta) == "juggernautXL_v9_portrait_leather_jacket_woman"


def test_generate_workflow_suggestions_keeps_model_first_option_first():
    meta = {
        "model": "realvisxl_v50.safetensors",
        "positive_prompt_clean": "golden retriever puppy in mountain meadow",
        "sampler": "dpmpp_2m",
        "scheduler": "karras",
    }
    suggestions = generate_workflow_suggestions(meta)
    assert suggestions[0] == "realvisxl_v50_golden_retriever_puppy_mountain"
    assert "golden_retriever_puppy_mountain_realvisxl_v50" in suggestions


def test_preview_batch_renames_marks_existing_target_as_conflict():
    root = _make_workspace_temp_dir("preview")
    try:
        first = root / "image_a.png"
        second = root / "image_b.png"
        conflict_target = root / "set_name_002.png"
        first.write_text("a", encoding="utf-8")
        second.write_text("b", encoding="utf-8")
        conflict_target.write_text("c", encoding="utf-8")

        previews = preview_batch_renames(
            [
                {"name": first.name, "path": str(first)},
                {"name": second.name, "path": str(second)},
            ],
            "set_name",
        )

        assert previews[0].conflict is False
        assert previews[0].new_name == "set_name_001.png"
        assert previews[1].conflict is True
        assert previews[1].reason == "path_exists"
    finally:
        shutil.rmtree(root, ignore_errors=True)


def test_build_sequenced_name_uses_three_digit_padding():
    assert build_sequenced_name("gallery_batch", 7) == "gallery_batch_007"


def test_rename_with_sidecars_renames_json_sidecar():
    root = _make_workspace_temp_dir("sidecar")
    try:
        source = root / "old_name.png"
        sidecar = root / "old_name.json"
        source.write_text("image", encoding="utf-8")
        sidecar.write_text("{}", encoding="utf-8")

        result = rename_with_sidecars(str(source), "new_name")

        assert result["new_name"] == "new_name.png"
        assert (root / "new_name.png").exists()
        assert (root / "new_name.json").exists()
        assert not source.exists()
        assert not sidecar.exists()
    finally:
        shutil.rmtree(root, ignore_errors=True)


def _make_workspace_temp_dir(label: str) -> Path:
    base_dir = Path.cwd() / ".tmp_test_runs"
    base_dir.mkdir(exist_ok=True)
    return Path(tempfile.mkdtemp(prefix=f"renaming_{label}_", dir=base_dir))
