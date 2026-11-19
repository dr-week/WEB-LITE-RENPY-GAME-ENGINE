# LOLA Asset Management & Execution Plan

Structured plan covering asset inventory decisions, remaining downloads, screen integration tasks, and the tooling pipeline.

---

## 1. Asset Audit & Download Decisions

| Asset Domain | Current State | Decision | Target Location | License / Source |
| --- | --- | --- | --- | --- |
| **Typography** | `Plus Jakarta Sans` (4 weights) | **Complete** | `game/fonts/` | SIL OFL 1.1 (`tokotype/PlusJakartaSans`) |
| **Core UI Icons** | 19 white 2x PNGs | **Complete** | `game/images/ui/icons/` | CC0 1.0 (`shorepine/kenney`) |
| **UI SFX** | 10 WAV interface sounds | **Complete** | `game/audio/sfx/ui/` | CC0 1.0 (`Calinou/kenney-interface-sounds`) |
| **Glass / Shadow / Blend** | 10 procedural PNGs | **Complete** | `game/images/ui/{glass,shadows,effects}/` | Generated (`developer-tools/generate_ui_surfaces.py`) |
| **Background Music** | **Empty** | **Download Needed** (4–5 `.ogg` loops) | `game/audio/music/` | CC0 / CC-BY (OpenGameArt / Freesound / Incompetech) |
| **Scene Ambience** | **Empty** | **Download Needed** (3–4 `.ogg` loops) | `game/audio/ambience/` | CC0 (Freesound / OpenGameArt) |
| **Map & Stat Icons** | Partial (19 base icons) | **Optional Expand** (pin, heart, coin, book) | `game/images/ui/icons/` | CC0 1.0 (`shorepine/kenney` Expansion) |
| **Story CGs & BGs** | Managed pipeline | **Generate via Workbench** (never generic packs) | `game/images/<category>/` | Sidecar + `ASSET_TAXONOMY.md` |

---

## 2. Screen Integration Plan (Downloaded Assets)

All screens reuse [gui_06_glass_surfaces.rpy](../../game/30_screens/theme/gui_06_glass_surfaces.rpy), [gui_07_blends_transforms.rpy](../../game/30_screens/theme/gui_07_blends_transforms.rpy), and [gui_08_ui_audio.rpy](../../game/30_screens/theme/gui_08_ui_audio.rpy).

| Screen / Module | Glass & Shadow | Opacity & Blend | Icons & SFX |
| --- | --- | --- | --- |
| `main_menu.rpy` | `gui.glass_elevated`, `gui.glass_pill`, `gui.glass_btn_*` | `ui_vignette_overlay(0.55)` (`multiply`) | Global button `click_001` / `click_002` |
| `dialogue.rpy` & `dialogue_styles.rpy` | `gui.glass_elevated` window, `gui.glass_pill` namebox | `ui_glass_opacity` | `ui_sfx_select` on choice pick |
| `status.rpy` & `status_styles.rpy` | `gui.glass_card` summary/columns | `ui_panel_entrance` | `star.png`, `barsHorizontal.png` |
| `character_info.rpy` | `gui.glass_card` relationship cards | `ui_panel_entrance` | `star.png`, `information.png` |
| `navigation.rpy` & `game_menu.rpy` | `gui.glass_panel`, `gui.glass_btn_*` | `ui_vignette_overlay` | `gear.png`, `save.png`, `home.png`, `power.png`, `return.png` |
| `confirm.rpy` & `notifications.rpy` | `gui.glass_elevated` modal, `gui.glass_pill` toast | `ui_blend_multiply_shadow` backdrop | `confirmation_001.wav`, `back_001.wav`, `glass_001.wav` |
| `save_load.rpy`, `preferences.rpy`, `history.rpy` | `gui.glass_card` slots, `gui.glass_panel` | `ui_panel_entrance` | `save.png`, `trashcan.png`, `audioOn/Off.png`, `ui_sfx_open`/`close` |
| `50_world_map/` | `gui.glass_pill` location pins | `ui_vignette_overlay`, `ui_blend_add_sheen` | `arrowRight.png`, `ui_sfx_select` |

---

## 3. Asset Management Tools & Ownership

| Tool | Entry Point | Owns | Outputs |
| --- | --- | --- | --- |
| **LOLA Image Workbench** | `launcher/tools/Launch Image Workbench.bat` | Visual intake, request cards, audit, placement | `game/images/`, `game/10_characters/`, `game/40_story/` |
| **Story Prompt Generator** | `developer-tools/generate_image_list.py` | Scans unillustrated dialogue beats | `image_generation_list.md`, `image_requests.json` |
| **Image Intake & Router** | `developer-tools/integrate_story_images.py` | Validates sidecars, moves art, writes aliases | Categorized folders + `.rpy` aliases |
| **Reconciliation & Audit** | `developer-tools/reconcile_story_images.py`, `audit_images.py` | Detects unused/missing art & places matches | `image_audit.sqlite`, story `scene` lines |
| **City Journal Catalog** | `developer-tools/build_image_story_catalog.py` | Builds gallery/journal data | `game/data/image_story_catalog.json` |
| **UI Surface Generator** | `developer-tools/generate_ui_surfaces.py` | Procedural 9-slice glass, shadow & blend PNGs | `game/images/ui/{glass,shadows,effects}/` |
| **Ren'Py Lint** | `launcher/tools/Lint LOLA.bat` | Validates `.rpy` syntax, styles, fonts, images, audio | Lint report (exit code 0) |
| **Player Game Launcher** | `launcher/Play LOLA.bat` | Single-instance silent launch to Main Menu | `launcher/last_launch.log` |

---

## 4. Phased Execution Tasks

### Phase A — Core UI Polish (Remaining Screens)
- [ ] Wire `gui.glass_card`, `gui.glass_elevated`, and `ui_panel_entrance` into `confirm.rpy`, `notifications.rpy`, `save_load_styles.rpy`, `preferences_styles.rpy`, `character_info_styles.rpy`, and `navigation_styles.rpy`.
- [ ] Add Kenney icons (`gear.png`, `save.png`, `home.png`, `return.png`, `audioOn.png`, `audioOff.png`, `checkmark.png`, `cross.png`) to quick menu and game menu headers.
- [ ] Bind semantic SFX (`ui_sfx_confirm` on Save/New Game, `ui_sfx_back` on Return/Cancel, `ui_sfx_glass` on notifications).

### Phase B — Music & Ambience Acquisition
- [ ] Download 4–5 CC0/CC-BY `.ogg` music loops into `game/audio/music/` (menu, home, campus, cafe, night) and document credits in `documentation/assets/AUDIO_CREDITS.md`.
- [ ] Download 3–4 CC0 `.ogg` ambient loops into `game/audio/ambience/` (city, cafe, library, rain).
- [ ] Create `game/00_systems/art/audio_tracks.rpy` (≤ 100 lines) with `define` constants and `play music` / `play ambience` helpers.

### Phase C — World Map & Story Visuals
- [ ] Expand `game/images/ui/icons/` if needed for map pins and stat badges.
- [ ] Run `LOLA Image Workbench` → `3. Story Prompts` to generate and place missing `cg_*` story beats into `game/40_story/`.

### Phase D — Quality Gates (Every Change)
- [ ] Keep all `.rpy`, `.py`, `.pyw`, `.ts`, `.rs` files ≤ 100 lines (`TARGET_STRUCTURE.md`).
- [ ] Keep all asset filenames ASCII-only (`a-z`, `0-9`, `_`, `-`).
- [ ] Run `launcher/tools/Lint LOLA.bat`, `python -m unittest discover -s tests -p "test_*.py"`, and `cargo test` before release.
