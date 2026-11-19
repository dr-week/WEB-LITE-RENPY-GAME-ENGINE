# Modular Flow Engine — Architecture & Implementation Plan

Structured plan for using `HKUDS/CLI-Anything` patterns inside `modules/modular_flow_engine/` to drive LOLA's Google Flow image generation, download ingestion, and story catalog pipeline.

## 1. Modular Folder Structure & Nomenclature

Mirrors `modules/modular_audio_engine/` so each responsibility lives in its own isolated subfolder (`<= 100` lines per `.py` file):

```text
modules/
  modular_flow_engine/
    __init__.py
    SKILL.md                        # CLI-Anything agent skill spec
    core/
      __init__.py
      batch_builder.py              # Builds [FIELD: {...}; (...)] prompt batches & queries open story beats
      session_state.py              # Persistent REPL session state (.flow_session.json)
    adapters/
      __init__.py
      flow_browser_adapter.py       # Clipboard copy + browser launch to Google Flow
      workbench_adapter.py          # Bridges to developer-tools/ (audit, catalog, preview, organize)
    ingest/
      __init__.py
      download_matcher.py           # Matches Flow downloads to .prompt_manifest.json, writes sidecars + SHA-256
    cli/
      __init__.py
      flow_cli.py                   # Click CLI + --json output + interactive REPL
```

Thin CLI entrypoint: `developer-tools/cli_anything_lola_flow.py` (13 lines) delegates directly to `modules.modular_flow_engine.cli.flow_cli:cli`.

---

## 2. End-to-End Flow Execution Plan

| Stage | Module | Command / Action | Output |
| --- | --- | --- | --- |
| **1. Story Scan** | `core/batch_builder.py` | `prompt story --refresh` | Open `needs_generation` story beats from `image_requests.json` |
| **2. Prompt Batch** | `core/batch_builder.py` | `prompt menu --count 5 --copy` | Structured prompts logged to `.prompt_manifest.json` & clipboard |
| **3. Flow Handoff** | `adapters/flow_browser_adapter.py` | `flow open --count 5` | Copies batch + opens `https://labs.google/fx/tools/flow` in browser |
| **4. Download Ingest** | `ingest/download_matcher.py` | `flow ingest --latest 5` | Renames to `<asset_id>.<ext>`, writes `.json` sidecar + SHA-256, moves to `game/images/<category>/`, rebuilds `image_story_catalog.json` |
| **5. Audit & Place** | `adapters/workbench_adapter.py` | `pipeline preview` / `pipeline audit` | Validates aliases & story targets via `developer-tools/` |

## 3. Verification
- Unit tests: `cd developer-tools && python -m unittest tests/test_cli_anything_flow.py -v`
- JSON CLI check: `python cli_anything_lola_flow.py --json prompt menu --count 2 --seed 42`
