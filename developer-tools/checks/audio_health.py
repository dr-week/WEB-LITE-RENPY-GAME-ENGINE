"""Verify DJ mix plan, music database files, and short transition SFX caps."""

import json
from pathlib import Path


def check_audio_health(game_root: Path, max_sfx_bytes: int = 105_000, budget_mb: float = 100.0) -> dict:
    """Validate audio manifests, short SFX caps, and total audio folder size budget."""
    missing, oversized_sfx = [], []
    audio_dir = game_root / "audio"
    total_bytes = sum(p.stat().st_size for p in audio_dir.rglob("*") if p.is_file()) if audio_dir.is_dir() else 0
    audio_mb = round(total_bytes / (1024 * 1024), 2)
    music_db = audio_dir / "music_database.json"
    if music_db.is_file():
        for track in json.loads(music_db.read_text(encoding="utf-8-sig")):
            rel = track.get("audio_file", "").replace("game/", "", 1)
            if rel and not (game_root / rel).is_file():
                missing.append(rel)

    mix_plan = game_root / "audio" / "dj_mix_plan.json"
    if mix_plan.is_file():
        tracks = json.loads(mix_plan.read_text(encoding="utf-8-sig")).get("tracks", {})
        for entry in tracks.values():
            for nxt in entry.get("next_tracks", []):
                rel = nxt.get("audio_file", "")
                if rel and not (game_root / rel).is_file():
                    missing.append(rel)

    sfx_json = game_root / "audio" / "sfx_transitions.json"
    if sfx_json.is_file():
        for item in json.loads(sfx_json.read_text(encoding="utf-8-sig")).get("sfx", []):
            p = game_root / item.get("file", "")
            if not p.is_file():
                missing.append(item.get("file", ""))
            elif p.stat().st_size > max_sfx_bytes:
                oversized_sfx.append((item["file"], p.stat().st_size))

    return {
        "ok": not missing and not oversized_sfx,
        "missing": sorted(set(missing)),
        "oversized_sfx": oversized_sfx,
        "audio_mb": audio_mb,
        "over_budget": audio_mb > budget_mb,
    }
