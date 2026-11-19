# LOLA Lofi Music Download Wishlist (70–85 BPM, CC-BY / Royalty-Free)

Curated list of tracks matching LOLA's existing soundtrack (`Artificial.Music`, `Barradeen`, `Tokyo Music Walker`, `Purrple Cat`, `Ghostrifter Official`) for future download.

## Sources
- **Free Stock Music (Lo-Fi)**: https://www.free-stock-music.com/lo-fi.html
- **Chosic (Lo-Fi & Chill)**: https://www.chosic.com/free-music/lofi/
- **Pixabay (Lo-Fi Search)**: https://pixabay.com/music/search/lofi/

---

## Wishlist by Game Mood

| Mood / Scene | Suggested Artists & Track Styles | Target BPM | Target Folder |
| :--- | :--- | :--- | :--- |
| **Morning / City Walk** | *Tokyo Music Walker* — upbeat warm guitar/piano lofi (*Day Off*, *Slowly*, *Brunch*) | `76–82 BPM` | `game/audio/music/lofi/` |
| **Cozy Apartment / Study** | *Purrple Cat* — soft Rhodes/rainy window beats (*Warm Horizon*, *Crescent Moon*, *Sugar Coat*) | `70–76 BPM` | `game/audio/music/lofi/` |
| **Cafe / Social Hangout** | *Artificial.Music* & *Lukrembo* — bouncy crisp snare & warm bass lofi | `75–82 BPM` | `game/audio/music/lofi/` |
| **Late Night / Tension** | *Ghostrifter Official* & *Barradeen* — moody minor-key pads & deep sub-bass | `70–78 BPM` | `game/audio/music/lofi/` |

## Import Steps (When Downloaded)
1. Save `.mp3`/`.ogg` files into `game/audio/music/lofi/`.
2. *(Optional)* Run through `developer-tools/audio_toolkit/colab_dj_studio.ipynb` for `-14 LUFS` mastering & `.ogg` compression.
3. Add entries to `game/audio/music_database.json` and run `python -m audio_toolkit.dj_planner`.
4. Verify with `python developer-tools/check_everything.py`.
