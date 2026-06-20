#!/usr/bin/env python3
"""Extract base64 images from index.html, save as WebP, replace src attributes."""

import re
import base64
import io
import os
from PIL import Image

HTML_FILE = "index.html"
IMAGES_DIR = "images"

os.makedirs(IMAGES_DIR, exist_ok=True)

with open(HTML_FILE, "r", encoding="utf-8") as f:
    html = f.read()

# Find all <img> tags with base64 src (not link/favicon tags — those are handled by Step 4)
# Pattern: match full <img ...> tag, capture base64 data and preserve all other attributes
IMG_PATTERN = re.compile(
    r'(<img\s)((?:[^>]*?\s)?)(src="data:image/(?P<fmt>jpeg|jpg|png|webp|gif);base64,(?P<data>[A-Za-z0-9+/=]+)")((?:\s[^>]*?)?)(\s*/>|>)',
    re.DOTALL | re.IGNORECASE,
)

counter = 1
replacements = 0

def replace_img(m):
    global counter
    fmt = m.group("fmt").lower()
    b64data = m.group("data")

    raw = base64.b64decode(b64data)
    img = Image.open(io.BytesIO(raw)).convert("RGBA")

    filename = f"img-{counter:03d}.webp"
    filepath = os.path.join(IMAGES_DIR, filename)
    img.save(filepath, "WEBP", quality=85)
    w, h = img.size
    print(f"  Saved {filename} ({w}x{h})")

    counter += 1

    # Reconstruct tag: replace only the src value, keep all other attributes
    prefix = m.group(1)           # "<img "
    before_src = m.group(2)       # attributes before src
    after_src = m.group(6)        # attributes after src
    close = m.group(7)            # "/>" or ">"

    new_src = f'src="{IMAGES_DIR}/{filename}"'
    return f"{prefix}{before_src}{new_src}{after_src}{close}"

new_html, n = IMG_PATTERN.subn(replace_img, html)
print(f"\nReplaced {n} <img> base64 src(s).")

with open(HTML_FILE, "w", encoding="utf-8") as f:
    f.write(new_html)

print("Done. index.html updated.")
