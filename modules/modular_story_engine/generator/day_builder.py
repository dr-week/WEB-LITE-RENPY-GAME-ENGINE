"""Creative 3-slot Day Arc generator with automatic SQLite narrative DB syncing."""

import random
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[3]
DEV_TOOLS = ROOT / "developer-tools"
if str(DEV_TOOLS) not in sys.path:
    sys.path.insert(0, str(DEV_TOOLS))

from modules.modular_story_engine.core.micro_dialogue import make_maya_line  # noqa: E402
from modules.modular_story_engine.core.story_schema import LOCATIONS  # noqa: E402
from modules.modular_story_engine.generator.beat_generator import build_beat_spec, render_rpy_beat  # noqa: E402
from story_db.narrative_db import StoryDatabase  # noqa: E402

DAY_THEMES = {
    "campus_hustle": (("home", "cozy", "hopeful", 3), ("college", "playful", "teasing", 5), ("cafe", "hustle", "tired", 6)),
    "cafe_leverage": (("bus_stop", "hustle", "neutral", 4), ("cafe", "tense", "worried", 7), ("street", "playful", "proud", 5)),
    "harbor_twilight": (("park", "cozy", "hopeful", 3), ("tower", "playful", "happy", 5), ("harbor_pier", "tense", "shy", 7)),
    "library_mystery": (("home", "cozy", "tired", 3), ("library", "tense", "worried", 6), ("viewpoint", "hustle", "proud", 8)),
}


def build_day_arc(day_num: int, theme: str = "campus_hustle", seed: int | None = None,
                  sync_db: bool = True, db_path: str | None = None) -> dict:
    if theme not in DAY_THEMES:
        raise ValueError(f"Unknown day theme: {theme}")
    slots = ("morning", "afternoon", "evening")
    beats = []
    chunks = [f"# LOLA - Day {day_num} ({theme.replace('_', ' ').title()})", ""]
    db = StoryDatabase(db_path or str(ROOT / "data" / "story_engine" / "story_arcs.db")) if sync_db else None

    for idx, (slot, (loc, tone, emo, tension)) in enumerate(zip(slots, DAY_THEMES[theme])):
        lbl = f"day_{day_num:02d}_{slot}_{loc}"
        nxt = f"day_{day_num:02d}_{slots[idx + 1]}_{DAY_THEMES[theme][idx + 1][0]}" if idx < 2 else "end_day_home"
        spec = build_beat_spec(lbl, location=loc, time_slot=slot, tone=tone, seed=(seed + idx if seed is not None else None))
        spec = type(spec)(**{**spec.__dict__, "next_label": nxt})
        thought = make_maya_line(tone, seed=(seed + idx if seed is not None else None), thought=True)
        rpy = render_rpy_beat(spec).replace("    menu:\n", f'    $ set_emotional_state("{emo}")\n    maya_thought "{thought}"\n    menu:\n', 1)
        chunks.append(rpy)
        beats.append({"label": lbl, "slot": slot, "location": loc, "tone": tone, "emotion": emo, "next": nxt})
        if db:
            db.upsert_beat(lbl.upper(), "Week_2", f"Day_{day_num:02d}", tension, f"{tone}/{loc}",
                           spec.hook_line, f"Choose {spec.option_a.stat} vs {spec.option_b.stat}", LOCATIONS[loc][1])
    if db:
        db.close()
    return {"ok": True, "day": day_num, "theme": theme, "beats": beats, "db_synced": sync_db, "rpy": "\n".join(chunks)}
