"""Thin developer-tools CLI shim for Maya's mumble synthesizer."""

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from modules.modular_voice_engine.synth.mumble_synthesizer import generate_all  # noqa: E402

if __name__ == "__main__":
    files = generate_all()
    print(f"Generated {len(files)} Maya voice mumble clips.")
