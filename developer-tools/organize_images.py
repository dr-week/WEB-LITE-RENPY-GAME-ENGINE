import argparse
from collections import Counter
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
GAME_ROOT = PROJECT_ROOT / "game"
IMAGE_ROOT = GAME_ROOT / "images"
RULES = (
    ("character_reference", ("character_turnaround", "multiple_frames", "photographer_assistant", "blue_outfit", "interacting_with_character")),
    ("relationships", ("couple", "boyfriend", "holding_hands", "embracing_man")),
    ("college", ("classroom", "college", "assignment", "computer_lab", "campus", "lecture", "club_fair", "in_class", "professor")),
    ("transport", ("bus", "train", "subway", "station", "airport", "ferry", "yacht", "boat", "harbour", "harbor", "luggage", "turnstile", "motorcycle")),
    ("social_events", ("party", "rave", "nightclub", "wedding", "reception", "jazz_club", "lounge", "karaoke", "rooftop_bar", "velvet_booth", "terrace", "champagne", "dive_bar")),
    ("home_lodging", ("home", "bedroom", "balcony", "bathtub", "shower", "kitchen", "cabin", "hotel", "loft", "sofa", "jacuzzi", "poolside", "window", "apartment")),
    ("food_drink", ("cafe", "café", "coffee", "espresso", "sushi", "ramen", "noodle", "diner", "bakery", "pizza", "food", "grape", "peach", "tea", "vineyard", "milkshake", "smoothie", "juice", "chopstick", "marshmallow", "dough", "chili", "cellar")),
    ("shops_markets", ("market", "store", "shop", "boutique", "mall", "auction", "dealership", "bookstore", "comic", "record", "vinyl", "antique", "hardware", "grocery", "groceries", "flower", "mart", "laundromat")),
    ("hobbies_outdoors", ("park", "garden", "beach", "gym", "skating", "skate", "arcade", "museum", "gallery", "art", "studio", "workshop", "pottery", "observatory", "aquarium", "planetarium", "greenhouse", "bike", "clock", "radio", "trail", "library", "mountain", "cliff", "succulent", "frisbee", "scarf", "alley", "rooftop", "ocean", "sunset", "fern", "conservatory", "merry-go-round", "ice_rink", "skee-ball", "planet", "shoelace")),
    ("public_places", ("lobby", "corridor", "directions", "street_interview", "stairwell")),
    ("generated_art", ("grok-image",)),
)


def category(filename):
    normalized = filename.casefold()
    for folder, keywords in RULES:
        if any(keyword in normalized for keyword in keywords):
            return folder
    return "general_scenes"


def rewrite_references():
    replacements = {}
    for image in IMAGE_ROOT.rglob("*"):
        if not image.is_file() or image.parent == IMAGE_ROOT:
            continue
        old = f"images/{image.name}"
        new = f"images/{image.relative_to(IMAGE_ROOT).as_posix()}"
        if old in replacements and replacements[old] != new:
            raise ValueError(f"Duplicate image filename across folders: {image.name}")
        replacements[old] = new
    for source in GAME_ROOT.rglob("*"):
        if not source.is_file():
            continue
        if source.suffix.lower() not in {".rpy", ".py", ".json", ".md"}:
            continue
        original = source.read_bytes()
        has_bom = original.startswith(b"\xef\xbb\xbf")
        text = original.decode("utf-8-sig")
        updated = text
        for old, new in replacements.items():
            updated = updated.replace(old, new).replace(old.replace("/", "\\"), new.replace("/", "\\"))
        if updated != text:
            bom = b"\xef\xbb\xbf" if has_bom else b""
            source.write_bytes(bom + updated.encode("utf-8"))


def main():
    parser = argparse.ArgumentParser(description="Sort root-level game images into filename-based folders.")
    parser.add_argument("--apply", action="store_true", help="Move images and update source references.")
    args = parser.parse_args()
    plan = [(source, IMAGE_ROOT / category(source.name) / source.name)
            for source in IMAGE_ROOT.iterdir() if source.is_file()]
    counts = Counter(destination.parent.name for _, destination in plan)
    for folder, count in sorted(counts.items()):
        print(f"{folder}: {count}")
    if not args.apply:
        print(f"Dry run: {len(plan)} files. Re-run with --apply to move them.")
        return
    collisions = [destination for _, destination in plan if destination.exists()]
    if collisions:
        raise FileExistsError(f"Refusing to overwrite {len(collisions)} existing image files.")
    moved = []
    try:
        for source, destination in plan:
            destination.parent.mkdir(exist_ok=True)
            source.rename(destination)
            moved.append((source, destination))
    except OSError:
        for source, destination in reversed(moved):
            destination.rename(source)
        raise
    rewrite_references()
    print(f"Moved {len(moved)} images and updated source references.")


if __name__ == "__main__":
    main()
