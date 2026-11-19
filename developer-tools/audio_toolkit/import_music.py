"""Batch-import lofi tracks, merge Colab DSP analysis, rebuild mix plan, and write credits."""

import argparse
import hashlib
import json
from pathlib import Path
import re
import shutil
import time

from .dj_planner import MIX_PLAN, MUSIC_DB, build_mix_plan

ROOT = Path(__file__).resolve().parents[2]
LOFI_DIR = ROOT / "game" / "audio" / "music" / "lofi"
CREDITS_OUT = ROOT / "game" / "audio" / "CREDITS_MUSIC.txt"
AUDIO_EXTS = {".mp3", ".ogg", ".wav"}


def _slugify(stem: str) -> str:
    return re.sub(r"[^a-z0-9]+", "_", stem.lower()).strip("_") or "track"


def _parse_artist_title(stem: str) -> tuple[str, str]:
    if " - " in stem:
        artist, title = stem.split(" - ", 1)
        return artist.strip(), title.strip()
    return "Independent", _slugify(stem).replace("_", " ").title()


def _existing_hashes(lofi_dir: Path) -> set[str]:
    if not lofi_dir.is_dir():
        return set()
    return {hashlib.sha256(p.read_bytes()).hexdigest()
            for p in lofi_dir.iterdir() if p.is_file() and p.suffix.lower() in AUDIO_EXTS}


def write_music_credits(db_path: Path = MUSIC_DB, out_path: Path = CREDITS_OUT) -> Path:
    """Write a clean CC-BY / royalty-free attribution file from music_database.json."""
    tracks = json.loads(db_path.read_text(encoding="utf-8-sig")) if db_path.is_file() else []
    lines = ["# LOLA Music Credits", ""]
    lines.extend(f"- {t.get('title', t['id'])} — {t.get('artist', 'Unknown')} ({t.get('license', 'CC BY 4.0')})"
                 for t in tracks)
    out_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return out_path


def merge_colab_analysis(analysis_path: Path, db_path: Path = MUSIC_DB, plan_path: Path = MIX_PLAN) -> int:
    """Merge BPM, key, beat_drop, and bridge cues from Colab music_analysis.json into DB."""
    if not analysis_path.is_file() or not db_path.is_file():
        return 0
    analyzed = {item["id"]: item for item in json.loads(analysis_path.read_text(encoding="utf-8-sig"))}
    db_tracks = json.loads(db_path.read_text(encoding="utf-8-sig"))
    updated = 0
    for track in db_tracks:
        if info := analyzed.get(track["id"]):
            track["bpm"] = info.get("bpm", track["bpm"])
            track["key"] = info.get("key", track["key"])
            cues = track.setdefault("cue_points", {})
            cues["beat_drop"] = info.get("beat_drop", cues.get("beat_drop", 12.0))
            cues["bridge"] = info.get("bridge", cues.get("bridge", 44.0))
            updated += 1
    if updated:
        db_path.write_text(json.dumps(db_tracks, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        plan_path.write_text(json.dumps(build_mix_plan(db_path), ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return updated


def import_music_folder(src_dir: Path, lofi_dir: Path = LOFI_DIR, db_path: Path = MUSIC_DB,
                        plan_path: Path = MIX_PLAN, credits_path: Path = CREDITS_OUT,
                        apply: bool = False, recent_minutes: float | None = None) -> dict:
    """Import unique audio files, append DB entries, rebuild mix plan, and update credits."""
    if not src_dir.is_dir():
        return {"imported": 0, "skipped": 0, "files": []}
    seen = _existing_hashes(lofi_dir)
    cutoff = (time.time() - recent_minutes * 60.0) if recent_minutes is not None else None
    db_tracks = json.loads(db_path.read_text(encoding="utf-8-sig")) if db_path.is_file() else []
    known_ids = {t["id"] for t in db_tracks}
    added, skipped = [], 0
    for src in sorted(src_dir.iterdir()):
        if not src.is_file() or src.suffix.lower() not in AUDIO_EXTS:
            continue
        if cutoff is not None and src.stat().st_mtime < cutoff:
            continue
        digest = hashlib.sha256(src.read_bytes()).hexdigest()
        if digest in seen:
            skipped += 1
            continue
        seen.add(digest)
        slug = _slugify(src.stem)
        artist, title = _parse_artist_title(src.stem)
        dest = lofi_dir / f"{slug}{src.suffix.lower()}"
        if apply:
            lofi_dir.mkdir(parents=True, exist_ok=True)
            shutil.copy2(str(src), str(dest))
            if slug not in known_ids:
                known_ids.add(slug)
                db_tracks.append({
                    "id": slug, "title": title, "artist": artist,
                    "audio_file": f"game/audio/music/lofi/{dest.name}", "bpm": 76, "key": "C Minor",
                    "mood": "Lofi Chill", "energy": 0.45,
                    "cue_points": {"intro": 0.0, "beat_drop": 12.0, "bridge": 44.0, "outro": 100.0},
                    "tags": ["lofi", "chill"], "license": "Creative Commons Attribution (CC BY 4.0)",
                })
        added.append(dest.name)
    if apply and added:
        db_path.write_text(json.dumps(db_tracks, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        plan_path.write_text(json.dumps(build_mix_plan(db_path), ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        write_music_credits(db_path, credits_path)
    return {"imported": len(added), "skipped": skipped, "files": added}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", type=Path, help="Folder of downloaded lofi tracks.")
    parser.add_argument("--recent-minutes", type=float, default=None, help="Only import files modified within N minutes.")
    parser.add_argument("--merge-analysis", type=Path, help="Colab music_analysis.json to merge.")
    parser.add_argument("--apply", action="store_true", help="Copy files and update DB/mix plan/credits.")
    args = parser.parse_args()
    if args.merge_analysis:
        print(f"Merged Colab analysis into {merge_colab_analysis(args.merge_analysis)} track(s).")
    if args.source:
        res = import_music_folder(args.source, apply=args.apply, recent_minutes=args.recent_minutes)
        print(f"{'Imported' if args.apply else 'Dry run'}: {res['imported']} track(s), {res['skipped']} duplicate(s) skipped.")


if __name__ == "__main__":
    main()
