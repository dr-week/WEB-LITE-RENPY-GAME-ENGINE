# LOLA Modular Rebuild Plan

## Goal

Restore a reliable Ren'Py game flow, make the user interface and story easy to
extend, and integrate artwork where it supports the narrative. Runtime UI and
story remain native Ren'Py; external web frameworks are not required.

## Project conventions

| Area | Location | Responsibility |
|---|---|---|
| Engine configuration and theme | `game/options.rpy`, `game/gui.rpy`, `game/gui/` | Ren'Py defaults, resolution, typography, theme assets |
| Reusable state and mechanics | `game/00_systems/` | Defaulted playthrough state and small, focused systems |
| Cast and visual declarations | `game/10_characters/` | Character data and named image aliases |
| Reusable screens | `game/30_screens/` | One screen concern per file: menus, preferences, save/load, history |
| Story chapters | `game/40_story/` | Chapter-sized Ren'Py labels and scenes |
| Location navigation | `game/50_world_map/` | Location metadata and travel flow |
| Story assets | `game/images/`, `game/audio/` | Source assets; declarations map narrative names to source files |

Keep files small and named by responsibility. Ren'Py loads `.rpy` files
throughout `game/`; labels and screen names must remain unique. Use `default`
for mutable playthrough state, `define` for constants, `jump` for one-way story
progression, and `call`/`return` for reusable scenes.

## Implementation sequence

1. **Runtime foundation (done):** fixed Ren'Py 8.6 history-tag/helper API
   compatibility and verified the project with SDK lint.
2. **UI baseline (implemented):** split the dialogue/quick menu, main menu,
   preferences, save/load, history, and overlays into focused files. The
   screens use Ren'Py special-screen names and built-in actions.
3. **Opening vertical slice (implemented):** mapped selected home, transit,
   campus, classroom, library, and cafe images; repaired missing Day 1 labels
   and added a short Day 2 continuation.
4. **UI smoke tests (added):** `game/tests/ui_testcases.rpy` checks menu to
   settings navigation and new-game/save/load navigation through Ren'Py's
   test runner.
5. **Asset audit:** inventory every file under `game/images/`, group by
   filename subject, then visually review each group before assigning it to
   story scenes. A filename is a clue, not proof of narrative fit.
6. **Story expansion:** develop one chapter at a time; each chapter should
   include a clear scene goal, choices with consequences, asset references,
   and a defined exit/next-chapter label.
7. **Polish and release checks:** replace placeholder UI artwork, check text
   readability and input navigation, then lint and play-test new game,
   preferences, save/load, rollback, and chapter transitions.

## UI design rules

- Use Ren'Py Screen Language for menus, settings, save/load, history, and
  overlays. Do not embed a web app or introduce a web-framework runtime.
- Keep shared menu framing and navigation reusable; keep preferences and file
  slots in separate screen modules.
- Prefer built-in `Preference`, `FileAction`, `FilePage`, `ShowMenu`, `Start`,
  and `Quit` actions so the engine owns persistence and settings behavior.
- Preserve keyboard navigation and readable contrast in addition to mouse
  interaction. Avoid side effects in screen bodies because screens can be
  evaluated repeatedly.
- Keep custom styling in `gui.rpy` and use the standard `gui/` assets where
  available.

## Asset-to-story workflow

1. Preserve original filenames and record a semantic subject and likely story
   use in `ASSET_STORY_MAP.md`.
2. Add a stable Ren'Py alias in `10_characters/scene_art.rpy`; story labels
   refer to aliases such as `bg_home`, not long source filenames.
3. Use a scene image only when its subject/location matches the scene. The
   current pass wires selected home, transit, campus, classroom, library, and
   cafe images into Day 1.
4. Keep visually different poses as separate assets; do not imply that a
   generated image is a transparent character sprite if it is a full-frame
   illustration.
5. Track missing assets explicitly and never reference an undeclared image or
   nonexistent audio file in a playable route.

## Validation gates

- **Compile/lint:** no parse, screen, or missing-label errors.
- **Startup:** new game opens the prologue; main-menu options are reachable.
- **UI:** preferences respond; save/load pages and history open and return.
- **Story:** every Day 1 branch reaches a valid ending/next-day label.
- **Persistence:** save, load, rollback, and a fresh game preserve expected
  state.
- **Presentation:** all referenced images load and text is legible at the
  project's target resolution.

Lint is a static check, not a substitute for playing through the route.

## Current validation

- Ren'Py 8.6.0 lint passes with no script, screen, missing-image, or
  missing-label errors.
- All three Ren'Py testcases pass, including menu/settings, save/load, and
  Day 1 through Day 2.
- Lint still warns about image filenames containing non-ASCII characters;
  those assets may not package reliably in ZIP distributions.
- The game process stayed open during a brief SDK launch smoke check. Visual
  review is still needed before calling the vertical slice release-ready.
