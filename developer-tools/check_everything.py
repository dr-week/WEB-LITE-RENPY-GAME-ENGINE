"""Unified 'check everything' runner for LOLA scripts, story graph, assets, tests, and Ren'Py lint."""

import argparse
from pathlib import Path
import subprocess
import sys

from checks import check_asset_hygiene, check_audio_health, check_module_sizes, check_story_integrity
from evaluate_story_db import evaluate

ROOT = Path(__file__).resolve().parents[1]
SDK_CANDIDATES = [
    Path("C:/RenPy/renpy-8.6.0/renpy-8.6.0-sdk"),
    Path("C:/RenPy/renpy-8.6.0-sdk"),
    Path("C:/renpy-8.6.0-sdk"),
]


def _run_tests(root: Path) -> bool:
    res = subprocess.run(
        [sys.executable, "-m", "unittest", "discover", "-s", "developer-tools/tests", "-v"],
        cwd=root, capture_output=True, text=True,
    )
    lines = [ln for ln in (res.stderr or res.stdout).splitlines() if ln.strip()]
    summary = " | ".join(lines[-2:]) if lines else "No test output"
    print(f"[{'PASS' if res.returncode == 0 else 'FAIL'}] Unit Tests: {summary}")
    if res.returncode != 0:
        print(res.stdout)
        print(res.stderr)
    return res.returncode == 0


def _run_renpy_lint(root: Path) -> bool:
    sdk = next((s for s in SDK_CANDIDATES if (s / "renpy.py").is_file()), None)
    if not sdk:
        print("[SKIP] Ren'Py SDK not found for lint.")
        return True
    py = sdk / "lib" / "py3-windows-x86_64" / "python.exe"
    res = subprocess.run([str(py), str(sdk / "renpy.py"), str(root), "lint"],
                         capture_output=True, text=True)
    if res.returncode != 0:
        print(res.stdout)
        print(res.stderr)
    print(f"[{'PASS' if res.returncode == 0 else 'FAIL'}] Ren'Py 8.6.0 lint")
    return res.returncode == 0


def run_all(root: Path = ROOT, skip_lint: bool = False) -> bool:
    game = root / "game"
    story = check_story_integrity(game)
    assets = check_asset_hygiene(game)
    audio = check_audio_health(game)
    modules = check_module_sizes(root)
    print(f"[{'PASS' if story['ok'] else 'FAIL'}] Story Integrity: {story['labels']} labels, "
          f"{len(story['missing_targets'])} missing targets, {len(story['bad_json'])} bad JSON")
    for src, ln, tgt in story["missing_targets"]:
        print(f"  MISSING LABEL {src}:{ln} -> {tgt}")
    print(f"[{'PASS' if assets['ok'] else 'FAIL'}] Asset Hygiene: "
          f"{len(assets['missing_audio'])} missing audio, {len(assets['missing_icons'])} missing icons, "
          f"{len(assets['non_ascii_files'])} non-ASCII image names")
    print(f"[{'PASS' if audio['ok'] else 'FAIL'}] Audio Health: "
          f"{len(audio['missing'])} missing tracks/SFX, {len(audio['oversized_sfx'])} oversized SFX, "
          f"{audio['audio_mb']:.2f} MB total")
    if audio.get("over_budget"):
        print(f"  [WARN] game/audio/ exceeds 100 MB budget ({audio['audio_mb']:.2f} MB) — run Colab .ogg pass")
    print(f"[INFO] Module Sizes: checked {modules['checked']} files, {len(modules['oversized'])} > 150 lines")
    evaluate(game)
    tests_ok = _run_tests(root)
    lint_ok = True if skip_lint else _run_renpy_lint(root)
    return story["ok"] and assets["ok"] and audio["ok"] and tests_ok and lint_ok


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--fast", action="store_true", help="Skip Ren'Py SDK lint.")
    args = parser.parse_args()
    ok = run_all(ROOT, skip_lint=args.fast)
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
