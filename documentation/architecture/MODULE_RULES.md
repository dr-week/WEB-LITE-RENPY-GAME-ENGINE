# Module rules

- Keep active source files at 100 lines or fewer. Split by responsibility and
  keep CLI wrappers thin.
- Every workflow action has one implementation and one owning module.
- Share scanners and typed inventory data; UI pages must not reimplement asset
  discovery or count logic.
- Keep stable IDs separate: request identity, file-content identity, and
  Ren'Py alias each solve a different lookup problem.
- Keep file movement and story editing behind a dry-run plan and explicit
  Apply action. The plan records why a route was selected.
- Treat filename matching as a category hint only. Story routing requires an
  exact request ID and a unique dialogue anchor.
- Keep reference art out of Ren'Py scene aliases. No character sprites.
- Keep concise operator docs beside their department; archive historical docs
  instead of leaving competing instructions in runtime folders.

## Owners

- `developer-tools/image_generation/`: scan dialogue and produce request identities/prompts (`generate_image_list.py` CLI wrapper).
- `developer-tools/image_import/`: validate sidecars, asset/request identities, and exact dialogue matching (`integrate_story_images.py` CLI wrapper).
- `developer-tools/image_reconciliation/`: audit, index, match, and place unplaced assets (`reconcile_story_images.py` CLI wrapper).
- `developer-tools/image_audit/`: scan image references and build `image_audit.sqlite` (`audit_images.py` CLI wrapper).
- `developer-tools/image_story_loop/`: group categorized images into Maya's City Journal story moments (`build_image_story_catalog.py` CLI wrapper).
- `developer-tools/tests/`: unit tests covering request generation, routing, reconciliation, and story loop catalog generation.
- `development/image-workbench/src-tauri/src/assets/`: authoritative image usage inventory for the Tauri desktop app.
- Workbench TypeScript modules (`development/image-workbench/src/`): present shared inventory data and invoke owner actions without duplicate scanning rules.
