# LOLA UI/UX Modular Migration Plan

> **Goal:** Upgrade LOLA's Ren'Py UI/UX to modern, crisp, diegetic standards by combining LOLA's existing purple/indigo glassmorphism & `PlusJakartaSans` identity with the best modular open-source Ren'Py patterns and *Dispatch* UI/UX heuristics—without rewriting the Ren'Py engine.

---

## 1. Combined Architecture (Best of Each Source)

| Component | Source / Inspiration | Role in LOLA |
| :--- | :--- | :--- |
| **Design Token System** | SCSS variables mindset + `EasyRenPyGui` | Single `ui_tokens.json` driving `gui_01_colors_fonts.rpy`, `*_styles.rpy` tokens, and `generate_ui_surfaces.py` RGBA values. |
| **Frosted Glass & Shaders** | Ren'Py 8 GLSL Blur + LOLA `gui_06_glass_surfaces.rpy` | Upgrade flat translucent PNGs to true backdrop-blurred glass panels (`gui_07_blends_transforms.rpy`). |
| **Unified Vector Icons** | `RuolinZheng08/renpy-template` + `feathericons/feather` | Replace mixed `.png`/`.webp` UI icons with crisp `@2x` PNGs rendered from Feather SVGs in LOLA's palette. |
| **Live Layout Inspector** | `Wendy-Nam/RenPy-LayoutTool` | Dev-only hotkey (`L`) overlay to position and align UI elements in-game instead of trial-and-error reloads. |
| **Diegetic & QoL UX** | *Dispatch* (`DISPATCH_BENCHMARK_AND_LESSONS.md`) | Color-coded map pin urgency states, 3-tier acoustic hierarchy, `text_scale` / `dialogue_pace` / `high_contrast` accessibility toggles. |

All third-party reference kits are kept modular and isolated under `developer-tools/ui_kits/` so Ren'Py does not auto-compile example `.rpy` files inside `game/`.

---

## 2. Phased Migration Schedule

### Phase 1: Single Source of Truth (SCSS-Style Tokens + Surface Compiler)
**Objective:** Eliminate hardcoded colors, paddings, and RGBA tuples duplicated across `.rpy` and Python.
- **Inputs:** `game/30_screens/theme/gui_01_colors_fonts.rpy`, `developer-tools/generate_ui_surfaces.py`, `game/30_screens/*_styles.rpy`.
- **Tasks:**
  1. Create `developer-tools/ui_tokens.json` capturing LOLA's exact palette (`#9b59b6`, `#8e44ad`, `#e8d5f5`, `#6366f1`, `#ffffff`, etc.), typography (`PlusJakartaSans`), spacing scale, border radii, and glass surface specs.
  2. Build `developer-tools/compile_ui_tokens.py` to:
     - Regenerate `game/30_screens/theme/gui_01_colors_fonts.rpy` (and a `gui_00_tokens.rpy` spacing/radius module).
     - Drive `developer-tools/generate_ui_surfaces.py` from `ui_tokens.json` instead of hardcoded RGBA tuples.
  3. Refactor `game/30_screens/dialogue_styles.rpy` and sibling `*_styles.rpy` files to reference token variables.
- **Exit Criteria:** Changing a single color or radius in `ui_tokens.json` and running one Python command updates both `.rpy` styles and 9-slice glass PNGs.

---

### Phase 2: Unified Crisp Icon Pipeline (Feather SVG → `@2x` PNG)
**Objective:** Replace inconsistent/mixed icons (`.png` + `.webp`) with a single, sharp, palette-matched icon set.
- **Inputs:** `developer-tools/ui_kits/feather-icons/`, `game/30_screens/theme/choice_icon_parser.rpy`, `game/images/ui/icons/`.
- **Tasks:**
  1. Map LOLA's choice tags (`[charm]`, `[logic]`, `[cash]`, `[energy]`, `[danger]`, `[target]`, `[social]`, `[quest]`) and navigation/HUD actions to Feather SVG icons.
  2. Add a Python icon-build script (`developer-tools/build_ui_icons.py`) that renders selected Feather SVGs into crisp `@2x` PNGs tinted with `ui_tokens.json` accent colors.
  3. Update `choice_icon_parser.rpy` and navigation/status screens to use the unified icon directory.
- **Exit Criteria:** Zero mixed-style or blurry icons across choice menus, navigation bars, and HUD pills.

---

### Phase 3: Real Frosted Glass (GLSL Backdrop Blur) & Transform Polish
**Objective:** Make LOLA's glassmorphism look genuinely modern instead of flat semi-transparent boxes.
- **Inputs:** `game/30_screens/theme/gui_06_glass_surfaces.rpy`, `game/30_screens/theme/gui_07_blends_transforms.rpy`, `developer-tools/ui_kits/renpy-template/`.
- **Tasks:**
  1. Register a clean Ren'Py 8 GLSL multi-pass / kawase blur shader in `gui_07_blends_transforms.rpy`.
  2. Apply backdrop blur transforms behind `glass_panel` / `glass_elevated` / `glass_card` overlays (with a toggleable low-spec fallback in Preferences).
  3. Standardize micro-animation transforms (hover lift, focus pulse, subtle entrance slide) across buttons and cards.
- **Exit Criteria:** Dialogue box, choice cards, and modal panels render smooth frosted glass over gameplay scenes at 60 FPS.

---

### Phase 4: Dev Layout Inspector & *Dispatch*-Style Diegetic QoL
**Objective:** Speed up screen iteration and add player-facing diegetic UX & accessibility.
- **Inputs:** `developer-tools/ui_kits/RenPy-LayoutTool/`, `game/30_screens/preferences.rpy`, `game/50_world_map/world_map_screen.rpy`, `game/30_screens/theme/gui_08_ui_audio.rpy`.
- **Tasks:**
  1. Drop the modular layout inspector from `RenPy-LayoutTool` into a dev-only `game/00_systems/dev/` hook (`config.developer` gated) so it never ships to players.
  2. Add player QoL/accessibility settings in `preferences.rpy` wired to tokens: `text_scale`, `dialogue_pace`, `high_contrast`, and `reduce_blur`.
  3. Upgrade `MAP_PINS` in `world_map_screen.rpy` with diegetic urgency/mood color states + `gui_08_ui_audio.rpy` pre-line audio cues.
- **Exit Criteria:** Live layout tweaking works in dev mode; players can scale text/contrast/blur cleanly; Solis Bay map pins communicate state without tutorial popups.
