# LOLA Modular Multi-Prologue Story & Unified Database Plan

## 1. Objectives
1. **Multiple Random Prologues**: Pressing **New Game** selects a random starting prologue (avoiding immediate back-to-back repeats) using newly imported high-quality images, each with distinct starting flavor, protagonist choices, and smooth routing into the main city week.
2. **Modular Endings**: Evaluate protagonist stats, relationships, active prologue ID, and story-loop exploration into multiple distinct endings (`END_*`), keeping each route in small (<150 line) `.rpy` modules.
3. **Stable IDs Everywhere**:
   - Prologues: `PROL_APT_MORNING`, `PROL_CAFE_EARLY`, `PROL_SUBWAY_ARRIVAL`, `PROL_ROOFTOP_DAWN`, `PROL_CAMPUS_FAIR`
   - Endings: `END_THRIVING`, `END_ACADEMIC`, `END_INDEPENDENT`, `END_CONNECTOR`, `END_WANDERER`, `END_STEADY`
   - Story Nodes & Choices: Deterministic `node_id` and `choice_id` stored in SQLite.
4. **Unified Story + Image Database (`developer-tools/image_audit.sqlite`)**:
   - Links `story_nodes`, `story_choices`, `story_endings`, and `story_image_links` with `image_assets` and `image_feedback`.
   - Enables evaluating how images shape the story (unlinked high-quality art ready for new scenes) and how story needs shape image generation/replacement.
5. **Quality-Based Image Replacement (`replace_low_quality.py`)**:
   - Identifies `needs_regen` or low-quality images used in story/alias definitions and swaps them with higher-scoring, higher-resolution images in the same category while preserving stable aliases/IDs.

---

## 2. Data & Story Flow

```text
[New Game] -> init_new_game_state() -> pick_random_prologue()
   ├── PROL_APT_MORNING     (day_01_home)
   ├── PROL_CAFE_EARLY      (prologue_cafe_early)
   ├── PROL_SUBWAY_ARRIVAL  (prologue_subway_arrival)
   ├── PROL_ROOFTOP_DAWN    (prologue_rooftop_dawn)
   └── PROL_CAMPUS_FAIR     (prologue_campus_fair)
           │
           ▼  (Protagonist choices shape stats & flags)
   [Day 1–6 Story + Image Story Hub]
           │
           ▼  (Day 7 Evaluation)
   [Modular Endings: END_THRIVING | END_ACADEMIC | END_INDEPENDENT | END_CONNECTOR | END_WANDERER | END_STEADY]
```

## 3. Module Map (All Files ≤ 130 Lines)
- `game/40_story/prologue/prologue_registry.rpy` — `PROLOGUE_REGISTRY`, random non-repeating selector, and `active_prologue_id` tracking.
- `game/40_story/prologue/prologue_cafe_early.rpy` — `PROL_CAFE_EARLY` using new cafe/bakery art.
- `game/40_story/prologue/prologue_subway_arrival.rpy` — `PROL_SUBWAY_ARRIVAL` using new subway/mart art.
- `game/40_story/prologue/prologue_rooftop_dawn.rpy` — `PROL_ROOFTOP_DAWN` using new rooftop/stairwell art.
- `game/40_story/prologue/prologue_campus_fair.rpy` — `PROL_CAMPUS_FAIR` using new club-fair/lecture art.
- `game/40_story/endings/ending_routes.rpy` — Modular `END_*` evaluator and epilogue outcomes.
- `developer-tools/image_audit/schema.py` — Adds `story_nodes`, `story_choices`, `story_image_links`, `story_endings`, `v_story_image_health`, `v_unlinked_good_images`.
- `developer-tools/story_db/scanner.py` & `sync.py` — Parses `.rpy` story files + `image_story_catalog.json` into SQLite.
- `developer-tools/evaluate_story_db.py` — Evaluates story graph, choices, endings, and image health.
- `developer-tools/replace_low_quality.py` — Replaces flagged/low-quality images with better-quality replacements.
