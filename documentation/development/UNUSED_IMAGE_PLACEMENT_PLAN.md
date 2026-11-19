# Put unused pictures into the story

## Why the old button could not help

The old place button was enabled only when a preview found a safe match. Most
images had no target in their metadata, so the button stayed disabled. The app
could not ask the user to choose a dialogue from the screen.

## Product rule

Make placement a picture-first task. The user should select a picture and a
story moment in the UI; the app creates IDs, metadata, aliases, and script
changes. No one should need to type JSON, Ren'Py aliases, or file paths for a
normal placement.

## Simple placement flow

1. **Pictures to sort** — thumbnail, simple filename, visual caption when
   available, and one status: `Ready to place`, `Needs a story moment`,
   `Reference only`, or `Already in story`.
2. **Choose a story moment** — search story dialogue, grouped by day, scene,
   and character. Show a short dialogue excerpt and current image.
3. **Place picture** — enabled after the user chooses a valid story moment.
   Show a final preview: picture, dialogue, and where it will appear.
4. **Save for a future scene** — planned next; if nothing fits, add the picture
   to a story ideas list. Do not silently create dialogue or edit Ren'Py files.
5. **Finish** — show placed, still needing a decision, and saved-for-later
   counts. Provide undo for the last batch.

The user chooses a story moment for one or more images, presses **Place chosen
pictures**, reviews the proposed changes, and confirms. Keep technical details
behind an expandable link.

## Implemented in the workbench

- Picture Check lists unused images by folder and offers searchable dialogue
  moments that do not already show a CG. The app writes the target metadata;
  no JSON or Ren'Py editing is needed.
- **Add chosen and matched pictures to story** is always visible. It previews
  selected routes plus safe automatic matches, then asks before changing story
  files. The dialogue picker is open by default.
- A maintained filename rule can suggest a target if it resolves to one exact
  dialogue and no CG is already there. Generic filename guesses do not place
  anything.
- The apply step creates aliases, updates sidecars, inserts scenes, and
  refreshes the list. Reference-only art is excluded.

## How the app should identify pictures and story moments

- Prefer an exact `story_key` from a matching sidecar or a Flow metadata record.
- Otherwise let the user search all unique, not-yet-illustrated story lines.
  Optional visual captions and ranked suggestions are later improvements.
- Let a person confirm or change the target. After confirmation, write the
  exact `story_file`, `story_label`, `dialogue_contains`, and `story_key` into
  the sidecar.
- Keep `asset_id` for duplicate detection and generate the Ren'Py alias inside
  the app. Filenames may stay descriptive; no special serial format is needed.
- Mark character/reference images as `Reference only`; never place those as
  story scenes.

## Placement automation

After a confirmed target, the placement script should preflight duplicates,
stale dialogue, alias collisions, image role, and existing scene art. It then
creates the alias, inserts the image at the chosen dialogue, updates the
sidecar, refreshes the image list, and records one reversible journal entry.
If any preflight check fails, change nothing and explain the issue plainly.

Batch placement shows a review screen and requires one explicit apply action.

## New story scenes

When no existing dialogue fits, write a structured idea record containing the
asset ID, image path, caption/tags, and reason no existing scene fit. An AI
writer may suggest a scene and dialogue from that record, but saves a draft for
human approval. Only approved dialogue creates a new image request and story
script change.

## Delivery phases

1. Add thumbnail previews and a clearer list of the proposed pictures and
   dialogue before confirmation.
2. Add a reversible placement journal and one-click undo.
3. Add local visual captions and searchable metadata as described in
   `../assets/VISUAL_METADATA.md`.
4. Add suggested story matches and future-scene drafts, always requiring user
   confirmation before story edits.

## Done when

- A user can place an image in a chosen scene without editing a sidecar.
- The app shows a thumbnail and the dialogue that will receive the image.
- Repeating refresh does not create duplicate requests or placements.
- Invalid targets and duplicate assets are blocked with a plain explanation.
- Unmatched images can be saved for later without being lost or auto-inserted.
