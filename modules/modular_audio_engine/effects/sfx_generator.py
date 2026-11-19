"""
Procedural sound synthesizer for DJ, Transitions, and Cinematic cues.
Generates 16-bit PCM WAV buffers or files with zero external dependencies.
"""
import math
import struct
import random

class SfxGenerator:
    @staticmethod
    def generate_riser(duration=2.5, sr=44100):
        n = int(sr * duration)
        samples = []
        phase = 0.0
        for i in range(n):
            t = i / sr
            frac = t / duration
            freq = 120.0 * (10.0 ** frac)
            phase += 2 * math.pi * freq / sr
            amp = (frac ** 1.5) * (0.8 + 0.2 * math.sin(2 * math.pi * 8 * t))
            samples.append(amp * math.sin(phase))
        return samples

    @staticmethod
    def generate_boom(duration=2.0, sr=44100):
        n = int(sr * duration)
        samples = []
        phase = 0.0
        for i in range(n):
            t = i / sr
            freq = max(30.0, 150.0 * math.exp(-6.0 * t))
            phase += 2 * math.pi * f / sr if "f" in locals() else 2 * math.pi * freq / sr
            amp = math.exp(-2.5 * t)
            samples.append(amp * (math.sin(phase) + 0.4 * math.sin(phase * 1.5)) * 0.9)
        return samples

    @staticmethod
    def generate_braam(duration=3.0, sr=44100):
        n = int(sr * duration)
        samples = []
        phase1, phase2 = 0.0, 0.0
        for i in range(n):
            t = i / sr
            f1 = 55.0 + 5.0 * math.exp(-2.0 * t)
            phase1 += 2 * math.pi * f1 / sr
            phase2 += 2 * math.pi * (f1 * 1.5) / sr
            raw = math.sin(phase1) + 0.6 * math.sin(phase2) + 0.3 * (random.random()*2 - 1) * math.exp(-t)
            dist = math.tanh(raw * 2.5)
            amp = min(1.0, t * 8.0) * math.exp(-1.0 * t)
            samples.append(dist * amp * 0.85)
        return samples

    @staticmethod
    def generate_spinback(duration=0.8, sr=44100):
        n = int(sr * duration)
        samples = []
        phase = 0.0
        for i in range(n):
            t = i / sr
            f = 300.0 + 1500.0 * ((1.0 - t / duration) ** 2)
            phase += 2 * math.pi * f / sr
            wobble = 0.8 + 0.2 * math.sin(2 * math.pi * 30.0 * t)
            amp = math.sin(math.pi * (t / duration)) ** 0.5
            samples.append(math.sin(phase) * wobble * amp * 0.85)
        return samples

    @staticmethod
    def generate_scratch(duration=0.5, sr=44100):
        n = int(sr * duration)
        samples = []
        phase = 0.0
        for i in range(n):
            t = i / sr
            f = 600.0 + 400.0 * math.sin(2 * math.pi * 12 * t) * (1 - t / duration)
            phase += 2 * math.pi * f / sr
            amp = (1.0 - t / duration) * 0.85
            samples.append(amp * math.sin(phase))
        return samples
