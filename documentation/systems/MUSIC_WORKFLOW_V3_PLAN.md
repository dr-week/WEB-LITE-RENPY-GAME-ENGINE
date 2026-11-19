# LOLA Music & Auto-DJ Workflow v3 Plan (Research-Backed)

## Already Built (v1–v2)
- Portable `audio_toolkit/` (`camelot.py`, `dj_planner.py`, `mastering.py`, `sfx_curator.py`, `import_music.py`, `colab_dj_studio.ipynb`).
- Dual-deck Ren'Py mixer (`dual_deck.rpy`), mood/Camelot/BPM Auto-DJ (`dj_remix_system.rpy`), and compact hover vinyl UI (`cd_music_widget.rpy`).

---

## Next Improvements (v3)

### 1. Vertical Layering via Ren'Py `synchro_start=True` (`dual_deck.rpy` + `colab_dj_studio.ipynb`)
- Register 4 synced stem channels on the `"music"` mixer (`layer_base`, `layer_beat`, `layer_melody`, `layer_ambient`, `loop=True`) and start them together with `synchro_start=True` for frame-exact alignment.
- **Sync Guardrail:** All stems for a track must share the **exact same duration and sample rate** (e.g., 44.1 kHz `.ogg`) to prevent clock drift; `synchro_start=True` preloads all stems before starting.
- Fade layers dynamically with `renpy.music.set_volume(vol, delay=..., channel=...)` based on scene intensity (e.g., quiet exploration = base + ambient; active/tension = bring in drums + melody; clear vs. muffled room toggle via paired `synchro_start` channels).
- Export Demucs 4-stem splits and ready-to-play Camelot mashup transitions from `colab_dj_studio.ipynb`.

### 2. Gapless `.ogg` Migration & Horizontal Resequencing (`colab_dj_studio.ipynb` + `dj_remix_system.rpy`)
- Batch-convert `.mp3` tracks (currently `89.43 MB` across `28` files; total `game/audio/` is `89.69 MB`) to `.ogg` VBR (`q=5`) in Colab to cut disk size and eliminate MP3 decoder padding/stutter for **gapless seamless looping** in Ren'Py.
- Expand horizontal resequencing in `dj_remix_system.rpy` to switch between neutral, minor/tension, and upbeat variations at `beat_drop`, `bridge`, and `outro` cue points.

### 3. Audio Size Budget Guardrail (`developer-tools/checks/audio_health.py`)
- Report `game/audio/` total MB inside `check_everything.py` and warn if it exceeds `100 MB`, prompting a Colab `.ogg` compression pass.

### 4. 1-Command Downloads Watcher (`import_music.py --recent-minutes 30`)
- Add `--source ~/Downloads --recent-minutes 30` filtering to `import_music.py` so only freshly downloaded Free Stock Music `.mp3`s are imported without touching unrelated files in `Downloads`.

### 5. Smooth Music Ducking & DSP References (`dual_deck.rpy`)
- Smoothly duck active music deck volume (`0.72` -> `1.0`) when transition SFX or voice/alerts play, then restore cleanly.
- Reference tools for future Colab/Ren'Py upgrades: `sergree/matchering` (Colab reference-track mastering for frequency response, RMS loudness, peak levels, and stereo width) and `niltwill/renpy-audiodsp` (load-time Ren'Py DSP filters, EQ, compression, and reverb returning `AudioData` objects).

---

## Mistakes Found & Fixed (CLI-Anything Workflow Audit)
1. **100 MB Budget Already Exceeded (`100.87 MB`):** `game/audio/` currently holds `28` `.mp3`s (`89.43 MB`) + `77` `.wav`s (`11.40 MB`). **Fix:** `colab unpack` in `music_cli.py` now updates `music_database.json` to `.ogg` and prunes superseded `.mp3`s automatically.
2. **Stem Overlap & Unwired Modular Auto-DJ:** `crossfade_decks` did not stop active stem channels, and `dj_skip_and_remix` bypassed `dj_play_modular`. **Fix:** `crossfade_decks` now calls `stop_stem_layers()`, and `dj_skip_and_remix` routes to `dj_play_modular()` when stems exist.
3. **Colab "Run All" Produced Empty `.ogg` Export:** `colab_dj_studio.ipynb` only defined functions without looping over `/content/tracks`. **Fix:** Added an automatic batch loop exporting `.ogg` for all tracks + Demucs 4-stems for the first 2 tracks.
4. **Binary Zip in Repo Tree:** `colab pack` defaulted inside `developer-tools/audio_toolkit/`. **Fix:** Moved default output to `~/Downloads/lola_colab_tracks.zip`.

## Remaining Next Steps
1. Upload [colab_dj_studio.ipynb](file:///c:/amd/aa/ASD/daa/GAME/LALALAND/LOLA/LOLA/developer-tools/audio_toolkit/colab_dj_studio.ipynb) + `~/Downloads/lola_colab_tracks.zip` to Google Colab, run all cells, and download `lola_dj_export.zip`.
2. Run `python developer-tools/cli_anything_lola_music.py --json colab unpack "$HOME\Downloads\lola_dj_export.zip"` to convert to gapless `.ogg`, install stems, and drop `game/audio/` under `100 MB`.
