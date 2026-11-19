# LOLA Modular Story Maker Architecture (Two-Option Standard)

Structured story generation and validation system in `modules/modular_story_engine/`, paired with `developer-tools/story_maker.py`.

## 1. Standard Story Beat Structure

Every story beat follows one seamless, predictable 5-part flow:
1. **Context & Atmosphere:** `$ travel_to(...)`, `$ go_to_time_slot(...)`, `$ set_story_music(...)`, `scene ... at bg_slow_zoom_in with dissolve`.
2. **Sensory Opener:** Grounded Solis Bay narration line matching the location.
3. **Character Hook:** Short, natural banter between `maya` and `elena` / `marcus` / `priya`.
4. **Strict Two-Option Menu:** `menu:` with **exactly 2 contrasting choices** (Social/Bold vs. Focus/Solo), each playing a verified `audio_registry.rpy` SFX (`SFX_SWOOSH_SOFT`), updating stats/relationships, and delivering a tailored reply.
5. **Clean Exit:** `jump day_hub` (or target next label).

## 2. Module Layout (`<= 100` lines per file)

| Module | Responsibility |
| --- | --- |
| `modules/modular_story_engine/core/story_schema.py` | `StoryBeatSpec`, `ChoiceOption`, canonical `LOCATIONS`, `CHARACTERS`, `STATS` |
| `modules/modular_story_engine/core/variation_pools.py` | Location sensory openers, character hooks, and 2-option contrast pairs |
| `modules/modular_story_engine/generator/beat_generator.py` | Procedural `.rpy` beat builder (`build_beat_spec`, `render_rpy_beat`) |
| `modules/modular_story_engine/checks/two_option_validator.py` | Enforces strictly 2 options per `menu:` across `game/40_story/` |
| `developer-tools/story_maker.py` | CLI for `generate` and `validate` |

## 3. CLI Usage (from `developer-tools/`)

```bash
# Generate a varied 2-option beat preview (tones: hustle, cozy, tense, playful)
python story_maker.py generate --label day_08_pier_beat --location harbor_pier --time-slot evening --tone tense --seed 42

# Validate the 2-option menu rule across game/40_story/
python story_maker.py validate --json
```
