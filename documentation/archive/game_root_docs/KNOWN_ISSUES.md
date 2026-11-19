# LOLA - Known Issues Report

**Date:** 2026-11-13
**Status:** Pre-migration audit complete

## Critical Issues

### 1. Nested `game/game/` Directory (Blocks Ren'Py Loading)

**Severity:** Critical
**Files affected:** All 35 `.rpy` files in `game/game/`

Ren'Py expects the project directory to be `game/`. The current structure has files in `game/game/`, which means Ren'Py won't discover them automatically.

**Evidence:**
```
./game/game/script.rpy
./game/game/systems/state.rpy
./game/game/story/prologue/day_01_home.rpy
...
```

**Required action:** Move contents from `game/game/` to `game/` (or verify this is intentional).

---

### 2. Duplicate `screens.rpy` (Causes Duplicate Screen Definitions)

**Severity:** Critical
**Files affected:** 
- `game/screens.rpy` (legacy, 1522 lines)
- `game/game/screens.rpy` (new implementation)

Both define `screen say`, `screen quick_menu`, `screen main_menu`, etc. Ren'Py will error on duplicate declarations.

**Required action:** Remove or rename one. The new modular screens should replace the legacy one.

---

### 3. Root-Level `.rpy` Files vs Nested (Loads Twice)

**Severity:** High
**Files affected:**
- `game/script.rpy` (root level, defines `start`, `game_start`)
- `game/game/script.rpy` (nested, also defines `start`, `game_start`)

Both define a `label start` entry point. Ren'Py will find both.

**Required action:** Delete root-level `game/script.rpy`, `game/gui.rpy`, `game/screens.rpy`, `game/options.rpy` (keep nested versions).

---

### 4. Legacy `modular/` Directory Conflicts

**Severity:** High
**Files affected:** 14 files in `game/modular/`

The `modular/` directory contains alternative implementations with duplicate labels:
- `label game_start` (in `modular/story/chapter1.rpy` and `game/game/script.rpy`)
- `label chapter_one` (in `modular/story/chapter1.rpy`)
- `label night` (in multiple files)
- Romance/love scene labels in `modular/story/love_events.rpy`

**Required action:** Decide which implementation to keep before migration.

---

### 5. Legacy `.rpyc` Files (Orphaned Compiled Scripts)

**Severity:** High
**Files affected:** 10 `.rpyc` files

```
./game/gui.rpyc
./game/modular/characters/main_character.rpyc
./game/modular/locations/cafe.rpyc
...
./game/script.rpyc
```

If matching `.rpy` files are moved/deleted, these orphaned `.rpyc` files may still execute.

**Required action:** Back up project, then clear orphaned `.rpyc` files after migration.

---

### 6. Image Declarations Use Solid Colors (Not Real Images)

**Severity:** Medium
**Files affected:**
- `game/script.rpy` - defines `bg_home`, `bg_school`, etc. as Solid colors
- `game/characters/characters.rpy` - defines character sprites as Solid colors

These are placeholders. No actual image files are referenced yet.

**Evidence:**
```
image bg_home = Solid("#8B7355", xysize=(1920, 1080))
image p neutral = Solid("#4a4a6a", xysize=(600, 900))
```

**Required action:** Replace with actual image references after visual review of `images/` folder.

---

### 7. Character Systems Not Using `default`

**Severity:** Medium
**Files affected:** `game/game/systems/state.rpy` and other system files

Ren'Py recommends `default` for mutable playthrough variables to ensure rollback works correctly. The current implementations use `init python:` blocks with `default` only in some places.

**Check needed:** Verify all playthrough state variables use `default` not just `init python:`.

---

### 8. Two Different `world_map` Screens

**Severity:** Medium
**Files affected:**
- `game/game/screens/navigation.rpy` - defines `screen world_map()`
- `game/game/world_map/world_map.rpy` - also defines `screen world_map()`

Duplicate screen definition.

**Required action:** Keep one, remove the other.

---

### 9. `game/characters/characters.rpy` Is Legacy File

**Severity:** Low
**Files affected:** `game/characters/characters.rpy` AND `game/game/characters/characters.rpy`

There's both a root-level `game/characters/characters.rpy` and a nested `game/game/characters/characters.rpy`.

**Required action:** Delete the root-level one, keep the nested implementation.

---

## Summary

| Issue | Severity | Action Required |
|-------|----------|-----------------|
| `game/game/` nesting | Critical | Move files to `game/` |
| Duplicate `screens.rpy` | Critical | Remove duplicate |
| Root-level `.rpy` files | High | Delete, keep nested |
| Legacy `modular/` conflicts | High | Decide kept implementation |
| Orphaned `.rpyc` files | High | Clear after migration |
| Solid color placeholders | Medium | Replace with real images |
| Non-`default` state vars | Medium | Audit and fix |
| Duplicate `world_map` screen | Medium | Keep one |
| Duplicate `characters.rpy` | Low | Delete root-level |

## Files Not Yet Reviewed

- `images/` - 277+ images not visually inspected
- `images/love/` - contents not inventoried
- `backgrounds/` - contents unknown
- `sprites/` - contents unknown
- `audio/` - contents unknown

## Recommended Order

1. Fix nested `game/game/` → `game/` structure
2. Remove duplicate screens and root-level `.rpy` files
3. Clear orphaned `.rpyc` files (after backup)
4. Audit system files for `default` usage
5. Inventory and review images
6. Test in Ren'Py
