"""Neural cute-girl TTS adapter using edge-tts (en-US-AnaNeural)."""

import asyncio
import importlib.util
from pathlib import Path
from modules.modular_voice_engine.core.emotion_profiles import EMOTION_TTS


def is_available() -> bool:
    return importlib.util.find_spec("edge_tts") is not None


async def _save_async(text: str, emotion: str, out_path: Path):
    import edge_tts  # type: ignore
    prof = EMOTION_TTS.get(emotion, EMOTION_TTS["neutral"])
    comm = edge_tts.Communicate(text, prof["voice"], pitch=prof["pitch"], rate=prof["rate"])
    out_path.parent.mkdir(parents=True, exist_ok=True)
    await comm.save(str(out_path))


def synthesize(text: str, emotion: str, out_path: Path) -> Path:
    if not is_available():
        raise RuntimeError("edge-tts is not installed (pip install edge-tts).")
    asyncio.run(_save_async(text, emotion, out_path))
    return out_path
