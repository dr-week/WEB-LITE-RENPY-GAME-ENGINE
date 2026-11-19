"""CLI for LOLA's Modular Story Engine: generate beats/days and validate story structure."""

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from modules.modular_story_engine.checks.menu_remixer import remix_story_menus  # noqa: E402
from modules.modular_story_engine.checks.two_option_validator import validate_two_option_rule  # noqa: E402
from modules.modular_story_engine.core.story_schema import CHARACTERS, LOCATIONS, TIME_SLOTS, TONES  # noqa: E402
from modules.modular_story_engine.generator.beat_generator import build_beat_spec, render_rpy_beat  # noqa: E402
from modules.modular_story_engine.generator.day_builder import DAY_THEMES, build_day_arc  # noqa: E402


def main() -> int:
    parser = argparse.ArgumentParser(description="Modular 2-option Ren'Py story maker & validator.")
    sub = parser.add_subparsers(dest="cmd", required=True)

    gen = sub.add_parser("generate", help="Generate a seamless 2-option story beat.")
    gen.add_argument("--label", required=True)
    gen.add_argument("--location", default="cafe", choices=sorted(LOCATIONS))
    gen.add_argument("--time-slot", default="afternoon", choices=TIME_SLOTS)
    gen.add_argument("--character", default=None, choices=CHARACTERS)
    gen.add_argument("--tone", default="hustle", choices=TONES)
    gen.add_argument("--seed", default=None, type=int)
    gen.add_argument("--out", default=None, type=Path)

    day_p = sub.add_parser("create-day", help="Create a full 3-slot Day Arc and auto-update SQLite.")
    day_p.add_argument("--day-num", required=True, type=int)
    day_p.add_argument("--theme", default="campus_hustle", choices=sorted(DAY_THEMES))
    day_p.add_argument("--seed", default=None, type=int)
    day_p.add_argument("--out", default=None, type=Path)
    day_p.add_argument("--no-db", action="store_true")

    val = sub.add_parser("validate", help="Validate 2-option menu rule across game/40_story/.")
    val.add_argument("--json", action="store_true")

    rmx = sub.add_parser("remix", help="Find >2-option menus, discard extras, and remix to 2 options.")
    rmx.add_argument("--apply", action="store_true", help="Write remixed menus back to .rpy files.")
    rmx.add_argument("--json", action="store_true")

    args = parser.parse_args()
    if args.cmd == "generate":
        text = render_rpy_beat(build_beat_spec(args.label, args.location, args.time_slot, args.character, args.tone, args.seed))
        if args.out:
            args.out.parent.mkdir(parents=True, exist_ok=True)
            args.out.write_text(text, encoding="utf-8")
        print(f"Wrote {args.out}" if args.out else text)
        return 0
    if args.cmd == "create-day":
        res = build_day_arc(args.day_num, args.theme, args.seed, sync_db=not args.no_db)
        if args.out:
            args.out.parent.mkdir(parents=True, exist_ok=True)
            args.out.write_text(res["rpy"], encoding="utf-8")
        print(f"Created Day {args.day_num} ({len(res['beats'])} beats, db_synced={res['db_synced']})" if args.out else res["rpy"])
        return 0
    if args.cmd == "remix":
        rep = remix_story_menus(ROOT / "game" / "40_story", apply=args.apply)
        print(json.dumps(rep, indent=2) if args.json else f"Remixed {rep['remixed_count']} menu(s) (applied={rep['applied']})")
        return 0
    report = validate_two_option_rule(ROOT / "game" / "40_story")
    print(json.dumps(report, indent=2) if args.json else f"Checked {report['files_checked']} files; violations: {len(report['violations'])}")
    return 0 if report["ok"] else 1


if __name__ == "__main__":
    sys.exit(main())
