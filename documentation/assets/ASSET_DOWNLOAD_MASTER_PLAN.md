# LOLA — Complete Asset, Logo & Media Download Plan

Master checklist of all remaining assets required for LOLA, exact target paths, approved licenses, and automated verification steps.

---

## 1. Current Inventory (Already Installed)

| Asset Group | Location | Status |
| --- | --- | --- |
| **Typography** (`Plus Jakarta Sans`) | `game/fonts/` | **Complete** (4 weights, SIL OFL 1.1) |
| **UI Icons** (38 PNG icons) | `game/images/ui/icons/` | **Complete** (CC0 1.0) |
| **Glass / Shadow / Blend Surfaces** | `game/images/ui/{glass,shadows,effects}/` | **Complete** (`generate_ui_surfaces.py`) |
| **Solis Bay Base Map** | `game/images/ui/map/solis_bay_day.png` | **Complete** (wired in `navigation.rpy` & `world_map_screen.rpy`) |
| **Lo-Fi Music** (16 `.mp3` tracks) | `game/audio/music/lofi/` | **Complete** |
| **UI & Transition SFX** | `game/audio/sfx/{ui,transitions}/` | **Complete** |
| **Maya Voice & Mumbles** | `game/audio/voice/{maya,tts}/` | **Complete** (8 mumbles + 25+ SAPI5 clips) |

---

## 2. Missing Assets to Download / Generate

### A. Brand Logos & App Icons (`game/images/ui/brand/`)
| Asset | Target Path | Spec | Source / Method |
| --- | --- | --- | --- |
| **LOLA Title Wordmark** | `game/images/ui/brand/lola_logo.png` | `1024x320` transparent PNG | Generate via Google Flow (prompt below) or vector SVG export |
| **LOLA App Emblem** | `game/gui/window_icon.png` & `launcher/tools/lola.ico` | `512x512` PNG + multi-size `.ico` | Export from logo emblem (`Pillow` / `tauri icon`) |
| **Tauri Launcher & Workbench Icons** | `development/{game-launcher,image-workbench}/src-tauri/icons/` | `icon.ico`, `icon.png` | Sync via `npx tauri icon <source.png>` |

**Google Flow Logo Prompt:**
> `[ASSET_ID: ui_brand_lola_logo_v1] [SCENE: Minimalist modern visual novel title logo for "LOLA", isolated centered typography] [STYLE: {Sleek geometric editorial serif-sans hybrid lettering in luminous soft lavender #F2D8FF and warm gold #FFE8A3 accent crescent, subtle glassmorphic sheen}; (clean crisp edges, zero background clutter)] [FRAME: {Centered horizontal wordmark on solid pure black #000000 or pure white #FFFFFF background for clean alpha extraction}] [AVOID: busy gradients, photorealistic background, extra words, subtitles, watermark]`

### B. Environmental Ambience Loops (`game/audio/ambience/`) — *Currently Empty*
| Track | Target Path | License | Source |
| --- | --- | --- | --- |
| **City Street** | `game/audio/ambience/amb_city_street.ogg` | CC0 1.0 | Freesound (`site:freesound.org "city ambience" CC0`) / OpenGameArt |
| **Cafe Murmur** | `game/audio/ambience/amb_cafe_murmur.ogg` | CC0 1.0 | Freesound (`site:freesound.org "cafe ambience" CC0`) |
| **Library Quiet** | `game/audio/ambience/amb_library_quiet.ogg` | CC0 1.0 | Freesound (`site:freesound.org "room tone" OR "library" CC0`) |
| **Rain & Harbor** | `game/audio/ambience/amb_rain_night.ogg` | CC0 1.0 | Freesound (`site:freesound.org "rain window" CC0`) |

### C. Extra Solis Bay Map Pin Icons (`game/images/ui/icons/`)
- **Needed:** `pin_tower.png`, `pin_viewpoint.png`, `pin_harbor.png`, `pin_slum.png`, `lock.png` (`64x64` white transparent PNGs).
- **Source:** `shorepine/kenney` (`Game Icons Expansion` / `Board Game Icons`, CC0 1.0).

### D. New District Backgrounds (`game/images/public_places/`)
- Generate 4 neutral-daylight scenes via Google Flow + `cli_anything_lola_flow.py` for the new Solis Bay sectors:
  - `bg_viewpoint` (Pinecrest Ridge overlook)
  - `bg_tower` (Observation Tower plaza)
  - `bg_slum_quarter` (Old Dockside Tenements)
  - `bg_harbor_pier` (Solis Harbor wooden piers)

### E. Optional Neural Cute-Girl TTS Upgrade
```bash
pip install edge-tts
python developer-tools/voice_maker.py synth --limit 50 --backend edge
```

---

## 3. Post-Download Verification Commands

```bash
python developer-tools/checks/fix_non_ascii_assets.py --apply
python developer-tools/checks/smoke_test_renpy.py
```
