"""Generates seamless, 2-option Ren'Py story beats with tone & continuity flags."""

import random
from modules.modular_story_engine.core.micro_dialogue import make_maya_line
from modules.modular_story_engine.core.story_schema import ChoiceOption, LOCATIONS, StoryBeatSpec, TONES
from modules.modular_story_engine.core.variation_pools import OPENERS, OPTION_CONTRASTS, TONE_HOOKS


def build_beat_spec(label: str, location: str = "cafe", time_slot: str = "afternoon",
                    character: str | None = None, tone: str = "hustle", seed: int | None = None) -> StoryBeatSpec:
    if location not in LOCATIONS:
        raise ValueError(f"Unknown location: {location}")
    if tone not in TONES:
        raise ValueError(f"Unknown tone: {tone}")
    rng = random.Random(seed)
    opener = rng.choice(OPENERS[location])
    hooks = TONE_HOOKS[tone]
    pool = [h for h in hooks if character is None or h[0] == character] or list(hooks)
    char, hook_line, _ = rng.choice(pool)
    maya_line = make_maya_line(tone, seed=(seed + 11 if seed is not None else None))
    a_lbl, a_stat, a_val, b_lbl, b_stat, b_val = rng.choice(OPTION_CONTRASTS)
    rel_char = char if char != "maya" else ""
    opt_a = ChoiceOption(a_lbl, a_stat, a_val, char, "Bold call. Let's go.",
                         rel_char, 4 if rel_char else 0, f"{label}_bold")
    opt_b = ChoiceOption(b_lbl, b_stat, b_val, "maya", make_maya_line(tone, seed=(seed + 23 if seed is not None else None)),
                         flag_name=f"{label}_solo")
    return StoryBeatSpec(label=label, location=location, time_slot=time_slot, tone=tone,
                         opener=opener, character=char, hook_line=hook_line, maya_line=maya_line,
                         option_a=opt_a, option_b=opt_b)


def render_rpy_beat(spec: StoryBeatSpec) -> str:
    bg, music_key = LOCATIONS[spec.location]
    lines = [
        f"# Generated modular 2-option story beat ({spec.location} / {spec.time_slot} / {spec.tone}).",
        "",
        f"label {spec.label}:",
        f'    $ travel_to("{spec.location}")',
        f'    $ go_to_time_slot("{spec.time_slot}")',
        f'    $ set_story_music("{music_key}", fadein=1.5)',
        f"    scene {bg} at bg_slow_zoom_in",
        "    with dissolve",
        f'    "{spec.opener}"',
        f'    {spec.character} "{spec.hook_line}"',
        f'    maya "{spec.maya_line}"',
        "    menu:",
    ]
    for opt in (spec.option_a, spec.option_b):
        lines.extend([
            f'        "{opt.label}":',
            f"            play sound {spec.sfx}",
            f'            $ change_stat("{opt.stat}", {opt.delta})',
        ])
        if opt.relationship_char:
            lines.append(f'            $ update_relationship("{opt.relationship_char}", "friendship", {opt.relationship_delta})')
        if opt.flag_name:
            lines.append(f'            $ set_flag("{opt.flag_name}", True)')
        lines.append(f'            {opt.reply_speaker} "{opt.reply_line}"')
    lines.extend([f"    jump {spec.next_label}", ""])
    return "\n".join(lines)
