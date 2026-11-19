# Modular Flow Engine (`CLI-Anything` Skill)

Self-contained, modular Google Flow & image pipeline harness located in `modules/modular_flow_engine/` (mirroring `modules/modular_audio_engine/`).

## Subfolder Architecture
- `core/` — `batch_builder.py` (structured `[FIELD: {...}]` prompt batches & story request lookup), `session_state.py` (REPL state).
- `adapters/` — `flow_browser_adapter.py` (clipboard + browser handoff to Google Flow), `workbench_adapter.py` (runs `audit`, `catalog`, `preview`, `organize`).
- `ingest/` — `download_matcher.py` (matches downloaded Flow images to `.prompt_manifest.json`, writes sidecar JSON + SHA-256, updates `image_story_catalog.json`).
- `cli/` — `flow_cli.py` (Click CLI, `--json` deterministic output, interactive `lola-flow>` REPL).
