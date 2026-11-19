"""Generate modular 9-slice glassmorphism, shadow, and blend textures for Ren'Py UI."""

import json
from pathlib import Path
from PIL import Image, ImageDraw, ImageFilter

TOOLS_DIR = Path(__file__).resolve().parent
TOKENS_PATH = TOOLS_DIR / "ui_tokens.json"
ROOT = TOOLS_DIR.parent / "game" / "images" / "ui"


def make_glass(path, size, radius, pad, fill, rim, border, blur_r, shadow_a):
    w, h = size
    img = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    sh = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    ImageDraw.Draw(sh).rounded_rectangle([pad, pad + 3, w - pad, h - pad + 3], radius=radius, fill=(6, 8, 20, shadow_a))
    sh = sh.filter(ImageFilter.GaussianBlur(blur_r))
    img.alpha_composite(sh)

    panel = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(panel)
    d.rounded_rectangle([pad, pad, w - pad, h - pad], radius=radius, fill=tuple(fill), outline=tuple(border), width=1)
    d.rounded_rectangle([pad + 1, pad + 1, w - pad - 1, h - pad - 1], radius=max(2, radius - 1), outline=tuple(rim), width=1)
    img.alpha_composite(panel)
    path.parent.mkdir(parents=True, exist_ok=True)
    img.save(path)


def make_shadow(path, size, radius, pad, blur_r, alpha):
    w, h = size
    sh = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    ImageDraw.Draw(sh).rounded_rectangle([pad, pad + 4, w - pad, h - pad + 4], radius=radius, fill=(4, 6, 18, alpha))
    sh = sh.filter(ImageFilter.GaussianBlur(blur_r))
    path.parent.mkdir(parents=True, exist_ok=True)
    sh.save(path)


def make_effects():
    fx = ROOT / "effects"
    fx.mkdir(parents=True, exist_ok=True)
    sheen = Image.new("RGBA", (512, 256), (0, 0, 0, 0))
    d = ImageDraw.Draw(sheen)
    for y in range(256):
        a = int(max(0, 70 * (1 - y / 256.0) ** 2))
        d.line([(0, y), (511, y)], fill=(232, 213, 245, a))
    sheen.save(fx / "sheen_top.png")

    vig = Image.new("RGBA", (640, 360), (255, 255, 255, 255))
    dv = ImageDraw.Draw(vig)
    dv.ellipse([60, 30, 580, 330], fill=(255, 255, 255, 255))
    mask = Image.new("L", (640, 360), 110)
    ImageDraw.Draw(mask).ellipse([40, 20, 600, 340], fill=255)
    mask = mask.filter(ImageFilter.GaussianBlur(55))
    vig_out = Image.new("RGBA", (640, 360), (14, 16, 36, 255))
    vig_out.paste((255, 255, 255, 255), (0, 0), mask)
    vig_out.save(fx / "vignette_ambient.png")


def generate_from_tokens(tokens_path: Path = TOKENS_PATH) -> None:
    """Generate all glass, shadow, and effect PNGs defined in ui_tokens.json."""
    data = json.loads(tokens_path.read_text(encoding="utf-8"))
    surfaces = data.get("surfaces", {})
    for name, spec in surfaces.items():
        out_path = ROOT / spec["file"]
        if name.startswith("shadow_"):
            make_shadow(
                out_path,
                tuple(spec["size"]),
                spec["radius"],
                spec["pad"],
                spec["blur_r"],
                spec["alpha"],
            )
        else:
            make_glass(
                out_path,
                tuple(spec["size"]),
                spec["radius"],
                spec["pad"],
                spec["fill"],
                spec["rim"],
                spec["border"],
                spec["blur_r"],
                spec["shadow_a"],
            )
    make_effects()
    print(f"Generated {len(surfaces)} token surfaces + effects in {ROOT}")


def main():
    generate_from_tokens()


if __name__ == "__main__":
    main()
