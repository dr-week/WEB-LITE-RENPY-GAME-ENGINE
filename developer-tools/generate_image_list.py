"""Generate fresh, story-linked image requests."""

from image_generation import beats, config, references, report, story_scan
from image_generation.config import GAME, OUTPUT, REQUESTS_OUTPUT, ROOT, RULES


def _sync_project():
    for module in (config, story_scan, references, beats, report):
        module.GAME = GAME
        module.RULES = RULES


def scan():
    _sync_project()
    return story_scan.scan()


def fresh_story_beats(definitions, events, story_lines):
    _sync_project()
    return beats.fresh_story_beats(definitions, events, story_lines)


def build_list():
    _sync_project()
    return report.build_list()


def build_outputs():
    _sync_project()
    return report.build_outputs()


def curated_request(rule, occurrences, definitions):
    _sync_project()
    return references.curated_request(rule, occurrences, definitions)


def tagged_story_assets():
    _sync_project()
    return references.tagged_story_assets()


def has_cg_at_dialogue(source, line):
    _sync_project()
    return references.has_cg_at_dialogue(source, line)


if __name__ == "__main__":
    import json
    markdown, catalog = build_outputs()
    OUTPUT.write_text(markdown, encoding="utf-8")
    REQUESTS_OUTPUT.write_text(json.dumps(catalog, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Generated {OUTPUT}")
    print(f"Generated {REQUESTS_OUTPUT} ({len(catalog['requests'])} story requests)")
