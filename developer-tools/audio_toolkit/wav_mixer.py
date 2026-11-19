"""
WAV mixer, crossfader, and DJ FX overlay engine.
"""
import wave
import struct
import math
import os

class WavMixer:
    @staticmethod
    def read_wav_mono(filepath):
        with wave.open(filepath, "rb") as wf:
            n_ch = wf.getnchannels()
            sw = wf.getsampwidth()
            sr = wf.getframerate()
            n_frames = wf.getnframes()
            frames = wf.readframes(n_frames)
            
            fmt = f"<{n_frames * n_ch}h" if sw == 2 else None
            if not fmt:
                raise ValueError("Only 16-bit PCM WAV supported.")
            raw = struct.unpack(fmt, frames)
            if n_ch == 2:
                samples = [(raw[i] + raw[i+1]) / (2.0 * 32768.0) for i in range(0, len(raw), 2)]
            else:
                samples = [s / 32768.0 for s in raw]
            return samples, sr

    @staticmethod
    def write_wav_mono(filepath, samples, sr=44100):
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        with wave.open(filepath, "wb") as wf:
            wf.setnchannels(1)
            wf.setsampwidth(2)
            wf.setframerate(sr)
            clipped = [max(-32767, min(32767, int(s * 32767))) for s in samples]
            packed = struct.pack(f"<{len(clipped)}h", *clipped)
            wf.writeframes(packed)

    @staticmethod
    def overlay_sfx(music_samples, sfx_samples, start_sec, sr=44100, sfx_vol=0.8):
        """Overlay an SFX (boom/riser/woosh) over existing audio track."""
        res = list(music_samples)
        start_idx = int(start_sec * sr)
        for i, s in enumerate(sfx_samples):
            pos = start_idx + i
            if pos < len(res):
                res[pos] = res[pos] + s * sfx_vol
        return res
