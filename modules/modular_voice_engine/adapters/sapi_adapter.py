"""Zero-dependency offline Windows SAPI5 female TTS fallback (.wav)."""

import os
import subprocess
from pathlib import Path


def is_available() -> bool:
    return os.name == "nt"


def synthesize(text: str, emotion: str, out_path: Path) -> Path:
    if not is_available():
        raise RuntimeError("Windows SAPI5 TTS is only available on Windows.")
    rate = {"happy": 1, "teasing": 1, "shy": -1, "tired": -2}.get(emotion, 0)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    safe_text = text.replace("'", "''")
    ps = (
        "Add-Type -AssemblyName System.Speech; "
        "$s = New-Object System.Speech.Synthesis.SpeechSynthesizer; "
        "$s.SelectVoiceByHints([System.Speech.Synthesis.VoiceGender]::Female); "
        f"$s.Rate = {rate}; "
        f"$s.SetOutputToWaveFile('{str(out_path)}'); "
        f"$s.Speak('{safe_text}'); "
        "$s.Dispose()"
    )
    subprocess.run(["powershell", "-NoProfile", "-Command", ps], check=True)
    return out_path
