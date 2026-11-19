"""Pure-NumPy DSP mastering: DC removal, equal-power crossfade, RMS match, and soft limiter."""

import numpy as np


def remove_dc_offset(samples: np.ndarray) -> np.ndarray:
    """Center waveform around zero to eliminate click/pop DC bias."""
    return samples - np.mean(samples, axis=0, keepdims=True)


def soft_clip_limiter(samples: np.ndarray, peak_db: float = -1.0) -> np.ndarray:
    """Apply smooth tanh soft-clipping and scale to target peak dBFS."""
    peak_lin = 10.0 ** (peak_db / 20.0)
    max_val = float(np.max(np.abs(samples))) if samples.size else 0.0
    if max_val == 0.0:
        return samples
    driven = np.tanh(samples * (1.2 / max(max_val, 1e-6)))
    norm = float(np.max(np.abs(driven)))
    return (driven / norm) * peak_lin if norm > 0 else driven


def match_rms_loudness(samples: np.ndarray, target_rms_db: float = -14.0) -> np.ndarray:
    """Scale waveform to approximate target RMS loudness before limiting."""
    rms = float(np.sqrt(np.mean(np.square(samples)))) if samples.size else 0.0
    if rms < 1e-7:
        return samples
    target_lin = 10.0 ** (target_rms_db / 20.0)
    return soft_clip_limiter(samples * (target_lin / rms), peak_db=-1.0)


def equal_power_crossfade(tail_a: np.ndarray, head_b: np.ndarray) -> np.ndarray:
    """Blend two equal-length float arrays using cos/sin equal-power curves."""
    n = min(len(tail_a), len(head_b))
    if n == 0:
        return np.array([], dtype=np.float32)
    t = np.linspace(0.0, np.pi / 2.0, n, dtype=np.float32)
    fade_out = np.cos(t)
    fade_in = np.sin(t)
    if tail_a.ndim == 2:
        fade_out = fade_out[:, None]
        fade_in = fade_in[:, None]
    return tail_a[:n] * fade_out + head_b[:n] * fade_in
