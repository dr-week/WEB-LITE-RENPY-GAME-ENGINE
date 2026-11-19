"""Scan game scripts and asset directories for image and alias references."""

from pathlib import Path
import re

PROJECT_ROOT = Path(__file__).resolve().parents[2]
GAME_ROOT = PROJECT_ROOT / "game"
IMAGE_EXTENSIONS = {".png", ".jpg", ".jpeg", ".webp", ".gif", ".bmp", ".avif"}
IMAGE_LITERAL = re.compile(r"""(['"])([^'"]+\.(?:png|jpe?g|webp|gif|bmp|avif))\1""", re.I)
ALIAS_DEF = re.compile(r"^\s*image\s+((?:bg|cg)_[A-Za-z0-9_]+)\s*=")
ALIAS_REF = re.compile(r"^\s*(?:scene|show)\s+(?:expression\s+)?((?:bg|cg)_[A-Za-z0-9_]+)\b")


def collect_sources(game_root: Path = GAME_ROOT):
    assets = [(p.relative_to(game_root).as_posix(), p.stat().st_size)
              for p in game_root.rglob("*")
              if p.is_file() and p.suffix.lower() in IMAGE_EXTENSIONS]
    references, aliases, alias_refs = [], {}, []
    sources = sorted((*game_root.rglob("*.rpy"), *game_root.rglob("*.py")))
    for source in sources:
        relative = source.relative_to(game_root).as_posix()
        is_test = relative.startswith("tests/")
        for line_number, line in enumerate(source.read_text(encoding="utf-8-sig").splitlines(), 1):
            if definition := ALIAS_DEF.match(line):
                aliases[definition.group(1)] = (relative, line_number)
            if alias_ref := ALIAS_REF.match(line):
                alias_refs.append((relative, line_number, alias_ref.group(1)))
            if is_test:
                continue
            for match in IMAGE_LITERAL.finditer(line):
                target = match.group(2).replace("\\", "/")
                if "://" in target or "%" in target:
                    continue
                candidate = (game_root / Path(target)).resolve()
                try:
                    candidate.relative_to(game_root.resolve())
                except ValueError:
                    continue
                references.append((relative, line_number, target, int(candidate.is_file())))
    return assets, references, aliases, alias_refs
