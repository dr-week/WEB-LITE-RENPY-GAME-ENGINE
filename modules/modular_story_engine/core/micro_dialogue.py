"""Combinatorial 2-to-5-word Gen-Z micro-dialogue generator for Maya."""

import random

MICRO_OPENERS = {
    "hustle": ("Lowkey,", "Say less.", "Bet.", "Okay—", "Clock in."),
    "cozy": ("Mmm,", "Ooh,", "Wait—", "Honestly?", "Nice."),
    "tense": ("Shh.", "Hold up.", "Easy.", "Stay cool.", "Wait."),
    "playful": ("Heh.", "Oops—", "Watch.", "Bet.", "Haha,"),
}

MICRO_CORES = {
    "hustle": ("lock in.", "move fast.", "stack cash.", "zero L's.", "we're up."),
    "cozy": ("so good.", "warm vibe.", "needed this.", "big chill.", "pure peace."),
    "tense": ("act chill.", "eyes up.", "no panic.", "play dumb.", "keep moving."),
    "playful": ("too easy.", "my bad.", "watch this.", "got 'em.", "so fun."),
}

THOUGHT_CORES = {
    "hustle": ("Focus up.", "Stay sharp.", "Eyes ahead.", "Clean play."),
    "cozy": ("Breathe out.", "Love this.", "So calm.", "Warm tea."),
    "tense": ("Don't blink.", "Read them.", "Stay calm.", "Quiet steps."),
    "playful": ("Too smooth.", "Main character.", "Watch me.", "Easy win."),
}


def make_maya_line(tone: str = "hustle", seed: int | None = None, thought: bool = False) -> str:
    rng = random.Random(seed)
    t = tone if tone in MICRO_OPENERS else "hustle"
    if thought:
        return rng.choice(THOUGHT_CORES[t])
    return f"{rng.choice(MICRO_OPENERS[t])} {rng.choice(MICRO_CORES[t])}"
