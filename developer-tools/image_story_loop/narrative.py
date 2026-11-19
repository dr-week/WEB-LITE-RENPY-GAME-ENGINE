"""Turn descriptive filenames into readable, replaceable story beats."""

import re
from pathlib import Path

from .grammar import noun_phrase, past_verb, place_phrase
from .phrases import DEFAULT_REFLECTIONS, INTRO, REFLECTIONS

HASH = re.compile(r"_[0-9a-f]{6,}(?:_2k)?$", re.I)
WORD = re.compile(r"[a-z0-9]+")
ACTORS = {"girl", "woman", "maya", "innocent", "adult"}
PREPOSITIONS = {"at", "in", "on", "near", "by", "from", "through", "along", "out", "for"}
def event_key(image: Path) -> str:
    stem = HASH.sub("", image.stem)
    stem = re.sub(r"\s+\(\d+\)$", "", stem)
    stem = stem.replace("caf�", "cafe").replace("�", "")
    return " ".join(WORD.findall(stem.casefold()))


def _words(image: Path) -> list[str]:
    stem = HASH.sub("", image.stem)
    stem = re.sub(r"\s+\(\d+\)$", "", stem).replace("caf�", "cafe").replace("�", " ")
    tokens = WORD.findall(stem.casefold())
    while tokens and tokens[0] in ACTORS | {"location"}:
        tokens.pop(0)
    return tokens


def _reflection(image: Path, category: str) -> str:
    options = REFLECTIONS.get(category, DEFAULT_REFLECTIONS)
    selector = int(event_key(image).encode().hex()[-4:], 16) % len(options)
    return options[selector]


def _narration(tokens: list[str], category: str, image: Path) -> str:
    if not tokens or tokens[0] in {"location", "grok", "image"}:
        return f"Maya found an uncaptioned moment in {category.replace('_', ' ')}. She left room in her journal to decide what it meant."
    if tokens[0] == "professor":
        return "The professor led the lecture at college. Maya wrote down one question to ask after class."
    if tokens[0] in {"classmate", "friend"}:
        place = place_phrase(tokens[tokens.index("at") + 1:]) if "at" in tokens else "nearby"
        return f"A classmate waved from {place}. Maya answered with a smile and made room for a new friendship."
    if "asking" in tokens and "directions" in tokens:
        return "When the streets stopped making sense, Maya asked for directions. The answer helped her feel less like a stranger."
    if "interacting" in tokens and "with" in tokens:
        return "Maya shared a quiet exchange with someone she did not yet know. The conversation left the city feeling less anonymous."
    if "smoking" in tokens or "stealing" in tokens:
        return "Maya faced a tempting shortcut. She thought about the trouble it could bring and chose to step back."
    if tokens[0] == "couple" or tokens[:2] == ["and", "boy"]:
        return "Maya shared a close moment with someone she was getting to know. It felt good to be wanted, and she still kept her own boundaries in view."
    split = next((i for i, word in enumerate(tokens) if word in PREPOSITIONS), len(tokens))
    action = tokens[:split]
    prep = tokens[split] if split < len(tokens) else ""
    remainder = tokens[split + 1:] if split < len(tokens) else []
    if not remainder and tokens[-2:] == ["ice", "rink"]:
        action, prep, remainder = tokens[:-2], "at", ["ice", "rink"]
    if "surprised" in tokens:
        place = place_phrase(remainder) or "the city"
        return f"Something unexpected happened at {place}. Maya took a breath and chose curiosity over panic."
    if not action:
        return "Maya paused and took in the scene. She was learning to notice the small moments that made a place feel real."
    verb, objects = action[0], action[1:]
    if verb == "posing":
        phrase = "paused for a photo"
    elif verb == "interacting":
        phrase = "shared a few words"
    elif verb == "waiting" and prep == "for":
        phrase = "waited for " + noun_phrase(remainder)
        prep, remainder = ("at", ["bus", "stop"]) if "bus" in remainder else ("", [])
    else:
        phrase = " ".join([past_verb(verb), noun_phrase(objects)]).strip()
    location = place_phrase(remainder)
    prep = "out of" if prep == "out" else prep
    setting = f" {prep} {location}" if location else ""
    return f"Maya {phrase}{setting}. {_reflection(image, category)}"


def story_event(image: Path, image_root: Path, category: str, caption: str = "") -> dict:
    tokens = _words(image)
    clean_cap = caption.strip()
    if clean_cap:
        narration = clean_cap if clean_cap.startswith("Maya") else f"Maya paused at the scene. {clean_cap.rstrip('.')} stayed with her."
    else:
        narration = _narration(tokens, category, image)
    return {"id": event_key(image), "category": category,
            "image": image.relative_to(image_root).as_posix(),
            "narration": narration, "intro": INTRO.get(category, INTRO["general_scenes"])}
