"""
DSP Math and Equal-Power Crossfade Curves.
Zero-dependency, high precision audio curve generation.
"""
import math

class AudioCurves:
    @staticmethod
    def linear_fade_out(progress):
        return max(0.0, min(1.0, 1.0 - progress))

    @staticmethod
    def linear_fade_in(progress):
        return max(0.0, min(1.0, progress))

    @staticmethod
    def equal_power_fade_out(progress):
        """Sine/Cosine equal-power curve to prevent perceived volume dips."""
        p = max(0.0, min(1.0, progress))
        return math.cos(p * (math.pi / 2.0))

    @staticmethod
    def equal_power_fade_in(progress):
        """Sine/Cosine equal-power curve to maintain unity sum of squares."""
        p = max(0.0, min(1.0, progress))
        return math.sin(p * (math.pi / 2.0))

    @staticmethod
    def s_curve_fade_in(progress):
        """Smooth cubic sigmoid for subtle atmospheric transitions."""
        p = max(0.0, min(1.0, progress))
        return p * p * (3.0 - 2.0 * p)
