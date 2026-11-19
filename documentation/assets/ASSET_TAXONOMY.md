# Image and audio taxonomy

## Runtime image roles

- **Background (`bg_`)** — still location art: home, transit, campus, library, cafe, public places.
- **Story CG (`cg_`)** — optional full-frame illustrated moment tied to a dialogue beat.
- **Reference-only** — character/location continuity inputs for image generation; never shown as a character sprite.

Character sprites are not part of this game. Remove the sprite role from future
asset instructions and do not build sprite display helpers or pose systems.

## Organization rules

- Keep source filenames and sidecar metadata; use stable semantic Ren'Py aliases in scripts.
- Group backgrounds and CGs by location/story category. Keep reference-only files separate.
- Each generated image request records its story label, dialogue, reference paths, stable key, and status.
- Add a request only when the dialogue requires a visual not already satisfied by a placed CG.
- Review image content before placement; filename keywords are suggestions, not narrative proof.

## Current categories

Continue the existing categories: home/lodging, transport, college, work/food,
public places, hobbies/outdoors, social events, character references, and general
scenes. Consolidate naming only after the existing asset map and aliases are audited.
