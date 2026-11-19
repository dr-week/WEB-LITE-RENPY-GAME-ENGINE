"""Extract transparent UI icons and panels from uploaded sprite sheets."""

from collections import deque
from pathlib import Path
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
SRC = Path("C:/Users/disha/.gemini/antigravity/brain/330db399-6a01-46a8-a409-3df68d8b223d/.user_uploaded")
ICONS_DIR = ROOT / "game" / "images" / "ui" / "icons"
PANELS_DIR = ROOT / "game" / "images" / "ui" / "panels"


def remove_border_bg(img: Image.Image, tol: int = 34) -> Image.Image:
    rgba = img.convert("RGBA")
    w, h = rgba.size
    px = rgba.load()
    corners = [px[0, 0][:3], px[w - 1, 0][:3], px[0, h - 1][:3], px[w - 1, h - 1][:3]]
    bg = tuple(sum(c[i] for c in corners) // 4 for i in range(3))
    visited = bytearray(w * h)
    q = deque([(x, 0) for x in range(w)] + [(x, h - 1) for x in range(w)] +
              [(0, y) for y in range(h)] + [(w - 1, y) for y in range(h)])
    while q:
        x, y = q.popleft()
        idx = y * w + x
        c = px[x, y]
        if visited[idx] or max(abs(c[0] - bg[0]), abs(c[1] - bg[1]), abs(c[2] - bg[2])) > tol:
            continue
        visited[idx] = 1
        px[x, y] = (0, 0, 0, 0)
        for nx, ny in ((x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)):
            if 0 <= nx < w and 0 <= ny < h and not visited[ny * w + nx]:
                q.append((nx, ny))
    bbox = rgba.getbbox()
    return rgba.crop(bbox) if bbox else rgba


def save_icon(crop: Image.Image, name: str, size: int = 64):
    crop.thumbnail((size, size), Image.Resampling.LANCZOS)
    canvas = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    canvas.paste(crop, ((size - crop.width) // 2, (size - crop.height) // 2), crop)
    canvas.save(ICONS_DIR / f"{name}.png")


def main():
    ICONS_DIR.mkdir(parents=True, exist_ok=True)
    PANELS_DIR.mkdir(parents=True, exist_ok=True)

    s1 = Image.open(SRC / "media_1794796420174_737c8e2d.jpg")
    xs1, ys1 = [75, 215, 360, 505, 650, 795, 955], [78, 200, 322, 445, 568, 695]
    for (r, c), name in {
        (0, 0): "gift", (0, 2): "soda", (0, 4): "coin", (1, 0): "intelligence",
        (1, 3): "energy", (1, 4): "cash", (2, 1): "stress", (2, 2): "people",
        (2, 3): "time", (2, 4): "trophy", (3, 5): "appeal", (4, 3): "calendar", (4, 4): "shop",
    }.items():
        save_icon(remove_border_bg(s1.crop((xs1[c], ys1[r], xs1[c + 1], ys1[r + 1])), 38), name)

    s2 = Image.open(SRC / "media_1794796420182_e6b941c8.jpg")
    xs2, ys2 = [45, 190, 330, 470], [45, 185, 320, 455, 590, 725, 860, 995]
    for (r, c), name in {(3, 0): "map", (3, 1): "education", (3, 2): "target", (4, 2): "bag", (5, 0): "home"}.items():
        save_icon(remove_border_bg(s2.crop((xs2[c], ys2[r], xs2[c + 1], ys2[r + 1])), 36), name)

    s3 = Image.open(SRC / "media_1794796420174_4972bc1a.jpg")
    for name, box, tw in (("stone_banner", (205, 18, 452, 92), 620), ("stone_panel", (200, 92, 470, 298), 860)):
        p = remove_border_bg(s3.crop(box), 24)
        p.resize((tw, int(p.height * (tw / p.width))), Image.Resampling.LANCZOS).save(PANELS_DIR / f"{name}.png")

    s4 = Image.open(SRC / "media_1794796420187_594f60c8.jpg")
    for name, box in (("parchment_wide", (135, 390, 545, 718)), ("parchment_card", (590, 405, 895, 715))):
        remove_border_bg(s4.crop(box), 28).save(PANELS_DIR / f"{name}.png")


if __name__ == "__main__":
    main()
