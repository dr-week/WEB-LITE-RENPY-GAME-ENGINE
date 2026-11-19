# Portable DJ Mixing & Mastering Toolkit (`audio_toolkit`)

Self-contained, lightweight Python package designed to be copied into any project or agent workspace.

## Modules (All <= 65 Lines)
- `camelot.py` — 24-key Camelot Wheel mapping and harmonic compatibility scoring.
- `dj_planner.py` — Ranks BPM + Camelot + energy transitions and generates `dj_mix_plan.json`.
- `mastering.py` — Pure-NumPy equal-power crossfades, DC removal, RMS match, and `-1 dBFS` soft limiter.
- `sfx_curator.py` — Filters and imports short-duration transition swooshes/risers.
- `colab_dj_studio.ipynb` — Google Colab GPU/DSP notebook for heavy beat-grid analysis, Rubberband time-stretching, 3-band EQ swaps, Demucs stems, and LUFS mastering.

## Colab -> Game Handoff
1. Upload `colab_dj_studio.ipynb` and your `.mp3`/`.wav` tracks to Google Colab (zero local heavy installs).
2. Run all cells to analyze BPM/keys/beat-grids and render mastered beatmatched transitions.
3. Download `lola_dj_export.zip` and extract into `game/audio/`.
4. Run `python developer-tools/check_everything.py` to verify all audio assets.
