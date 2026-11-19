"""Automated narration auditor: flags long Maya lines (>6 words) and dry/robotic prose."""

import argparse
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
STORY_DIRS = (ROOT / "game" / "40_story", ROOT / "game" / "20_locations")
TAG_RE = re.compile(r"\{[^}]+\}")
NARR_RE = re.compile(r'^"([^"]+)"$')


def audit_narration(max_maya_words: int = 6) -> dict:
    issues = []
    for base in STORY_DIRS:
        for rpy in sorted(base.rglob("*.rpy")):
            rel = rpy.relative_to(ROOT).as_posix()
            for idx, raw in enumerate(rpy.read_text(encoding="utf-8-sig").splitlines(), 1):
                s = raw.strip()
                if s.startswith(('maya "', 'maya_thought "')):
                    txt = TAG_RE.sub("", s.split('"', 1)[1].rsplit('"', 1)[0]).strip()
                    wc = len(txt.split())
                    if wc > max_maya_words:
                        issues.append({"type": "long_maya_line", "words": wc, "file": rel, "line": idx, "text": txt})
                elif m := NARR_RE.match(s):
                    txt = m.group(1)
                    if "Day [current_day]" in txt or "m'kay" in txt.lower() or "earned some money" in txt or txt in ("Home again.",):
                        issues.append({"type": "dry_or_tic_narration", "file": rel, "line": idx, "text": txt})
    return {"ok": not issues, "issue_count": len(issues), "issues": issues}


def main() -> int:
    p = argparse.ArgumentParser(description="Audit LOLA narration for Maya line length and prose quality.")
    p.add_argument("--json", action="store_true")
    p.add_argument("--max-words", type=int, default=6)
    args = p.parse_args()
    rep = audit_narration(args.max_words)
    print(json.dumps(rep, indent=2, ensure_ascii=False) if args.json else f"Narration issues: {rep['issue_count']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
