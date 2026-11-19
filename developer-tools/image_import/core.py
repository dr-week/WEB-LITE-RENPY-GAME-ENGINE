import hashlib
import json
import re
from dataclasses import dataclass

from .matching import explicit_story_target, image_category, load_metadata


EXTENSIONS = {".png", ".jpg", ".jpeg", ".webp"}
ALIAS = re.compile(r"^\s*image\s+([\w]+)\s*=")


@dataclass
class ImportPlan:
    image: object
    sidecar: object
    destination: object
    alias: str | None
    asset_id: str
    role: str
    metadata: dict
    target: tuple | None
    review: str


def asset_id(path):
    digest = hashlib.sha256()
    with path.open("rb") as source:
        for chunk in iter(lambda: source.read(1024 * 1024), b""):
            digest.update(chunk)
    return "asset_" + digest.hexdigest()[:16]


def plan_imports(root):
    game, images = root / "game", root / "game" / "images"
    if not images.is_dir():
        raise FileNotFoundError(images)
    definitions = {m.group(1) for path in game.rglob("*.rpy")
                   for line in path.read_text(encoding="utf-8-sig").splitlines()
                   if (m := ALIAS.match(line))}
    existing_ids = _registered_asset_ids(images)
    plans, aliases, targets = [], set(), set()
    candidates = sorted(p for p in images.iterdir()
                       if p.is_file() and p.suffix.lower() in EXTENSIONS)
    for image in candidates:
        metadata, sidecar = load_metadata(image)
        identifier = asset_id(image)
        if identifier in existing_ids:
            raise ValueError(f"Duplicate asset content: {image.name} matches {existing_ids[identifier]}.")
        existing_ids[identifier] = image.name
        role = str(metadata.get("role", "cg")).lower()
        if role not in {"cg", "scene", "background", "reference"}:
            raise ValueError(f"Unsupported role {role!r} in {sidecar or image}.")
        category = image_category(image, metadata)
        alias = _alias(image, role, definitions, aliases)
        destination = images / category / image.name
        if destination.exists() or destination.with_suffix(".json").exists():
            raise FileExistsError(destination)
        target = None if role == "reference" else explicit_story_target(game, metadata)
        if target and target[:2] in targets:
            raise ValueError(f"Multiple assets target {target[0]}:{target[1]}.")
        if target:
            targets.add(target[:2])
        review = "" if target or role == "reference" else "No exact sidecar target; category only."
        plans.append(ImportPlan(image, sidecar, destination, alias, identifier,
                                role, metadata, target, review))
    return game, plans


def _registered_asset_ids(images):
    found = {}
    for sidecar in images.rglob("*.json"):
        metadata = json.loads(sidecar.read_text(encoding="utf-8-sig"))
        identifier = metadata.get("asset_id") if isinstance(metadata, dict) else None
        if identifier:
            found[identifier] = sidecar.with_suffix("").relative_to(images).as_posix()
    return found


def _alias(image, role, definitions, aliases):
    if role == "reference":
        return None
    slug = re.sub(r"[^a-z0-9]+", "_", image.stem.lower()).strip("_")
    if not slug:
        raise ValueError(f"Cannot create a Ren'Py alias from {image.name}.")
    alias = f"{'bg' if role == 'background' else 'cg'}_{slug}"
    if alias in definitions or alias in aliases:
        raise ValueError(f"Duplicate Ren'Py image alias {alias!r}.")
    aliases.add(alias)
    return alias
