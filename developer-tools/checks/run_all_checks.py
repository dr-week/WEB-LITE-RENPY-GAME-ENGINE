"""Unified automated pre-launch gate for LOLA assets, story integrity, and tests."""

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DEV_TOOLS = ROOT / "developer-tools"
for p in (str(ROOT), str(DEV_TOOLS)):
    if p not in sys.path:
        sys.path.insert(0, p)

from checks.fix_non_ascii_assets import find_non_ascii_files  # noqa: E402
from checks.story_integrity import check_story_integrity  # noqa: E402
from checks.verify_game_assets import verify_game  # noqa: E402
from modules.modular_story_engine.checks.two_option_validator import validate_two_option_rule  # noqa: E402


def run_checks(strict_two_option: bool = True) -> dict:
    asset_errors = verify_game()
    non_ascii = [p.name for p, _ in find_non_ascii_files()]
    integrity = check_story_integrity(ROOT / "game")
    two_opt = validate_two_option_rule(ROOT / "game" / "40_story")
    ok = (not asset_errors) and (not non_ascii) and integrity["ok"] and (two_opt["ok"] or not strict_two_option)
    return {
        "ok": ok,
        "asset_errors": asset_errors,
        "non_ascii_files": non_ascii,
        "story_integrity": integrity,
        "two_option_rule": two_opt,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Run unified LOLA pre-launch verification gate.")
    parser.add_argument("--json", action="store_true", help="Emit JSON summary.")
    parser.add_argument("--strict-two-option", action="store_true", help="Fail if any legacy menu != 2 options.")
    args = parser.parse_args()
    report = run_checks(strict_two_option=args.strict_two_option)
    if args.json:
        print(json.dumps(report, indent=2))
    else:
        print(f"Assets: {len(report['asset_errors'])} error(s) | "
              f"Story labels: {report['story_integrity']['labels']} (missing: {len(report['story_integrity']['missing_targets'])}) | "
              f"2-option legacy warnings: {len(report['two_option_rule']['violations'])}")
    return 0 if report["ok"] else 1


if __name__ == "__main__":
    sys.exit(main())
