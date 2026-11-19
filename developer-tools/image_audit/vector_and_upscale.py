"""
Vector Icon & Background Upscaler Pipeline.
Converts raster PNG icons to SVG vectors and applies lightweight Lanczos upscaling.
"""
import glob
import os
import cv2
import numpy as np
from PIL import Image

def convert_icons_to_svg(src_dir="game/images/ui/icons", dst_dir="game/images/ui/svg_icons"):
    os.makedirs(dst_dir, exist_ok=True)
    icons = glob.glob(os.path.join(src_dir, "*.png"))
    converted = 0
    for ic in icons:
        img = cv2.imread(ic, cv2.IMREAD_UNCHANGED)
        if img is None:
            continue
        h, w = img.shape[:2]
        if img.shape[2] == 4:
            alpha = img[:, :, 3]
            color = img[:, :, :3]
            mask = alpha > 20
            if np.any(mask):
                avg_bgr = color[mask].mean(axis=0)
                hex_color = f"#{int(avg_bgr[2]):02x}{int(avg_bgr[1]):02x}{int(avg_bgr[0]):02x}"
            else:
                hex_color = "#ffffff"
            bin_img = (alpha > 80).astype(np.uint8) * 255
        else:
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            bin_img = (gray > 128).astype(np.uint8) * 255
            hex_color = "#ffffff"

        contours, _ = cv2.findContours(bin_img, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        svg_lines = [
            f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}">',
            f'  <g fill="{hex_color}" stroke="none">'
        ]
        for cnt in contours:
            if cv2.contourArea(cnt) < 4:
                continue
            epsilon = 0.005 * cv2.arcLength(cnt, True)
            approx = cv2.approxPolyDP(cnt, epsilon, True)
            pts = approx.reshape(-1, 2)
            if len(pts) < 3:
                continue
            path_str = f"M {pts[0][0]} {pts[0][1]} " + " ".join([f"L {p[0]} {p[1]}" for p in pts[1:]]) + " Z"
            svg_lines.append(f'    <path d="{path_str}" fill-rule="evenodd"/>')
        svg_lines.append("  </g>\n</svg>")

        dst_file = os.path.join(dst_dir, os.path.splitext(os.path.basename(ic))[0] + ".svg")
        with open(dst_file, "w", encoding="utf-8") as f:
            f.write("\n".join(svg_lines))
        converted += 1
    return converted

def upscale_background_lanczos(image_path, target_width=1920, target_height=1080):
    """Lightweight high-fidelity upscaler using Lanczos resampling."""
    with Image.open(image_path) as im:
        w, h = im.size
        if w >= target_width and h >= target_height:
            return False
        scale = max(target_width / w, target_height / h)
        new_size = (int(w * scale), int(h * scale))
        upscaled = im.resize(new_size, Image.Resampling.LANCZOS)
        # Center crop to exact 1920x1080
        left = (new_size[0] - target_width) // 2
        top = (new_size[1] - target_height) // 2
        cropped = upscaled.crop((left, top, left + target_width, top + target_height))
        cropped.save(image_path, quality=95)
        return True
