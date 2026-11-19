"""Build exact-ID-only proposals for unplaced image assets."""

import re
from image_import.core import EXTENSIONS
from image_import.matching import explicit_story_target, load_metadata
from image_story_loop.catalog import story_loop_image_paths
from .index import active_scene, registered_art
from .match import filename_story_target


def plan_reconciliation(game):
    definitions, used = registered_art(game)
    proposals, unmatched, targets = [], [], set()
    known_paths, aliases = {path for _, path in definitions.values()}, set(definitions)
    in_story_loop = story_loop_image_paths(game)
    for alias, (source, relative) in definitions.items():
        if alias in used:
            continue
        image = game / "images" / relative
        if relative.casefold() in in_story_loop:
            continue
        if not image.is_file():
            unmatched.append((alias, relative, "registered image file is missing"))
            continue
        metadata, _ = load_metadata(image)
        _candidate(game, image, relative, alias, source, metadata, targets,
                   proposals, unmatched, aliases)
    for image in sorted((game / "images").rglob("*")):
        if not image.is_file() or image.suffix.lower() not in EXTENSIONS:
            continue
        relative = image.relative_to(game / "images").as_posix()
        if relative in known_paths or relative.casefold() in in_story_loop:
            continue
        metadata, _ = load_metadata(image)
        _candidate(game, image, relative, image.name, None, metadata, targets,
                   proposals, unmatched, aliases)
    return proposals, unmatched


def _candidate(game, image, relative, name, source, metadata, targets,
               proposals, unmatched, aliases):
    if image.parent.name == "character_reference" or metadata.get("role") == "reference":
        return
    explicit = True
    try:
        target = explicit_story_target(game, metadata)
        if not target:
            explicit = False
            target, suggested, reason = filename_story_target(game, image)
            if not target:
                raise ValueError(reason)
            metadata.update(suggested)
    except (ValueError, KeyError) as error:
        unmatched.append((name, relative, str(error)))
        return
    if target[:2] in targets:
        unmatched.append((name, relative, "another image is proposed for this dialogue"))
        return
    current = active_scene(game, target)
    if current and current.startswith("cg_") and metadata.get("replace_existing") is not True:
        unmatched.append((name, relative, f"story already shows {current} at target"))
        return
    alias = metadata.get("alias") if source else _new_alias(image, metadata, aliases, unmatched, relative)
    if not alias:
        return
    targets.add(target[:2])
    title = f"{metadata['story_label']}: {metadata['dialogue_contains']}"
    if not explicit:
        title += f" (matched by {metadata['match_rule']})"
    proposals.append((alias, relative, title, target, current, source, metadata.copy()))


def _new_alias(image, metadata, aliases, unmatched, relative):
    role = str(metadata.get("role", "cg")).lower()
    if role not in {"cg", "scene", "background"}:
        unmatched.append((image.name, relative, f"unsupported scene role: {role}"))
        return None
    prefix = "bg" if role == "background" else "cg"
    slug = re.sub(r"[^a-z0-9]+", "_", image.stem.lower()).strip("_")
    alias = f"{prefix}_{slug}"
    if not slug or alias in aliases:
        unmatched.append((image.name, relative, f"Ren'Py alias collision: {alias}"))
        return None
    aliases.add(alias)
    return alias
