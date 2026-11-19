# Lightweight Gen-Z cute mumble + TTS voice callback system for Maya.

init -1 python:
    import hashlib
    import re

    renpy.music.register_channel("maya_voice", mixer="sfx", loop=True)
    renpy.music.register_channel("maya_tts", mixer="sfx", loop=False)

    MAYA_VOICE_PROFILES = {
        "neutral": "audio/voice/maya/maya_neutral.wav",
        "happy": "audio/voice/maya/maya_happy.wav",
        "proud": "audio/voice/maya/maya_proud.wav",
        "hopeful": "audio/voice/maya/maya_hopeful.wav",
        "teasing": "audio/voice/maya/maya_teasing.wav",
        "shy": "audio/voice/maya/maya_shy.wav",
        "tired": "audio/voice/maya/maya_tired.wav",
        "worried": "audio/voice/maya/maya_worried.wav",
    }

    def resolve_maya_emotion():
        emo = str(getattr(store, "emotional_state", "") or "").lower()
        if emo in MAYA_VOICE_PROFILES:
            return emo
        if hasattr(store, "get_protagonist_expression"):
            expr = get_protagonist_expression()
            if expr in MAYA_VOICE_PROFILES:
                return expr
        return "neutral"

    def resolve_maya_tts_clip(text, emo):
        if not text:
            return None
        stripped = re.sub(r"\{[^}]+\}", "", str(text))
        clean = " ".join(stripped.strip().split())
        for candidate_emo in (emo, "neutral"):
            key = hashlib.sha1(f"{candidate_emo}|{clean}".encode("utf-8")).hexdigest()[:12]
            for ext in ("mp3", "wav"):
                rel = f"audio/voice/tts/{key}.{ext}"
                if renpy.loadable(rel):
                    return rel
        return None

    def maya_unseen_mumble(emotion=None):
        """Play Maya's cute emotional mumble without displaying a dialogue box."""
        emo = emotion if emotion in MAYA_VOICE_PROFILES else resolve_maya_emotion()
        renpy.music.play(MAYA_VOICE_PROFILES[emo], channel="maya_tts")

    def maya_voice_callback(event, interact=True, **kwargs):
        if not interact:
            return
        if event == "begin":
            emo = resolve_maya_emotion()
            what = getattr(store, "_maya_current_what", "")
            tts_clip = resolve_maya_tts_clip(what, emo)
            if tts_clip:
                renpy.music.stop(channel="maya_voice", fadeout=0.05)
                renpy.music.play(tts_clip, channel="maya_tts")
            else:
                renpy.music.play(MAYA_VOICE_PROFILES[emo], channel="maya_voice", if_changed=True)
        elif event in ("slow_done", "end"):
            renpy.music.stop(channel="maya_voice", fadeout=0.08)
            if event == "end":
                store._maya_current_what = ""

    class MayaCharacter(ADVCharacter):
        def __call__(self, what, **kwargs):
            store._maya_current_what = what
            return super(MayaCharacter, self).__call__(what, **kwargs)
