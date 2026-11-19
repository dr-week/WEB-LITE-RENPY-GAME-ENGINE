"""Headless Ren'Py compile, static asset/symbol check, and lint smoke test."""

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SDK = Path("C:/RenPy/renpy-8.6.0/renpy-8.6.0-sdk")
RENPY_PY = SDK / "lib" / "py3-windows-x86_64" / "python.exe"


def run_step(label: str, cmd: list[str]) -> bool:
    print(f"==> {label}")
    proc = subprocess.run(cmd, cwd=str(ROOT))
    return proc.returncode == 0


def main() -> int:
    if not run_step("Static asset & story checks", [sys.executable, str(ROOT / "developer-tools/checks/run_all_checks.py")]):
        return 1
    if RENPY_PY.is_file():
        for action in ("compile", "lint"):
            if not run_step(f"Ren'Py {action}", [str(RENPY_PY), str(SDK / "renpy.py"), str(ROOT), action]):
                return 1
    print("OK: Headless Ren'Py smoke test passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
