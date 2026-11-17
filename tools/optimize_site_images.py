#!/usr/bin/env python3
"""Produce smaller WebP assets and update portfolio HTML without touching source PNGs.

Requires Pillow. Safe to rerun: only the intended local <img> sources are changed,
with original PNG files retained and existing links left untouched.
"""
from __future__ import annotations
import argparse
import json
import re
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "docs" / "assets"
DOCS = ROOT / "docs"
SPECS = (
    ("portrait.png", "portrait.webp", 83),
    ("solution-field-photo.png", "solution-field-photo.webp", 82),
    ("solution-web-responsive.png", "solution-web-responsive.webp", 82),
)
HTML_PAGES = ("index.html", "about.html", "gallery.html")


def get_asset_info():
    result = {}
    for original, optimized, _ in SPECS:
        source = ASSETS / original
        target = ASSETS / optimized
        if not source.exists():
            raise FileNotFoundError(source)
        with Image.open(source) as photo:
            original_dimensions = photo.size
        result[original] = {
            "original_bytes": source.stat().st_size,
            "optimized_bytes": target.stat().st_size if target.exists() else None,
            "dimensions": original_dimensions,
        }
    return result


def compress_images():
    for original, optimized, quality in SPECS:
        source = ASSETS / original
        if not source.exists():
            raise FileNotFoundError(source)
        with Image.open(source) as raw:
            raw.load()
            if raw.mode not in ("RGB", "RGBA"):
                raw = raw.convert("RGBA" if "A" in raw.getbands() else "RGB")
            raw.save(ASSETS / optimized, "WEBP", quality=quality, method=6)
            if original == "portrait.png":
                if raw.width > 640:
                    thumb = raw.copy()
                    thumb.thumbnail((640, 10000), Image.Resampling.LANCZOS)
                    thumb.save(ASSETS / "portrait-640.webp", "WEBP", quality=80, method=6)


def update_html():
    original_to_optimized = {
        "assets/" + before: "assets/" + after
        for before, after, _ in SPECS
    }
    portrait_path = ASSETS / "portrait.png"
    with Image.open(portrait_path) as photo:
        original_width = photo.width
    has_small = (ASSETS / "portrait-640.webp").exists()
    small_width = min(640, original_width)
    tag_rx = re.compile(r"<img\b[^>]*>", re.IGNORECASE)

    def update_tag(match):
        tag = match.group(0)
        for old, new in original_to_optimized.items():
            if 'src="' + old + '"' not in tag:
                continue
            tag = tag.replace('src="' + old + '"', 'src="' + new + '"', 1)
            if old.endswith("portrait.png") and 'srcset=' not in tag and has_small:
                tag = tag[:-1] + (
                    ' srcset="assets/portrait-640.webp ' + str(small_width) +
                    'w, assets/portrait.webp ' + str(original_width) +
                    'w" sizes="(max-width:760px) 90vw, 500px">'
                )
            if 'decoding=' not in tag:
                tag = tag[:-1] + ' decoding="async">'
            return tag
        return tag

    for filename in HTML_PAGES:
        path = DOCS / filename
        raw = path.read_bytes()
        original_text = raw.decode("utf-8")
        updated_text = tag_rx.sub(update_tag, original_text)
        if updated_text != original_text:
            path.write_bytes(updated_text.encode("utf-8"))


def check():
    data = get_asset_info()
    for original, optimized, _ in SPECS:
        source = ASSETS / original
        target = ASSETS / optimized
        if not target.is_file():
            raise AssertionError("Missing optimized file: " + str(target))
        with Image.open(source) as old, Image.open(target) as new:
            if old.size != new.size:
                raise AssertionError("Original dimensions changed for " + optimized)
            new.verify()
        if target.stat().st_size >= source.stat().st_size:
            raise AssertionError("No size reduction for " + optimized)
    for page in HTML_PAGES:
        content = (DOCS / page).read_text(encoding="utf-8")
        for original, optimized, _ in SPECS:
            if page == "gallery.html" and original == "portrait.png":
                continue
            if page != "gallery.html" and original != "portrait.png":
                continue
            if 'src="assets/' + original + '"' in content:
                raise AssertionError("Old image source remains in " + page)
            if 'src="assets/' + optimized + '"' not in content:
                raise AssertionError("Missing image optimization in " + page)
    if not (ASSETS / "portrait-640.webp").is_file() and data["portrait.png"]["dimensions"][0] > 640:
        raise AssertionError("Missing responsive portrait image")
    print(json.dumps(data, indent=2))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    if args.check:
        check()
    else:
        compress_images()
        update_html()
        check()


if __name__ == "__main__":
    main()
