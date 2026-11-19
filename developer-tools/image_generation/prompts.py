import hashlib

MEME_STARTERS = (
    "Distracted Boyfriend glance composition; generic original characters, no text",
    "This Is Fine calm-in-chaos gag; original character, no copied mascot or text",
    "Drake Hotline Bling two-choice pose; original character, no labels",
    "Surprised Pikachu reaction beat; original character, no copied face",
    "Woman-yelling-at-cat contrast gag; original cast, no text",
    "Doge-style exaggerated approval; original animal cameo, no captions",
)


def starter_egg(story_key):
    index = int.from_bytes(hashlib.sha256(story_key.encode()).digest()[:4], "big") % len(MEME_STARTERS)
    return MEME_STARTERS[index]


def structured_prompt(story_key, scene, beat, location, references):
    refs = ", ".join(references[:4]) or "tagged story references"
    egg = starter_egg(story_key)
    fields = [f"[SCENE: {scene}]", f"[BEAT: {beat}]",
              "[CAST: Maya (East Asian young woman with soft round-oval face, blonde-dipped dark hair, innocent sweet face, bold mischievous con-artist energy) and story characters]",
              f"[PLACE: {location or 'story setting'}]", "[FRAME: clear cinematic medium shot]",
              "[PHYSICS: solid ground contact under feet/seated weight, natural gravity and accurate two-leg/two-arm anatomy]",
              "[STYLE: cell-shaded illustrated cast, photoreal environment, matched light]",
              "[CONTINUITY: Maya wears her exact oversized dark navy-blue t-shirt short dress and dark slide sandals; change only when story supports it]",
              f"[REFERENCES: {refs}]", f"[STARTER_EGG: subtle background-only {egg}]",
              "[AVOID: extra legs, extra arms, extra fingers, distorted hands, floating or levitating subjects, disconnected shadows, text, logos, watermark, unrelated props]"]
    return " ".join(fields)
