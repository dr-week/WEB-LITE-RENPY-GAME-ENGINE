"""Generate crisp 4x-supersampled transparent thumbs-up and thumbs-down icons."""

from pathlib import Path
from PIL import Image, ImageDraw

OUT = Path(__file__).resolve().parents[1] / "game" / "images" / "ui" / "icons"


def draw_thumb(up: bool, fill: tuple[int, int, int, int], out_path: Path):
    s = 256
    img = Image.new("RGBA", (s, s), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    # Cuff on left
    d.rounded_rectangle([24, 108, 72, 212], radius=14, fill=fill)
    # Palm + thumb silhouette
    pts = [(78, 112), (118, 38), (144, 38), (146, 94), (212, 94), (226, 112),
           (218, 198), (196, 212), (78, 212)]
    d.polygon(pts, fill=fill)
    if not up:
        img = img.transpose(Image.Transpose.FLIP_TOP_BOTTOM)
    img.resize((64, 64), Image.Resampling.LANCZOS).save(out_path)


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    draw_thumb(True, (110, 231, 183, 255), OUT / "thumb_up.png")
    draw_thumb(False, (253, 164, 175, 255), OUT / "thumb_down.png")
    print("Generated thumb_up.png and thumb_down.png")


if __name__ == "__main__":
    main()
