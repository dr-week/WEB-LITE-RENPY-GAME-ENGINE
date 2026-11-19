# LOLA Music & Auto-DJ Workflow v2 Improvement Plan

## Current State
- `import_music.py` imports `.mp3`/`.ogg`/`.wav` files, deduplicates by SHA-256, updates `music_database.json`, rebuilds `dj_mix_plan.json`, and generates `CREDITS_MUSIC.txt`.
- `dual_deck.rpy`, `dj_remix_system.rpy`, and `cd_music_widget.rpy` support dual-deck crossfading, Camelot + BPM + mood selection, hot-cueing (`CUE`), and `dj_history` (`arrowLeft`).

---

## Next Improvements

### 1. Smart Metadata & Colab Merge (`audio_toolkit/`)
- **Filename & Tag Parsing**: Parse `artist-track-title.mp3` naming (common on Free Stock Music) in `import_music.py` instead of defaulting `artist` to `"Independent"`.
- **`--merge-analysis` Bridge**: Add a lightweight command to merge `music_analysis.json` exported by `colab_dj_studio.ipynb` (`bpm`, `key`, `beat_drop`, `bridge`) directly into `game/audio/music_database.json` and rebuild `dj_mix_plan.json`.

### 2. True Continuous Auto-DJ Loop (`game/00_systems/audio_transitions/`)
- Wire `auto_dj_enabled` to a lightweight screen timer / `renpy.music.get_pos()` check in `cd_music_widget.rpy` so when a track nears its `outro` (or ends), the DJ automatically crossfades across `dual_deck.rpy` into the next Camelot + mood-matched track.
- Add an **Auto-DJ On/Off** toggle indicator inside the hover pill.

### 3. Player Track Preferences (`persistent.dj_track_weights`)
- Track how often the player skips a song early vs. lets it play (or clicks a quick favorite toggle), biasing `_pick_context_track()` toward preferred tracks without extra UI clutter.

### 4. Size & Format Guardrail (`checks/audio_health.py`)
- Add a total `game/audio/` size budget check (warn if `> 100 MB`) to encourage `.ogg` VBR export from `colab_dj_studio.ipynb` as the library grows.
