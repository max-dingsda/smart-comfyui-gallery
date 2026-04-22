from __future__ import annotations

from dataclasses import dataclass
import os
import re
from pathlib import Path


_BOILERPLATE = {
    "the",
    "and",
    "but",
    "for",
    "nor",
    "yet",
    "both",
    "either",
    "her",
    "his",
    "its",
    "our",
    "their",
    "your",
    "my",
    "she",
    "he",
    "it",
    "we",
    "they",
    "you",
    "who",
    "whom",
    "this",
    "that",
    "these",
    "those",
    "one",
    "two",
    "three",
    "with",
    "from",
    "into",
    "onto",
    "upon",
    "about",
    "above",
    "below",
    "under",
    "over",
    "after",
    "before",
    "between",
    "masterpiece",
    "best",
    "quality",
    "high",
    "ultra",
    "detailed",
    "extremely",
    "highly",
    "very",
    "incredible",
    "amazing",
    "stunning",
    "beautiful",
    "perfect",
    "realistic",
    "photorealistic",
    "hyperrealistic",
    "sharp",
    "resolution",
    "absurdres",
    "highres",
    "hires",
    "8k",
    "4k",
    "uhd",
    "intricate",
    "cinematic",
    "professional",
    "raw",
    "photo",
    "photograph",
    "digital",
    "art",
    "painting",
    "illustration",
    "render",
    "rendering",
    "unreal",
    "engine",
    "octane",
    "trending",
    "artstation",
    "solo",
    "focus",
    "simple",
    "background",
    "white",
    "looking",
    "viewer",
    "front",
    "view",
    "full",
    "body",
    "upper",
    "close",
    "face",
    "1girl",
    "1boy",
    "1man",
    "1woman",
    "female",
    "male",
    "person",
    "human",
    "anime",
    "character",
}


@dataclass(frozen=True)
class RenamePreview:
    old_name: str
    new_name: str
    old_path: str | None = None
    new_path: str | None = None
    conflict: bool = False
    reason: str = ""


def sanitize_filename(name: str, max_length: int = 200) -> str:
    name = re.sub(r'[<>:"/\\|?*\x00-\x1f]', "_", name or "")
    name = re.sub(r"_+", "_", name).strip("_. ")
    return name[:max_length]


def clean_model_name(name: str, max_length: int = 40) -> str:
    if not name:
        return ""
    name = os.path.basename(name)
    name = os.path.splitext(name)[0]
    name = re.sub(
        r"([._-])(fp16|fp32|bf16|pruned|full|ema|merged)$",
        "",
        name,
        flags=re.IGNORECASE,
    )
    name = re.sub(r"[^\w]+", "_", name)
    name = re.sub(r"_+", "_", name).strip("_")
    return name[:max_length]


def prompt_keywords(prompt: str, max_words: int = 4, max_length: int = 60) -> str:
    if not prompt:
        return ""
    prompt = re.sub(r"<[^>]+>", "", prompt)
    prompt = re.sub(r"\(([^:)]+)(?::[^)]+)?\)", r"\1", prompt)
    prompt = prompt.replace("/", " ")
    clauses = [clause.strip() for clause in re.split(r"[,\n]", prompt) if clause.strip()]

    collected: list[str] = []
    for clause in clauses[:20]:
        for raw_word in clause.split():
            word = re.sub(r"[^\w-]", "", raw_word).strip("_-")
            if len(word) <= 2:
                continue
            if word.lower() in _BOILERPLATE:
                continue
            collected.append(word.lower())
            if len(collected) >= max_words:
                break
        if len(collected) >= max_words:
            break

    result = sanitize_filename("_".join(collected), max_length=max_length)
    return result.lower()


def workflow_prompt_text(meta: dict) -> str:
    return (meta.get("positive_prompt_clean") or meta.get("positive_prompt") or "").strip()


def extract_name_components(meta: dict, prompt_word_limit: int = 4) -> dict:
    loras = meta.get("loras") or []
    sampler = sanitize_filename("_".join(filter(None, [meta.get("sampler"), meta.get("scheduler")])))
    return {
        "model": clean_model_name(meta.get("model", "")),
        "prompt": prompt_keywords(workflow_prompt_text(meta), max_words=prompt_word_limit),
        "loras": [clean_model_name(item) for item in loras if item][:3],
        "sampler": sampler.lower(),
        "steps": str(meta.get("steps", "")).strip(),
        "cfg": str(meta.get("cfg", "")).strip(),
        "seed": str(meta.get("seed", "")).strip(),
    }


def build_workflow_name(
    meta: dict,
    *,
    priority: str = "model",
    include_prompt: bool = True,
    include_model: bool = True,
    include_loras: bool = False,
    include_sampler: bool = False,
    include_steps: bool = False,
    prompt_word_limit: int = 4,
) -> str:
    components = extract_name_components(meta, prompt_word_limit=prompt_word_limit)
    parts: list[str] = []

    prompt_part = components["prompt"] if include_prompt else ""
    model_part = components["model"] if include_model else ""

    if priority == "prompt":
        ordered = [prompt_part, model_part]
    else:
        ordered = [model_part, prompt_part]

    for item in ordered:
        if item:
            parts.append(item)

    if include_loras and components["loras"]:
        parts.extend(components["loras"][:2])
    if include_sampler and components["sampler"]:
        parts.append(components["sampler"])
    if include_steps and components["steps"]:
        parts.append(f"{components['steps']}steps")

    return sanitize_filename("_".join(parts))


def generate_workflow_suggestions(meta: dict, prompt_word_limit: int = 4) -> list[str]:
    components = extract_name_components(meta, prompt_word_limit=prompt_word_limit)
    model = components["model"]
    prompt = components["prompt"]
    sampler = components["sampler"]
    steps = components["steps"]
    loras = "_".join(components["loras"][:2])

    suggestions = [
        build_workflow_name(meta, priority="model", prompt_word_limit=prompt_word_limit),
        build_workflow_name(meta, priority="prompt", prompt_word_limit=prompt_word_limit),
    ]

    if model and sampler:
        suggestions.append(sanitize_filename(f"{model}_{sampler}"))
    if model and steps and sampler:
        suggestions.append(sanitize_filename(f"{model}_{steps}steps_{sampler}"))
    if model and prompt and loras:
        suggestions.append(sanitize_filename(f"{model}_{prompt}_{loras}"))
    if prompt and loras:
        suggestions.append(sanitize_filename(f"{prompt}_{loras}"))

    unique: list[str] = []
    seen: set[str] = set()
    for item in suggestions:
        if item and item not in seen:
            seen.add(item)
            unique.append(item)
    return unique


def build_sequenced_name(base_name: str, index: int, padding: int = 3) -> str:
    sanitized_base = sanitize_filename(base_name)
    return f"{sanitized_base}_{index:0{padding}d}" if sanitized_base else ""


def preview_batch_renames(
    file_infos: list[dict],
    base_name: str,
    *,
    start_index: int = 1,
    padding: int = 3,
) -> list[RenamePreview]:
    previews: list[RenamePreview] = []
    reserved_targets: set[str] = set()

    for offset, info in enumerate(file_infos):
        old_name = info["name"]
        old_path = info.get("path")
        extension = Path(old_name).suffix
        stem = build_sequenced_name(base_name, start_index + offset, padding=padding)
        new_name = f"{stem}{extension}"
        new_path = str(Path(old_path).with_name(new_name)) if old_path else None

        conflict = False
        reason = ""
        if not stem:
            conflict = True
            reason = "invalid_name"
        elif new_path and os.path.abspath(new_path) != os.path.abspath(old_path or ""):
            if os.path.exists(new_path):
                conflict = True
                reason = "path_exists"
            elif new_path in reserved_targets:
                conflict = True
                reason = "duplicate_target"

        if new_path:
            reserved_targets.add(new_path)

        previews.append(
            RenamePreview(
                old_name=old_name,
                new_name=new_name,
                old_path=old_path,
                new_path=new_path,
                conflict=conflict,
                reason=reason,
            )
        )

    return previews


def rename_with_sidecars(
    old_path: str,
    new_name: str,
    *,
    sidecar_extensions: tuple[str, ...] = (".json",),
) -> dict:
    source = Path(old_path)
    if not source.exists():
        raise FileNotFoundError(f"Source file not found: {old_path}")

    target_name = new_name if source.suffix and Path(new_name).suffix else f"{new_name}{source.suffix}"
    target = source.with_name(target_name)

    if target.exists() and target.resolve() != source.resolve():
        raise FileExistsError(f"Target file already exists: {target}")

    source.rename(target)

    renamed_sidecars: list[tuple[str, str]] = []
    for extension in sidecar_extensions:
        old_sidecar = source.with_suffix(extension)
        new_sidecar = target.with_suffix(extension)
        if old_sidecar.exists():
            old_sidecar.rename(new_sidecar)
            renamed_sidecars.append((str(old_sidecar), str(new_sidecar)))

    return {
        "old_path": str(source),
        "new_path": str(target),
        "new_name": target.name,
        "renamed_sidecars": renamed_sidecars,
    }
