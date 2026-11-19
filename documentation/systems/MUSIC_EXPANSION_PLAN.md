# LOLA Music Expansion & Auto-DJ Improvement Plan

## Goal
Make downloading new lofi tracks (e.g. from Free Stock Music / Chosic) and turning them into beat-matched, loudness-normalized, credited in-game DJ mixes effortless.

---

## Improvement Roadmap

### 1. Batch Music Importer (`developer-tools/audio_toolkit/import_music.py`)
- **Input**: `--source <folder>` (e.g. `Downloads`) + `--apply`.
- **Actions**:
  1. Deduplicate against existing `game/audio/music/lofi/` by SHA-256.
  2. Sanitize filenames to ASCII `snake_case` (preventing Ren'Py ZIP lint warnings).
  3. Copy tracks into `game/audio/music/lofi/`, append default entries to `game/audio/music_database.json`, and regenerate `game/audio/dj_mix_plan.json`.
  4. Auto-generate `game/audio/CREDITS_MUSIC.txt` from `license` + `artist` fields for CC-BY compliance.

### 2. Colab Auto-Analysis & `.ogg` Compression (`colab_dj_studio.ipynb`)
- Upload newly imported tracks to Colab to:
  1. Replace estimated `bpm`, `key`, `beat_drop`, and `bridge` values in `music_database.json` with exact `librosa` detections.
  2. Master every track to `-14 LUFS` / `-1.0 dBTP` (`pyloudnorm`) and export VBR `.ogg` (`q=5`), keeping `game/audio/` compact even at 30+ tracks.

### 3. In-Game Auto-DJ & History (`game/00_systems/audio_transitions/`)
- **Continuous Setlist**: Optional `auto_dj_enabled` toggle so finishing a track smoothly crossfades across `dual_deck.rpy` into the next Camelot + mood-matched track.
- **Previous Track / History**: Keep a small `dj_history` stack so players can step back to the previous track from the hover pill.

### 4. Verification
- Run `python developer-tools/check_everything.py` after every music import to confirm `Audio Health`, `Asset Hygiene`, unit tests, and Ren'Py `lint` all pass.
