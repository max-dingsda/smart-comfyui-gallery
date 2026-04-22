from __future__ import annotations

from dataclasses import dataclass
import hashlib
import json
import os
from pathlib import Path
import time
import urllib.error
import urllib.parse
import urllib.request


MODEL_SECTION_CONFIG = {
    "checkpoints": {
        "folders": ("checkpoints", "diffusion_models"),
        "extensions": {".ckpt", ".safetensors", ".pt", ".pth", ".bin"},
    },
    "loras": {
        "folders": ("loras", "lora"),
        "extensions": {".safetensors"},
    },
    "embeddings": {
        "folders": ("embeddings", "embedding"),
        "extensions": {".pt", ".bin", ".safetensors"},
    },
}


@dataclass(frozen=True)
class ModelRecord:
    id: str
    section: str
    source_folder: str
    name: str
    path: str
    relative_path: str
    size: int
    mtime: int
    trigger: str | None = None
    tags: str | None = None
    architecture: str | None = None
    sha256: str | None = None
    civitai_checked_at: int | None = None
    civitai_model_url: str | None = None
    civitai_name: str | None = None
    civitai_version_name: str | None = None
    civitai_type: str | None = None
    civitai_base_model: str | None = None
    civitai_creator: str | None = None
    civitai_license: str | None = None
    civitai_trigger: str | None = None
    civitai_tags: str | None = None
    civitai_status: str | None = None
    civitai_error: str | None = None


def derive_models_root(base_output_path: str) -> Path:
    output_path = Path(base_output_path).resolve()
    comfy_root = output_path.parent
    return comfy_root / "models"


def fast_model_id(path: str) -> str:
    try:
        with open(path, "rb") as handle:
            handle.seek(0x100000)
            head = handle.read(0x10000)
            handle.seek(-0x10000, os.SEEK_END)
            tail = handle.read(0x10000)
        return hashlib.sha256(head + tail).hexdigest()[:16]
    except Exception:
        return hashlib.md5(path.encode("utf-8")).hexdigest()[:16]


def calculate_file_sha256(path: str) -> str | None:
    try:
        digest = hashlib.sha256()
        with open(path, "rb") as handle:
            for chunk in iter(lambda: handle.read(65536), b""):
                digest.update(chunk)
        return digest.hexdigest()
    except Exception:
        return None


def read_safetensors_header(path: str) -> dict | None:
    try:
        with open(path, "rb") as handle:
            header_size_bytes = handle.read(8)
            if len(header_size_bytes) < 8:
                return None
            header_size = int.from_bytes(header_size_bytes, "little")
            if header_size <= 0 or header_size > 100_000_000:
                return None
            header_json = handle.read(header_size).decode("utf-8", errors="ignore")
        return json.loads(header_json)
    except Exception:
        return None


def extract_safetensors_details(path: str) -> dict:
    header = read_safetensors_header(path)
    if not header:
        return {}

    meta = header.get("__metadata__", {})
    trigger = None
    tags = None
    architecture = detect_architecture_from_keys(list(header.keys()))

    for key in ("ss_trigger_word", "activation_text", "trigger_word"):
        if meta.get(key):
            trigger = str(meta[key]).strip()
            break

    tag_blob = meta.get("ss_tag_frequency")
    if tag_blob:
        try:
            tag_json = json.loads(tag_blob)
            tag_names: list[str] = []
            for dataset_tags in tag_json.values():
                tag_names.extend(dataset_tags.keys())
            unique_tags = sorted(set(tag_names))
            if unique_tags:
                tags = ", ".join(unique_tags[:50])
        except Exception:
            tags = None

    base_model = None
    for key in ("ss_base_model_version", "ss_sd_model_name", "modelspec.architecture"):
        if meta.get(key):
            base_model = str(meta[key]).strip()
            break

    return {
        "trigger": trigger,
        "tags": tags,
        "architecture": architecture or base_model,
    }


def detect_architecture_from_keys(metadata_keys: list[str]) -> str | None:
    keys_lower = [key.lower() for key in metadata_keys]
    if any("cascade" in key or "effnet" in key for key in keys_lower):
        return "Stable Cascade"
    if any("pony" in key for key in keys_lower):
        return "Pony"
    if "model.diffusion_model.joint_blocks.0.x_block.attn.qkv.weight" in metadata_keys:
        return "Flux"
    if any("double_blocks" in key or "single_blocks" in key for key in keys_lower):
        return "Flux"
    if any("down_blocks.2.attentions.1.transformer_blocks.9" in key for key in metadata_keys):
        return "SDXL"
    if any("cond_stage_model.transformer.text_model.embeddings" in key for key in metadata_keys):
        return "SD 1.x/2.x"
    return None


def scan_model_library(models_root: str | Path, *, include_sha256: bool = False) -> list[ModelRecord]:
    root_path = Path(models_root)
    records: list[ModelRecord] = []

    for section, config in MODEL_SECTION_CONFIG.items():
        for folder_name in config["folders"]:
            folder_path = root_path / folder_name
            if not folder_path.exists():
                continue

            for path in folder_path.rglob("*"):
                if not path.is_file():
                    continue
                if path.suffix.lower() not in config["extensions"]:
                    continue

                file_stat = path.stat()
                details = extract_safetensors_details(str(path)) if path.suffix.lower() == ".safetensors" else {}
                records.append(
                    ModelRecord(
                        id=fast_model_id(str(path)),
                        section=section,
                        source_folder=folder_name,
                        name=path.stem,
                        path=str(path),
                        relative_path=str(path.relative_to(root_path)),
                        size=file_stat.st_size,
                        mtime=int(file_stat.st_mtime),
                        trigger=details.get("trigger"),
                        tags=details.get("tags"),
                        architecture=details.get("architecture"),
                        sha256=calculate_file_sha256(str(path)) if include_sha256 else None,
                    )
                )

    records.sort(key=lambda item: (item.section, item.name.lower(), item.path.lower()))
    return records


def persist_model_records(conn, records: list[ModelRecord]) -> None:
    scanned_at = int(time.time())
    conn.executemany(
        """
        INSERT OR REPLACE INTO sg_models (
            id, section, source_folder, name, path, relative_path, size, mtime, scanned_at,
            trigger_local, tags_local, architecture_local, sha256,
            civitai_checked_at, civitai_model_url, civitai_name, civitai_version_name, civitai_type,
            civitai_base_model, civitai_creator, civitai_license, civitai_trigger, civitai_tags,
            civitai_status, civitai_error
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        [
            (
                record.id,
                record.section,
                record.source_folder,
                record.name,
                record.path,
                record.relative_path,
                record.size,
                record.mtime,
                scanned_at,
                record.trigger,
                record.tags,
                record.architecture,
                record.sha256,
                record.civitai_checked_at,
                record.civitai_model_url,
                record.civitai_name,
                record.civitai_version_name,
                record.civitai_type,
                record.civitai_base_model,
                record.civitai_creator,
                record.civitai_license,
                record.civitai_trigger,
                record.civitai_tags,
                record.civitai_status,
                record.civitai_error,
            )
            for record in records
        ],
    )

    existing_paths = {record.path for record in records}
    rows = conn.execute("SELECT path FROM sg_models").fetchall()
    for row in rows:
        if row["path"] not in existing_paths:
            conn.execute("DELETE FROM sg_models WHERE path = ?", (row["path"],))


def fetch_model_records(conn, section: str | None = None) -> list[dict]:
    query = """
        SELECT
            id, section, source_folder, name, path, relative_path, size, mtime, scanned_at,
            trigger_local, tags_local, architecture_local, sha256,
            civitai_checked_at, civitai_model_url, civitai_name, civitai_version_name, civitai_type,
            civitai_base_model, civitai_creator, civitai_license, civitai_trigger, civitai_tags,
            civitai_status, civitai_error
        FROM sg_models
    """
    params: tuple = ()
    if section:
        query += " WHERE section = ?"
        params = (section,)
    query += " ORDER BY section, LOWER(name), LOWER(path)"

    rows = conn.execute(query, params).fetchall()
    payload = []
    for row in rows:
        payload.append(
            {
                "id": row["id"],
                "section": row["section"],
                "source_folder": row["source_folder"],
                "name": row["name"],
                "path": row["path"],
                "relative_path": row["relative_path"],
                "size": row["size"],
                "mtime": row["mtime"],
                "scanned_at": row["scanned_at"],
                "trigger": row["civitai_trigger"] or row["trigger_local"],
                "tags": row["civitai_tags"] or row["tags_local"],
                "architecture": row["civitai_base_model"] or row["architecture_local"],
                "sha256": row["sha256"],
                "civitai_checked_at": row["civitai_checked_at"],
                "civitai_model_url": row["civitai_model_url"],
                "civitai_name": row["civitai_name"],
                "civitai_version_name": row["civitai_version_name"],
                "civitai_type": row["civitai_type"],
                "civitai_base_model": row["civitai_base_model"],
                "civitai_creator": row["civitai_creator"],
                "civitai_license": row["civitai_license"],
                "civitai_status": row["civitai_status"],
                "civitai_error": row["civitai_error"],
            }
        )
    return payload


def build_license_summary(model_data: dict | None) -> str | None:
    if not model_data:
        return None
    if model_data.get("license"):
        return str(model_data["license"])

    parts = []
    if model_data.get("allowCommercialUse") is not None:
        parts.append(f"Commercial: {model_data['allowCommercialUse']}")
    if model_data.get("allowNoCredit") is not None:
        parts.append(f"NoCredit: {'yes' if model_data['allowNoCredit'] else 'no'}")
    if model_data.get("allowDerivatives") is not None:
        parts.append(f"Derivatives: {'yes' if model_data['allowDerivatives'] else 'no'}")
    if model_data.get("allowDifferentLicense") is not None:
        parts.append(f"Relicense: {'yes' if model_data['allowDifferentLicense'] else 'no'}")
    return " | ".join(parts) if parts else None


def civitai_request_json(url: str, api_key: str | None = None, timeout: int = 20) -> dict:
    headers = {"User-Agent": "SmartGallery/2.11"}
    if api_key:
        headers["Authorization"] = f"Bearer {api_key}"
    request = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(request, timeout=timeout) as response:
        return json.loads(response.read().decode("utf-8"))


def fetch_civitai_metadata_for_model(path: str, api_key: str | None = None) -> dict:
    sha256 = calculate_file_sha256(path)
    if not sha256:
        raise RuntimeError("Failed to calculate SHA256 hash.")

    try:
        version_data = civitai_request_json(
            f"https://civitai.com/api/v1/model-versions/by-hash/{urllib.parse.quote(sha256)}",
            api_key=api_key,
        )
    except urllib.error.HTTPError as exc:
        if exc.code == 404:
            return {
                "sha256": sha256,
                "found": False,
                "checked_at": int(time.time()),
                "civitai_status": "not_found",
                "civitai_error": "Model not found on CivitAI.",
            }
        detail = exc.read().decode("utf-8", errors="replace")[:300]
        raise RuntimeError(f"CivitAI version lookup failed with HTTP {exc.code}: {detail}") from exc

    model_id = version_data.get("modelId")
    model_details = None
    if model_id:
        try:
            model_details = civitai_request_json(
                f"https://civitai.com/api/v1/models/{model_id}",
                api_key=api_key,
            )
        except Exception:
            model_details = None

    trigger_words = (
        version_data.get("trainedWords")
        or version_data.get("triggers")
        or version_data.get("activationText")
        or version_data.get("triggerWords")
        or []
    )
    trigger_string = ", ".join(trigger_words) if isinstance(trigger_words, list) else (trigger_words or None)
    creator_username = (
        (model_details or {}).get("creator", {}).get("username")
        or (version_data.get("model") or {}).get("creator", {}).get("username")
        or (version_data.get("model") or {}).get("user", {}).get("username")
    )
    model_tags = (version_data.get("model") or {}).get("tags")
    tags_string = ", ".join(model_tags) if isinstance(model_tags, list) else (model_tags or None)

    return {
        "sha256": sha256,
        "found": True,
        "checked_at": int(time.time()),
        "civitai_name": (version_data.get("model") or {}).get("name"),
        "civitai_version_name": version_data.get("name"),
        "civitai_type": (version_data.get("model") or {}).get("type") or (model_details or {}).get("type"),
        "civitai_base_model": version_data.get("baseModel") or (version_data.get("model") or {}).get("baseModel"),
        "civitai_creator": creator_username,
        "civitai_license": build_license_summary(model_details) or (version_data.get("model") or {}).get("license") or version_data.get("license"),
        "civitai_trigger": trigger_string,
        "civitai_tags": tags_string,
        "civitai_status": "matched",
        "civitai_error": None,
        "civitai_model_url": (
            f"https://civitai.com/models/{model_id}?modelVersionId={version_data.get('id')}"
            if model_id and version_data.get("id")
            else None
        ),
    }


def update_model_civitai_data(conn, model_id: str, civitai_data: dict) -> None:
    conn.execute(
        """
        UPDATE sg_models
        SET
            sha256 = ?,
            civitai_checked_at = ?,
            civitai_model_url = ?,
            civitai_name = ?,
            civitai_version_name = ?,
            civitai_type = ?,
            civitai_base_model = ?,
            civitai_creator = ?,
            civitai_license = ?,
            civitai_trigger = ?,
            civitai_tags = ?,
            civitai_status = ?,
            civitai_error = ?
        WHERE id = ?
        """,
        (
            civitai_data.get("sha256"),
            civitai_data.get("checked_at"),
            civitai_data.get("civitai_model_url"),
            civitai_data.get("civitai_name"),
            civitai_data.get("civitai_version_name"),
            civitai_data.get("civitai_type"),
            civitai_data.get("civitai_base_model"),
            civitai_data.get("civitai_creator"),
            civitai_data.get("civitai_license"),
            civitai_data.get("civitai_trigger"),
            civitai_data.get("civitai_tags"),
            civitai_data.get("civitai_status"),
            civitai_data.get("civitai_error"),
            model_id,
        ),
    )
