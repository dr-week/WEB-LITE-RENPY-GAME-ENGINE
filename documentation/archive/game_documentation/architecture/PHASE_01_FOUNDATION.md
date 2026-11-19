# Phase 1 - Runtime Foundation and Testability

## Objective

Keep the game reliably bootable, windowed by default, and testable in Ren'Py
8.6. Ensure the main-menu screen is the actual game entry interface.

## Work items

- [x] Replace removed Ren'Py history-tag API usage with the supported tag set.
- [x] Remove old GUI helper aliases that do not exist in Ren'Py 8.6.
- [x] Remove the conflicting `main_menu` script label that bypassed the screen.
- [x] Default to windowed mode; leave fullscreen as an optional preference.
- [x] Register the quick menu as an overlay so Save/Load/Settings remain
  reachable during dialogue.
- [x] Add the missing native choice screen to render story menus consistently.
- [ ] Resolve remaining warnings in unrelated optional world/location content.
- [x] Run an automated Day 1 route through the Day 2 continuation.
- [ ] Visually verify keyboard/mouse paths in the game window.

## Test gates

- SDK lint completes without parse, screen, missing-image, or missing-label
  errors.
- Ren'Py testcases verify main menu -> settings -> return.
- Ren'Py testcases verify new game -> save/load navigation.
- Playthrough verifies each Day 1 branch reaches a defined outcome.

## Current status

Lint passes. All three Ren'Py testcases pass, including the Day 1-to-Day 2
route. A visual keyboard/mouse pass is still needed.
