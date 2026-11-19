from .config import GAME, RULES, SCENE, VISUAL_CUE
from .identity import story_request_id
from .prompts import starter_egg, structured_prompt
from .references import character_references, curated_request, has_cg_at_dialogue, tagged_story_assets


def fresh_story_beats(definitions, events, story_lines):
    targets = set()
    for rule in RULES:
        if events[rule["title"]]:
            request = curated_request(rule, events[rule["title"]], definitions)
            targets.add((request["source"], request["line"]))
    references, drafts, existing = character_references(), [], []
    tagged, source_lines = tagged_story_assets(), {}
    for index, item in enumerate(story_lines):
        label, scene, background, line, dialogue, source = item
        if ((source, line) in targets or has_cg_at_dialogue(source, line)
                or len(dialogue.strip()) < 18 or not VISUAL_CUE.search(dialogue)):
            continue
        if not background or background not in definitions:
            continue
        if source not in source_lines:
            source_lines[source] = (GAME / source).read_text(encoding="utf-8-sig").splitlines()
        before = source_lines[source][max(0, line - 4):line - 1]
        if any((match := SCENE.match(row)) and match.group(1).startswith("cg_") for row in before):
            continue
        location = GAME / definitions[background]
        if not location.is_file():
            continue
        nearby = [row for row in story_lines[max(0, index - 3):index + 4]
                  if row[0] == label and row[5] == source and row[3] != line]
        before_text = next((row[4] for row in reversed(nearby) if row[3] < line), "")
        after_text = next((row[4] for row in nearby if row[3] > line), "")
        drafts.append({"source": source, "label": label, "line": line, "dialogue": dialogue,
                       "scene": background, "location": definitions[background],
                       "category": location.parent.name, "references": references + [definitions[background]],
                       "context_before": before_text, "context_after": after_text})
    return _finalize(drafts, existing, tagged)


def _finalize(drafts, existing, tagged):
    grouped = []
    for beat in drafts:
        previous = grouped[-1] if grouped else None
        same = (previous and previous["source"] == beat["source"] and previous["label"] == beat["label"]
                and previous["scene"] == beat["scene"] and beat["line"] - previous["line"] <= 3)
        if same:
            grouped[-1] = beat
        else:
            grouped.append(beat)
    fresh = []
    for beat in grouped:
        story_key = story_request_id(beat["source"], beat["label"], beat["dialogue"])
        if story_key in tagged:
            existing.append((story_key, tagged[story_key], beat["source"], beat["line"], beat["label"], beat["dialogue"]))
            continue
        egg = starter_egg(story_key)
        metadata = {"category": beat["category"], "role": "cg", "story_file": beat["source"],
                    "story_label": beat["label"], "dialogue_contains": beat["dialogue"],
                    "story_key": story_key, "reference_images": beat["references"], "starter_egg": egg}
        context = " ".join(text for text in (beat["context_before"], beat["dialogue"], beat["context_after"]) if text)
        beat.update({"key": story_key, "metadata": metadata, "starter_egg": egg,
                     "prompt": structured_prompt(story_key, context, beat["dialogue"], beat["location"], beat["references"])})
        fresh.append(beat)
    return fresh, existing
