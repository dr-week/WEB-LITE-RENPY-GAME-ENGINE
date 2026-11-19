# Target code structure

Keep Ren'Py's numbered load areas. Ren'Py discovers `.rpy` files recursively;
these folders organize responsibilities, they are not Python import packages.

```text
LOLA/
  game/
    script.rpy, options.rpy, gui.rpy, screens.rpy  # stable engine entry files
    00_systems/
      core/       # state.rpy, state_init.rpy (defaults & new-game reset), state_helpers.rpy
      time/       # calendar, time slots, single start_new_day() transition
      player/     # bounded skills, intelligence, appeal, wellbeing, mood
      economy/    # wallet, ledger, expenses, offline BTC portfolio
      work/       # job catalog, shifts, payroll
      education/  # classes, assignments, library study
      social/     # relationships, encounters, recurring cast registry, events
      world/      # locations, travel, unlocks
      art/        # full-frame fit_scene_art() helper & image_story_loop loader
    10_characters/  # protagonist, recurring cast, scene_art & generated_art aliases
    20_locations/   # home, transit, college, cafe, public locations (3 choices each)
    30_screens/     # navigation, status, character_info, menus, styles, theme/gui_0*.rpy
    40_story/
      prologue/     # Day 1 opening route, Day 2 home, end_day transition
      chapters/     # day_router, 3-pillar day_hub, Days 2-6 chapters, day_free_morning
      endings/      # week_01_eval.rpy (Day 7 Week-1 evaluation)
      image_loop/   # Maya's City Journal interactive moment loop
    50_world_map/   # location selection & navigation screen
    data/           # image_story_catalog.json & asset_manifest.json
    images/         # categorized backgrounds, full-frame CGs, character references
    audio/          # music and sound
  developer-tools/
    generate_image_list.py, integrate_story_images.py, audit_images.py,
    reconcile_story_images.py, build_image_story_catalog.py, organize_images.py  # CLI entry points
    image_generation/, image_import/, image_reconciliation/, image_audit/, image_story_loop/, tests/
  development/
    image-workbench/  # Tauri + TypeScript Image Workbench desktop GUI
  launcher/
    Play LOLA.bat, Play LOLA Direct.bat, game_launcher.pyw, game_launcher_core.py  # Player-only, single-instance game launcher
    tools/            # Separate developer launchers (Image Workbench, Release build, Ren'Py Lint)
  documentation/      # Design, systems, architecture, assets, development, audits, archive
  tests/              # Captured Ren'Py lint logs and UI test cases
```

## Current modular layout

- `00_systems/core/state_init.rpy` owns `init_new_game_state()` and canonical recurring cast setup (`elena`, `marcus`, `priya`).
- Every active source file across `game/`, `developer-tools/`, and `development/` (`.rpy`, `.py`, `.pyw`, `.ts`, `.rs`) stays at 100 lines or fewer.
- `developer-tools/` keeps thin root CLI scripts for Workbench execution while implementation lives in focused subpackages.
- `development/` holds the `image-workbench` source, while `launcher/` holds all unified game & tool launchers, keeping `game/` strictly runtime-only.

## Safe-move rules

- Preserve public label names, screen names, image aliases, and save fields.
- Keep one owner for each mutable field; other systems call its public functions.
- Use `default` for saved playthrough state and `define` for constants.
- Never edit `.rpyc` files. When deliberately moving source, move its cache pair,
  then run lint to regenerate and verify the compiled script.
- Never move save or persistent data. Move one responsibility at a time, then
  lint, inspect labels/aliases, and test old saves.
- Keep each code file below 100 lines. Split at function or data boundaries, not inside a story choice.
