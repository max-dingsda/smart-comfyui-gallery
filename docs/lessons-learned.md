## Lessons Learned

### 2026-04-22: `sg_models` migration gap broke the models page

- Symptom: the models page failed with `Unexpected token '<'` in the browser because `/galleryout/api/models/list` returned an HTML 500 page instead of JSON.
- Root cause: the existing SQLite table `sg_models` was reused from an earlier schema state, but the migration logic only added missing columns to `files`. New model-management fields such as `civitai_status` and `civitai_error` were present in code, but not in the live table.
- Fix: add an explicit `sg_models` schema guard in `smartgallery_core/storage.py` and call it from the model routes before read/write operations.
- Prevention rule: every newly introduced table must get the same incremental migration treatment as legacy tables. Do not rely on `CREATE TABLE IF NOT EXISTS` alone once a feature is already in use.

### 2026-04-22: optional SQLite tuning must not break feature APIs

- Symptom: in the `maxpic` Conda environment, SQLite PRAGMAs such as `journal_mode=WAL` and `synchronous=NORMAL` could raise `sqlite3.OperationalError`.
- Root cause: the runtime environment can open the database but may still reject optional journal/sync configuration calls.
- Fix: make connection-tuning PRAGMAs best-effort instead of mandatory in `smartgallery_core/storage.py`.
- Prevention rule: treat SQLite tuning as an optimization layer, not as a hard dependency for normal route behavior.

### 2026-04-23: `workflow_files` cannot be assumed to contain canonical model-folder paths

- Symptom: the new workflow model/LoRA dropdowns initially rendered empty or showed misleading values because detection logic expected tokens such as `/checkpoints/...` or `/loras/...`.
- Root cause: `workflow_files` stores a mixed set of workflow references. Some entries are full or partial relative paths, but many are plain filenames such as `flux1-schnell-fp8.safetensors` or other non-canonical tokens.
- Fix: classify workflow assets using basename plus known library metadata from `sg_models`, and avoid relying solely on path fragments.
- Prevention rule: treat workflow token storage as lossy and heterogeneous. When building feature logic on top of it, validate assumptions against live database samples first.

### 2026-04-23: CSS grid template areas must remain rectangular

- Symptom: the filter dialog briefly collapsed into a broken layout with overlapping groups after the desktop cleanup pass.
- Root cause: the assigned `grid-template-areas` used a non-rectangular area for `comment`, which makes the whole template invalid and causes the browser to discard the intended grid layout.
- Fix: replace the invalid area map with a valid rectangular desktop grid and assign each filter group explicitly.
- Prevention rule: when refactoring complex dashboards or filter overlays with named grid areas, verify that every named area forms a rectangle before testing visual polish.
