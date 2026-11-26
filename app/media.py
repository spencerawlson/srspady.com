"""srspady.com admin — image derivatives with Pillow.

Filters are applied to a DERIVED copy only. The original upload in
data/media/originals/ is never modified. Derivatives are saved with NO
EXIF data at all — which strips GPS and everything else with it.
Supported: warm, cool, black-and-white, faded, high-contrast, plus crop
(fractions of width/height) and rotate (degrees, expand).
"""
from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageEnhance

FILTERS = ["warm", "cool", "black-and-white", "faded", "high-contrast", "none"]
IMAGE_EXTS = {".jpg", ".jpeg", ".png", ".webp", ".gif"}
VIDEO_EXTS = {".mp4", ".webm", ".mov"}
ALLOWED_EXTS = IMAGE_EXTS | VIDEO_EXTS


def is_image(path: Path) -> bool:
    return path.suffix.lower() in IMAGE_EXTS


def apply_filter(img: Image.Image, name: str) -> Image.Image:
    img = img.convert("RGB")
    if name == "warm":
        r, g, b = img.split()
        r = r.point(lambda v: min(255, int(v * 1.08)))
        b = b.point(lambda v: int(v * 0.92))
        return Image.merge("RGB", (r, g, b))
    if name == "cool":
        r, g, b = img.split()
        b = b.point(lambda v: min(255, int(v * 1.08)))
        r = r.point(lambda v: int(v * 0.92))
        return Image.merge("RGB", (r, g, b))
    if name == "black-and-white":
        return img.convert("L").convert("RGB")
    if name == "faded":
        img = ImageEnhance.Contrast(img).enhance(0.75)
        img = ImageEnhance.Brightness(img).enhance(1.08)
        return ImageEnhance.Color(img).enhance(0.8)
    if name == "high-contrast":
        img = ImageEnhance.Contrast(img).enhance(1.6)
        return ImageEnhance.Sharpness(img).enhance(1.3)
    return img


def derive_image(src: Path, dest: Path, filter_name: str = "none",
                 crop: tuple[float, float, float, float] | None = None,
                 rotate: float = 0.0) -> Path:
    """Build a derivative from src. Never touches src. No EXIF is written."""
    with Image.open(src) as img:
        img = img.convert("RGB")
        if crop:
            w, h = img.size
            x, y, cw, ch = crop
            box = (int(x * w), int(y * h), int((x + cw) * w), int((y + ch) * h))
            img = img.crop(box)
        if rotate:
            img = img.rotate(-rotate, expand=True)
        img = apply_filter(img, filter_name)
        dest.parent.mkdir(parents=True, exist_ok=True)
        img.save(dest, quality=88)  # no exif= argument: EXIF (incl. GPS) is dropped
    return dest
