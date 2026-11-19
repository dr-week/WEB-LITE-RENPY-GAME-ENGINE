"""Camelot Wheel harmonic key mapping and DJ compatibility scoring."""

CAMELOT_WHEEL = {
    "A-Flat Minor": "1A", "G-Sharp Minor": "1A", "B Major": "1B",
    "E-Flat Minor": "2A", "D-Sharp Minor": "2A", "F-Sharp Major": "2B", "G-Flat Major": "2B",
    "B-Flat Minor": "3A", "A-Sharp Minor": "3A", "D-Flat Major": "3B", "C-Sharp Major": "3B",
    "F Minor": "4A", "A-Flat Major": "4B", "G-Sharp Major": "4B",
    "C Minor": "5A", "E-Flat Major": "5B", "D-Sharp Major": "5B",
    "G Minor": "6A", "B-Flat Major": "6B", "A-Sharp Major": "6B",
    "D Minor": "7A", "F Major": "7B",
    "A Minor": "8A", "C Major": "8B",
    "E Minor": "9A", "G Major": "9B",
    "B Minor": "10A", "D Major": "10B",
    "F-Sharp Minor": "11A", "G-Flat Minor": "11A", "A Major": "11B",
    "C-Sharp Minor": "12A", "D-Flat Minor": "12A", "E Major": "12B",
}


def to_camelot(key_name: str) -> str:
    """Convert a musical key name (e.g. 'C Minor') into Camelot notation ('5A')."""
    cleaned = " ".join(key_name.strip().title().split())
    return CAMELOT_WHEEL.get(cleaned, "")


def camelot_compatibility(key_a: str, key_b: str) -> float:
    """Return harmonic compatibility score in [0.0, 1.0] using Camelot Wheel rules."""
    ca, cb = to_camelot(key_a), to_camelot(key_b)
    if not ca or not cb:
        return 0.5
    if ca == cb:
        return 1.0
    num_a, mode_a = int(ca[:-1]), ca[-1]
    num_b, mode_b = int(cb[:-1]), cb[-1]
    dist = min((num_a - num_b) % 12, (num_b - num_a) % 12)
    if num_a == num_b and mode_a != mode_b:
        return 0.92
    if mode_a == mode_b and dist == 1:
        return 0.90
    if mode_a == mode_b and dist == 2:
        return 0.65
    return 0.25
