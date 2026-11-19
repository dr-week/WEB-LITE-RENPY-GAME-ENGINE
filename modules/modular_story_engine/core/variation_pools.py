"""Short, natural Gen-Z story openers, character banter, and 2-option contrasts."""

OPENERS = {
    "home": ("Morning light hit Maya's desk. New day, clean slate.",),
    "bus_stop": ("The express bus hissed to a stop at the corner.",),
    "street": ("Midtown buzzed with bikes, neon signs, and quick deals.",),
    "cafe": ("Espresso steam curled through The Daily Grind's low lo-fi.",),
    "college": ("Students spilled across the campus quad between bells.",),
    "library": ("Rain tapped the glass rotunda over quiet oak tables.",),
    "park": ("Bay breeze drifted through the park's winding garden paths.",),
    "viewpoint": ("All of Solis Bay sparkled below Pinecrest Ridge.",),
    "tower": ("The Observation Tower's clock chimed over the plaza.",),
    "slum_quarter": ("Rain slicked the brick alleys by the old rail siding.",),
    "harbor_pier": ("Salt spray and ferry lights drifted across the bay piers.",),
}

TONE_HOOKS = {
    "hustle": (
        ("marcus", "Early again? You're angling for extra hours, aren't you?", "Lowkey, yeah. Gotta stack cash."),
        ("maya", "Okay, two plays here. No overthinking.", "Say less. Let's move."),
    ),
    "cozy": (
        ("elena", "Grabbed us warm cups before the rush.", "Wait—you're literally the best."),
        ("priya", "Saved you the corner seat. Breathe for a sec.", "Ugh, needed this so bad."),
    ),
    "tense": (
        ("marcus", "Keep it quiet. Someone's checking yesterday's ledger.", "Wait, seriously? I'm on it."),
        ("elena", "Heads up—act natural and don't look back.", "Cool, cool. Zero panic."),
    ),
    "playful": (
        ("elena", "Oh no, I know that grin. What's the scheme?", "Heh... just watch me work."),
        ("priya", "Bet you five bucks you can't pull this off.", "Make it ten. Watch."),
    ),
}

THOUGHTS = {
    "hustle": ("Focus up, Maya. Eyes on the bag.", "No fumbling this—keep it clean."),
    "cozy": ("Okay, tiny breather... feels nice.", "Lowkey loving this vibe."),
    "tense": ("Stay chill. Heartbeat down.", "Don't blink—read the room."),
    "playful": ("Heh, this is kinda fun ngl.", "Okay, main-character energy."),
}

OPTION_CONTRASTS = (
    ("Play it smooth and win the room", "communication", 3, "Keep quiet and read the details", "intelligence", 3),
    ("Take the bold social angle", "appeal", 3, "Protect your cash and play it smart", "financial_literacy", 3),
    ("Step up and own the spotlight", "confidence", 4, "Hang back and pocket the edge", "learning", 3),
)
