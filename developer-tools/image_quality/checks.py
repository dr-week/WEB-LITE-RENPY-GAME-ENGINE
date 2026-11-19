"""Lightweight PIL-based visual quality inspection for scene and CG artwork."""

from pathlib import Path
from PIL import Image, ImageFilter, ImageStat

IMAGE_EXTS = {".png", ".jpg", ".jpeg", ".webp", ".bmp"}


def inspect_image(path: Path) -> dict:
    """Inspect a single image for readability, dimensions, exposure, contrast, and sharpness."""
    try:
        with Image.open(path) as img:
            img.verify()
        with Image.open(path) as img:
            rgb = img.convert("RGB")
            width, height = rgb.size
            gray = rgb.convert("L")
            stat = ImageStat.Stat(gray)
            brightness = round(stat.mean[0], 2)
            contrast = round(stat.stddev[0], 2)
            edges = gray.filter(ImageFilter.FIND_EDGES)
            sharpness = round(ImageStat.Stat(edges).mean[0], 2)
    except Exception as exc:
        return _fail_result(f"corrupt_or_unreadable: {exc}")

    aspect = round(width / height, 3) if height else 0.0
    flags = _evaluate_flags(width, height, aspect, brightness, contrast, sharpness)
    score = _compute_score(flags, width, height, contrast, sharpness)
    status = "fail" if any(f.startswith("critical_") for f in flags) else ("warn" if flags else "pass")
    return {
        "ok": status != "fail",
        "status": status,
        "width": width,
        "height": height,
        "aspect_ratio": aspect,
        "brightness": brightness,
        "contrast": contrast,
        "sharpness": sharpness,
        "quality_score": score,
        "flags": flags,
    }


def inspect_directory(directory: Path) -> list[tuple[Path, dict]]:
    """Inspect all images in a directory recursively."""
    results = []
    for path in sorted(directory.rglob("*")):
        if path.is_file() and path.suffix.lower() in IMAGE_EXTS:
            results.append((path, inspect_image(path)))
    return results


def _evaluate_flags(width, height, aspect, brightness, contrast, sharpness) -> list[str]:
    flags = []
    if width < 256 or height < 256:
        flags.append("critical_too_small")
    elif width < 640 or height < 360:
        flags.append("low_resolution")
    if aspect < 1.2 or aspect > 2.2:
        flags.append("unusual_aspect_ratio")
    if brightness < 18:
        flags.append("too_dark")
    elif brightness > 245:
        flags.append("overexposed")
    if contrast < 12:
        flags.append("low_contrast_or_blank")
    if sharpness < 4.0:
        flags.append("blurry_or_low_detail")
    return flags


def _compute_score(flags, width, height, contrast, sharpness) -> int:
    score = 100
    for flag in flags:
        score -= 45 if flag.startswith("critical_") else 15
    if width >= 1280 and height >= 720:
        score = min(100, score + 5)
    if contrast < 20:
        score -= 5
    if sharpness < 6.0:
        score -= 5
    return max(0, min(100, score))


def _fail_result(reason: str) -> dict:
    return {
        "ok": False,
        "status": "fail",
        "width": 0,
        "height": 0,
        "aspect_ratio": 0.0,
        "brightness": 0.0,
        "contrast": 0.0,
        "sharpness": 0.0,
        "quality_score": 0,
        "flags": [f"critical_{reason}"],
    }
