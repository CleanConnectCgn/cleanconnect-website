#!/usr/bin/env python3
"""Add loading=lazy, fetchpriority=high, width/height to img tags."""

import re
from PIL import Image

HTML_FILE = "index.html"

# Known dimensions for images missing width/height
DIMS = {
    "images/img-001.webp": (500, 500),
    "images/img-002.webp": (500, 500),
    "images/img-003.webp": (667, 651),
    "images/img-004.webp": (500, 500),
    "images/img_08.webp":  (800, 449),
}

with open(HTML_FILE, "r", encoding="utf-8") as f:
    html = f.read()

# Find all <img ...> tags (single-line or multi-line)
IMG_RE = re.compile(r'<img\s[^>]*>', re.DOTALL | re.IGNORECASE)

first_img = True

def process_img(m):
    global first_img
    tag = m.group(0)

    # Extract src value
    src_m = re.search(r'src="([^"]*)"', tag, re.IGNORECASE)
    src = src_m.group(1) if src_m else ""

    # --- width/height ---
    has_width  = bool(re.search(r'\bwidth=', tag, re.IGNORECASE))
    has_height = bool(re.search(r'\bheight=', tag, re.IGNORECASE))
    if not (has_width and has_height) and src in DIMS:
        w, h = DIMS[src]
        if not has_width:
            tag = re.sub(r'(<img\s)', rf'\1width="{w}" ', tag, count=1, flags=re.IGNORECASE)
        if not has_height:
            tag = re.sub(r'(<img\s)', rf'\1height="{h}" ', tag, count=1, flags=re.IGNORECASE)

    # --- loading / fetchpriority ---
    has_loading = bool(re.search(r'\bloading=', tag, re.IGNORECASE))
    has_fetchpri = bool(re.search(r'\bfetchpriority=', tag, re.IGNORECASE))

    if first_img:
        first_img = False
        # Hero: add fetchpriority="high", do NOT add loading=lazy
        if not has_fetchpri:
            tag = re.sub(r'(<img\s)', r'\1fetchpriority="high" ', tag, count=1, flags=re.IGNORECASE)
        # Remove loading=lazy if somehow present on hero
        if has_loading:
            tag = re.sub(r'\s*loading="[^"]*"', '', tag, flags=re.IGNORECASE)
    else:
        # All other imgs: add loading=lazy
        if not has_loading:
            tag = re.sub(r'(<img\s)', r'\1loading="lazy" ', tag, count=1, flags=re.IGNORECASE)

    return tag

new_html = IMG_RE.sub(process_img, html)

with open(HTML_FILE, "w", encoding="utf-8") as f:
    f.write(new_html)

print("Done. Lazy loading and dimensions applied.")
