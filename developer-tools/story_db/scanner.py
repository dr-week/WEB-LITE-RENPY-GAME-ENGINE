"""Parse Ren'Py story scripts, prologues, endings, and image links with stable IDs."""

import hashlib
import json
import re
from pathlib import Path

LABEL_RE = re.compile(r"^\s*label\s+([\w]+)\s*:")
SCENE_RE = re.compile(r"^\s*(?:scene|show)\s+(?:expression\s+)?([A-Za-z0-9_]+)")
CHOICE_RE = re.compile(r'^\s{8}"([^"]+)"\s*:')
STAT_RE = re.compile(r'change_stat\("(\w+)"')
JUMP_RE = re.compile(r"^\s*jump\s+([\w]+)")
ALIAS_DEF_RE = re.compile(r'^\s*image\s+([\w]+)\s*=.*?["\'](images/[^"\']+)["\']')
END_ID_RE = re.compile(r'"id":\s*"(END_[\w]+)"')
END_TITLE_RE = re.compile(r'"title":\s*"([^"]+)"')


def _stable_id(prefix: str, *parts: str) -> str:
    digest = hashlib.sha1("|".join(parts).encode("utf-8")).hexdigest()[:10]
    return f"{prefix}_{digest}"


def _alias_map(game: Path) -> dict[str, str]:
    aliases = {}
    for rpy in sorted((game / "10_characters").glob("*.rpy")):
        for line in rpy.read_text(encoding="utf-8-sig").splitlines():
            if m := ALIAS_DEF_RE.match(line):
                aliases[m.group(1)] = m.group(2)
    return aliases


def collect_story_graph(game: Path) -> dict:
    aliases = _alias_map(game)
    nodes, choices, links, endings = [], [], [], []
    _scan_prologues(game, aliases, nodes, links)
    _scan_story_scripts(game, aliases, nodes, choices, links)
    _scan_endings(game, endings)
    _scan_story_loop(game, nodes, links)
    return {"nodes": nodes, "choices": choices, "links": links, "endings": endings}


def _scan_prologues(game: Path, aliases: dict, nodes: list, links: list) -> None:
    starts_file = game / "data" / "story_starts.json"
    if not starts_file.is_file():
        return
    data = json.loads(starts_file.read_text(encoding="utf-8-sig"))
    for item in data.get("starts", []):
        nid = item["id"]
        nodes.append((nid, "prologue", "prologue_random_start", "data/story_starts.json", nid, item.get("location", "")))
        scene = item.get("scene", "")
        if scene in aliases:
            links.append((nid, aliases[scene], scene, "prologue"))


def _scan_story_scripts(game: Path, aliases: dict, nodes: list, choices: list, links: list) -> None:
    story_dir = game / "40_story"
    for rpy in sorted(story_dir.rglob("*.rpy")):
        rel = rpy.relative_to(game).as_posix()
        ntype = "prologue" if "/prologue/" in rel else ("ending" if "/endings/" in rel else "chapter")
        current_node, current_choice = None, None
        for line in rpy.read_text(encoding="utf-8-sig").splitlines():
            if m := LABEL_RE.match(line):
                lbl = m.group(1)
                current_node = f"NODE_{lbl.upper()}"
                nodes.append((current_node, ntype, lbl, rel, lbl.replace("_", " ").title(), rpy.parent.name))
                current_choice = None
            elif current_node and (m := SCENE_RE.match(line)):
                alias = m.group(1)
                if alias in aliases:
                    links.append((current_node, aliases[alias], alias, "scene"))
            elif current_node and (m := CHOICE_RE.match(line)):
                text = m.group(1)
                cid = _stable_id("CHOICE", current_node, text)
                current_choice = [cid, current_node, text, [], ""]
                choices.append(current_choice)
            elif current_choice and (m := STAT_RE.search(line)):
                current_choice[3].append(m.group(1))
            elif current_choice and (m := JUMP_RE.match(line)):
                current_choice[4] = m.group(1)
                current_choice = None


def _scan_endings(game: Path, endings: list) -> None:
    routes = game / "40_story" / "endings" / "ending_routes.rpy"
    if not routes.is_file():
        return
    text = routes.read_text(encoding="utf-8-sig")
    ids = END_ID_RE.findall(text)
    titles = END_TITLE_RE.findall(text)
    for idx, eid in enumerate(ids):
        title = titles[idx] if idx < len(titles) else eid
        endings.append((eid, "week_01_evaluation", "40_story/endings/ending_routes.rpy", title))


def _scan_story_loop(game: Path, nodes: list, links: list) -> None:
    cat_file = game / "data" / "image_story_catalog.json"
    if not cat_file.is_file():
        return
    catalog = json.loads(cat_file.read_text(encoding="utf-8-sig"))
    for event in catalog.get("events", []):
        nid = f"LOOP_{event['id']}"
        nodes.append((nid, "story_loop", "image_story_play", "data/image_story_catalog.json",
                      event.get("title", ""), event.get("category", "")))
        for img in event.get("images", []):
            path = img if img.startswith("images/") else f"images/{img}"
            links.append((nid, path, "", "story_loop"))
