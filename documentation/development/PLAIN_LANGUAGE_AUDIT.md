# 4. Audit & Place in plain language

## Section structure

**4. Audit & Place** separates script verification from unused-art placement cleanly in two panels:

1. **Script & Asset Check**
   - **Check Script References:** verifies that every story background and CG alias points to an existing file in `game/images/`.
   - **Plain-language result:** summarizes verified counts, City Journal catalog rebuilds, or broken asset links.
   - **Scan Details:** keeps script paths and technical details collapsed until needed.
2. **Place Unused Art in Story**
   - **Choose pictures and dialogue locations:** select unplaced category images and bind them to unillustrated story lines without editing JSON.
   - **Preview Matches / Add Chosen & Matched Pictures:** previews safe matches and asks confirmation before modifying `.rpy` scripts.
   - **Rebuild Story Catalog / Future Scene Proposals:** regenerates `game/data/image_story_catalog.json` or opens `developer-tools/story_image_proposals.json`.

The scan does not infer visual scene contents from pixels. Captions and image thumbnails remain planned under `assets/VISUAL_METADATA.md`.
