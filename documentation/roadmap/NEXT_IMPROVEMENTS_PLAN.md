# LOLA — Next Improvements Master Plan

Prioritized roadmap of concrete improvements across gameplay polish, story structure, art/map integration, and developer tooling, based on current lint, test, and audit findings.

---

## Priority 1 — Stability, Lint & Test Health (Quick Wins)

1. **[x] Full Python Test Suite Passing (53/53)**
   - Verified `test_audio_toolkit.py`, `test_modular_audio_engine.py`, `test_vector_and_upscale.py`, `test_cli_anything_flow.py`, and `test_modular_story_engine.py` all pass (`53` tests) when run from repo root with `PYTHONPATH=developer-tools;.`; automated in `launcher/tools/Verify Project.bat`.
2. **[x] Fix Duplicate `config.main_menu_music` Warning**
   - Removed duplicate definition in `game/script.rpy` (canonical owner: `game/options.rpy:6`).
3. **[x] Normalize Non-ASCII Filenames in `game/images/`**
   - Created `developer-tools/checks/fix_non_ascii_assets.py`, renamed all 18 `…` image/sidecar files to ASCII-safe names, and integrated the check into `run_all_checks.py`.
4. **[x] Unified Pre-Launch Gate (`developer-tools/checks/run_all_checks.py`)**
   - Combines `verify_game_assets.py`, `story_integrity.py`, and `two_option_validator.py`, wired into `launcher/tools/Verify Project.bat`.

---

## Priority 2 — Story Structure & Narrative Depth

1. **[x] Enforce 2-Option Rule Across Legacy Story Files**
   - Refactored `day_free_morning.rpy`, `day_02_home.rpy`, and `day_01_work_search.rpy` to strictly 2-option menus, added `day_end.rpy`/`image_story_hub.rpy` to system-hub allowlist, and enabled strict 2-option enforcement in `run_all_checks.py` (`0` violations).
2. **[x] Expand `modules/modular_story_engine/` Variations**
   - Added tone presets (`hustle`, `cozy`, `tense`, `playful`), all Solis Bay districts (`viewpoint`, `tower`, `slum_quarter`, `harbor_pier`), and automatic `set_flag(...)` continuity hooks.
3. **Week 2 & New District Story Arcs**
   - Add playable beats for the newly mapped Solis Bay districts (`viewpoint`, `tower`, `slum_quarter`, `harbor_pier`) using `story_maker.py generate`.

---

## Priority 3 — UI/UX Polish & World Map Completion

1. **[x] Complete Glassmorphism Rollout on Remaining Screens**
   - Applied `gui.glass_elevated`, `gui.glass_card`, `gui.glass_pill`, `gui.glass_btn_*`, `ui_panel_entrance`, and `ui_sfx_confirm`/`ui_sfx_back` to `confirm.rpy`, `notifications.rpy`, `save_load_styles.rpy`, `preferences_styles.rpy`, and `navigation_styles.rpy`.
2. **[x] Wire Solis Bay Curved 3x3 Map (`solis_bay_day.png`)**
   - `game/images/ui/map/solis_bay_day.png` is present and `screen world_map_screen()` is wired into `game/30_screens/navigation.rpy` (`Explore Solis Bay Map`) with `travel_from_map` pin navigation.
3. **Thumbnail Previews in `lola-image-workbench`**
   - Complete the remaining follow-up items in `development/IMAGE_WORKBENCH_TASKS.md` (thumbnail previews alongside dialogue targets before placement + reviewed image tags).

---

## Priority 4 — Code Hygiene & Automation

1. **[x] Split `launcher_core.rs` (`120` lines → `<= 100` lines)**
   - Extracted `encode_b64` / `hero_data_url` into `development/game-launcher/src-tauri/src/media.rs` (`26` lines; `launcher_core.rs` now `97` lines).
2. **[x] Exclude `game/images/ui/` from Story-CG Quality Warnings**
   - Updated `developer-tools/audit_images.py` so 9-slice UI textures and icons are not flagged as low-resolution story CGs.
3. **[x] Automated Ren'Py Compile & Lint Smoke Test**
   - Created `developer-tools/checks/smoke_test_renpy.py` running static checks, headless `renpy.py compile`, and `renpy.py lint`.
