"""
Sound Effect Combiner & Dual-Stinger Overlap Mixer.
Mixes and staggers two sound effects with custom gain envelopes and delays.
"""
from ..crossfader.audio_curves import AudioCurves

class SfxOverlapMixer:
    @staticmethod
    def mix_two_sfx(samples_a, samples_b, delay_sec=0.3, gain_a=1.0, gain_b=0.85, sr=44100):
        """Overlaps two sound effects (e.g. Riser into Boom, or Scratch into Woosh)."""
        offset_samples = int(delay_sec * sr)
        total_len = max(len(samples_a), offset_samples + len(samples_b))
        out = [0.0] * total_len

        for i, s in enumerate(samples_a):
            out[i] += s * gain_a

        for j, s in enumerate(samples_b):
            pos = offset_samples + j
            if pos < total_len:
                out[pos] += s * gain_b

        # Soft clip limit
        return [max(-1.0, min(1.0, x)) for x in out]
