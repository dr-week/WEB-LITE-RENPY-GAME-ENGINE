# Story image placement and Ren'Py lint

## Run result (2026-11-15)

- `build_image_story_catalog.py`: Built **254 story moments** from **360 images** across **11 routes** into `game/data/image_story_catalog.json` (while wiring 8 additional `cg_*` aliases directly into Days 1–5 scenes).
- `generate_image_list.py`: Generated **26 open story requests** in `developer-tools/image_requests.json` and `developer-tools/image_generation_list.md`.
- `audit_images.py`: Indexed **474 image files**, **43 file references**, and **42 scene aliases** (`image_audit.sqlite`). No missing image files or `bg_`/`cg_` aliases found.

## Ren'Py check

- Ren'Py **8.6.0.26110915** lint completed with exit code **0**, **0 errors**, and **0 warnings** (`162` dialogue blocks, `40` menus, `43` images, `19` screens).
- All 21 previously flagged non-ASCII filenames have been renamed to ASCII-only paths.
- Full output: `tests/renpy-lint.stdout.log`; `tests/renpy-lint.stderr.log` is empty.

## Next placement work

Review unplaced categorized art in **4. Audit & Place** inside LOLA Workbench, assign images to unique unillustrated story lines, and confirm preview before applying script changes.

Focused test suites: `python -m unittest discover -s developer-tools -p "test_*.py" -v` (**13 passed**); `cargo test --manifest-path development/image-workbench/src-tauri/Cargo.toml` (**7 passed**).
