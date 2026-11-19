# Creative Day Creation & Lightweight Emotional Voice System

## 1. How a Day Is Created (`story_maker.py create-day`)

Each generated day builds a cohesive **3-slot arc** (`Morning -> Afternoon -> Evening -> end_day_home`) using [day_builder.py](../../modules/modular_story_engine/generator/day_builder.py):
- **Themes:** `campus_hustle`, `cafe_leverage`, `harbor_twilight`, `library_mystery`
- **Strict 2-Option Rule:** Every beat has exactly 2 contrasting choices with `set_flag(...)` continuity hooks.
- **Emotion & Unseen Dialogue:** Each slot updates `set_emotional_state(...)` and uses `maya_thought` (italic, no namebox) for Maya's inner monologue.
- **Auto-Database Sync:** Every generated beat is automatically upserted into `data/story_engine/story_arcs.db` via `StoryDatabase`.

```bash
python developer-tools/story_maker.py create-day --day-num 8 --theme harbor_twilight --seed 5
```

---

## 2. Lightweight Emotional Cute Voice / Mumbling System

Instead of multi-GB voice files, Maya uses **procedural harmonic vowel-mumble clips** (~70 KB each) paired with Ren'Py's `Character(..., callback=maya_voice_callback)`:

| Component | Location | Role |
| --- | --- | --- |
| **Modular Voice Engine** | `modules/modular_voice_engine/` | Scans Maya lines (`voice_manifest.json`), maps 8 emotions (`en-US-AnaNeural` pitch/rate), supports `edge-tts` (neural) & Windows SAPI5 (offline) |
| **Voice CLI** | `developer-tools/voice_maker.py` | `scan`, `synth --limit N --backend auto|edge|sapi`, and `say "..."` |
| **Mumble Synthesizer** | `developer-tools/generate_maya_voice.py` | Generates 8 warm harmonic vowel-mumble `.wav` clips (`neutral`, `happy`, `proud`, `hopeful`, `teasing`, `shy`, `tired`, `worried`) |
| **Ren'Py Callback** | `game/00_systems/art/maya_voice_system.rpy` | Registers `maya_voice` channel (`mixer="voice"`), reads `emotional_state` / `get_protagonist_expression()`, plays on `begin`/`show`, stops on `slow_done`/`end` |
| **Characters** | `game/10_characters/protagonist.rpy` | Binds `maya_voice_callback` to both `maya` (spoken) and `maya_thought` (unseen inner monologue) |
