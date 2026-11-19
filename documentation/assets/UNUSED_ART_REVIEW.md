# Unused art review and story proposals

## Current behavior

Picture Check has an always-visible **Add chosen and matched pictures to
story** button and an open dialogue picker. The button places selected images
at the chosen dialogue and adds other safe matches after preview and
confirmation. The scanner accepts a unique target from a maintained filename
rule; generic filename keywords alone never select dialogue. Applying writes
Ren'Py placement and updates sidecars. Items without a safe target stay for
review.

## Next improvements

1. Preview shows each unused image with thumbnail, visual caption (when
   available), existing alias, candidate dialogue, and why it matched.
2. Add a visible list of the chosen picture and dialogue before applying.
3. Preview regenerates `developer-tools/story_image_proposals.json` with a
   structured snapshot of images that could not be safely placed. It includes
   asset ID, path, category, any caption/target metadata, and review reason.
   Reference-only assets are excluded. The log is a planning input; it does not
   edit story code.
4. A separate story-authoring step may turn approved proposals into draft
   dialogue and fresh image requests. Human review remains required before
   story scripts change.
5. Apply should write a journal with asset ID, old/new paths, sidecar, alias, story
   file, label, dialogue anchor, and timestamp. Journal supports audit/undo.

## Matching policy

Captions, tags, generic filename words, and dialogue similarity may help rank
candidates later. They cannot independently authorize placement. Only an exact
validated target or a unique maintained rule can be applied after confirmation.
Ambiguous targets stay in review. Reference art is never inserted as a scene.

## Outcome counters

Show total assets, story-used, unused, pending review, safe proposals, and
story-proposal count. Refresh counts after preview/apply; never count a proposal
as placed until the Ren'Py script and sidecar have both been updated.
