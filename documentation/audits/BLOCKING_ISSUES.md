# LOLA Blocking Issues Log

**Last Updated:** 2026-11-15  
**Phase:** Story & Workbench Consolidation Complete

---

## Blocking Issues Resolved

### Issue #1: college_manager.rpy Syntax Error
- **File:** `game/00_systems/college_manager.rpy`
- **Error:** `default` statements inside `init python:` block
- **Fix:** Moved all `default` statements to script level before `init python:`
- **Status:** ✅ RESOLVED

### Issue #2: navigation.rpy Invalid Child
- **File:** `game/30_screens/navigation.rpy`
- **Error:** `text` statement as direct child of `imagebutton`
- **Fix:** Wrapped `imagebutton` and `text` in `fixed:` container
- **Status:** ✅ RESOLVED

### Issue #3: employment_manager.rpy Syntax Error
- **File:** `game/00_systems/employment_manager.rpy`
- **Error:** `default` statements inside `init python:` block
- **Fix:** Moved all `default` statements to script level
- **Status:** ✅ RESOLVED

### Issue #4: state.rpy Syntax Error
- **File:** `game/00_systems/state.rpy`
- **Error:** Multiple `default` statements inside `init python:` block
- **Fix:** Restructured file with `define` first, then `default` statements, then `init python:`
- **Status:** ✅ RESOLVED

### Issue #5: protagonist.rpy Syntax Error
- **File:** `game/10_characters/protagonist.rpy`
- **Error:** `default player_name` inside `init python:` block
- **Fix:** Moved to separate `init python:` block after `define p`
- **Status:** ✅ RESOLVED

### Issue #6: world_map.rpy Missing Screen Declaration
- **File:** `game/50_world_map/world_map.rpy`
- **Error:** Screen content without `screen world_map():` header
- **Fix:** Added proper screen declaration
- **Status:** ✅ RESOLVED

### Issue #7: world_map.rpy Imagebutton Error
- **File:** `game/50_world_map/world_map.rpy`
- **Error:** `text` inside `imagebutton`
- **Fix:** Wrapped in `fixed:` container
- **Status:** ✅ RESOLVED

### Issue #8: characters_legacy_backup.rpy Runtime Error
- **File:** `game/10_characters/characters_legacy_backup.rpy`
- **Error:** `renpy.show(..., at center, ...)` invalid syntax
- **Fix:** Changed to `renpy.show(..., at_list=[center], layer="bg")`
- **Status:** ✅ RESOLVED

### Issue #9: script.rpy Config Syntax Error
- **File:** `game/script.rpy`
- **Error:** `define config.archives manage = True` invalid syntax
- **Fix:** Changed to `define config.archives = [manage]`
- **Status:** ✅ RESOLVED

### Issue #10: screens.rpy Include Statements
- **File:** `game/screens.rpy`
- **Error:** `include` statements not in valid context
- **Fix:** Removed include statements (screens are loaded separately)
- **Status:** ✅ RESOLVED

### Issue #11: Duplicate Defaults Across Files
- **Files:** Multiple
- **Error:** Same `default` variable defined in multiple files
- **Fix:** Consolidated all defaults into `state.rpy`, removed from other files
- **Status:** ✅ RESOLVED

### Issue #12: Nested game/game/ Directory
- **File:** `game/game/`
- **Error:** Duplicate directory causing old versions to load
- **Fix:** Removed nested directory
- **Status:** ✅ RESOLVED

### Issue #13: Developer Tools in Runtime
- **Files:** `game/developer-tools/`, `game/pixel-anime-converter/`
- **Error:** Developer tools being linted as runtime code
- **Fix:** Moved `developer-tools/` to project root, removed `pixel-anime-converter/` from game/
- **Status:** ✅ RESOLVED

---

## Current Status: NO BLOCKING ISSUES (0 Errors, 0 Warnings)

Additional fixes landed on 2026-11-15:
- Renamed 21 non-ASCII image filenames to ASCII-only paths (resolved `renpy/lint.py` `OSError` and ZIP distribution warnings).
- Unified cafe routes (`location_cafe` -> `location_work`), fixed `$ coworker_break` call syntax, renamed colliding `label work_shift:` to `cafe_shift_scene`, and replaced fixed `grid 3 2` in `navigation.rpy` with `vpgrid`.
- Replaced Day 2 infinite morning loop with `day_router.rpy`, 3-pillar `day_hub.rpy`, Days 2–6 chapters, Day 7 `week_01_evaluation`, and `day_free_morning.rpy`.
- Standardized every story and location menu to 2–3 meaningful choices updating `intelligence`, `appeal`, skills, `money`, wellbeing, or relationships.
- Lint (`Ren'Py 8.6.0.26110915`) passes with **exit code 0, zero errors, and zero warnings**.
