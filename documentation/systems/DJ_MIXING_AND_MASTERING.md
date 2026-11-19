# DJ Mixing, Harmonic Matching & Audio Mastering Guide

## 1. Why Amateur Transitions Sound Bad
- **Random BPM jumps**: Cutting from 70 BPM to 85 BPM without BPM-proximity matching causes rhythmic whiplash.
- **Clashing musical keys**: Transitioning between incompatible keys creates dissonance.
- **Linear fades & hard cuts**: Fading in a new track without fading out the old track (or using linear volume ramps) causes a `-3 dB` volume dip or abrupt cut.
- **Overpowering SFX**: Firing loud airhorns/booms simultaneously at `100%` volume buries the music instead of smoothing the transition.

---

## 2. Core DJ & Mastering Techniques

### A. Harmonic Mixing (Camelot Wheel)
Every musical key maps to a Camelot code (`1A`–`12A` minor, `1B`–`12B` major). Clean transitions follow:
- **Same Key (`0` steps)**: e.g. `5A -> 5A` (seamless)
- **Adjacent Key (`±1` on wheel)**: e.g. `5A -> 6A` or `4A` (smooth energy shift)
- **Relative Major/Minor (`A <-> B` same number)**: e.g. `5A -> 5B` (mood shift without dissonance)

### B. Beatmatching & Phrase Cueing
- Keep `|BPM_next - BPM_current| <= 6` BPM (or double/half-time).
- Start the incoming track on a **structural phrase cue** (`intro`, `beat_drop`, or `bridge` in `game/audio/music_database.json`) rather than an arbitrary timestamp.

### C. Equal-Power Crossfades & Mastering
- **Equal-Power Curve**: Fade out with $\cos(\frac{\pi}{2} t)$ and fade in with $\sin(\frac{\pi}{2} t)$ so $\cos^2 + \sin^2 = 1$ (constant perceived loudness).
- **Loudness & Limiting**: Match integrated RMS/LUFS across tracks and apply a `-1.0 dBFS` soft-clip limiter to prevent digital clipping.
- **Subtle Transition SFX**: Use short-duration (`< 1.2s`) filtered swooshes/risers mixed at `-9 dB` to `-12 dB` (`relative_volume=0.35`) under the crossfade.

---

## 3. Open-Source Python References
- `caffettino87/auto-dj-ai` — Beatmatching, Camelot harmonic scoring, 3-band EQ swaps
- `oguzhan-yilmaz/pycrossfade` — Gradual BPM shifts, 3-band DJ EQ crossfade, equal-power curves
- `superkevinyen/DJ_Analyzer` & `Supercarlillos/cuekey` — BPM, Camelot key, energy profiling
- `sergree/matchering` — Automated reference EQ/RMS/peak mastering

## 4. LOLA Automation Scripts (`developer-tools/audio_toolkit/`)
- `camelot.py` — 24-key Camelot Wheel mapping & harmonic compatibility scoring
- `dj_planner.py` — Ranks compatible transitions and builds `game/audio/dj_mix_plan.json`
- `mastering.py` — Pure-NumPy equal-power crossfade, DC/high-pass filter, RMS match, and limiter
- `sfx_curator.py` — Imports short-duration transition SFX from `C:\Users\disha\Videos\FX\SFX`
