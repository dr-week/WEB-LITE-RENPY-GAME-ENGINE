# Phase 4 - Code Modularity and the 100-Line Rule

## Objective

Make every code file shorter than 100 lines while preserving tested behavior.
Count all lines, including blank lines and comments. Markdown documentation and
non-code assets are excluded.

## Completed refactor

- Split persistent defaults from state helpers.
- Split encounter generation from recurrence/event queries.
- Split relationship updates/descriptions from summary queries.
- Split location metadata/read queries from travel/unlock operations.
- Split character registry operations from name-pool generation.
- Split encounter categories/creation from recurring-character helpers.
- Split status and character-info screens from their style definitions.
- Split legacy character helper functions from the legacy declarations.
- Split the dialogue/choice screen from the in-game quick menu.

## Already split in the current pass

The GUI theme configuration is split into focused palette, dialogue,
menu/slot, history/control, and mobile-variant files. The main menu,
game-menu frame and styles, about screen, save/load controls and styles,
preferences controls and styles, confirmation modal, notification overlays,
and Day 1 story responsibilities are also in focused files.

## Current audit

The active `game/` source audit currently finds **zero** code files at or above
100 lines. Markdown documentation and image/audio assets are not code and are
not counted. Re-run the audit after every source change.

Refactor the external `developer-tools/` utilities separately if the same
line-count rule is intended to include tools that are not part of the game.

## Enforcement checklist

- Before adding code: identify the smallest cohesive source module.
- After editing: count lines in every touched code file.
- If a file reaches 100 lines, split before considering the task complete.
- Run Ren'Py lint after each logical split.
- Run relevant UI/story tests; compare key behavior before and after.
- Never split a story label in the middle of a menu or state transition.
- Keep each test file below 100 lines and group tests by feature.

## Completion gate

The source-size audit reports no code files at or above 100 lines, Ren'Py
lint is clean of errors, and all required focused tests pass.

The active-game source-size gate passes. Lint and the two UI testcases passed
after the system and screen splits; remaining lint output is limited to
non-ASCII asset filename packaging warnings.
