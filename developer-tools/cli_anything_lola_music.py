"""Thin developer-tools shim for LOLA Music & Colab CLI-Anything interface."""

import sys
from pathlib import Path

DEV_TOOLS = Path(__file__).resolve().parent
if str(DEV_TOOLS) not in sys.path:
    sys.path.insert(0, str(DEV_TOOLS))

from audio_toolkit.music_cli import cli  # noqa: E402

if __name__ == "__main__":
    cli()
