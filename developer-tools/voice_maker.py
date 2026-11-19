"""CLI for LOLA's Modular Voice Engine: status, scan, and cute Gen-Z TTS synthesis."""

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from modules.modular_voice_engine.adapters import edge_tts_adapter, sapi_adapter  # noqa: E402
from modules.modular_voice_engine.core.dialogue_scanner import scan_maya_lines, voice_coverage, write_voice_manifest  # noqa: E402
from modules.modular_voice_engine.core.emotion_profiles import line_hash, stylize_genz_mumble  # noqa: E402

TTS_DIR = ROOT / "game" / "audio" / "voice" / "tts"
MANIFEST = ROOT / "game" / "audio" / "voice" / "voice_manifest.json"
STORY_DIR = ROOT / "game" / "40_story"


def _synth_one(text: str, emotion: str, backend: str, key: str, genz: bool) -> Path:
    spoken = stylize_genz_mumble(text, emotion) if genz else text
    use_edge = backend == "edge" or (backend == "auto" and edge_tts_adapter.is_available())
    if use_edge:
        return edge_tts_adapter.synthesize(spoken, emotion, TTS_DIR / f"{key}.mp3")
    return sapi_adapter.synthesize(spoken, emotion, TTS_DIR / f"{key}.wav")


def main() -> int:
    p = argparse.ArgumentParser(description="Modular cute Gen-Z TTS & mumble voice CLI.")
    sub = p.add_subparsers(dest="cmd", required=True)
    sub.add_parser("scan", help="Scan story scripts and update voice_manifest.json.")
    sub.add_parser("status", help="Report voice coverage and available TTS backends.")
    syn = sub.add_parser("synth", help="Synthesize missing Maya spoken lines.")
    syn.add_argument("--limit", type=int, default=5)
    syn.add_argument("--backend", default="auto", choices=("auto", "edge", "sapi"))
    syn.add_argument("--genz", action="store_true", help="Prepend Gen-Z mumble fillers.")
    say = sub.add_parser("say", help="Synthesize a single line.")
    say.add_argument("text")
    say.add_argument("--emotion", default="happy")
    say.add_argument("--backend", default="auto", choices=("auto", "edge", "sapi"))
    say.add_argument("--genz", action="store_true")
    args = p.parse_args()

    if args.cmd == "status":
        cov = voice_coverage(STORY_DIR, TTS_DIR)
        print(json.dumps({"ok": True, "backends": {"edge_tts": edge_tts_adapter.is_available(), "sapi": sapi_adapter.is_available()}, **cov}, indent=2))
        return 0
    if args.cmd == "scan":
        print(json.dumps(write_voice_manifest(STORY_DIR, MANIFEST), indent=2))
        return 0
    if args.cmd == "say":
        out = _synth_one(args.text, args.emotion, args.backend, line_hash(args.text, args.emotion), args.genz)
        print(f"Synthesized -> {out.relative_to(ROOT)}")
        return 0
    items = [it for it in scan_maya_lines(STORY_DIR) if it["speaker"] == "maya"]
    write_voice_manifest(STORY_DIR, MANIFEST)
    made = [str(_synth_one(it["text"], it["emotion"], args.backend, it["hash"], args.genz).relative_to(ROOT))
            for it in items[:args.limit]
            if not (TTS_DIR / f"{it['hash']}.mp3").is_file() and not (TTS_DIR / f"{it['hash']}.wav").is_file()]
    print(json.dumps({"ok": True, "synthesized": made}, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
