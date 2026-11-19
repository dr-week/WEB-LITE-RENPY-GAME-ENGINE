"""Thin developer-tools shim for Modular Flow Engine's CLI-Anything interface."""

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from modules.modular_flow_engine.cli.flow_cli import cli  # noqa: E402

if __name__ == "__main__":
    cli()
