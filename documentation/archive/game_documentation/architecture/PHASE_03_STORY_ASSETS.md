# Phase 3 - Story Structure and Image Integration

## Objective

Expand the playable story while connecting the existing artwork to scenes
where its content and tone fit.

## Work items

- [x] Define stable image aliases for selected Day 1 home, transit, campus,
  classroom, library, and cafe images.
- [x] Use a classroom-note image on the corresponding introduction choice.
- [x] Use the coffee-spill image in a cafe mishap moment.
- [x] Close the Day 1 -> Day 2 story transition with a short continuation.
- [ ] Visually review each selected illustration for crop, aspect ratio,
  content, and continuity before release.
- [ ] Inventory all remaining `game/images/` assets; assign category, likely
  chapter, intended role, and review status.
- [ ] Separate true backgrounds from full-frame CGs and character sprites.
- [ ] Write chapter briefs with scene goal, choices, state effects, and exit
  labels before expanding story content.
- [ ] Add chapters in short, focused `.rpy` files and keep branches reachable.
- [ ] Review romantic/adult-themed images for age, consent, and story context
  before using any of them.
- [ ] Add fallback art or a clear placeholder only where an image is
  intentionally unavailable; never leave broken image/audio paths.

## Acceptance criteria

- Every image used in a story label has a stable alias and exact source file.
- Each asset is visually checked; names alone are not treated as evidence.
- The Day 1 route has explicit outcomes and all next-label references exist.
- New story source files are each below 100 lines.
