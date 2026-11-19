# Story image reconciliation

## Purpose

Find unused registered aliases and organized files with no alias, then suggest
a story placement using the shared image rules.

## Steps

1. Preview: `python developer-tools/reconcile_story_images.py`
2. Check each proposed label, dialogue line, and current scene.
3. Apply reviewed placements: `python developer-tools/reconcile_story_images.py --apply`

## Matching and safety

- Sidecar matches must resolve to one exact dialogue. Filename suggestions use
  only maintained rules and must also resolve to one exact dialogue.
- The workbench can save a chosen generation-list story moment into an image
  sidecar so the user does not edit JSON by hand.
- Existing `scene` and `show` uses, screen references, and other script uses
  count as already used.
- Existing CGs at the proposed dialogue and competing candidates are sent to
  manual review.
- For an organized file without an alias, apply creates the Ren'Py alias and
  inserts its story statements. It does not move files.
- Ren'Py `scene` clears the current layer, so proposals are for full-frame art.

## When a match is missing

Add or refine a filename rule in `story_image_rules.json`, or choose a current
generation-list request in the workbench. Setting
`replace_existing` to `true` explicitly permits replacing a CG at the selected
dialogue. Preview again before applying.
