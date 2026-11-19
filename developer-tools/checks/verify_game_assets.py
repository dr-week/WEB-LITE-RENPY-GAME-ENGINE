"""Pre-flight static verifier for Ren'Py audio symbols, asset paths, and missing files."""

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
GAME = ROOT / "game"

PLAY_SYM_RE = re.compile(r"^\s*(?:play|queue)\s+(?:sound|music|audio|ambience)\s+([A-Z][A-Z0-9_]+)\b")
DEF_SYM_RE = re.compile(r"^\s*(?:define\s+)?([A-Z][A-Z0-9_]+)\s*=")
ASSET_PATH_RE = re.compile(r'"((?:audio|images|fonts)/[^"]+\.(?:png|jpg|jpeg|webp|wav|mp3|ogg|ttf|otf))"')


def verify_game() -> list[str]:
    rpy_files = sorted(GAME.rglob("*.rpy"))
    defined_syms: set[str] = set()
    errors: list[str] = []

    for path in rpy_files:
        for line in path.read_text(encoding="utf-8", errors="ignore").splitlines():
            m = DEF_SYM_RE.match(line)
            if m:
                defined_syms.add(m.group(1))

    for path in rpy_files:
        rel = path.relative_to(ROOT).as_posix()
        for idx, line in enumerate(path.read_text(encoding="utf-8", errors="ignore").splitlines(), 1):
            m_sym = PLAY_SYM_RE.match(line)
            if m_sym and m_sym.group(1) not in defined_syms:
                errors.append(f"UNDEFINED AUDIO SYMBOL: {rel}:{idx} -> {m_sym.group(1)}")
            for asset in ASSET_PATH_RE.findall(line):
                if "{" in asset or "%" in asset:
                    continue
                if not (GAME / asset).is_file():
                    errors.append(f"MISSING ASSET FILE: {rel}:{idx} -> {asset}")
    return errors


def main() -> int:
    errors = verify_game()
    if errors:
        print("\n".join(errors))
        print(f"\nFAILED: {len(errors)} issue(s) found.")
        return 1
    print("OK: All Ren'Py audio symbols and asset paths verified.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
