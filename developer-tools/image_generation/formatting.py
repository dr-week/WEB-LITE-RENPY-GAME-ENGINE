import json
from .story_scan import story_time


def curated_section(rule, occurrences, request):
    rows = [f"### {rule['title']}", f"- **Story time:** {story_time(occurrences[0][0], rule['time'])}",
            f"- **Story target:** `{request['source']}:{request['line']}` (label `{request['label']}`)",
            f"- **Dialogue:** `{request['dialogue']}`", f"- **Reference images:** {_refs(request['references'])}",
            f"- **Generation tag:** `{request['key']}`", f"- **Starter egg:** {request['starter_egg']}",
            f"- **Suggested filename:** `{request['key']}.jpg` with same-stem `.json` sidecar",
            f"- **Sidecar metadata:** `{json.dumps(request['metadata'], ensure_ascii=False)}`"]
    rows.extend(f"  - `{text}` — `{path}:{line}` (label `{label}`; scene `{scene or 'none'}`)"
                for label, scene, line, text, path in occurrences)
    return rows + [f"- **Generate:** {request['prompt']}", ""]


def fresh_section(beat):
    return [f"### {beat['key']}", f"- **Story target:** `{beat['source']}:{beat['line']}` (label `{beat['label']}`)",
            f"- **Dialogue:** `{beat['dialogue']}`", f"- **Current location:** `{beat['scene']}` → `{beat['location']}`",
            f"- **Reference images:** {_refs(beat['references'])}", f"- **Generation tag:** `{beat['key']}`",
            f"- **Starter egg:** {beat['starter_egg']}", f"- **Suggested filename:** `{beat['key']}.jpg` with same-stem `.json` sidecar",
            f"- **Sidecar metadata:** `{json.dumps(beat['metadata'], ensure_ascii=False)}`",
            f"- **Generate:** {beat['prompt']}", ""]


def available_section(rule, occurrences, found):
    return [f"### {rule['title']}", "- **Match status:** filename/category hint only; no story placement is inferred.",
            "- **Existing files:**", *[f"  - `{path}`" for path in found], ""]


def tagged_section(item):
    key, image, source, line, label, dialogue = item
    return [f"### Request `{key}`", f"- **Exact request target:** `{source}:{line}` (label `{label}`)",
            f"- **Dialogue:** `{dialogue}`", f"- **Generated file:** `{image}`", ""]


def _refs(paths):
    return ", ".join(f"`{path}`" for path in paths) or "None"
