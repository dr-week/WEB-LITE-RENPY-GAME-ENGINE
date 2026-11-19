# Workbench sections and ownership

Each of the five numbered sections has one clear title, one goal, and reads the same shared project inventory without duplicating KPI strips.

| Section | Goal | Reads | Writes |
| --- | --- | --- | --- |
| 1. Dashboard (`overview`) | Inspect pipeline counts, unillustrated line totals, category bars, and run quick actions (`Refresh All`, `Rebuild Story Catalog`, `Organize Loose Art`, `Story Bible`, `Roadmap`) | Project status, inventory, request catalog | Only when triggering `Rebuild Story Catalog` or `Organize Loose Art` |
| 2. Stage & Route (`intake`) | Stage files, bind request ID/category/role, preview plan, apply imports, or organize loose art | Root files, request catalog, sidecars | Sidecars, category folders, aliases, explicit story insertions |
| 3. Story Prompts (`generation`) | Review structured open request cards and refresh/copy/open the Markdown prompt report | Story scripts and registered assets | Markdown request report (`image_generation_list.md` / `image_requests.json`) |
| 4. Audit & Place (`audit`) | Run script/asset validation in Panel 1 and bind/place unused art into unillustrated dialogue in Panel 2 | Scripts, images, sidecars, story targets | Only reviewed reconciliation placements or catalog rebuilds |
| 5. Asset Catalog (`data`) | Inspect compact totals, rebuild the journal catalog, and browse assets by category | Shared image inventory and sidecars | Only when triggering `Rebuild Story Catalog` |

## Single sources of truth

- `game/40_story/**/*.rpy` is the source for dialogue and request targets.
- Same-stem JSON sidecars carry image role, category, request and asset IDs,
  placement status, and target provenance.
- Ren'Py `image` definitions map aliases to file paths; story `scene` / `show`
  statements prove actual use.
- `developer-tools/image_generation_list.md` is human-readable output and
  `image_requests.json` is its generated UI catalog; neither is hand-edited.
- Workbench counts come from `src-tauri/src/assets/`; pages format those
  values rather than rescanning files independently.

No sprites or character pose layers are part of the asset model. `reference`
images are continuity inputs and are never registered as scene images.
