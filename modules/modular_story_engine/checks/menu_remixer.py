"""Finds menus with >2 options, discards extra options, and remixes the remaining 2."""

import re
from pathlib import Path

MENU_RE = re.compile(r"^(\s*)menu\s*:\s*$")
CHOICE_RE = re.compile(r'^(\s*)"([^"]+)"(?:\s+if\s+[^:]+)?\s*:\s*$')
STAT_RE = re.compile(r"^\s*\$\s*(?:change_stat|set_flag)\(")


def _split_options(lines: list[str], menu_idx: int, menu_indent: int) -> tuple[int, list[tuple[str, str, list[str]]]]:
    options, cur_label, cur_hdr, cur_body = [], None, "", []
    choice_indent = None
    j = menu_idx + 1
    while j < len(lines):
        raw = lines[j]
        stripped = raw.strip()
        indent = len(raw) - len(raw.lstrip(" "))
        if stripped and not stripped.startswith("#") and indent <= menu_indent:
            break
        cm = CHOICE_RE.match(raw)
        if cm and (choice_indent is None or indent == choice_indent):
            choice_indent = indent
            if cur_label is not None:
                options.append((cur_label, cur_hdr, cur_body))
            cur_label, cur_hdr, cur_body = cm.group(2), raw, []
        elif cur_label is not None:
            cur_body.append(raw)
        j += 1
    if cur_label is not None:
        options.append((cur_label, cur_hdr, cur_body))
    return j, options


def remix_file(rpy_path: Path, apply: bool = False) -> list[dict]:
    lines = rpy_path.read_text(encoding="utf-8-sig").splitlines()
    out, findings, i = [], [], 0
    while i < len(lines):
        m = MENU_RE.match(lines[i])
        if not m:
            out.append(lines[i])
            i += 1
            continue
        menu_indent = len(m.group(1))
        end_idx, opts = _split_options(lines, i, menu_indent)
        if len(opts) <= 2:
            out.extend(lines[i:end_idx])
            i = end_idx
            continue
        kept_a, discarded, kept_b = opts[0], opts[1:-1], opts[-1]
        extra_stats = [ln for _, _, body in discarded for ln in body if STAT_RE.match(ln) and ln not in kept_b[2]]
        remixed_b_body = extra_stats + kept_b[2]
        out.append(lines[i])
        out.extend([kept_a[1], *kept_a[2], kept_b[1], *remixed_b_body])
        findings.append({"file": rpy_path.name, "line": i + 1, "original_options": len(opts),
                         "discarded": [d[0] for d in discarded], "kept": [kept_a[0], kept_b[0]]})
        i = end_idx
    if apply and findings:
        rpy_path.write_text("\n".join(out) + "\n", encoding="utf-8")
    return findings


def remix_story_menus(story_root: Path, apply: bool = False, allow_files: set[str] | None = None) -> dict:
    allow = allow_files or {"day_hub.rpy", "prologue_starts.rpy", "week_01_eval.rpy", "day_end.rpy", "image_story_hub.rpy"}
    all_findings = []
    for rpy in sorted(story_root.rglob("*.rpy")):
        if rpy.name not in allow:
            all_findings.extend(remix_file(rpy, apply=apply))
    return {"ok": True, "applied": apply, "remixed_count": len(all_findings), "menus": all_findings}
