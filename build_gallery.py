#!/usr/bin/env python3
"""
GALLERY REBUILD COMMAND
-----------------------
Run from this folder after changing files inside images/:
python3 build_gallery.py

The script collapses resolution copies, selects an approximately 1200px version,
and writes the categorized lazy-loading manifest to gallery-data.js.
"""

from __future__ import annotations

import json
import re
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).parent
IMAGE_DIR = ROOT / "images"
OUTPUT = ROOT / "gallery-data.js"
VALID_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp"}

# Visual classification of the existing Vistoriz collection. Each number is the
# position of a distinct, alphabetically sorted source photograph in the archive.
CATEGORY_INDEXES = {
    "portfolio": [7, 17, 20, 45, 49, 56, 81, 88, 101, 108, 112, 119],
    "headshots": [0, 2, 4, 6, 8, 10, 16, 32, 33, 36, 39, 43, 46, 51, 70, 73, 86, 95, 97, 104, 114],
    "portraits": [22, 57, 63, 68, 84, 93, 94, 98, 103, 107],
    "family": [11, 28, 40, 47, 77, 91, 116],
    "matrimonial": [12, 19, 55, 89, 111, 118],
    "couples": [18, 48, 58, 76, 90, 110, 115],
    "maternity": [13, 24, 26, 27, 37, 41, 42, 59, 64, 65, 67, 69, 72, 74, 75, 80, 99, 105, 106, 117],
    "baby": [1, 3, 5, 9, 14, 15, 23, 25, 29, 30, 31, 34, 35, 38, 62, 66, 79, 82, 87, 92, 96, 102, 109, 113],
}

# Logos and unusable low-resolution Wix placeholders are not photographs.
EXCLUDED_INDEXES = {21, 44, 50, 52, 53, 54, 60, 61, 71, 78, 83, 85, 100}

ALT_TEXT = {
    "portfolio": "Creative portfolio photograph",
    "headshots": "Professional headshot",
    "portraits": "Artistic studio portrait",
    "family": "Family studio photograph",
    "matrimonial": "Matrimonial profile photograph",
    "couples": "Couple portrait",
    "maternity": "Maternity portrait",
    "baby": "Baby and child portrait",
}


def group_key(path: Path) -> str:
    return re.sub(r"_\d+(?=\.[^.]+$)", "", path.name)


def image_details(path: Path) -> tuple[int, int]:
    with Image.open(path) as image:
        return image.size


def choose_representative(paths: list[Path]) -> tuple[Path, int, int]:
    candidates = []
    for path in paths:
        width, height = image_details(path)
        longest = max(width, height)
        # Prefer a fast web-sized copy close to 1200px, then the larger copy.
        candidates.append((abs(longest - 1200), -(width * height), path, width, height))
    _, _, path, width, height = min(candidates)
    return path, width, height


def inventory() -> list[tuple[Path, int, int]]:
    groups: dict[str, list[Path]] = {}
    for path in sorted(IMAGE_DIR.iterdir()):
        if path.is_file() and path.suffix.lower() in VALID_EXTENSIONS:
            if "logo" in path.name.lower() or "sloppyframe" in path.name.lower():
                continue
            groups.setdefault(group_key(path), []).append(path)
    return [choose_representative(groups[key]) for key in sorted(groups)]


def main() -> None:
    photos = inventory()
    assigned = {index for indexes in CATEGORY_INDEXES.values() for index in indexes}
    expected = set(range(len(photos))) - EXCLUDED_INDEXES
    if assigned != expected:
        missing = sorted(expected - assigned)
        extra = sorted(assigned - expected)
        raise SystemExit(f"Gallery classification needs review. Missing={missing}; extra={extra}")

    gallery: dict[str, list[dict[str, object]]] = {}
    for category, indexes in CATEGORY_INDEXES.items():
        gallery[category] = []
        for position, index in enumerate(indexes, start=1):
            path, width, height = photos[index]
            gallery[category].append({
                "src": f"images/{path.name}",
                "width": width,
                "height": height,
                "alt": f"{ALT_TEXT[category]} {position}",
            })

    total = sum(map(len, gallery.values()))
    output = "window.GALLERY_DATA = " + json.dumps(gallery, ensure_ascii=False, indent=2) + ";\n"
    OUTPUT.write_text(output, encoding="utf-8")
    print(f"Generated {OUTPUT.name} with {total} photographs across {len(gallery)} categories.")


if __name__ == "__main__":
    main()
