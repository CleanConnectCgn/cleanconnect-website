#!/usr/bin/env python3
"""Schreibt Titel, Beschreibung, Urheber und Copyright (XMP) in alle WebP-Bilder der Website.

Ohne neue Komprimierung (nur webpmux). Titel kommen aus scripts/standorte/bilder.py und
praxis.py, dazu die festen Titel unten. Nach jedem neuen oder umbenannten Bild laufen lassen:

    python3 scripts/bild_metadaten.py

Braucht webpmux (macOS: brew install webp). Neue Bilder vorher mit
`cwebp -metadata none` erzeugen, damit keine Kamera- oder GPS-Daten mitkommen.
"""
import os
os.chdir(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
import sys, os, subprocess, tempfile, html, glob
sys.path.insert(0, "scripts/standorte")
from bilder import BILDER
from praxis import PRAXIS
FIRMA = "Clean Connect Gebäudereinigung UG (haftungsbeschränkt)"
titel = dict(BILDER)
titel.update({
 "gebaeudereinigung-koeln-clean-connect-showroom": "Mitarbeiter von Clean Connect im Firmen-Shirt im Showroom von Harley-Davidson Köln-Bonn",
 "fynn-laubkermeier-geschaeftsfuehrer-clean-connect": "Fynn Laubkermeier, Geschäftsführer von Clean Connect Gebäudereinigung in Köln",
 "clean-connect-logo": "Logo von Clean Connect Gebäudereinigung Köln",
 "clean-connect-logo-96": "Logo von Clean Connect Gebäudereinigung Köln",
})
ART = {"vorher": "Vorher", "nachher": "Nachher", "einsatz": "Im Einsatz"}
for f in PRAXIS:
    for datei, k in (f.get("bilder") or [(f["vorher"], "vorher"), (f["nachher"], "nachher")]):
        titel["praxis/" + datei[:-5]] = f"{f['leistung']}, {ART[k]}: {f['bildtext']}"
def xmp(t):
    t = html.escape(t)
    return f'''<?xpacket begin="﻿" id="W5M0MpCehiHzreSzNTczkc9d"?>
<x:xmpmeta xmlns:x="adobe:ns:meta/"><rdf:RDF xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
<rdf:Description rdf:about="" xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:photoshop="http://ns.adobe.com/photoshop/1.0/">
<dc:title><rdf:Alt><rdf:li xml:lang="x-default">{t}</rdf:li></rdf:Alt></dc:title>
<dc:description><rdf:Alt><rdf:li xml:lang="x-default">{t}</rdf:li></rdf:Alt></dc:description>
<dc:creator><rdf:Seq><rdf:li>{html.escape(FIRMA)}</rdf:li></rdf:Seq></dc:creator>
<dc:rights><rdf:Alt><rdf:li xml:lang="x-default">© {html.escape(FIRMA)}</rdf:li></rdf:Alt></dc:rights>
<photoshop:Credit>Clean Connect Gebäudereinigung Köln</photoshop:Credit>
</rdf:Description></rdf:RDF></x:xmpmeta>
<?xpacket end="w"?>'''
ok = fehlt = 0
for p in sorted(glob.glob("images/*.webp") + glob.glob("images/praxis/*.webp")):
    key = p[len("images/"):-5]
    basis = key[:-4] if key.endswith("-560") else key
    if basis not in titel:
        print("ohne Titel (bleibt):", p); fehlt += 1; continue
    with tempfile.NamedTemporaryFile("w", suffix=".xmp", delete=False, encoding="utf-8") as tf:
        tf.write(xmp(titel[basis])); tmp = tf.name
    ziel = p + ".neu"
    subprocess.run(["webpmux", "-set", "xmp", tmp, p, "-o", ziel], check=True, capture_output=True)
    os.replace(ziel, p); os.remove(tmp); ok += 1
print("mit Metadaten:", ok, "| ohne:", fehlt)
