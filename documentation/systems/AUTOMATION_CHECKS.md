# LOLA Game Development Automation & QA Suite

## Single-Command Verification
Run everything (story integrity, asset hygiene, module line-count check, Story DB sync, all unit tests, and Ren'Py 8.6.0 lint):
```powershell
$env:PYTHONPATH="developer-tools"
python developer-tools/check_everything.py
```
Use `--fast` to skip Ren'Py SDK lint during rapid iteration.

---

## Complete Automation Script Map
1. **Master Verification (`check_everything.py` + `checks/`)**
   - `checks/story_integrity.py` — Validates every `jump`/`call` and `story_starts.json` `next_label` against defined `label`s, plus JSON syntax.
   - `checks/asset_hygiene.py` — Checks `audio/` and `ui/icons/` references and flags non-ASCII image filenames.
   - `checks/module_health.py` — Enforces the modular file-size limit across `.py` and `.rpy` files.
2. **Asset & Visual Quality Pipeline**
   - `import_collection.py` — Batch-imports external image folders with PIL visual QC (`image_quality/checks.py`), SHA-256 deduplication, and catalog rebuild.
   - `audit_images.py` — Scans all game files and persists asset/quality/feedback state in `developer-tools/image_audit.sqlite`.
   - `replace_low_quality.py` — Replaces `needs_regen` or low-score alias images with higher-quality matches.
3. **Story, Prompt & Feedback Loop**
   - `evaluate_story_db.py` — Syncs `story_nodes`, `story_choices`, `story_endings`, and `story_image_links` into SQLite.
   - `sync_feedback.py` — Imports in-game Thumbs Up/Down ratings (`game/data/image_feedback.json`) into SQLite.
   - `prompt_batch.py` & `flow_session.py` — Generates 5-prompt Flow Agent batches and tracks per-session generation/download counts.
   - `lola_api_server.py` — Local FastAPI bridge (`127.0.0.1:8765`) for workbench/agent integration.
