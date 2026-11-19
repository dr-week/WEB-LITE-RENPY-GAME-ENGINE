"""Persistent session state for the CLI-Anything Modular Flow Engine."""

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
STATE_FILE = Path(__file__).resolve().parent / ".flow_session.json"


def load_session() -> dict:
    default = {
        "project_root": str(ROOT),
        "downloads_dir": str(Path.home() / "Downloads"),
        "last_count": 5,
        "last_asset_ids": [],
    }
    try:
        default.update(json.loads(STATE_FILE.read_text(encoding="utf-8")))
    except (OSError, ValueError):
        pass
    return default


def save_session(updates: dict) -> dict:
    state = load_session()
    state.update(updates)
    STATE_FILE.write_text(json.dumps(state, indent=2) + "\n", encoding="utf-8")
    return state
