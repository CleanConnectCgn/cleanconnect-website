#!/usr/bin/env python3
"""Erzeugt die Standortseiten standorte/<leistung>-<ort>.html (13.10.2026).

Aufruf (im Repo-Root):  python3 scripts/standorte/build.py
Danach:                 python3 scripts/standorte/aehnlichkeit.py   (Pruefung)

Jede Seite = Leistung x Ort. Damit die Seiten keine Kopien mit getauschtem
Ortsnamen sind (Google: Doorway Pages / Scaled Content Abuse), stammt der
groesste Teil des Textes aus den Ortsdaten (orte.py): Lage, Stadtteile,
Bebauung, Wirtschaft, Anfahrt, Satzung, Entsorger. Die Leistung bestimmt, WELCHE
Ortsthemen auf der Seite stehen und wie sie mit der Leistung verbunden werden.
Dazu kommen ein Rechner je Leistung und ortsbezogene FAQ.

Ausnahme: Buero-Reinigung Koeln hat mit /bueroreinigung-koeln.html bereits eine
eigene, ausgearbeitete Seite - dafuer wird keine Standortseite erzeugt.
"""
import html
import json
import math
import os
import re
import sys

sys.path.insert(0, os.path.dirname(__file__))
from orte import ORTE, ORT_REIHENFOLGE, BUERO  # noqa: E402
from leistungen import LEISTUNGEN, LEISTUNG_REIHENFOLGE  # noqa: E402
from extras import FAQ_EXTRA, VORTEILE_EXTRA, ZUSATZ_THEMEN  # noqa: E402
from fokus import FOKUS  # noqa: E402
from bilder import BILDER  # noqa: E402
from ratgeber import RATGEBER  # noqa: E402

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
OUT = os.path.join(ROOT, "standorte")
BASE = "https://cleanconnect.de"
AUSNAHMEN = {("bueroreinigung", "koeln"): "../bueroreinigung-koeln.html"}

e = html.escape


def km(a, b):
    r = 6371
    p1, p2 = math.radians(a[0]), math.radians(b[0])
    dp, dl = p2 - p1, math.radians(b[1] - a[1])
    x = math.sin(dp / 2) ** 2 + math.cos(p1) * math.cos(p2) * math.sin(dl / 2) ** 2
    return 2 * r * math.asin(math.sqrt(x))


def url(leistung, ort):
    if (leistung, ort) in AUSNAHMEN:
        return AUSNAHMEN[(leistung, ort)]
    return f"{leistung}-{ort}.html"


def nachbarn(ort, n=3):
    g = ORTE[ort]["geo"]
    andere = [o for o in ORT_REIHENFOLGE if o != ort]
    return sorted(andere, key=lambda o: km(g, ORTE[o]["geo"]))[:n]


def auswahl(liste, start, n):
    """n Elemente ab Position start (rotierend) - jede Leistung zeigt andere Stadtteile zuerst."""
    return [liste[(start + i) % len(liste)] for i in range(min(n, len(liste)))]


def aufzaehlung(xs):
    return xs[0] if len(xs) == 1 else ", ".join(xs[:-1]) + " und " + xs[-1]


ICON = {
    "ort": '<path d="M12 21s-7-6.2-7-11a7 7 0 0 1 14 0c0 4.8-7 11-7 11z"/><circle cx="12" cy="10" r="2.5"/>',
    "uhr": '<circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/>',
    "euro": '<path d="M17 6.5A6.5 6.5 0 1 0 17 17.5"/><path d="M5 10h8M5 14h8"/>',
    "haken": '<path d="M5 12.5l4.5 4.5L19 7.5"/>',
}


def svg(name, size=18):
    return (f'<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="currentColor" '
            f'stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{ICON[name]}</svg>')


def entfernungs_grafik(ort):
    """Kleine Grafik: Ort im Verhaeltnis zu unserem Buero (Luftlinie)."""
    o = ORTE[ort]
    if ort == "koeln":
        return ('<div class="dist"><svg viewBox="0 0 120 120" aria-hidden="true"><circle cx="60" cy="60" r="52" class="r1"/>'
                '<circle cx="60" cy="60" r="30" class="r2"/><circle cx="60" cy="60" r="7" class="pt"/></svg>'
                '<div><b>Heimatstandort</b><span>Büro in Köln-Rath/Heumar</span></div></div>')
    d = km(BUERO, o["geo"])
    # Richtung als Winkel fuer den Punkt auf dem Ring
    dy, dx = o["geo"][0] - BUERO[0], (o["geo"][1] - BUERO[1]) * math.cos(math.radians(BUERO[0]))
    w = math.atan2(dy, dx)
    rad = 18 + min(d, 40) / 40 * 34
    x, y = 60 + rad * math.cos(w), 60 - rad * math.sin(w)
    return (f'<div class="dist"><svg viewBox="0 0 120 120" aria-hidden="true"><circle cx="60" cy="60" r="52" class="r1"/>'
            f'<circle cx="60" cy="60" r="30" class="r2"/><line x1="60" y1="60" x2="{x:.1f}" y2="{y:.1f}" class="ln"/>'
            f'<circle cx="60" cy="60" r="5" class="hq"/><circle cx="{x:.1f}" cy="{y:.1f}" r="7" class="pt"/></svg>'
            f'<div><b>rund {round(d)} km</b><span>Luftlinie von unserem Büro in Köln-Rath/Heumar</span></div></div>')


_BLOG_TITEL = {}


def blog_titel(slug):
    """H1 eines veroeffentlichten Artikels, None solange er nur als Entwurf existiert."""
    if slug not in _BLOG_TITEL:
        p = os.path.join(ROOT, "blog", f"{slug}.html")
        m = re.search(r"<h1[^>]*>(.*?)</h1>", open(p, encoding="utf-8").read(), re.S) if os.path.exists(p) else None
        _BLOG_TITEL[slug] = html.unescape(re.sub(r"<[^>]+>", "", m.group(1)).strip()) if m else None
    return _BLOG_TITEL[slug]


def ratgeber(lk, ort, n=3):
    """Bis zu n veroeffentlichte Artikel zur Leistung, je Ort rotierend; Koeln-Artikel nur auf Koelner Seiten."""
    treffer = []
    for slug in RATGEBER.get(lk, []):
        if "-koeln" in slug and ort != "koeln":
            continue
        t = blog_titel(slug)
        if t:
            treffer.append((slug, t))
    return auswahl(treffer, ORT_REIHENFOLGE.index(ort), n) if treffer else []


def lokale_faq(lk, ort, li_index):
    o, l = ORTE[ort], LEISTUNGEN[lk]
    st = auswahl(o["stadtteile"], li_index * 2, 4)
    faq = [(
        f"Sind Sie für {l['name']} auch in {aufzaehlung(st[:3])} im Einsatz?",
        f"Ja. {l['name']} bieten wir im ganzen Stadtgebiet von {o['name']} an, auch in {aufzaehlung(st)}. {o['anfahrt']}",
    )]
    if lk == "winterdienst":
        faq.append((f"Welche Regeln gelten für den Winterdienst {o['in']}?",
                    f"{o['winter_satzung']} Mit dem Winterdienstvertrag übernehmen wir die Räum- und Streupflicht für die vereinbarte Fläche und dokumentieren jeden Einsatz."))
    elif lk == "entruempelung":
        faq.append((f"Wohin kommen die Sachen aus einer Entrümpelung {o['in']}?",
                    f"Wir trennen nach Holz, Metall, Elektrogeräten, Papier und Restmüll und bringen alles zu zugelassenen Annahmestellen. {o['sperrmuell']} Reicht Ihnen diese Abholung, sagen wir Ihnen das ehrlich."))
    elif ort == "koeln":
        faq.append(("Wie schnell können Sie in Köln anfangen?",
                    "Da wir selbst in Köln-Rath/Heumar sitzen, ist eine Besichtigung meist innerhalb weniger Tage möglich. Den Start legen wir danach gemeinsam fest, bei Bedarf auch kurzfristig."))
    else:
        d = round(km(BUERO, o["geo"]))
        faq.append((f"Wie schnell können Sie {o['in']} anfangen?",
                    f"{o['name']} liegt rund {d} km Luftlinie von unserem Büro in Köln-Rath/Heumar entfernt. Eine Besichtigung ist meist innerhalb weniger Tage möglich, die Anfahrt ist im Preis enthalten."))
    return faq


CSS_EXTRA = """
.facts{display:grid;grid-template-columns:repeat(3,1fr);gap:12px;margin-top:22px}
@media(max-width:700px){.facts{grid-template-columns:1fr}}
.fact{background:var(--s1);border:1px solid var(--br);border-radius:14px;padding:14px 16px;display:flex;gap:12px;align-items:center}
.fact svg{color:var(--teal);flex-shrink:0}
.fact b{display:block;color:#fff;font-size:14px}
.fact span{font-size:12.5px;color:var(--mu2)}
.dist{display:flex;gap:14px;align-items:center}
.dist svg{width:84px;height:84px;flex-shrink:0}
.dist .r1{fill:none;stroke:var(--br2);stroke-dasharray:3 4}
.dist .r2{fill:var(--td);stroke:var(--br2)}
.dist .ln{stroke:var(--teal);stroke-width:1.5;stroke-dasharray:4 3}
.dist .hq{fill:#fff}
.dist .pt{fill:var(--teal)}
.dist b{display:block;color:#fff;font-size:16px}
.dist span{font-size:12.5px;color:var(--mu2)}
.lokal p{font-size:15px;color:var(--mu2);margin-bottom:14px}
.lokal p strong{color:#fff;font-weight:600}
.chips{display:flex;flex-wrap:wrap;gap:8px;margin:14px 0}
.chips span{font-size:12.5px;color:var(--mu2);border:1px solid var(--br2);padding:6px 12px;border-radius:100px;background:var(--s1)}
ol.steps{list-style:none;counter-reset:s;display:grid;gap:10px}
ol.steps li{counter-increment:s;position:relative;padding:12px 16px 12px 52px;background:var(--s1);border:1px solid var(--br);border-radius:12px;font-size:14px;color:var(--tx)}
ol.steps li::before{content:counter(s);position:absolute;left:14px;top:50%;transform:translateY(-50%);width:26px;height:26px;border-radius:50%;background:var(--tg);color:var(--teal);font-weight:800;font-size:13px;display:flex;align-items:center;justify-content:center}
.rechner{background:var(--s1);border:1px solid var(--br2);border-radius:16px;padding:22px}
.rechner h3{color:#fff;font-size:16px;margin-bottom:14px}
.rechner-form{display:grid;grid-template-columns:repeat(auto-fit,minmax(180px,1fr));gap:12px;margin-bottom:16px}
.rechner-form label{display:flex;flex-direction:column;gap:6px;font-size:12.5px;color:var(--mu2)}
.rechner-form input,.rechner-form select{background:var(--bg);color:var(--tx);border:1px solid var(--br2);border-radius:10px;padding:10px 12px;font:inherit;font-size:14px}
.rechner-out{display:grid;grid-template-columns:repeat(auto-fit,minmax(160px,1fr));gap:10px}
.rechner-out div{background:var(--td);border:1px solid var(--br2);border-radius:12px;padding:12px 14px}
.rechner-out span{display:block;font-size:12px;color:var(--mu2)}
.rechner-out b{color:#fff;font-size:17px}
.rechner-fuss{font-size:12.5px;color:var(--mu);margin-top:12px}
.preis{display:flex;gap:14px;align-items:flex-start}
.preis svg{color:var(--teal);margin-top:3px;flex-shrink:0}
.preis p{font-size:14.5px;color:var(--mu2)}
.preis a{color:var(--teal);font-weight:600}
.nachbar{margin-top:14px;font-size:13.5px;color:var(--mu2)}
.nachbar a{color:var(--teal)}
.kurz{background:var(--td);border:1px solid var(--br2);border-radius:16px;padding:20px 22px}
.kurz h2{font-size:15px;color:var(--teal);margin-bottom:8px}
.kurz p{font-size:15.5px;color:var(--tx);line-height:1.65}
.beispiel{margin-top:14px;font-size:14.5px;color:var(--mu2)}
.beispiel strong{color:#fff;font-weight:600}
"""


def lade_basis_css():
    """CSS der bestehenden Seiten wiederverwenden (eine Quelle fuer das Design)."""
    # basis.css = CSS der Standortseiten vor dem Umbau (13.10.2026), unveraendert uebernommen
    return open(os.path.join(os.path.dirname(__file__), "basis.css"), encoding="utf-8").read().strip()


def seite(lk, ort, basis_css):
    l, o = LEISTUNGEN[lk], ORTE[ort]
    li_index = LEISTUNG_REIHENFOLGE.index(lk)
    oi_index = ORT_REIHENFOLGE.index(ort)
    titel = f"{l['name']} {o['name']} | Clean Connect Gebäudereinigung"
    if len(titel) > 60:
        titel = f"{l['name']} {o['name']} | Clean Connect"
    meta = l["meta"].format(**{"in": o["in"]})
    if len(meta) > 158:  # Google kuerzt laengere Beschreibungen
        meta = meta[:157].rsplit(" ", 1)[0].rstrip(",:") + "…"
    lead = l["lead"].format(**{"in": o["in"]})
    canonical = f"{BASE}/standorte/{lk}-{ort}.html"
    bild = l["bild"][oi_index % len(l["bild"])]
    bild_text = BILDER[bild]
    fk = FOKUS.get((lk, ort), {})

    # Lokaler Teil: Ortsfacetten in der Reihenfolge der Leistung, je mit Bezugssatz
    absaetze = []
    for t in l["themen"]:
        fakt = o["facetten"].get(t)
        if fakt:
            absaetze.append(f"<p>{e(fakt)} <strong>{e(l['bezug'].get(t, ''))}</strong></p>")
    absaetze.append(f"<p>{e(o['anfahrt'])}</p>")
    if lk == "winterdienst":
        quelle = (f' <a href="{e(o["winter_quelle"])}" rel="noopener" target="_blank">Satzung im Wortlaut (PDF)</a>'
                  if o.get("winter_quelle") else "")
        absaetze.append(f"<p>{e(o['winter_satzung'])}{quelle}</p>")
    stadtteile = auswahl(o["stadtteile"], li_index * 2, len(o["stadtteile"]))

    # Aus den Pools je Ort eine andere Auswahl (rotierend), siehe extras.py
    faq_pool = l["faq"] + FAQ_EXTRA.get(lk, [])
    faq = fk.get("fragen", []) + lokale_faq(lk, ort, li_index) + auswahl(faq_pool, oi_index * 3, 3)
    vorteile = auswahl(l["vorteile"] + VORTEILE_EXTRA.get(lk, []), oi_index, 4)
    zusatz = [o["facetten"][t] for t in ZUSATZ_THEMEN.get(lk, []) if t in o["facetten"]]

    weitere = [x for x in LEISTUNG_REIHENFOLGE if x != lk]
    nb = nachbarn(ort)

    if ort == "koeln":
        fact_ort = ("Einsatzgebiet", "alle Kölner Stadtbezirke")
    else:
        fact_ort = ("Einsatzgebiet", f"{o['name']}, {o['kreis']}")
    preis_kurz = {
        "unterhalt": "32 € netto / Std.", "glas": "45 € netto / Std.", "grund": "38 € netto / Std.",
        "treppenhaus": "120–300 € netto / Monat",
    }.get(l["rechner"], "Angebot nach Besichtigung")

    schema = {
        "@context": "https://schema.org",
        "@graph": [
            {
                "@type": "Service",
                "serviceType": l["name"],
                "name": f"{l['name']} {o['name']}",
                "provider": {"@id": f"{BASE}/#business"},
                "areaServed": {"@type": "City", "name": o["name"]},
                "description": meta,
                "url": canonical,
            },
            {
                "@type": "FAQPage",
                "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faq],
            },
            {
                "@type": "BreadcrumbList",
                "itemListElement": [
                    {"@type": "ListItem", "position": 1, "name": "Start", "item": f"{BASE}/"},
                    {"@type": "ListItem", "position": 2, "name": "Leistungen & Standorte", "item": f"{BASE}/standorte.html"},
                    {"@type": "ListItem", "position": 3, "name": f"{l['name']} {o['name']}", "item": canonical},
                ],
            },
        ],
    }

    eco = "" if lk in ("winterdienst", "entruempelung", "photovoltaikreinigung") else (
        '<div class="eco-badge"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true">'
        '<path d="M11 20A7 7 0 0 1 9.8 6.1C15.5 5 17 4.48 19 2c1 2 2 4.18 2 8 0 5.5-4.78 10-10 10Z"/>'
        '<path d="M2 21c0-3 1.85-5.36 5.08-6C9.5 14.52 12 13 13 12"/></svg>Reinigungsmittel mit dem Umweltzeichen Blauer Engel</div>')

    teile = []
    a = teile.append
    a('<!DOCTYPE html>\n<html lang="de-DE">\n<head>\n<meta charset="UTF-8">')
    a('<meta name="viewport" content="width=device-width, initial-scale=1.0, viewport-fit=cover">')
    a(f"<title>{e(titel)}</title>")
    a(f'<meta name="description" content="{e(meta)}">')
    a('<meta name="robots" content="index, follow, max-image-preview:large, max-snippet:-1">')
    a(f'<link rel="canonical" href="{canonical}">')
    a('<meta property="og:type" content="website">')
    a(f'<meta property="og:url" content="{canonical}">')
    a(f'<meta property="og:title" content="{e(titel)}">')
    a(f'<meta property="og:description" content="{e(meta)}">')
    a('<meta property="og:locale" content="de_DE">\n<meta property="og:site_name" content="Clean Connect Gebäudereinigung">')
    a(f'<meta property="og:image" content="{BASE}/images/{bild}.jpg">\n<meta name="twitter:card" content="summary_large_image">')
    a(f'<meta name="geo.region" content="DE-NW">\n<meta name="geo.placename" content="{e(o["name"])}">')
    a('<link rel="icon" type="image/x-icon" href="../favicon.ico">\n<link rel="icon" type="image/png" sizes="32x32" href="../favicon-32x32.png">\n<link rel="apple-touch-icon" sizes="180x180" href="../apple-touch-icon.png">')
    a('<script type="application/ld+json">\n' + json.dumps(schema, ensure_ascii=False, indent=1) + "\n</script>")
    a('<link rel="preload" href="../fonts/inter-400-latin.woff2" as="font" type="font/woff2" crossorigin>\n<link rel="preload" href="../fonts/plus-jakarta-sans-400-latin.woff2" as="font" type="font/woff2" crossorigin>\n<link rel="stylesheet" href="../fonts.css">')
    a("<style>\n" + basis_css + CSS_EXTRA + "</style>\n</head>\n<body>")
    a('<a href="#main" class="skip-link">Zum Inhalt springen</a>')
    a('<nav aria-label="Hauptnavigation">\n  <a href="../"><img src="../images/logo-96.webp" alt="Clean Connect Logo" width="96" height="96"></a>\n  <a class="back" href="../standorte.html">&larr; Alle Leistungen &amp; Standorte</a>\n</nav>')
    a('<main id="main">\n<div class="wrap hero">')
    a(f'  <div class="kicker"><span style="width:6px;height:6px;border-radius:50%;background:var(--teal);display:inline-block"></span>{e(l["kicker"])}</div>')
    a(f'  <h1>{e(l["name"])} in <em>{e(o["name"])}</em></h1>')
    a(f'  <p class="lead">{e(lead)}</p>')
    a(f"  {eco}")
    a('  <div class="cta-row">\n    <a href="../#kontakt" class="btn btn-p">Kostenloses Angebot &rarr;</a>\n    <a href="tel:022195490625" class="btn btn-g">&#128222; 0221 95490625</a>\n  </div>')
    a('  <div class="facts">')
    a(f'    <div class="fact">{svg("ort")}<div><b>{e(fact_ort[0])}</b><span>{e(fact_ort[1])}</span></div></div>')
    a(f'    <div class="fact">{svg("euro")}<div><b>{e(preis_kurz)}</b><span>Anfahrt inklusive</span></div></div>')
    a(f'    <div class="fact">{svg("uhr")}<div><b>Rückmeldung in 24 Std.</b><span>Besichtigung kostenlos</span></div></div>')
    a("  </div>\n</div>")
    a('<div class="wrap">')
    if fk.get("kurz"):
        a(f'<section>\n  <div class="kurz">\n    <h2>Kurz gesagt</h2>\n    <p>{e(fk["kurz"])}</p>\n  </div>\n</section>')
    if fk.get("praxis"):
        a(f'<section class="lokal">\n  <h2>Aus unserer Arbeit {e(o["in"])}</h2>')
        a("  " + "\n  ".join(f"<p>{e(x)}</p>" for x in fk["praxis"]))
        a("</section>")
    a(f'<section class="lokal">\n  <h2>{e(l["name"])} {e(o["in"])}: was vor Ort zählt</h2>')
    a("  " + "\n  ".join(absaetze))
    a(f"  {entfernungs_grafik(ort)}")
    a("</section>")
    if zusatz:
        a(f'<section class="lokal">\n  <h2>Mehr über {e(o["name"])}</h2>')
        a("  " + "\n  ".join(f"<p>{e(z)}</p>" for z in zusatz))
        a("</section>")
    a(f'<section>\n  <div class="media-box"><img src="../images/{bild}.webp" alt="{e(bild_text)}" loading="lazy" width="880" height="380"><div class="media-cap">{e(bild_text)}.</div></div>\n</section>')
    a(f'<section>\n  <h2>Darauf können Sie sich {e(o["in"])} verlassen</h2>\n  <div class="grid2">')
    for t, txt in vorteile:
        a(f'    <div class="card"><h3>{e(t)}</h3><p>{e(txt)}</p></div>')
    a("  </div>\n</section>")
    a(f'<section>\n  <h2>Leistungsumfang</h2>\n  <ul class="inc">')
    for x in l["umfang"]:
        a(f"    <li>{e(x)}</li>")
    a("  </ul>\n</section>")
    a(f'<section>\n  <h2>So läuft es ab</h2>\n  <ol class="steps">')
    for x in l["ablauf"]:
        a(f"    <li>{e(x)}</li>")
    a("  </ol>\n</section>")
    a(f'<section>\n  <h2>Rechner: {e(l["name"])} {e(o["in"])}</h2>\n  <div class="rechner" data-rechner="{l["rechner"]}"></div>\n  <p class="rechner-fuss"><a href="../rechner.html#{l["rechner"]}">Alle Rechner auf einer Seite</a></p>\n  <noscript><p class="rechner-fuss">Der Rechner braucht JavaScript. Ein Angebot bekommen Sie auch ohne: einfach anfragen.</p></noscript>\n</section>')
    beispiel = f'\n  <p class="beispiel"><strong>Rechenbeispiel:</strong> {e(fk["beispiel"])}</p>' if fk.get("beispiel") else ""
    a(f'<section>\n  <h2>Preise</h2>\n  <div class="preis">{svg("euro", 22)}<p>{e(l["preis"])} <a href="../preise.html">Alle Preise ansehen</a></p></div>{beispiel}\n</section>')
    a(f'<section>\n  <h2>Einsatzgebiet {e(o["name"])}</h2>\n  <div class="chips">' + "".join(f"<span>{e(s)}</span>" for s in stadtteile) + "</div>")
    a(f'  <div class="map-wrap"><div class="cc-map"><iframe data-src="https://maps.google.com/maps?q={e(o["name"]).replace(" ", "+")}%2C+Deutschland&z=12&output=embed" title="Kartenausschnitt {e(o["name"])}" loading="lazy" referrerpolicy="no-referrer-when-downgrade"></iframe></div></div>')
    a('  <p class="nachbar">' + e(l["name"]) + " auch in der Nähe: " + ", ".join(
        f'<a href="{url(lk, n)}">{e(ORTE[n]["name"])}</a>' for n in nb) + "</p>\n</section>")
    a(f'<section>\n  <h2>Häufige Fragen: {e(l["name"])} {e(o["in"])}</h2>')
    for q, ans in faq:
        a(f"  <details><summary>{e(q)}</summary><p>{e(ans)}</p></details>")
    a("</section>")
    a(f'<section>\n  <h2>Weitere Leistungen {e(o["in"])}</h2>\n  <div class="related">')
    for x in weitere:
        a(f'    <a href="{url(x, ort)}">{e(LEISTUNGEN[x]["name"])}</a>')
    a("  </div>\n</section>")
    artikel = ratgeber(lk, ort)
    if artikel:
        a(f'<section>\n  <h2>Ratgeber zum Thema {e(l["name"])}</h2>\n  <div class="related">')
        for slug, t in artikel:
            a(f'    <a href="../blog/{slug}.html">{e(t)}</a>')
        a("  </div>\n</section>")
    a(f'<section>\n  <div class="cta-box">\n    <h2>Angebot für {e(l["name"])} {e(o["in"])} anfordern</h2>\n    <p>Eine kurze Nachricht mit Objekt und Anliegen genügt, Sie bekommen innerhalb von 24 Stunden eine Rückmeldung.</p>\n    <a href="../#kontakt" class="btn btn-p">Kostenloses Angebot &rarr;</a>\n  </div>\n</section>')
    a("</div>\n</main>")
    a('<footer>\n  <a href="../">Clean Connect Gebäudereinigung UG</a> &middot;\n  <a href="../impressum.html">Impressum</a> &middot;\n  <a href="../datenschutz.html">Datenschutz</a> &middot;\n  <a href="../agb.html">AGB</a> &middot;\n  <a href="../widerruf.html">Widerruf</a>\n  <div style="margin-top:8px">&copy; 2026 Clean Connect Gebäudereinigung UG</div>\n  <div style="margin-top:8px">Büro &amp; Lager: Forststraße 33, 51107 Köln &middot; Rechnungsanschrift: Berliner Straße 957, 51069 Köln &middot; <a href="tel:+4922195490625">0221 95490625</a> &middot; Mo–Fr 7–18 Uhr</div>\n</footer>')
    a('<script src="../maps-consent.js" defer></script>\n<script src="rechner.js" defer></script>\n</body>\n</html>\n')
    return "\n".join(teile)


# Bei neuen Stundensaetzen hier und auf preise.html nachziehen.
PREISSTAND = ("2026-11-04", "November 2026")


def rechner_seite(basis_css, geaendert):
    """rechner.html: alle Rechner der Standortseiten auf einer Seite (04.11.2026)."""
    canonical = f"{BASE}/rechner.html"
    titel = "Reinigungskosten-Rechner Köln | Clean Connect"
    meta = ("Was kostet Büro-, Glas-, Grund- oder Treppenhausreinigung in Köln? Unsere Rechner schätzen Zeit und Preis "
            "mit denselben Stundensätzen wie die Preisliste.")
    # je Rechnerart eine Leistung; Bueroreinigung teilt sich den Rechner mit der Unterhaltsreinigung
    arten = []
    for lk in LEISTUNG_REIHENFOLGE:
        art = LEISTUNGEN[lk]["rechner"]
        if art not in [x[1] for x in arten]:
            arten.append((lk, art))
    namen = {"unterhaltsreinigung": "Unterhalts- und Büroreinigung"}
    kurz = ("Eine Büroreinigung von 200 m² zweimal pro Woche kostet bei uns rund 277 € netto im Monat, eine Stunde je Einsatz "
            "zu 32 € netto. Ein Treppenhaus mit vier Etagen, wöchentlich gereinigt, liegt bei rund 195 € netto im Monat. "
            "Die Anfahrt ist immer inklusive.")
    schema = {
        "@context": "https://schema.org",
        "@graph": [
            {
                "@type": "WebPage",
                "name": titel,
                "description": meta,
                "url": canonical,
                "inLanguage": "de-DE",
                "isPartOf": {"@type": "WebSite", "url": f"{BASE}/"},
                "about": {"@id": f"{BASE}/#business"},
                "dateModified": PREISSTAND[0],
            },
            {
                "@type": "BreadcrumbList",
                "itemListElement": [
                    {"@type": "ListItem", "position": 1, "name": "Start", "item": f"{BASE}/"},
                    {"@type": "ListItem", "position": 2, "name": "Preise", "item": f"{BASE}/preise.html"},
                    {"@type": "ListItem", "position": 3, "name": "Rechner", "item": canonical},
                ],
            },
        ],
    }
    teile = []
    a = teile.append
    a('<!DOCTYPE html>\n<html lang="de-DE">\n<head>\n<meta charset="UTF-8">')
    a('<meta name="viewport" content="width=device-width, initial-scale=1.0, viewport-fit=cover">')
    a(f"<title>{e(titel)}</title>")
    a(f'<meta name="description" content="{e(meta)}">')
    a('<meta name="robots" content="index, follow, max-image-preview:large, max-snippet:-1">')
    a(f'<link rel="canonical" href="{canonical}">')
    a('<meta property="og:type" content="website">')
    a(f'<meta property="og:url" content="{canonical}">')
    a(f'<meta property="og:title" content="{e(titel)}">')
    a(f'<meta property="og:description" content="{e(meta)}">')
    a('<meta property="og:locale" content="de_DE">\n<meta property="og:site_name" content="Clean Connect Gebäudereinigung">')
    a(f'<meta property="og:image" content="{BASE}/og-image.jpg">\n<meta name="twitter:card" content="summary_large_image">')
    a('<link rel="icon" type="image/x-icon" href="favicon.ico">\n<link rel="icon" type="image/png" sizes="32x32" href="favicon-32x32.png">\n<link rel="apple-touch-icon" sizes="180x180" href="apple-touch-icon.png">')
    a('<script type="application/ld+json">\n' + json.dumps(schema, ensure_ascii=False, indent=1) + "\n</script>")
    a('<link rel="preload" href="fonts/inter-400-latin.woff2" as="font" type="font/woff2" crossorigin>\n<link rel="preload" href="fonts/plus-jakarta-sans-400-latin.woff2" as="font" type="font/woff2" crossorigin>\n<link rel="stylesheet" href="fonts.css">')
    a("<style>\n" + basis_css + CSS_EXTRA + "</style>\n</head>\n<body>")
    a('<a href="#main" class="skip-link">Zum Inhalt springen</a>')
    a('<nav aria-label="Hauptnavigation">\n  <a href="./"><img src="images/logo-96.webp" alt="Clean Connect Logo" width="96" height="96"></a>\n  <a class="back" href="preise.html">&larr; Alle Preise</a>\n</nav>')
    a('<main id="main">\n<div class="wrap hero">')
    a('  <div class="kicker"><span style="width:6px;height:6px;border-radius:50%;background:var(--teal);display:inline-block"></span>Preise schätzen in einer Minute</div>')
    a("  <h1>Was kostet die Reinigung? <em>Rechner</em> für alle Leistungen</h1>")
    a('  <p class="lead">Die Rechner nutzen dieselben Stundensätze wie unsere <a href="preise.html">Preisliste</a>: 32 € netto für '
      "Unterhalts- und Büroreinigung, 38 € für Grundreinigung und 45 € für Glasreinigung. Das Ergebnis ist eine Schätzung, "
      "das verbindliche Angebot bekommen Sie nach einer kostenlosen Besichtigung oder anhand von Fotos.</p>")
    a(f'  <p class="rechner-fuss" style="margin:-14px 0 22px">Preisstand: {PREISSTAND[1]}</p>')
    a('  <div class="cta-row">\n    <a href="./#kontakt" class="btn btn-p">Kostenloses Angebot &rarr;</a>\n    <a href="tel:022195490625" class="btn btn-g">&#128222; 0221 95490625</a>\n  </div>')
    a("</div>")
    a('<div class="wrap">')
    a(f'<section>\n  <div class="kurz">\n    <h2>Kurz gesagt</h2>\n    <p>{e(kurz)}</p>\n  </div>\n</section>')
    for lk, art in arten:
        name = namen.get(lk, LEISTUNGEN[lk]["name"])
        a(f'<section id="{art}">\n  <h2>Rechner: {e(name)}</h2>\n  <div class="rechner" data-rechner="{art}"></div>')
        ziel = url(lk, "koeln")
        ziel = ziel[3:] if ziel.startswith("../") else f"standorte/{ziel}"
        a(f'  <p class="nachbar">Mehr dazu: <a href="{ziel}">{e(LEISTUNGEN[lk]["name"])} in Köln</a></p>\n</section>')
    a('<noscript><p class="rechner-fuss">Die Rechner brauchen JavaScript. Ein Angebot bekommen Sie auch ohne: einfach anfragen.</p></noscript>')
    a('<section>\n  <div class="cta-box">\n    <h2>Lieber ein genaues Angebot?</h2>\n    <p>Eine kurze Nachricht mit Objekt und Anliegen genügt, Sie bekommen innerhalb von 24 Stunden eine Rückmeldung.</p>\n    <a href="./#kontakt" class="btn btn-p">Kostenloses Angebot &rarr;</a>\n  </div>\n</section>')
    a("</div>\n</main>")
    a('<footer>\n  <a href="./">Clean Connect Gebäudereinigung UG</a> &middot;\n  <a href="impressum.html">Impressum</a> &middot;\n  <a href="datenschutz.html">Datenschutz</a> &middot;\n  <a href="agb.html">AGB</a> &middot;\n  <a href="widerruf.html">Widerruf</a>\n  <div style="margin-top:8px">&copy; 2026 Clean Connect Gebäudereinigung UG</div>\n  <div style="margin-top:8px">Büro &amp; Lager: Forststraße 33, 51107 Köln &middot; Rechnungsanschrift: Berliner Straße 957, 51069 Köln &middot; <a href="tel:+4922195490625">0221 95490625</a> &middot; Mo–Fr 7–18 Uhr</div>\n</footer>')
    a('<script src="standorte/rechner.js" defer></script>\n</body>\n</html>\n')
    schreibe(os.path.join(ROOT, "rechner.html"), "\n".join(teile), geaendert)


def aktualisiere_hub(geaendert):
    """standorte.html: eine Karte je Leistung mit allen Orten."""
    p = os.path.join(ROOT, "standorte.html")
    s = open(p, encoding="utf-8").read()
    karten = []
    for lk in LEISTUNG_REIHENFOLGE:
        l = LEISTUNGEN[lk]
        links = "\n".join(
            f'      <a href="{("" if (lk, o) in AUSNAHMEN else "standorte/")}{url(lk, o).replace("../", "")}">{e(ORTE[o]["name"])}</a>'
            for o in ORT_REIHENFOLGE)
        karten.append(f'  <div class="hub-card">\n    <h2>{e(l["name"])}</h2>\n    <p>{e(l["kicker"])}</p>\n    <div class="hub-links">\n{links}\n    </div>\n  </div>')
    neu = '<div class="wrap hub-grid">\n' + "\n".join(karten) + "\n</div>\n<footer>"
    s, n = re.subn(r'<div class="wrap hub-grid">.*?</div>\s*</div>\s*<footer>', lambda m: neu, s, count=1, flags=re.S)
    assert n == 1, "hub-grid nicht gefunden"
    s = re.sub(r"mit \S+ Leistungen in elf Städten", f"mit {len(LEISTUNG_REIHENFOLGE)} Leistungen in elf Städten", s)
    schreibe(p, s, geaendert)


def schreibe(pfad, inhalt, geaendert):
    """Datei nur bei echter Aenderung schreiben und sie dann fuer lastmod vormerken."""
    if os.path.exists(pfad) and open(pfad, encoding="utf-8").read() == inhalt:
        return
    open(pfad, "w", encoding="utf-8").write(inhalt)
    geaendert.add(os.path.relpath(pfad, ROOT))


def aktualisiere_sitemap(heute, geaendert):
    """/standorte/-Eintraege neu schreiben. lastmod wird nur fuer geaenderte Seiten
    auf heute gesetzt, sonst bleibt das alte Datum stehen (04.11.2026)."""
    p = os.path.join(ROOT, "sitemap.xml")
    s = open(p, encoding="utf-8").read()
    alt = dict(re.findall(r"<loc>([^<]+)</loc>\s*<lastmod>([^<]+)</lastmod>", s))

    def datum(rel):
        return heute if rel in geaendert else alt.get(f"{BASE}/{rel}", heute)

    s = re.sub(r"\s*<url>\s*<loc>https://cleanconnect\.de/standorte/[^<]+</loc>.*?</url>", "", s, flags=re.S)
    s = re.sub(r"(<loc>https://cleanconnect\.de/standorte\.html</loc>\s*<lastmod>)[^<]+", lambda m: m.group(1) + datum("standorte.html"), s)
    eintraege = []
    for lk in LEISTUNG_REIHENFOLGE:
        for o in ORT_REIHENFOLGE:
            if (lk, o) in AUSNAHMEN:
                continue
            rel = f"standorte/{lk}-{o}.html"
            eintraege.append(f"  <url>\n    <loc>{BASE}/{rel}</loc>\n    <lastmod>{datum(rel)}</lastmod>\n    <changefreq>monthly</changefreq>\n    <priority>0.7</priority>\n  </url>")
    s = s.replace("</urlset>", "\n".join(eintraege) + "\n</urlset>")
    rechner = f"{BASE}/rechner.html"
    if rechner in s:
        s = re.sub(r"(<loc>" + re.escape(rechner) + r"</loc>\s*<lastmod>)[^<]+", lambda m: m.group(1) + datum("rechner.html"), s)
    else:
        s = s.replace("</urlset>", f"  <url>\n    <loc>{rechner}</loc>\n    <lastmod>{heute}</lastmod>\n    <changefreq>monthly</changefreq>\n    <priority>0.8</priority>\n  </url>\n</urlset>")
    open(p, "w", encoding="utf-8").write(s)


def main():
    import datetime
    heute = datetime.date.today().isoformat()
    basis_css = lade_basis_css()
    geaendert = set()
    n = 0
    for lk in LEISTUNG_REIHENFOLGE:
        for ort in ORT_REIHENFOLGE:
            if (lk, ort) in AUSNAHMEN:
                continue
            schreibe(os.path.join(OUT, f"{lk}-{ort}.html"), seite(lk, ort, basis_css), geaendert)
            n += 1
    rechner_seite(basis_css, geaendert)
    aktualisiere_hub(geaendert)
    aktualisiere_sitemap(heute, geaendert)
    print(f"{n} Seiten gebaut, davon {len(geaendert)} Dateien geaendert, sitemap.xml aktualisiert")


if __name__ == "__main__":
    main()
