# LOLA Image Asset and Story Map

## Integration policy

Image filenames describe a likely subject, but not every asset belongs in the
current prologue. Keep a source-to-alias mapping here, then place assets only
where location, characters, and tone match. Many images depict later-life
activities (parties, travel, hobbies, relationships) and should be reserved
for matching chapters rather than inserted into Day 1.

## Day 1: opening route

| Ren'Py alias | Source image | Planned story use |
|---|---|---|
| `bg_home` | `Girl_standing_at_home_b25ae9df.jpg` | Maya checks the time and her finances before leaving home |
| `bg_bus_stop` | `Girl_waiting_for_bus_37a9f56c.jpg` | Waiting for transit on the first college morning |
| `bg_college_entrance` | `Girl_standing_at_bus_stand_4d65aae2.jpg` | Temporary transit/campus-arrival illustration until a clear entrance image is selected |
| `bg_classroom` | `Girl_standing_in_classroom_7ffb471a.jpg` | First arrival in the classroom |
| `cg_class_notes` | `Girl_passing_notes_in_classroom_483dbd01.jpg` | Optional classroom moment; use only if the matching choice/event is authored |
| `bg_library` | `Girl_sorting_library_books_c230afae.jpg` | Library visit |
| `bg_cafe` | `Girl_sipping_espresso_at_cafe_8dea6314.jpg` | First cafe visit and job inquiry |
| `cg_cafe_spill` | `Girl_spilling_coffee_at_cafe_e8bec485.jpg` | Optional awkward cafe event; not forced into the current route |

These are alias candidates, not a claim that every image is compositionally
correct for a final background. Review crop, resolution, and continuity in the
game before release. In particular, the bus-stand image is only a provisional
match for the college-arrival background.

## Filename-based groups for the remaining image audit

The image directory contains many more assets than the opening chapter needs.
Use these filename terms as search categories during the next visual review:

- **Transit:** `bus`, `train`, `subway`, `airport`, `ferry`
- **College and work:** `classroom`, `assignment`, `computer_lab`, `workshop`,
  `convenience_store`, `bakery`
- **Food and cafes:** `cafe`, `coffee`, `diner`, `ramen`, `market`, `restaurant`
- **Friends and social events:** `house_party`, `rave`, `nightclub`, `wedding`
- **Hobbies and locations:** `museum`, `arcade`, `garden`, `beach`, `vineyard`,
  `skating`, `gym`, `rooftop`
- **Relationship scenes:** `couple`, `boyfriend`, `holding_hands`, `alley`
- **Unclear/generated:** `grok-image`, malformed `__LOCATION__` prefixes, or
  names that end mid-word

Do not use the relationship or adult-themed assets in the opening chapter
without confirming the characters, ages, and narrative context. Do not rename
or delete source files as part of the mapping pass.

All full-frame scene and CG aliases use `fit_scene_art` from
`00_systems/artwork_display.rpy`. It sizes artwork to the configured viewport,
preserves its aspect ratio with Ren'Py's `contain` fit, and fills unused space
with a dark matte. Portrait, landscape, and other source dimensions therefore
fit without stretching or cropping.

## Image folder organization

The 338 story images are grouped under `game/images` by filename hints:
`college`, `transport`, `food_drink`, `shops_markets`, `social_events`,
`relationships`, `home_lodging`, `hobbies_outdoors`, `public_places`,
`character_reference`, `generated_art`, and `general_scenes`. Filenames are
preserved; folder assignment is organizational, not visual-content review.
Preview future root-level additions with `python developer-tools/organize_images.py`;
add `--apply` to move them and update Ren'Py source paths.

## Automated image audit

Run `developer-tools/run_image_audit.ps1` to inventory image files and scan
Ren'Py/Python sources for missing literal image paths and undeclared `bg_`/`cg_`
scene aliases. The script regenerates `developer-tools/image_audit.sqlite`;
query its `missing_images` and `missing_aliases` views to review problems.
The audit uses only Python's standard library and does not rename or modify
artwork.

For dialogue-driven image needs, run `python developer-tools/generate_image_list.py`.
To import new art, add a per-image metadata sidecar and preview/apply
`developer-tools/integrate_story_images.py`; see `developer-tools/IMAGE_IMPORT.md`.

## Next asset-audit deliverable

For each remaining image, record: exact filename, visual category, likely
chapter/location, intended role (background, full-frame illustration, CG, or
sprite), and review status. Inspect image content before assigning story
meaning; filenames alone cannot establish what an image depicts.
