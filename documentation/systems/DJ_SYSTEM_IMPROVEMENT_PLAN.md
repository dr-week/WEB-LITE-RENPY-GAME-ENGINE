# LOLA Music & DJ System Architecture & Improvement Phases

## 1. System Architecture
```text
[Google Colab: colab_dj_studio.ipynb] (Heavy DSP/GPU: librosa, rubberband, pyloudnorm, demucs)
        │  exports music_database.json + mastered .ogg/.mp3
        ▼
[Local Toolkit: developer-tools/audio_toolkit/] (Zero heavy dependencies, <= 65 lines/file)
  ├─ camelot.py       -> 24-key Camelot Wheel harmonic scoring
  ├─ dj_planner.py    -> Ranks Camelot + BPM + energy -> game/audio/dj_mix_plan.json
  ├─ mastering.py     -> NumPy DC removal, equal-power crossfade, RMS/soft-clip limiter
  └─ sfx_curator.py   -> Curates short-duration swooshes/risers -> game/audio/sfx_transitions.json
        │
        ▼
[Game Runtime: game/00_systems/audio_transitions/ + cd_music_widget.rpy]
  ├─ dual_deck.rpy          -> Alternates Deck A ('music') & Deck B ('music_deck_b')
  ├─ overlap_transitions.rpy-> Fires 1 subtle short SFX (0.35 vol) + dual-deck crossfade
  ├─ dj_remix_system.rpy    -> Mood/time-aware Camelot + BPM track selection
  └─ cd_music_widget.rpy    -> Small spinning vinyl (idle) -> animated italic skip pill (hover)
```

---

## 2. Improvement Phases & Status

### Phase 1: Dual-Deck Overlapping Crossfade Engine — **IMPLEMENTED**
- `dual_deck.rpy` registers `music_deck_b` on the `music` mixer and alternates decks so outgoing and incoming tracks overlap simultaneously (`fadeout` + `fadein`) instead of cutting on one channel.

### Phase 2: Google Colab `-14 LUFS` Mastering & `.ogg` Size Optimization — **READY FOR COLAB**
- Run `developer-tools/audio_toolkit/colab_dj_studio.ipynb` on Google Colab to:
  1. Extract exact `librosa` beat-grid `beat_drop` and `bridge` cues.
  2. Normalize all tracks to `-14 LUFS` / `-1.0 dBTP` (`pyloudnorm`).
  3. Export VBR `.ogg` (`q=5`) to reduce `game/audio/` from **89.69 MB** to **~45–55 MB**.

### Phase 3: Story-Mood & Time-Slot Aware DJ — **IMPLEMENTED**
- `dj_remix_system.rpy` biases candidate selection from `dj_mix_plan.json` using `time_slot` (`morning`/`evening`/`night`) and `emotional_state` (`tired`/`calm` vs `proud`/`hopeful`).

### Phase 4: Automated Audio QA — **IMPLEMENTED**
- `developer-tools/checks/audio_health.py` verifies all `music_database.json`, `dj_mix_plan.json`, and `sfx_transitions.json` files exist and meet the `<= 105 KB` short-SFX cap inside `check_everything.py`.
