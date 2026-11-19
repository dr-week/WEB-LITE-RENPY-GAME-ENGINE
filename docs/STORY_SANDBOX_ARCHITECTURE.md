# LOLA Modular Sandbox Story & Non-Repeating Image Architecture

## 1. Random-Start Prologue (`game/data/story_starts.json` + `prologue_starts.rpy`)
Every `New Game` jumps to `prologue_random_start`, which selects an **unseen** Day 1 opening scenario from `game/data/story_starts.json`:
- `kitchen_overslept`: Apartment morning (`$120`, Energy `70`, `home`)
- `rooftop_sunrise`: Fire-escape sunrise (`$135`, Energy `75`, `home`)
- `cafe_early_shift`: Pre-class Daily Grind shift (`$145`, Energy `65`, `cafe`)
- `bus_stop_drizzle`: Rainy downtown bus shelter (`$115`, Energy `68`, `bus_stop`)
- `campus_quad_early`: Early arrival on campus quad (`$125`, Energy `80`, `college`)

## 2. Non-Repeating Image & Start Database (`game/00_systems/art/story_seen_db.rpy`)
- `persistent.seen_prologue_starts` ensures consecutive playthroughs start in different situations until all starts are seen.
- `persistent.seen_story_images` + `pick_unseen_entry(...)` tracks displayed scenes so sandbox routes never repeat an image prematurely.
- `game/data/image_feedback.json` + `persistent.image_feedback` logs Good / Fix ratings for developer-tools review.

## 3. Interchangeable Scene Aliases (`game/10_characters/prologue_scenes.rpy`)
Story labels reference semantic aliases (`scene_day1_home`, `scene_day1_bus_stop`, `scene_day1_campus_gate`, etc.). Replacing old art with newly generated Google Flow images only requires updating the path in `prologue_scenes.rpy` or running:
```powershell
python developer-tools/ingest_flow_download.py --latest 5
```
