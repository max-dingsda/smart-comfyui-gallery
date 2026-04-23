# SmartGallery Refactor Plan

## Goal

Evolve SmartGallery from a single-file Flask application into a modular monolith that can absorb:

- model management
- batch renaming
- future workflow-centered extensions

without turning `smartgallery.py` into a higher-risk bottleneck.

## Current Constraints

- Runtime behavior is concentrated in `smartgallery.py`
- Route handlers contain business logic, storage access, and filesystem operations
- `templates/index.html` contains a large amount of inline UI logic
- Shared concerns such as config, DB access, path normalization, and background work are reused across unrelated features

## Target Shape

Keep one deployable app, but split responsibilities into modules:

- `config`
- `startup`
- `gallery`
- `workflow`
- `files`
- `storage`
- `jobs`
- `models`
- `renaming`

## Domain Boundaries

### `gallery`

- folder navigation
- search/filter state
- lightbox and listing payloads
- favorites and presentation-oriented file actions

### `workflow`

- workflow extraction from images/videos
- prompt and workflow-files indexing
- node summary generation
- workflow download/serialization

### `files`

- file rename/move/delete primitives
- thumbnail generation
- MIME and media handling
- safe path resolution

### `storage`

- SQLite connection management
- schema and migrations
- repository queries
- transaction helpers

### `jobs`

- long-running rescans
- zip creation
- AI indexing queue/watcher
- future model scans and rename jobs

### `models`

- model library scan
- model metadata
- source/provider sync
- references from workflow files and prompts

### `renaming`

- rename rule definitions
- preview/dry-run
- conflict detection
- execution journal and undo support

## Migration Strategy

1. Extract stable cross-cutting concerns first.
2. Preserve route behavior while moving code behind module seams.
3. Introduce new features only after the basic service boundaries exist.

## Recommended Refactor Waves

### Wave 1

- extract configuration loading
- extract startup checks/banner/update logic
- keep route behavior unchanged

### Wave 2

- centralize DB access into `storage`
- centralize path helpers and file operations into `files`
- reduce direct `sqlite3.connect(...)` and `os/shutil` usage from routes

### Wave 3

- move workflow extraction and node summary into `workflow`
- move background watcher/queue logic into `jobs`

### Wave 4

- add batch renaming as the first new bounded domain
- implement preview, validation, execution log, and undo design

### Wave 5

- add model management on top of the new storage/workflow/job primitives

## Why Batch Renaming First

- narrower scope than model management
- forces a clean design for preview vs execution
- exercises file operations, DB updates, and background jobs
- creates patterns directly reusable for model operations

## Immediate Next Step

After Wave 1, extract:

- DB bootstrap and connection helpers into `storage`
- file/path helpers into `files`

Those two seams are the minimum required before building `renaming` safely.

## Current Status

The first planned seams are now in place:

- `smartgallery_core/storage.py`
- `smartgallery_core/files.py`
- `smartgallery_core/renaming.py`
- `smartgallery_core/models.py`

The app is still a modular monolith rather than a fully separated service design, but the new feature work no longer has to start life inside `smartgallery.py`.

## Implemented Since Baseline

### Storage

- centralized SQLite connection creation
- centralized DB bootstrap and schema creation
- explicit `sg_models` schema guard for incremental model-management rollout
- best-effort SQLite PRAGMA setup to avoid hard failures in restrictive Windows/Conda environments

### Files

- extracted unique-path generation
- extracted safe file deletion helpers
- created a stable base for rename/move/copy/delete operations

### Renaming

- workflow-aware rename core extracted into `smartgallery_core/renaming.py`
- batch rename suggestion, preview, and execution endpoints added
- current UI integrated into the `2.11` selection flow instead of reviving the old plugin shell
- rename naming strategy supports model-first and prompt-first organization

### Models

- model library scan extracted into `smartgallery_core/models.py`
- three-section model catalog implemented:
  - checkpoints
  - loras
  - embeddings
- checkpoint scan includes both `models/checkpoints` and `models/diffusion_models`
- first CivitAI enrichment flow implemented for single-model and selected-batch lookups
- model-manager selection is now explicit via checkboxes instead of relying on the current visible filter result
- model-manager CivitAI fetch now exposes progress feedback in the UI while selected models are processed

### Gallery Filters

- filename search now supports negative matching for practical exclusion workflows:
  - `!term`
  - `NOT term`
  - `!= term`
- advanced filters now include:
  - workflow model filter
  - workflow LoRA filter
  - rating filter
- workflow model and LoRA filters use dropdown-based selections populated from indexed `workflow_files` values instead of raw free-text guessing
- LoRA filtering now supports an explicit `No LoRA in workflow` state for workflows that do not reference any LoRA
- filter-panel layout was reworked on desktop to keep workflow-related filters grouped coherently instead of relying on incidental auto-grid placement

## Revised Near-Term Plan

### Completed

- Wave 2 foundation: `storage` and `files`
- first bounded domain: `renaming`
- initial `models` slice with scan, list, and first CivitAI enrichment

### Next

- harden workflow-derived asset classification further where tokenizer ambiguity still exists
- improve dropdown UX for large workflow-model/LoRA lists:
  - in-dropdown search
  - clearer labels
  - better ordering/grouping
- extend model metadata handling beyond first-pass local/CivitAI fields
- connect model catalog to workflow/image usage where useful
- continue shrinking route-level DB and filesystem logic inside `smartgallery.py`
