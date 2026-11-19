# Workbench sections

Each sidebar item opens one numbered, focused section with a single topbar title:

- **1. Dashboard (`overview`)** — KPI summary, pipeline stage counts, category bars, and one-click `Refresh All`, `Rebuild Story Catalog`, `Organize Loose Art`, `Story Bible`, and `Roadmap` actions.
- **2. Stage & Route (`intake`)** — drop/select files, bind request/category/role, run `01 Preview Plan`, `02 Apply & Place`, or `03 Organize Loose Art`.
- **3. Story Prompts (`generation`)** — structured open request cards above the raw Markdown prompt report (`Refresh Prompts`, `Copy Markdown`, `Open File`).
- **4. Audit & Place (`audit`)** — **Script & Asset Check** + **Place Unused Art in Story** dialogue picker, preview/apply, catalog rebuild, and future scene proposals.
- **5. Asset Catalog (`data`)** — compact summary counts, catalog rebuild action, and categorized inventory cards.

## Fresh scan flow

- Startup refreshes the generation list and image inventory.
- Opening **3. Story Prompts** runs a fresh story scan before displaying open request cards and the report.
- Opening **5. Asset Catalog** refreshes inventory totals and categories cleanly.
- Staging, applying, or organizing images refreshes both the inventory and request catalog.

## Code layout

- `src/actions/` contains grouped UI actions (`imports.ts`, `navigation.ts`, `project.ts`, `metadata.ts`) and the shared runner (`runner.ts`).
- `src/pages/` contains one focused module per workflow section.
- `src/ui/navigation.ts` defines the numbered sidebar navigation.
- `src-tauri/src/assets/` scans files, story aliases, and inventory counts; `pipeline.rs` executes `developer-tools/*.py`.
- `developer-tools/` separates CLI entry wrappers from `image_generation/`, `image_import/`, `image_reconciliation/`, `image_audit/`, and `image_story_loop/`.

All active TypeScript, Rust, Python, and Ren'Py modules stay at or below 100 lines each.

## Browser preview

Run `npm run dev:browser`, then open `http://127.0.0.1:1421/?preview=browser`.
The preview uses sample data and does not access or change game files. Add
`&section=generation`, `&section=audit`, or `&section=data` to preview a page directly.

## Prompt format

Requests use short `[SCENE] [BEAT] [CAST] [PLACE] [FRAME] [STYLE] [CONTINUITY]
[REFERENCES] [STARTER_EGG] [AVOID]` fields. The meme-format starter egg is
selected from the stable story key, so refreshes do not change an existing request.
