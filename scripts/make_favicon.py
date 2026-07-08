#!/usr/bin/env python3
"""Remove cream background from house logo and generate favicon set.

Usage:
    python3 scripts/make_favicon.py <path_to_source_png>
"""
import json
import os
import sys

from PIL import Image, ImageFilter

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(BASE, 'static', 'images', 'favicon')

APPLE_BG = (242, 236, 227)  # --color-surface
# Source logo cream: ~#F2EDE7
CREAM_REF = (242, 237, 231)


def _is_cream(r, g, b, threshold=28):
    return (
        abs(r - CREAM_REF[0]) <= threshold
        and abs(g - CREAM_REF[1]) <= threshold
        and abs(b - CREAM_REF[2]) <= threshold
        and r > 200
        and g > 200
        and b > 190
    )


def remove_cream_background(src_path):
    img = Image.open(src_path).convert('RGBA')
    pixels = list(img.getdata())
    out = []
    for r, g, b, a in pixels:
        if _is_cream(r, g, b):
            out.append((r, g, b, 0))
        else:
            out.append((r, g, b, a if a else 255))
    result = Image.new('RGBA', img.size)
    result.putdata(out)
    alpha = result.split()[3].filter(ImageFilter.GaussianBlur(0.4))
    result.putalpha(alpha)
    return result


def crop_to_content(img, pad_ratio=0.08):
    bbox = img.split()[3].getbbox()
    if not bbox:
        return img
    img = img.crop(bbox)
    w, h = img.size
    side = max(w, h)
    pad = int(side * pad_ratio)
    canvas = side + pad * 2
    square = Image.new('RGBA', (canvas, canvas), (0, 0, 0, 0))
    square.paste(img, ((canvas - w) // 2, (canvas - h) // 2), img)
    return square


def save_png(img, name, size, background=None):
    resized = img.resize((size, size), Image.LANCZOS)
    if background is not None:
        bg = Image.new('RGBA', (size, size), background + (255,))
        bg.paste(resized, (0, 0), resized)
        resized = bg.convert('RGB')
    path = os.path.join(OUT, name)
    resized.save(path, optimize=True)
    print('saved', name)


def main():
    if len(sys.argv) < 2:
        print('usage: python3 scripts/make_favicon.py <source.png>')
        sys.exit(1)

    os.makedirs(OUT, exist_ok=True)

    cleaned = remove_cream_background(sys.argv[1])
    icon = crop_to_content(cleaned)

    icon.resize((512, 512), Image.LANCZOS).save(
        os.path.join(OUT, 'icon.png'), optimize=True,
    )
    print('saved icon.png (512, transparent master)')

    save_png(icon, 'favicon-16x16.png', 16)
    save_png(icon, 'favicon-32x32.png', 32)
    save_png(icon, 'android-chrome-192x192.png', 192)
    save_png(icon, 'android-chrome-512x512.png', 512)
    save_png(icon, 'apple-touch-icon.png', 180, background=APPLE_BG)

    ico_sizes = [(16, 16), (32, 32), (48, 48), (64, 64)]
    icon.save(os.path.join(OUT, 'favicon.ico'), sizes=ico_sizes)
    print('saved favicon.ico', ico_sizes)

    manifest = {
        'name': 'Покрівля під ключ',
        'short_name': 'Покрівля',
        'icons': [
            {
                'src': '/static/images/favicon/android-chrome-192x192.png',
                'sizes': '192x192',
                'type': 'image/png',
            },
            {
                'src': '/static/images/favicon/android-chrome-512x512.png',
                'sizes': '512x512',
                'type': 'image/png',
            },
        ],
        'theme_color': '#8c5d28',
        'background_color': '#f2ece3',
        'display': 'standalone',
    }
    with open(os.path.join(OUT, 'site.webmanifest'), 'w', encoding='utf-8') as handle:
        json.dump(manifest, handle, ensure_ascii=False, indent=2)
    print('saved site.webmanifest')


if __name__ == '__main__':
    main()
