"""Canonical 2-option story beat schema and validation rules."""

from dataclasses import dataclass

LOCATIONS = {
    "home": ("bg_home", "home_chill"),
    "bus_stop": ("bg_bus_stop", "daily_commute"),
    "street": ("bg_street", "city_hustle"),
    "cafe": ("bg_cafe", "cafe_work"),
    "college": ("bg_college_entrance", "college_social"),
    "library": ("bg_library", "study_focus"),
    "park": ("bg_park", "park_breeze"),
    "viewpoint": ("bg_park", "park_breeze"),
    "tower": ("bg_street", "city_hustle"),
    "slum_quarter": ("bg_street", "city_hustle"),
    "harbor_pier": ("bg_park", "park_breeze"),
}

CHARACTERS = ("maya", "elena", "marcus", "priya")
TIME_SLOTS = ("morning", "afternoon", "evening")
TONES = ("hustle", "cozy", "tense", "playful")
STATS = ("intelligence", "appeal", "communication", "confidence", "financial_literacy", "learning")


@dataclass(frozen=True)
class ChoiceOption:
    label: str
    stat: str
    delta: int
    reply_speaker: str
    reply_line: str
    relationship_char: str = ""
    relationship_delta: int = 0
    flag_name: str = ""


@dataclass(frozen=True)
class StoryBeatSpec:
    label: str
    location: str
    time_slot: str
    tone: str
    opener: str
    character: str
    hook_line: str
    maya_line: str
    option_a: ChoiceOption
    option_b: ChoiceOption
    next_label: str = "day_hub"
    sfx: str = "SFX_SWOOSH_SOFT"
