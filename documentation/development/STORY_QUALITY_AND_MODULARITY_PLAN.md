# LOLA Story Quality, Variation & Modularity Plan

Structured plan to eliminate runtime story mistakes, enforce the 2-option narrative rule, and scale seamless story variations across LOLA.

---

## 1. Root Causes Identified

| Problem | Concrete Example Found | Fix / Guardrail |
| --- | --- | --- |
| **Rule Drift (Menu Options != 2)** | 8 legacy menus in `day_free_morning.rpy`, `image_story_hub.rpy`, `day_01_work_search.rpy`, `day_02_home.rpy`, `day_end.rpy` | `two_option_validator.py` |
| **Runtime-Only Symbol Errors** | `play sound SFX_SWOOSH` (`NameError`) & `"ui/icons/..."` missing `images/` prefix | `verify_game_assets.py` |
| **Uneven Narration & Pacing** | Ad-hoc hand-written beats without shared sensory/character templates | `modules/modular_story_engine/` |
| **Fragmented Quality Checks** | Separate lint, asset, and story checks not run together | Unified `story_maker.py` gate + `Lint LOLA.bat` |

---

## 2. Phased Execution Plan

### Phase 1 — Unified Story Quality Gate
- Combine all static checks into one command (`verify_game_assets.py` + `story_integrity.py` + `two_option_validator.py` + `<= 100`-line check).
- Run automatically inside `launcher/tools/Lint LOLA.bat` before `renpy.py ... lint` so broken symbols, dead labels, or 3-option menus fail fast before launch.

### Phase 2 — Clean Up Legacy 2-Option Violations
- Refactor the 8 flagged menus in `game/40_story/` to strictly 2 contrasting choices (keeping `day_hub.rpy`, `prologue_starts.rpy`, and `week_01_eval.rpy` in the system-menu allowlist):
  - `day_01_work_search.rpy` (lines 13, 40, 66)
  - `day_02_home.rpy` (lines 15, 28)
  - `day_free_morning.rpy` (line 12)
  - `image_story_hub.rpy` (line 34)
  - `day_end.rpy` (line 10)
- Preserve all public label names and save-state fields (`TARGET_STRUCTURE.md` safe-move rules).

### Phase 3 — Modular Story Variations & Continuity
- Expand `modules/modular_story_engine/core/variation_pools.py` with:
  - **Tone presets:** `hustle`, `cozy`, `tense`, `playful`
  - **Time-of-day sensory hooks:** `morning`, `afternoon`, `evening`, `night`
  - **New Solis Bay districts:** `viewpoint`, `tower`, `slum_quarter`, `harbor_pier`
- Add **continuity hooks** (`set_flag` / `has_flag` + `story_db` SQLite beat sync) so choices in one chapter naturally callback in later chapters.

### Phase 4 — Story-to-Image Flow Integration
- Connect `story_maker.py generate` with `modules/modular_flow_engine/` so any newly generated beat can optionally emit a structured `image_requests.json` entry for Google Flow artwork generation.

---

## 3. Definition of Done (Every Story PR / Edit)
1. `python developer-tools/checks/verify_game_assets.py` exits `0`.
2. `python developer-tools/story_maker.py validate --json` reports `0` violations.
3. `launcher/tools/Lint LOLA.bat` exits `0` with zero missing targets or tracebacks.
4. All `.rpy` and `.py` files stay `<= 100` lines.
