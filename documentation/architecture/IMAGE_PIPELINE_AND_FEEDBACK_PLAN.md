# LOLA Image Pipeline, Visual Audit, Feedback UI & Database Plan

## 1. Goals & Problem Statement
1. **Batch-import 63 new images** from `C:\Users\disha\Downloads\story collection 01` into `game/images/<category>/`, catalog them for the story loop, and verify no duplicates or broken references exist.
2. **Fix automation & animation issues**:
   - `audit_images.py` currently drops/recreates `image_audit.sqlite` on every run and flags format strings (`ui/icons/%s.png`) and test screenshot outputs as missing files.
   - `ingest_flow_download.py` / `integrate_story_images.py` lack a clean batch-folder intake path for named images without `.json` sidecars and do not automatically refresh `image_story_catalog.json` or run visual checks.
   - `main_menu_slideshow.rpy` stretches non-16:9 images (`xysize=(1920, 1080)` without `fit="cover"`), uses a static `timer` delay, and runs `5.0s` ease animations longer than `3.0–4.0s` slide intervals.
3. **Add lightweight visual quality checking** (dimensions, aspect ratio, file integrity, brightness/contrast, edge sharpness, perceptual/content hashing) so bad/corrupted/low-res images are caught automatically.
4. **Add in-game bottom-right Thumbs Up / Thumbs Down UI** so players/testers can rate the currently displayed scene image and submit quick feedback reasons.
5. **Maintain a persistent lightweight SQLite database** (`developer-tools/image_audit.sqlite`) that connects:
   - Asset inventory & visual quality metrics
   - Script/alias references
   - In-game player feedback (`image_feedback`)
   - Prompt generation & regeneration queue (`prompt_history`)
6. **Strict modularity**: Keep every Python and Ren'Py file under **100–150 lines** by splitting responsibilities into small, single-purpose modules.

---

## 2. End-to-End Data Flow

```text
[External Folder / Flow Downloads]
        │
        ▼  (1. Batch Intake + Visual Check)
developer-tools/import_collection.py
  ├─ image_quality/checks.py      (PIL: integrity, size, aspect, brightness, sharpness)
  ├─ organize_images.py           (category inference)
  └─ image_import/core.py         (sha256 dedup, move to game/images/<category>/)
        │
        ▼  (2. Story Catalog & Reconciliation)
developer-tools/reconcile_story_images.py / build_image_story_catalog.py
  └─ game/data/image_story_catalog.json
        │
        ▼  (3. Persistent SQLite Sync)
developer-tools/audit_images.py
  ├─ image_audit/scanner.py       (assets, aliases, script refs; skips format/test artifacts)
  ├─ image_audit/database.py      (persistent tables: image_assets, image_feedback, prompt_history)
  └─ image_quality/checks.py      (populates width, height, quality_score, quality_flags)
        │
        ▼  (4. In-Game Playback & Rating UI)
game/30_screens/image_feedback.rpy + game/00_systems/art/feedback_store.rpy
  ├─ Bottom-right Thumbs Up / Thumbs Down buttons on overlay
  ├─ Quick reason picker on Thumbs Down
  └─ Saves to game/data/image_feedback.json (+ persistent.image_feedback)
        │
        ▼  (5. Feedback Sync & Improved Prompt Generation)
developer-tools/sync_feedback.py
  ├─ Imports game/data/image_feedback.json -> image_audit.sqlite (image_feedback)
  ├─ Flags down-voted assets in image_assets.status = 'needs_regen'
  └─ image_generation/feedback_prompts.py injects corrective hints into next prompts
```

---

## 3. Modular File Plan (All Files < 100–150 Lines)

### A. Developer Tools (Python)
1. `developer-tools/image_quality/`
   - `__init__.py` — Exports `inspect_image`, `inspect_directory`.
   - `checks.py` (~95 lines) — Lightweight PIL-only visual checks: readability, `(width, height)`, aspect ratio vs 16:9, mean brightness, contrast std-dev, Laplacian-like edge sharpness score, quality flags, and pass/warn/fail status.
2. `developer-tools/image_audit/`
   - `schema.py` (~65 lines) — Persistent SQLite schema (`image_assets`, `image_references`, `image_aliases`, `alias_references`, `image_feedback`, `prompt_history`, plus `missing_images` / `missing_aliases` / `flagged_assets` views). Never drops `image_feedback` or `prompt_history`.
   - `database.py` (~85 lines) — Upserts audit scan + visual quality results, queries missing refs and flagged assets.
   - `scanner.py` (~65 lines) — Fixes `%s` format-string false positives and ignores `tests/ui_testcases.rpy` screenshot output filenames.
   - `feedback_sync.py` (~75 lines) — Reads `game/data/image_feedback.json`, inserts/updates `image_feedback` in SQLite, marks down-voted assets as `needs_regen`, and exports regeneration candidates.
3. `developer-tools/import_collection.py` (~95 lines) — CLI to inspect, visually validate, deduplicate (sha256), categorize, write sidecar `.json`, move images from a source folder (e.g. `C:\Users\disha\Downloads\story collection 01`) into `game/images/<category>/`, rebuild `image_story_catalog.json`, and update `image_audit.sqlite`.
4. `developer-tools/sync_feedback.py` (~45 lines) — CLI wrapper to sync `game/data/image_feedback.json` into `image_audit.sqlite` and print regeneration recommendations.
5. `developer-tools/image_generation/feedback_prompts.py` (~70 lines) — Reads `needs_regen` + feedback reasons from `image_audit.sqlite` and appends targeted corrective prompt guidance (e.g., outfit consistency, anatomy, framing) when generating new prompts.

### B. Game UI & Animations (Ren'Py)
1. `game/00_systems/art/feedback_store.rpy` (~75 lines) — Tracks `current_scene_image` (resolving `cg_`/`bg_` aliases to `images/...` paths and `image_story_path`), records Thumbs Up/Down ratings + reason tags, and persists them to `game/data/image_feedback.json` and `persistent.image_feedback`.
2. `game/30_screens/image_feedback.rpy` (~85 lines) — Renders the bottom-right Thumbs Up / Thumbs Down buttons (`zorder 105`, `xalign 0.99`, `yalign 0.992`) and a compact feedback-reason modal when Thumbs Down is clicked.
3. `game/options.rpy` — Registers `"image_feedback_overlay"` in `config.overlay_screens`.
4. `game/30_screens/main_menu_slideshow.rpy` — Fixes `fit="cover"` aspect handling, aligns transform duration (`3.8s`) with slide duration, and ensures smooth transitions.

### C. Tests & Verification
1. `developer-tools/tests/test_image_quality.py` (~65 lines) — Tests visual quality checks (good image, dark/blank image, corrupt file).
2. `developer-tools/tests/test_feedback_db.py` (~75 lines) — Tests persistent SQLite schema, feedback sync, and prompt guidance generation.
3. End-to-end execution:
   - Run `import_collection.py` on `C:\Users\disha\Downloads\story collection 01`
   - Run `audit_images.py` and `reconcile_story_images.py`
   - Run `python -m unittest discover -s developer-tools/tests -v`
   - Run Ren'Py 8.6.0 `lint` to verify zero script/screen errors.
