"""Verify referenced audio/icon assets and filename ASCII hygiene."""

from pathlib import Path
import re

AUDIO_LITERAL = re.compile(r"""['"](audio/[^'"%{}]+\.(?:mp3|ogg|wav))['"]""", re.I)
ICON_LITERAL = re.compile(r"""['"](ui/icons/[^'"%{}]+\.png)['"]""", re.I)


def check_asset_hygiene(game_root: Path) -> dict:
    """Check missing audio/icon literals and non-ASCII image filenames."""
    missing_audio, missing_icons = [], []
    for rpy in sorted(game_root.rglob("*.rpy")):
        rel = rpy.relative_to(game_root).as_posix()
        for ln, line in enumerate(rpy.read_text(encoding="utf-8-sig").splitlines(), 1):
            for m in AUDIO_LITERAL.finditer(line):
                if not (game_root / m.group(1)).is_file():
                    missing_audio.append((rel, ln, m.group(1)))
            for m in ICON_LITERAL.finditer(line):
                target = m.group(1)
                if not (game_root / target).is_file() and not (game_root / "images" / target).is_file():
                    missing_icons.append((rel, ln, target))

    non_ascii = [
        p.relative_to(game_root).as_posix()
        for p in sorted((game_root / "images").rglob("*"))
        if p.is_file() and not p.name.isascii()
    ]
    return {
        "ok": not missing_audio and not missing_icons,
        "missing_audio": missing_audio,
        "missing_icons": missing_icons,
        "non_ascii_files": non_ascii,
    }
