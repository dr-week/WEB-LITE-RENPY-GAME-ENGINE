# UI Assets, Glassmorphism, Shadows & Blending Architecture

Structured reference for LOLA's downloaded third-party UI assets, procedural glassmorphism surfaces, and modular Ren'Py theme helpers.

## 1. Asset Inventory & Licenses

| Category | Asset / Pack | Location | License | Source |
| --- | --- | --- | --- | --- |
| **Typography** | Plus Jakarta Sans (`Regular`, `SemiBold`, `Bold`, `Italic`) | `game/fonts/PlusJakartaSans-*.ttf` | SIL OFL 1.1 | `tokotype/PlusJakartaSans` |
| **UI Icons** | Kenney Game Icons (White 2x, 19 icons) | `game/images/ui/icons/*.png` | CC0 1.0 | `shorepine/kenney` |
| **UI Audio** | Kenney Interface Sounds (10 WAV files) | `game/audio/sfx/ui/*.wav` | CC0 1.0 | `Calinou/kenney-interface-sounds` |
| **Glass 9-Slice** | `glass_panel`, `glass_panel_elevated`, `glass_card`, `glass_pill`, `glass_btn_idle`, `glass_btn_hover` | `game/images/ui/glass/*.png` | Project (Generated) | `developer-tools/generate_ui_surfaces.py` |
| **Shadow 9-Slice** | `shadow_soft`, `shadow_deep` | `game/images/ui/shadows/*.png` | Project (Generated) | `developer-tools/generate_ui_surfaces.py` |
| **Blend Effects** | `sheen_top.png`, `vignette_ambient.png` | `game/images/ui/effects/*.png` | Project (Generated) | `developer-tools/generate_ui_surfaces.py` |

## 2. Modular Ren'Py Theme Modules (`game/30_screens/theme/`)

All modules load at `init offset = -2` so every screen and style file can reuse them without duplication.

| Module | Responsibility | Exports |
| --- | --- | --- |
| `gui_06_glass_surfaces.rpy` | 9-slice `Frame` surfaces & effect image aliases | `gui.glass_panel`, `gui.glass_elevated`, `gui.glass_card`, `gui.glass_pill`, `gui.glass_btn_idle`, `gui.glass_btn_hover`, `gui.shadow_soft`, `gui.shadow_deep`, `ui_sheen_top`, `ui_vignette_ambient` |
| `gui_07_blends_transforms.rpy` | Reusable opacity, blur, blending modes, and motion | `ui_glass_opacity(opacity)`, `ui_glass_blur(blur_px, opacity)`, `ui_blend_add_sheen(opacity)`, `ui_blend_multiply_shadow(opacity)`, `ui_vignette_overlay(opacity)`, `ui_panel_entrance(delay_s)` |
| `gui_08_ui_audio.rpy` | Global & reusable UI sound bindings | `ui_sfx_click`, `ui_sfx_hover`, `ui_sfx_select`, `ui_sfx_confirm`, `ui_sfx_back`, `ui_sfx_open`, `ui_sfx_close`, `ui_sfx_glass`, `config.button_sound`, `config.button_hover_sound` |

## 3. Reuse Guide for Screens & Styles

```renpy
# 1. Glassmorphic panel with baked shadow, translucent fill, and specular rim
style my_card:
    background gui.glass_card
    padding (24, 20)

# 2. Interactive glass button
style my_button:
    background gui.glass_btn_idle
    hover_background gui.glass_btn_hover

# 3. Blending modes & opacity in any screen
screen my_overlay():
    add "ui_vignette_ambient" at ui_vignette_overlay(0.55)   # blend "multiply"
    frame at ui_panel_entrance(0.05):                         # alpha fade + lift
        background gui.glass_elevated
```

## 4. Regenerating Procedural Surfaces

Run `python developer-tools/generate_ui_surfaces.py` to regenerate all 9-slice glass, shadow, and blend PNGs.
