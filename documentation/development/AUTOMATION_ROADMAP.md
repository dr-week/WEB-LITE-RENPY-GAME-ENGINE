# Development automation roadmap

## Automated now

- Refresh request list from current story and assets (local Python; no LLM call).
- Refresh the report from the Generation List page with one explicit action.
- Copy selected generated images and sidecars into intake without overwriting.
- Assign request ID, category, and role in Intake; the UI writes a validated
  sidecar so routine routing does not require hand-editing JSON.
- Preview category, content ID, request ID, alias, and exact story target.
- Refuse stale IDs, ambiguous dialogue, duplicate story targets, duplicate
  imported content, and alias/path collisions.
- Apply reviewed imports; regenerate inventory and request list afterward.
- Preview unplaced files and place exact sidecar targets or unique curated
  filename-rule matches after confirmation.
- Save a fresh story-proposal snapshot for images with no safe match.
- Search unillustrated story dialogue and place pictures without editing sidecars.
- Rebuild Maya's City Journal story catalog (`build_image_story_catalog.py`) and sort loose root artwork (`organize_images.py --apply`) directly from the Workbench.
- Open core documentation (`Story Bible`, `Roadmap`, `Import guide`) directly from the Workbench.

## Next operator controls

1. Add image thumbnails and a clear before/after preview for each selected
   picture and dialogue.
2. Add Undo for the last import using a journal of source path, destination,
   sidecar, alias file, and story edit. Do not infer undo from current names.
3. Add inventory filters and a one-click open action for each reference and
   story target.
4. *(Completed — legacy `developer-tools/pixel-anime-converter/` was removed after timestamp verification; active tools live in modular `developer-tools/` subpackages.)*
5. Add a future-scene draft workflow over `story_image_proposals.json`; never
   write new dialogue without approval.
6. Add visual captions and searchable tags using the local catalog plan in
   `documentation/assets/VISUAL_METADATA.md`.
7. Preserve Google Flow metadata exports and map their media IDs to workbench
   requests; Flow's requested rename is best-effort, not an export-name rule.

## Later automation

- Watch story files for changes and mark cached request reports stale; refresh
  locally when requested or on app focus.
- Allow editing filename-to-category hints in the UI, with preview and tests.
- Add batch import with an all-items preflight and rollback journal.
- Add a story settings form for simple non-code game choices only after a
  versioned config schema and save migration are designed.

## Guardrails

Apply is always previewed. Generic filename keywords never choose a dialogue;
only a maintained rule with one exact story match can suggest a placement.
Scripts do not overwrite files or place reference art. No live image-generation
API is required for scanning, sorting, copying, auditing, or story integration.
