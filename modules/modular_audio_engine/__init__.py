"""
Modular Audio Engine
Zero-dependency, standalone audio management, mixing, and BPM transition suite.
Portable to Ren'Py, Godot, Pygame, Unity, or web backends.
"""
from .catalog.audio_catalog import AudioCatalog
from .core.mix_planner import MixPlanner
from .effects.sfx_generator import SfxGenerator
from .adapters.renpy_adapter import RenpyAudioAdapter

__all__ = ["AudioCatalog", "MixPlanner", "SfxGenerator", "RenpyAudioAdapter"]
