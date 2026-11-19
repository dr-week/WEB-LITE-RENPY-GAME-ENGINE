"""Scans Ren'Py story scripts for Maya dialogue lines and tracks TTS coverage."""

import json
import re
from collections import Counter
from pathlib import Path
from modules.modular_voice_engine.core.emotion_profiles import line_hash

MAYA_LINE_RE = re.compile(r'^\s*(maya|maya_thought)\s+"([^"]+)"')
EMO_SET_RE = re.compile(r'set_emotional_state\("([^"]+)"\)')


def scan_maya_lines(story_root: Path) -> list[dict]:
    items = []
    seen = set()
    for rpy in sorted(story_root.rglob("*.rpy")):
        emo = "neutral"
        for line in rpy.read_text(encoding="utf-8-sig").splitlines():
            if em := EMO_SET_RE.search(line):
                emo = em.group(1).lower()
            if m := MAYA_LINE_RE.match(line):
                speaker, text = m.group(1), m.group(2)
                key = line_hash(text, emo)
                if key not in seen:
                    seen.add(key)
                    items.append({"hash": key, "speaker": speaker, "emotion": emo, "text": text})
    return items


def write_voice_manifest(story_root: Path, out_path: Path) -> dict:
    items = scan_maya_lines(story_root)
    payload = {it["hash"]: it for it in items}
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return {"count": len(items), "path": str(out_path)}


def voice_coverage(story_root: Path, tts_dir: Path) -> dict:
    items = scan_maya_lines(story_root)
    tts_ready = sum(1 for it in items if (tts_dir / f"{it['hash']}.mp3").is_file() or (tts_dir / f"{it['hash']}.wav").is_file())
    emotions = dict(Counter(it["emotion"] for it in items))
    return {"total_lines": len(items), "tts_clips": tts_ready, "mumble_fallback": len(items) - tts_ready, "emotions": emotions}
