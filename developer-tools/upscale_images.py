"""Upscale low-resolution game images to 1920x1080 using Lanczos + UnsharpMask."""

import argparse
from pathlib import Path
from PIL import Image, ImageFilter

ROOT = Path(__file__).resolve().parents[1]
EXTS = {".png", ".jpg", ".jpeg", ".webp"}


def upscale_image(path: Path, target_w: int = 1920, target_h: int = 1080) -> bool:
    with Image.open(path) as im:
        if im.width >= target_w and im.height >= target_h:
            return False
        scale = max(target_w / im.width, target_h / im.height)
        nw, nh = int(round(im.width * scale)), int(round(im.height * scale))
        up = im.resize((nw, nh), Image.Resampling.LANCZOS)
        up = up.filter(ImageFilter.UnsharpMask(radius=1.2, percent=110, threshold=3))
        up.save(path, quality=95)
        return True


def main():
    parser = argparse.ArgumentParser(description="Upscale small images in a folder.")
    parser.add_argument("folder", type=Path, help="Folder of images to check/upscale.")
    args = parser.parse_args()
    count = sum(1 for p in sorted(args.folder.rglob("*"))
                if p.is_file() and p.suffix.lower() in EXTS and upscale_image(p))
    print(f"Upscaled {count} images.")


if __name__ == "__main__":
    main()
