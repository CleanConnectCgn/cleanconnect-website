#!/usr/bin/env python3
"""Replace base64 favicon link tags with real file references."""
import re

HTML_FILE = "index.html"

with open(HTML_FILE, "r", encoding="utf-8") as f:
    html = f.read()

# Replace SVG base64 favicon (the generic CC logo)
html = re.sub(
    r'<link\s+rel="icon"\s+type="image/svg\+xml"\s+href="data:image/svg\+xml;base64,[A-Za-z0-9+/=]+"[^>]*>',
    '<link rel="icon" type="image/x-icon" href="favicon.ico">',
    html
)

# Replace PNG base64 favicon
html = re.sub(
    r'<link\s+rel="icon"\s+type="image/png"\s+href="data:image/png;base64,[A-Za-z0-9+/=]+"[^>]*>',
    '<link rel="icon" type="image/png" href="logo.png">',
    html
)

# Replace apple-touch-icon base64
html = re.sub(
    r'<link\s+rel="apple-touch-icon"\s+href="data:image/png;base64,[A-Za-z0-9+/=]+"[^>]*>',
    '<link rel="apple-touch-icon" href="logo.png">',
    html
)

with open(HTML_FILE, "w", encoding="utf-8") as f:
    f.write(html)

# Verify
remaining = len(re.findall(r'data:image', html))
print(f"Done. Remaining data:image references: {remaining}")
