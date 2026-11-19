"""Adapter invoking LOLA's existing developer-tools pipeline scripts."""

import subprocess
import sys
from pathlib import Path

DEV_TOOLS = Path(__file__).resolve().parents[3] / "developer-tools"
SCRIPTS = {
    "audit": "audit_images.py",
    "catalog": "build_image_story_catalog.py",
    "preview": "integrate_story_images.py",
    "organize": "organize_images.py",
}


def run_pipeline_action(action: str) -> dict:
    if action not in SCRIPTS:
        raise ValueError(f"Unsupported pipeline action: {action}")
    proc = subprocess.run([sys.executable, str(DEV_TOOLS / SCRIPTS[action])],
                          cwd=str(DEV_TOOLS), capture_output=True, text=True)
    return {"ok": proc.returncode == 0, "action": action,
            "returncode": proc.returncode, "stdout": proc.stdout.strip()}
