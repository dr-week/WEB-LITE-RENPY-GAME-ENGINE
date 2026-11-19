# LOLA Image Workbench

A native Windows desktop window for running the game's existing image workflow
without an AI agent or a browser tab. It uses Zuari's DOM, signals, glyphs,
and Studio theme from `C:\CODES\webframework\fast`.
Keep that Zuari checkout in place when rebuilding; the compiled app bundles
the theme and UI code, so launching an existing release does not need it.

## Launch

Double-click `launcher\tools\Launch Image Workbench.bat` to open the native
development window with automatic updates. Keep its console open while using
the app. Vite refreshes frontend edits in the window, and Tauri watches Rust
sources and rebuilds/restarts the native window when they change. Node.js and
Rust must be installed.

For a browser-only review with safe sample data, run `npm run dev:browser` from
this folder and open `http://127.0.0.1:1421/?preview=browser`.

Use `launcher\tools\Build Image Workbench Release.bat` when you want a standalone
release executable instead of the auto-updating development window.

## Image workflow

1. **1. Dashboard** shows unified totals, unillustrated line counts, category distribution, and quick triggers (`Refresh All`, `Rebuild Story Catalog`, `Organize Loose Art`, `Story Bible`, `Roadmap`).
2. **2. Stage & Route** lets you drop or select images into `game\images`, assign request/category/role sidecars, run **01 Preview Plan** (read-only validation), **02 Apply & Place** (creates category folders, aliases, and scene insertions), or **03 Organize Loose Art**.
3. **3. Story Prompts** displays structured open request cards alongside the copyable Markdown prompt report regenerated from `developer-tools\generate_image_list.py`.
4. **4. Audit & Place** runs **Check Script References** (`audit_images.py` -> SQLite inventory) and provides **Place Unused Art in Story** to bind categorized images directly to unillustrated dialogue lines.
5. **5. Asset Catalog** lists every category card with per-file usage status, asset IDs, request keys, and story targets.

To preview or apply reconciliations from CLI, run `python developer-tools/reconcile_story_images.py` (add `--apply` after reviewing). Guide: `developer-tools/IMAGE_IMPORT.md`.

## Native build

From this directory, run `npm run tauri:build` to create
`src-tauri\target\release\lola_image_workbench.exe`. Run `npm run tauri:dev`
for local development.
