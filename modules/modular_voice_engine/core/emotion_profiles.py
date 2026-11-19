"""Gen-Z cute mumble girl emotion profiles and deterministic line hashing."""

import hashlib

DEFAULT_VOICE = "en-US-AnaNeural"

EMOTION_TTS = {
    "neutral": {"voice": DEFAULT_VOICE, "pitch": "+6Hz", "rate": "+4%"},
    "happy": {"voice": DEFAULT_VOICE, "pitch": "+14Hz", "rate": "+10%"},
    "proud": {"voice": DEFAULT_VOICE, "pitch": "+11Hz", "rate": "+6%"},
    "hopeful": {"voice": DEFAULT_VOICE, "pitch": "+12Hz", "rate": "+6%"},
    "teasing": {"voice": DEFAULT_VOICE, "pitch": "+13Hz", "rate": "+12%"},
    "shy": {"voice": DEFAULT_VOICE, "pitch": "+9Hz", "rate": "-6%"},
    "tired": {"voice": DEFAULT_VOICE, "pitch": "-4Hz", "rate": "-12%"},
    "worried": {"voice": DEFAULT_VOICE, "pitch": "+7Hz", "rate": "-2%"},
}

GENZ_MUMBLE_FILLERS = {
    "neutral": "hmm...",
    "happy": "ooh, okay—",
    "proud": "heh, nailed it—",
    "hopeful": "lowkey, maybe—",
    "teasing": "wait, seriously? ",
    "shy": "uhm... ",
    "tired": "ughh... ",
    "worried": "wait wait—",
}


def line_hash(text: str, emotion: str = "neutral") -> str:
    clean = " ".join(text.strip().split())
    emo = emotion if emotion in EMOTION_TTS else "neutral"
    return hashlib.sha1(f"{emo}|{clean}".encode("utf-8")).hexdigest()[:12]


def stylize_genz_mumble(text: str, emotion: str = "neutral") -> str:
    prefix = GENZ_MUMBLE_FILLERS.get(emotion, "")
    return f"{prefix}{text}" if prefix and not text.lower().startswith(("hmm", "uhm", "wait", "ugh", "lowkey")) else text
