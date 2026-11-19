"""
CLI entry point for querying music database and previewing DJ mixes.
"""
import sys
import os
from .audio_remixer import AudioRemixer
from .wav_mixer import WavMixer

def print_catalog():
    remixer = AudioRemixer()
    print("=== LOLA MUSIC DATABASE & REMIX PAIRINGS ===")
    for t in remixer.tracks:
        print(f"[{t['id']}] {t['title']} - {t['artist']} ({t['bpm']} BPM, {t['key']})")
        compat = remixer.find_compatible_mixes(t["id"])
        if compat:
            pairs = [f"{c['track']['id']} (Δ{c['bpm_diff']} BPM)" for c in compat]
            print(f"   -> Compatible Beatmatch: {', '.join(pairs)}")
        print()

def main():
    print_catalog()

if __name__ == "__main__":
    main()
