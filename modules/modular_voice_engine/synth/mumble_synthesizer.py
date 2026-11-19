"""Synthesize cute, warm Gen-Z harmonic vowel-mumble WAV clips for Maya."""

import math
import random
import struct
import wave
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
DEFAULT_OUT_DIR = ROOT / "game" / "audio" / "voice" / "maya"
SR = 22050

PROFILES = {
    "neutral": (355.0, 5.8, 0.21, 0.04),
    "happy": (415.0, 7.2, 0.25, 0.08),
    "proud": (395.0, 6.5, 0.24, 0.06),
    "hopeful": (390.0, 6.2, 0.23, 0.06),
    "teasing": (385.0, 6.8, 0.23, 0.09),
    "shy": (365.0, 4.6, 0.15, 0.03),
    "tired": (305.0, 3.8, 0.14, 0.02),
    "worried": (340.0, 5.0, 0.17, 0.05),
}


def synth_mumble(name: str, base_f: float, syl_hz: float, amp: float, lilt: float,
                 out_dir: Path = DEFAULT_OUT_DIR, seed: int = 42) -> Path:
    rng = random.Random(seed + sum(ord(c) for c in name))
    n = int(SR * 1.1)
    frames = bytearray()
    phase = 0.0
    syl_len = int(SR / syl_hz)
    f_mult = 1.0
    for i in range(n):
        if i % syl_len == 0:
            f_mult = rng.uniform(1.0 - lilt * 0.6, 1.0 + lilt * 1.5)
        t_syl = (i % syl_len) / syl_len
        env = math.sin(math.pi * t_syl) ** 1.25
        up_lilt = 1.0 + 0.04 * (i / n) if name in ("happy", "teasing", "hopeful") else 1.0
        freq = base_f * f_mult * up_lilt * (1.0 + 0.018 * math.sin(2 * math.pi * 5.5 * i / SR))
        phase += 2 * math.pi * freq / SR
        raw = 0.68 * math.sin(phase) + 0.24 * math.sin(2 * phase) + 0.08 * math.sin(3 * phase)
        fade = min(1.0, i / 450.0, (n - i) / 450.0)
        frames.extend(struct.pack("<h", int(max(-1.0, min(1.0, raw * env * amp * fade)) * 32767)))
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / f"maya_{name}.wav"
    with wave.open(str(out_path), "wb") as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(SR)
        wf.writeframes(bytes(frames))
    return out_path


def generate_all(out_dir: Path = DEFAULT_OUT_DIR) -> list[Path]:
    return [synth_mumble(name, *params, out_dir=out_dir) for name, params in PROFILES.items()]
