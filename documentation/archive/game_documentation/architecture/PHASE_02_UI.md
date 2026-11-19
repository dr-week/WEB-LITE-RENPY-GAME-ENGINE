# Phase 2 - UI Completion and Polish

## Objective

Make the main menu, game menus, settings, save/load, history, and dialogue
controls consistent and usable without changing Ren'Py's native behavior.

## Work items

- [x] Split menu, game-menu frame, preferences, save/load, history,
  confirmation, and notification screens by function.
- [x] Add main-menu actions for new game, load, settings, about, and quit.
- [x] Add a native choice screen with themed, readable choice buttons.
- [x] Add padded dialogue captions and styled speaker/title banners.
- [x] Use Ren'Py preferences for display, skip, transitions, text speed,
  auto-forward, and audio levels.
- [x] Provide save/load pages and a quick menu for in-game access.
- [ ] Visually inspect layout at 1920x1080 and a smaller window size.
- [ ] Review focus, hover, keyboard navigation, font sizes, contrast, and
  long translated strings.
- [ ] Replace temporary solid-color menu panels with intentional GUI artwork
  after visual review of available GUI assets.
- [ ] Confirm save/load deletion, empty slots, pages, autosave, and quicksave.
- [ ] Add focused automated UI tests for remaining states, without brittle
  hard-coded timing.

## Styling references

- [Ren'Py screen language](https://www.renpy.org/doc/html/screens.html#screen-language)
  documents the `say` screen and frame containers.
- [Ren'Py padding style property](https://www.renpy.org/doc/html/style_properties.html#style-property-padding)
  documents frame/window insets.
- The [official Ren'Py tutorial screens](https://github.com/renpy/renpy/blob/master/tutorial/game/screens.rpy)
  use padded frames for speaker nameboxes and GUI panels.

## Acceptance criteria

- User can start, continue/load, change settings, save, return, and quit.
- Default launch remains windowed; fullscreen is opt-in.
- No custom screen replaces built-in persistence or preference actions.
- All changed UI source files are below 100 lines.
