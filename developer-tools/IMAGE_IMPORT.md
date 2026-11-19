# Story image import

The generation list starts each prompt with Maya's consistent oversized,
mid-thigh dark slate-blue T-shirt dress, then the hybrid art style: 2D
anime-influenced, cell-shaded characters composited over photorealistic
environments. Occasion-specific layers (such as a cafe apron or photographer's
vest) may change; keep the base dress color and silhouette consistent. Every
prompt repeats these instructions so it can be copied independently.

## Import workflow

1. Copy new images into the top level of `game/images`.
2. A story placement requires exact `story_file`, `story_label`, and
   `dialogue_contains` fields plus the matching request ID (`story_key`). Start
   from `image_metadata.template.json`; copy the metadata printed beside that
   request in the generation list. The importer recalculates and validates the
   ID against those target fields before it edits a story script. If the ID is
   blank, it is derived from those exact fields; a supplied stale ID is rejected.
3. `category` controls the destination folder. Intake filename rules suggest a
   category only. **4. Audit & Place** in the Workbench can suggest a story moment from a maintained
   rule, or lets the user choose an unillustrated story dialogue. Set `role` to `cg`, `background`, or
   `reference`; references are filed under `character_reference` and never
   receive a Ren'Py scene alias.
4. `story_file` is relative to `game/`. The importer resolves the exact quoted
   dialogue inside the specified label and refuses ambiguous or stale targets.
5. Preview with `python developer-tools/integrate_story_images.py`. Apply only
   after confirming the proposed story location:
   `python developer-tools/integrate_story_images.py --apply`.

The importer assigns a content-based `asset_id`, moves the image and sidecar,
creates a Ren'Py alias using the shared aspect-fit transform, and inserts
`scene` plus `with dissolve` before the exact matched dialogue. Images without
a verified request target are categorized and marked `needs_review`; they are
never silently placed based on filename keywords. Duplicate targets and alias
collisions stop preview before changes are applied.
Existing files and aliases are never overwritten. Generated `.rpy` files are
split to stay below 100 lines.

## Keep generation needs growing with the story

Refresh the generation list after adding or editing story dialogue. It includes
curated gaps and scans story dialogue for new action or emotion beats that do
not already have a CG at that line. Adjacent cues in the same label and scene
are grouped into one request. Each request includes its story file, label,
dialogue anchor, stable `story_key`, and character/location reference files.

Save generated art using the suggested `story_<key>` filename and keep the
provided JSON sidecar beside it. `story_key` identifies a story request;
`asset_id` identifies the generated file content; the Ren'Py alias connects
that file to script code. These IDs have separate jobs. The request remains
visible as existing art to review until the dialogue is placed. After placement,
the `scene cg_...` use marks that beat as illustrated, so a fresh scan removes
it from the generation needs. New story beats create new request IDs.

## Find registered art that is still unused

After organizing assets, run `python developer-tools/reconcile_story_images.py`
to find both unreferenced aliases and categorized images that have no Ren'Py
alias yet. The scan includes screen references such as `add "bg_menu"`.

The preview proposes a route only when an image sidecar has a valid request ID
and exact target fields. It skips a target that already shows a CG and flags
ambiguous or competing art for manual review. Check each `PLACE` and `REVIEW`
line. Applying adds an alias for unregistered art and places the scene in the
story; it does not move image files. Apply reviewed placements with
`python developer-tools/reconcile_story_images.py --apply`.

For any image, its same-stem JSON sidecar may set
`story_file`, `story_label`, and `dialogue_contains` to choose a precise target.
Set `replace_existing` to `true` only when you intend to replace a CG already
shown at that dialogue; the normal preview protects existing CG placements.

`scene` clears the current Ren'Py layer, so use this step only for full-frame
scene art. Use explicit sidecar metadata with the importer when a new image
needs a different or more precise dialogue anchor.
