"""Safe browser and clipboard handoff for Google Flow."""

import subprocess
import webbrowser

FLOW_URL = "https://labs.google/fx/tools/flow"


def copy_to_clipboard(text: str) -> bool:
    try:
        subprocess.run(["clip"], input=text, text=True, check=True)
        return True
    except Exception:
        return False


def open_flow_session(batch_text: str, count: int) -> dict:
    copied = copy_to_clipboard(batch_text)
    opened = webbrowser.open(FLOW_URL)
    return {"ok": True, "flow_url": FLOW_URL, "browser_opened": opened,
            "copied_to_clipboard": copied, "copied_prompts": count}
