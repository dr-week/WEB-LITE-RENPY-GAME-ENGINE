"""Silent, single-instance core for the LOLA player game launcher."""

import ctypes
import json
import os
import re
import subprocess
from pathlib import Path

HERE = Path(__file__).resolve().parent
PROJECT = HERE.parents[1]
GAME_DIR = PROJECT / "game"
CONFIG = HERE / "launcher_settings.json"
PID_FILE = HERE / ".lola_game.pid"
LOG_FILE = HERE / "last_launch.log"
SDK_CANDIDATES = ["C:/RenPy/renpy-8.6.0/renpy-8.6.0-sdk", "C:/RenPy/renpy-8.6.0-sdk", "C:/renpy-8.6.0-sdk"]
MODES = {"Auto (Recommended)": "", "ANGLE / DirectX": "angle2", "Software (No GPU)": "sw"}
_MUTEX_HANDLE = None


def acquire_launcher_mutex():
    global _MUTEX_HANDLE
    if os.name != "nt":
        return True
    _MUTEX_HANDLE = ctypes.windll.kernel32.CreateMutexW(None, False, "Global\\LOLA_Game_Launcher_Mutex")
    return ctypes.windll.kernel32.GetLastError() != 183


def is_game_running():
    if not PID_FILE.is_file():
        return False
    try:
        pid = int(PID_FILE.read_text(encoding="utf-8").strip())
    except (OSError, ValueError):
        return False
    if os.name == "nt":
        handle = ctypes.windll.kernel32.OpenProcess(0x100000, False, pid)
        if not handle:
            return False
        alive = ctypes.windll.kernel32.WaitForSingleObject(handle, 0) == 0x102
        ctypes.windll.kernel32.CloseHandle(handle)
        return alive
    return False


def load():
    data = {"sdk": "", "mode": "Auto (Recommended)", "fullscreen": False}
    try:
        saved = json.loads(CONFIG.read_text(encoding="utf-8"))
        if saved.get("mode") in MODES:
            data["mode"] = saved["mode"]
        data["fullscreen"] = bool(saved.get("fullscreen", False))
        data["sdk"] = saved.get("sdk", "")
    except (OSError, ValueError):
        pass
    if not data["sdk"] or not (Path(data["sdk"]) / "renpy.py").is_file():
        data["sdk"] = next((s for s in SDK_CANDIDATES if (Path(s) / "renpy.py").is_file()), "")
    return data


def save(data):
    CONFIG.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")


def detect_game_version():
    try:
        text = (GAME_DIR / "script.rpy").read_text(encoding="utf-8", errors="ignore")
        match = re.search(r'define\s+config\.version\s*=\s*"([^"]+)"', text)
        return match.group(1) if match else "0.1.0"
    except OSError:
        return "0.1.0"


def launch_game(cfg):
    """Launch LOLA silently straight to Main Menu. Returns (ok, message)."""
    if is_game_running():
        return False, "LOLA is already running."
    sdk = cfg.get("sdk", "")
    if not sdk or not (GAME_DIR).is_dir():
        return False, "Ren'Py SDK or game folder not found."
    sdk_path = Path(sdk)
    pyw = sdk_path / "lib" / "py3-windows-x86_64" / "pythonw.exe"
    cmd = ([str(pyw), str(sdk_path / "renpy.py"), str(PROJECT), "run"]
           if pyw.is_file() else [str(sdk_path / "renpy.exe"), str(PROJECT), "run"])
    env = dict(os.environ)
    renderer = MODES.get(cfg.get("mode", ""), "")
    if renderer:
        env["RENPY_RENDERER"] = renderer
    if cfg.get("fullscreen"):
        env["RENPY_FULLSCREEN"] = "1"
    flags = 0x08000000 if os.name == "nt" else 0
    try:
        with open(LOG_FILE, "w", encoding="utf-8") as log:
            proc = subprocess.Popen(cmd, cwd=sdk, env=env, stdout=log, stderr=log, creationflags=flags)
        PID_FILE.write_text(str(proc.pid), encoding="utf-8")
    except OSError as exc:
        return False, str(exc)
    return True, "Starting LOLA..."
