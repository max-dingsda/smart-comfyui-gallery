# Smart ComfyUI Gallery Fork

This repository is a maintained fork of [Smart ComfyUI Gallery](https://github.com/biagiomaf/smart-comfyui-gallery), based on upstream **version 2.11**.

Current fork release line:

- fork version: `1.0.0-fork.1`
- upstream baseline: `2.11`

Versioning policy:

- this fork has its own release numbers
- upstream `2.11` is the baseline, not the current fork version
- fork-specific changes are tracked at the top of `CHANGELOG.md`

## Thanks

First, credit where it belongs:

- Thanks to **Biagio Maffettone** for creating and publishing the original SmartGallery / Smart ComfyUI Gallery project.
- Thanks to all contributors around the original project, including the Docker and deployment work that helped make it easier to run in more environments.

This fork exists because the original project already solved the hard base problem very well: a fast, practical, ComfyUI-aware gallery and DAM. The goal here is not to erase that work, but to continue it in a direction that fits this repository's workflow and priorities.

## What This Fork Is

This fork keeps the SmartGallery 2.11 foundation and extends it with:

- incremental architecture cleanup
- batch renaming for workflow-driven filenames
- an integrated model manager
- CivitAI enrichment for locally scanned models
- more workflow-aware filtering in the main gallery

It remains a **local-first ComfyUI-aware gallery and DAM**, but with additional emphasis on:

- handling large real-world model libraries
- filtering by workflow-derived assets
- practical curation workflows during active generation
- improving maintainability without throwing away the existing app

## Fork Status

Base:

- upstream project: `smart-comfyui-gallery`
- upstream reference: [https://github.com/biagiomaf/smart-comfyui-gallery](https://github.com/biagiomaf/smart-comfyui-gallery)
- fork baseline: `2.11`
- current fork release: `1.0.0-fork.1`

Current fork direction:

- preserve the existing behavior where possible
- add missing handling features before chasing larger new feature scope
- gradually reduce risk inside `smartgallery.py` by extracting stable seams

## What Changed In This Fork

### 1. Architecture Work

The codebase started from a large single-file application. This fork has already introduced reusable seams for the most fragile cross-cutting areas:

- `smartgallery_core/storage.py`
- `smartgallery_core/files.py`
- `smartgallery_core/renaming.py`
- `smartgallery_core/models.py`

This is still a modular monolith, not a service split. The point is pragmatic: new work should stop making `smartgallery.py` worse.

### 2. Batch Renaming

This fork adds workflow-aware batch renaming:

- preview before apply
- naming suggestions derived from workflow metadata
- model-first and prompt-first naming strategies
- integration into the existing gallery selection flow

This is useful when the raw ComfyUI output names are no longer enough and you want stable, human-readable filenames.

### 3. Model Manager

This fork adds an integrated model manager with:

- local library scan for:
  - checkpoints
  - loras
  - embeddings
- support for both:
  - `models/checkpoints`
  - `models/diffusion_models`
- local safetensors metadata extraction where available
- CivitAI enrichment for selected models
- explicit checkbox selection instead of “whatever is currently visible”
- progress feedback during CivitAI fetches

### 4. Improved Gallery Filters

The advanced filter panel has been extended with:

- dedicated workflow `Model` filter
- dedicated workflow `LoRA` filter
- `Ratings` filter
- negative filename search in `Search by Name`

Supported negative filename syntax:

- `!term`
- `NOT term`
- `!= term`

Example:

```text
Model = dreamshaper
Search by Name = !dreamshaper
```

This lets you find images created with a model even when the filename does not explicitly mention it.

### 5. Workflow-Aware Dropdown Filters

The `Model` and `LoRA` are implemented as dropdown-based multi-selects populated from detected workflow references already indexed in the database.

Special handling:

- `LoRA` includes a `No LoRA in workflow` option

This matters because many real workflows do not use LoRAs at all, and that state is often worth filtering explicitly.

## What Is New Right Now

If you are coming from upstream 2.11, the main fork-specific additions to pay attention to are:

1. Batch renaming
2. Model manager
3. CivitAI fetch from the model manager
4. workflow-derived model and LoRA filtering
5. ratings filter
6. negative filename search

## How To Use This Fork

## 1. Start The App

Run it the same way as SmartGallery:

```bash
python smartgallery.py
```

Typical local URL:

```text
http://127.0.0.1:8189/galleryout/
```

The usual environment variables and launch parameters from the original project still apply.

## 2. Scan Your Gallery

On startup, SmartGallery scans the configured output path and updates the SQLite cache.

That gives you:

- filename search
- workflow-based filtering
- prompt-based filtering
- comment and rating filtering
- model/LoRA dropdown options derived from indexed workflow data

## 3. Use Batch Renaming

Batch renaming is intended for selected files in the gallery.

Typical workflow:

1. select a set of files
2. open the rename actions
3. generate rename suggestions from workflow metadata
4. preview the result
5. apply only once the preview looks correct

## 4. Use The Model Manager

Open the model manager from the app and:

1. scan the model library
2. filter the catalog
3. explicitly select models via checkboxes
4. run CivitAI fetch on the selected set

The fetch is selection-based on purpose. This avoids sending unintended models just because they happen to be visible in the current filtered view.

## 5. Use The New Filters

The advanced filter panel now supports more targeted workflow filtering.

Examples:

Filter by workflow model:

- choose `flux1-schnell-fp8` in the `Model` dropdown

Filter by workflow LoRA:

- choose one or more LoRAs in the `LoRA` dropdown

Find files with no LoRA in the workflow:

- choose `No LoRA in workflow`

Exclude a string from the filename:

```text
!dreamshaper
```

or

```text
NOT dreamshaper
```

## Current Notes

This fork intentionally reflects real-world ComfyUI usage rather than an idealized metadata model.

Two practical consequences:

- workflow token storage is heterogeneous, so workflow-derived filters are built to be tolerant of mixed path styles and plain filenames
- model filtering aims to represent actual checkpoint / diffusion-model usage, not every auxiliary asset that might appear in a workflow

## Project Docs

For the current architecture and implementation notes in this fork, see:

- [docs/architecture-plan.md](docs/architecture-plan.md)
- [docs/lessons-learned.md](docs/lessons-learned.md)
- [CHANGELOG.md](CHANGELOG.md)

## Scope And Philosophy

This fork is not trying to become a different product overnight.

The current priorities are:

- stabilize the new handling features
- improve filtering and curation workflows
- make model-management more practical
- continue the architecture cleanup only where it directly helps feature work

In short:

- first make the app even more usable
- then make the internals safer
- only then widen scope again

## License

This fork inherits the licensing context of the upstream project. See the repository license file and the upstream repository for original attribution and licensing details.
