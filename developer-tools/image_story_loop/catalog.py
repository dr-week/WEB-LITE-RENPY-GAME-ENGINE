"""Catalog unused full-frame artwork for the game's repeating story route."""

import hashlib
import json
import re
from collections import defaultdict
from pathlib import Path

from image_import.core import EXTENSIONS
from image_import.matching import load_metadata
from image_reconciliation.index import registered_art
from .narrative import event_key, story_event


def _asset_files(game):
    images = game / "images"
    definitions, used = registered_art(game)
    already_used = {relative for alias, (_, relative) in definitions.items() if alias in used}
    seen_bytes, groups = set(), defaultdict(list)
    duplicates = []
    for image in sorted(images.rglob("*")):
        if not image.is_file() or image.suffix.lower() not in EXTENSIONS:
            continue
        if any(part in {"character_reference", "generated_art", "menu_assets", "ui"} for part in image.parts):
            continue
        if image.stem.lower().startswith(("grok-image", "grok_image", "image_")):
            continue
        metadata, _ = load_metadata(image)
        if str(metadata.get("role", "")).lower() == "reference":
            continue
        relative = image.relative_to(images).as_posix()
        if relative in already_used:
            continue
        fingerprint = hashlib.sha256(image.read_bytes()).hexdigest()
        if fingerprint in seen_bytes:
            duplicates.append(relative)
            continue
        seen_bytes.add(fingerprint)
        category = str(metadata.get("category") or image.parent.name).lower()
        identity = event_key(image).replace(" ", "_")
        groups[(category, identity)].append((image, metadata, relative))
    return groups, definitions, duplicates


def build_catalog(game):
    groups, definitions, duplicates = _asset_files(game)
    events = []
    for (category, identity), assets in sorted(groups.items()):
        image, metadata, _ = assets[0]
        caption = str(metadata.get("caption") or metadata.get("description") or metadata.get("alt_text") or "")
        event = story_event(image, game / "images", category, caption)
        event["id"] = hashlib.sha256(f"{category}/{identity}".encode()).hexdigest()[:16]
        event["images"] = [item[2] for item in assets]
        event["title"] = str(metadata.get("title") or " ".join(identity.replace("_", " ").split()).title())
        event["variants"] = len(assets)
        events.append(event)
    return {"schema_version": 1, "events": events, "exact_duplicates_skipped": duplicates}


def story_loop_image_paths(game):
    path = game / "data" / "image_story_catalog.json"
    if not path.is_file():
        return set()
    catalog = json.loads(path.read_text(encoding="utf-8-sig"))
    return {image.casefold() for event in catalog.get("events", [])
            for image in event.get("images", [])}


def write_catalog(game):
    catalog = build_catalog(game)
    path = game / "data" / "image_story_catalog.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(catalog, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return path, catalog
