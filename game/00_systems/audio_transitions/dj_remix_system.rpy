# Context-aware Harmonic + BPM DJ transition, Auto-DJ loop, history & hot-cue system.

default current_dj_track_id = "downtown_glow"
default current_dj_track_name = "Downtown Glow"
default dj_history = []
default auto_dj_enabled = True

init -3 python:
    import json
    import random

    if not isinstance(persistent.dj_track_weights, dict):
        persistent.dj_track_weights = {}

    def _load_json_dict(path, key=None):
        try:
            with renpy.open_file(path, encoding="utf-8") as handle:
                data = json.load(handle)
            return data.get(key, {}) if key else {t["id"]: t for t in data}
        except Exception:
            return {}

    DJ_MIX_PLAN = _load_json_dict("audio/dj_mix_plan.json", "tracks")
    DJ_TRACK_CUES = _load_json_dict("audio/music_database.json")

    def _pick_context_track(candidates):
        slot = getattr(renpy.store, "time_slot", "morning")
        mood = getattr(renpy.store, "emotional_state", "hopeful")
        prefer_chill = slot in ("night", "evening") or mood in ("tired", "calm")
        weights = persistent.dj_track_weights if isinstance(persistent.dj_track_weights, dict) else {}
        scored = []
        for item in candidates:
            bpm_bonus = 0.08 if (prefer_chill and item["bpm"] <= 78) or (not prefer_chill and item["bpm"] >= 76) else 0.0
            pref_bonus = max(-0.15, min(0.15, float(weights.get(item["id"], 0.0))))
            scored.append((item["score"] + bpm_bonus + pref_bonus, item))
        scored.sort(key=lambda pair: -pair[0])
        return random.choice([pair[1] for pair in scored[:3]])

    def _adjust_weight(track_id, delta):
        if isinstance(persistent.dj_track_weights, dict) and track_id:
            persistent.dj_track_weights[track_id] = round(persistent.dj_track_weights.get(track_id, 0.0) + delta, 3)

    def dj_skip_and_remix(auto=False):
        """Crossfade across dual decks to a mood/Camelot/BPM compatible track."""
        global current_dj_track_id, current_dj_track_name
        node = DJ_MIX_PLAN.get(current_dj_track_id)
        candidates = node.get("next_tracks", []) if node else []
        if not candidates and DJ_MIX_PLAN:
            candidates = DJ_MIX_PLAN[random.choice(list(DJ_MIX_PLAN.keys()))].get("next_tracks", [])
        if not candidates:
            return
        _adjust_weight(current_dj_track_id, 0.04 if auto else -0.03)
        if current_dj_track_id and (not dj_history or dj_history[-1] != current_dj_track_id):
            dj_history.append(current_dj_track_id)
            if len(dj_history) > 12:
                del dj_history[0]
        chosen = _pick_context_track(candidates)
        current_dj_track_id, current_dj_track_name = chosen["id"], chosen["title"]
        start_sec = chosen["entry_sec"] if random.random() < 0.75 else chosen["bridge_sec"]
        if not dj_play_modular(chosen["id"], fade_sec=1.6):
            play_random_overlap_transition(next_music_track=chosen["audio_file"], start_sec=start_sec, fade_sec=1.6)
        renpy.notify(f"DJ Mix: {chosen['title']} ({chosen['bpm']} BPM • {chosen['camelot']})")

    def dj_prev_track():
        """Step back to the previous track in dj_history across dual decks."""
        global current_dj_track_id, current_dj_track_name
        if not dj_history:
            renpy.notify("DJ: At start of session history")
            return
        track = DJ_TRACK_CUES.get(dj_history.pop())
        if not track:
            return
        current_dj_track_id, current_dj_track_name = track["id"], track["title"]
        rel_path = track["audio_file"].replace("game/", "", 1)
        start_sec = float(track.get("cue_points", {}).get("beat_drop", 0.0))
        play_random_overlap_transition(next_music_track=rel_path, start_sec=start_sec, fade_sec=1.4)
        renpy.notify(f"DJ Back: {track['title']}")

    def dj_cue_bridge_remix():
        """Hot-cue the current track to its bridge or beat_drop across dual decks."""
        track = DJ_TRACK_CUES.get(current_dj_track_id)
        if not track:
            return
        cues = track.get("cue_points", {})
        cue_name, start_sec = random.choice([("Bridge", cues.get("bridge", 40.0)), ("Drop", cues.get("beat_drop", 12.0))])
        play_random_overlap_transition(next_music_track=track["audio_file"].replace("game/", "", 1),
                                       start_sec=float(start_sec), fade_sec=1.1)
        renpy.notify(f"DJ Cue ({cue_name}): {track['title']}")

    def dj_check_auto_advance():
        """Auto-crossfade when current track reaches its outro cue point."""
        if not auto_dj_enabled:
            return
        track = DJ_TRACK_CUES.get(current_dj_track_id)
        outro_sec = float(track.get("cue_points", {}).get("outro", 110.0)) if track else 110.0
        pos = renpy.music.get_pos(channel=_active_music_deck)
        if pos is not None and pos >= outro_sec:
            dj_skip_and_remix(auto=True)

    def toggle_auto_dj():
        global auto_dj_enabled
        auto_dj_enabled = not auto_dj_enabled
        renpy.notify("Auto-DJ: ON" if auto_dj_enabled else "Auto-DJ: OFF")

    STEM_MOOD_PRESETS = {
        "calm": {"layer_base": 1.0, "layer_beat": 0.35, "layer_melody": 0.75, "layer_ambient": 1.0},
        "active": {"layer_base": 1.0, "layer_beat": 0.85, "layer_melody": 1.0, "layer_ambient": 0.5},
        "tense": {"layer_base": 1.0, "layer_beat": 1.0, "layer_melody": 0.4, "layer_ambient": 0.7},
    }

    def dj_apply_mood_stems(mood=None, fade_sec=1.4):
        """Adjust vertical stem channel volumes to match current scene mood/time_slot."""
        slot = getattr(renpy.store, "time_slot", "morning")
        state = mood or getattr(renpy.store, "emotional_state", "hopeful")
        if state in ("stressed", "anxious", "tense"):
            preset = STEM_MOOD_PRESETS["tense"]
        elif slot in ("night", "evening") or state in ("tired", "calm"):
            preset = STEM_MOOD_PRESETS["calm"]
        else:
            preset = STEM_MOOD_PRESETS["active"]
        set_stem_layer_volumes(preset, fade_sec=fade_sec)

    def dj_resequence_cue(cue_name="beat_drop", fade_sec=1.1):
        """Horizontally resequence the active track to a named cue point across dual decks."""
        track = DJ_TRACK_CUES.get(current_dj_track_id)
        if not track:
            return
        start_sec = float(track.get("cue_points", {}).get(cue_name, 0.0))
        rel_path = track["audio_file"].replace("game/", "", 1)
        play_random_overlap_transition(next_music_track=rel_path, start_sec=start_sec, fade_sec=fade_sec)

    def dj_play_modular(track_id=None, mood=None, fade_sec=1.2):
        """Play 4-stem modular layers if exported by Colab, else fall back to dual-deck track."""
        tid = track_id or current_dj_track_id
        stems = {ch: f"audio/music/stems/{tid}/{ch}.ogg" for ch in STEM_CHANNELS}
        if all(renpy.loadable(p) for p in stems.values()):
            renpy.music.stop(channel=_active_music_deck, fadeout=fade_sec)
            play_stem_layers(stems, fade_sec=fade_sec)
            dj_apply_mood_stems(mood=mood, fade_sec=fade_sec)
            return True
        stop_stem_layers(fade_sec=fade_sec)
        track = DJ_TRACK_CUES.get(tid)
        if track:
            crossfade_decks(track["audio_file"].replace("game/", "", 1), fade_sec=fade_sec)
        return False
