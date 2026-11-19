# LOLA — Phase 1 Audit & Roadmap

Record of the audit performed on the existing project, plus the phased plan.
Update the task tracker at the bottom as work lands.

## 1. Project shape

- Engine: Ren'Py `8.6.0.26110915` at `C:\RenPy\renpy-8.6.0\renpy-8.6.0-sdk`
- Project basedir (`C:\amd\aa\ASD\daa\GAME\LALALAND\LOLA\LOLA`): houses `game/`, `developer-tools/`, `development/`, `documentation/`, and `tests/`.
- Content: `0.1.0 vertical slice`, protagonist Maya (19), full Days 1–7 Week 1 story arc (`day_router.rpy` -> `day_01_*` -> `day_02_*..day_06_*` -> `week_01_evaluation` -> Week 2 open life).
- Lint (verified 2026-11-15): **exit 0**, zero errors and zero warnings (`162 dialogue blocks`, `994 words`, `40 menus`, `43 images`, `19 screens`).

## 2. Architecture as found

| Layer | Files | Notes |
| --- | --- | --- |
| Entry | `script.rpy` | `label start` → `game_start`; sets ~40 globals; registers Elena; jumps `day_01_home` |
| State | `00_systems/core/state.rpy`, `state_helpers.rpy` | ~35 `default`s; protagonist dict; flag + event helpers |
| Time | `00_systems/time/time_manager.rpy` | 4 slots (morning…night); `start_new_day()` |
| Stats | `00_systems/player/stats_manager.rpy` | 8 bounded stats + emotional state |
| Economy | `economy/{economy,wallet,investment}_manager.rpy` | cash + ledger + offline Bitcoin cost-basis model |
| Education | `education/college_manager.rpy` | progress, class, library, assignments |
| Work | `work/employment_manager.rpy` | cafe barista job, shifts, wages |
| World | `world/{location_manager,location_travel}.rpy` | 6 locations, travel/unlock/availability |
| Social | `social/*.rpy` (6 files) | names, registry, encounters, relationships, events |
| Characters | `10_characters/*.rpy` | protagonist, cast helpers, encounter→recurring, scene art |
| Art | `00_systems/art/{artwork_display,image_story_loop}.rpy` | `fit_scene_art()`; JSON catalog loader |
| Story | `40_story/prologue/*.rpy`, `40_story/image_loop/image_story_hub.rpy` | Day 1 route, cafe route, day end, image hub |
| Screens | `30_screens/*.rpy` + `theme/gui_0*.rpy` | main menu, game menu, status, character info, map, save/load, prefs, history |
| Data | `data/image_story_catalog.json`, `data/asset_manifest.json` | catalog populated; manifest placeholder |
| Images | `images/` (12 categories, hundreds of JPGs) | referenced through `scene_art.rpy` + `generated_art_001.rpy` |

## 3. Issues found

1. **FIXED — 3 jumps to a nonexistent label.** `image_story_hub.rpy` (×2) and
   `day_02_home.rpy` jumped to `day_end`; the file defines `end_day`.
   Corrected to `jump end_day`; lint now reports none.
2. **Stale reports.** `errors.txt` and `tests/LINT_REPORT_8.6.0_INITIAL.*`
   describe two errors that no longer exist (the `default` inside
   `init python:` was already removed; the `imagebutton` text statement is
   already restructured). They should be regenerated, not trusted.
3. **`world_map` grid is fragile.** `grid 3 2` requires exactly 6 children,
   but the loop adds a variable number of `fixed` cells. It will raise
   "Not enough children"/"Too many children" at runtime whenever the
   available-location count differs from 5.
4. **Duplicate/overlapping cafe entry.** `50_world_map/world_map.rpy` defines
   `location_cafe`, while `20_locations/work/location_work.rpy` defines
   `location_work` for the same place; `travel_to_cafe` lives in the prologue.
   Only `location_cafe` is reachable from the map (via `Jump("location_cafe")`).
5. **`assets/`, `audio/`, `sprites/`, `routes/`, `50_world_map` partial,
   `40_story/chapters`, `40_story/endings` are empty scaffolding.**
6. **`data/asset_manifest.json` is a placeholder** (`assets: []`).
7. **25 image filenames contain non-ASCII characters** (e.g. `…`, `é`) —
   warnings only, but they block ZIP distributions and are easy to avoid.
8. **Orphan image definitions.** `generated_art_001.rpy` defines 26 images,
   but only a handful are used by story files; `fit_scene_art` handles the rest.
9. **No picture pipeline in the project.** No `.py` files exist;
   `integrate_story_images.py` (referenced in a comment) is absent. The
   "picture environment" is not present in this folder — it must be supplied
   or re-created before image-management work can be wired in.
10. **Editor SDK mismatch.** `.vscode/settings.json` points the Ren'Py Warp
    extension at SDK 8.5.2 while the project runs on 8.6.0.

## 4. Roadmap

- **Phase 1 Audit** — done (this file).
- **Phase 2 Analysis** — done (issues above).
- **Phase 3 Planning** — ordered backlog below.
- **Phase 4 Implementation** — one system per change, lint after each.
- **Phase 5 Testing** — lint + brief launch + `tests/ui_testcases.rpy`.
- **Phase 6 Integration** — story ↔ images ↔ economy.
- **Phase 7 Final validation** — full pass + launcher confirmed.

### Backlog (ordered, one at a time)

1. ~~Fix broken `day_end` jumps~~ — done.
2. Launcher in `launcher/` (Launch Game, Version, Settings, Exit) — done.
3. Make `world_map` tolerate a variable number of locations
   (replace hard-coded `grid 3 2` with a `vpgrid`/`grid` sized from data).
4. De-duplicate the cafe route (`location_cafe` vs `location_work`).
5. Confirm/obtain the picture environment, then reconcile
   `image_story_catalog.json` ↔ `scene_art.rpy` ↔ actual files.
6. Wire story beats to the correct images (placement review).
7. Economy ↔ story verification (bus fare, coffee, wages, BTC).
8. Regenerate lint/error reports; clean non-ASCII filenames.
9. Run `tests/ui_testcases.rpy`.

## 5. Task tracker

- [x] Phase 1 audit documented
- [x] Broken `day_end` jumps fixed (lint clean)
- [x] Launcher moved to `development/game-launcher/` and verified
- [x] `world_map` grid robustness (`vpgrid cols 3 allow_underfull True`)
- [x] Cafe route de-duplication (`location_cafe` unified into `location_work`, colliding `work_shift` label renamed)
- [x] Picture environment integrated & modularized into `developer-tools/` subpackages (`generate_image_list.py`, `integrate_story_images.py`, `audit_images.py`, `reconcile_story_images.py`, `build_image_story_catalog.py`, `organize_images.py`)
- [x] Unused `cg_*` art wired into Days 1–5; City Journal catalog synced (`254` moments across `360` images)
- [x] Economy/stats/story verification (`intelligence`, `appeal`, skills, cash, fictional BTC; 2–3 choices per menu)
- [x] Non-ASCII image filenames normalized to ASCII; `tests/renpy-lint.stdout.log` regenerated with 0 warnings
- [x] Workbench UI simplified (`1. Dashboard`–`5. Asset Catalog`) and verified (`npm run build` + `cargo test`)
