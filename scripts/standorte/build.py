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
from fragen import FRAGEN, STAND as FRAGEN_STAND  # noqa: E402
from praxis import PRAXIS  # noqa: E402

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
.fall{padding:22px;background:var(--s1);border:1px solid var(--br);border-radius:16px;margin-bottom:14px}
.fall h3{color:#fff;font-size:17px;margin-bottom:6px}
.fall p{font-size:14.5px;color:var(--mu2);line-height:1.65;margin-bottom:8px}
.fall p strong{color:#fff;font-weight:600}
.fall .bilder{display:grid;grid-template-columns:1fr 1fr;gap:10px;margin-top:12px}
.fall figure{margin:0;position:relative}
.fall img{width:100%;height:auto;aspect-ratio:3/4;object-fit:cover;border-radius:12px;display:block}
.fall.quer img{aspect-ratio:4/3}
.fall .bilder.drei{grid-template-columns:repeat(3,1fr)}
@media(max-width:600px){.fall .bilder.drei{grid-template-columns:1fr 1fr}}
.fall figure.einsatz figcaption{background:#fff;color:#111}
.fall figcaption{position:absolute;left:8px;top:8px;font-size:11px;font-weight:700;letter-spacing:.06em;text-transform:uppercase;background:rgba(0,0,0,.65);color:#fff;padding:3px 8px;border-radius:6px}
.fall figure.nachher figcaption{background:var(--teal);color:#06201f}
.fall-mehr{font-size:14px;margin-top:4px}
.fall-mehr a{color:var(--teal);font-weight:600}
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
.chips span,.chips a{font-size:12.5px;color:var(--mu2);border:1px solid var(--br2);padding:6px 12px;border-radius:100px;background:var(--s1)}
.chips a{text-decoration:none}
.chips a:hover{color:var(--teal);border-color:var(--teal)}
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

# Nur fuer die Seiten im Hauptverzeichnis (fragen, preisspiegel, team), damit sich die Standortseiten nicht aendern
CSS_SEITEN = """
.inhalt{display:flex;flex-wrap:wrap;gap:8px;margin-top:4px}
.inhalt a{font-size:13px;color:var(--mu2);border:1px solid var(--br2);padding:7px 14px;border-radius:100px}
.frage{padding:18px 0;border-bottom:1px solid var(--br)}
.frage:last-child{border-bottom:0}
.frage h3{font-size:17px;color:#fff;font-weight:700;margin-bottom:8px}
.frage p{font-size:15px;color:var(--mu2);line-height:1.65}
.frage a{color:var(--teal);font-weight:600}
.stand{font-size:12.5px;color:var(--mu);margin:-14px 0 22px}
.tabelle{overflow-x:auto}
.tabelle table{width:100%;border-collapse:collapse;font-size:14.5px}
.tabelle th,.tabelle td{text-align:left;padding:11px 12px;border-bottom:1px solid var(--br)}
.tabelle th{color:var(--mu2);font-weight:600;font-size:12.5px;text-transform:uppercase;letter-spacing:.05em}
.tabelle td{color:var(--tx)}
.tabelle td b{color:#fff}
.text p{font-size:15px;color:var(--mu2);line-height:1.7;margin-bottom:14px}
.text p strong{color:#fff;font-weight:600}
.text ul{color:var(--mu2);font-size:15px;margin:0 0 14px 20px}
.text li{margin-bottom:6px}
.text a{color:var(--teal)}
.person{display:grid;grid-template-columns:140px 1fr;gap:22px;align-items:start;padding:22px;background:var(--s1);border:1px solid var(--br);border-radius:16px;margin-bottom:14px}
@media(max-width:600px){.person{grid-template-columns:1fr}}
.person img{width:140px;height:140px;border-radius:14px;object-fit:cover;object-position:top center}
.person .ico{width:140px;height:140px;border-radius:14px;background:#0a1a2a;display:flex;align-items:center;justify-content:center}
.person h3{color:#fff;font-size:19px;margin-bottom:2px}
.person .rolle{color:var(--teal);font-size:13px;font-weight:600;margin-bottom:10px;display:block}
.person p{font-size:14.5px;color:var(--mu2);line-height:1.65}
"""


def lade_basis_css():
    """CSS der bestehenden Seiten wiederverwenden (eine Quelle fuer das Design)."""
    # basis.css = CSS der Standortseiten vor dem Umbau (13.10.2026), unveraendert uebernommen
    return open(os.path.join(os.path.dirname(__file__), "basis.css"), encoding="utf-8").read().strip()


# Kurzer Anreiz im Suchergebnis-Titel (05.11.2026). Preise NUR wie auf preise.html.
TITEL_ANREIZ = {
    "unterhaltsreinigung": "32 €/Std. netto",
    "bueroreinigung": "32 €/Std. netto",
    "glasreinigung": "45 €/Std. netto",
    "grundreinigung": "38 €/Std. netto",
    "treppenhausreinigung": "ab 120 €/Monat",
    "winterdienst": "Räumen nach Satzung",
    "bauendreinigung": "Angebot nach Fotos",
    "entruempelung": "Festpreis nach Besichtigung",
    "photovoltaikreinigung": "ohne Chemie",
}


def standort_titel(lk, name, ort):
    """Erster Kandidat bis 60 Zeichen: mit Anreiz und Marke, mit Anreiz, ohne Anreiz."""
    anreiz = TITEL_ANREIZ.get(lk)
    kandidaten = ([f"{name} {ort}: {anreiz} | Clean Connect", f"{name} {ort}: {anreiz}"] if anreiz else []) + [
        f"{name} {ort} | Clean Connect Gebäudereinigung", f"{name} {ort} | Clean Connect"]
    return next((k for k in kandidaten if len(k) <= 60), kandidaten[-1])


def seite(lk, ort, basis_css):
    l, o = LEISTUNGEN[lk], ORTE[ort]
    li_index = LEISTUNG_REIHENFOLGE.index(lk)
    oi_index = ORT_REIHENFOLGE.index(ort)
    titel = standort_titel(lk, l["name"], o["name"])
    meta = l["meta"].format(**{"in": o["in"]})
    while len(meta) > 158 and meta.count(". ") >= 1:  # Google kuerzt laengere Beschreibungen: lieber ganzen Satz weglassen
        meta = meta.rsplit(". ", 1)[0] + "."
    if len(meta) > 158:
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
    a('<nav aria-label="Hauptnavigation">\n  <a href="../"><img src="../images/clean-connect-logo-96.webp" alt="Clean Connect Logo" width="96" height="96"></a>\n  <a class="back" href="../standorte.html">&larr; Alle Leistungen &amp; Standorte</a>\n</nav>')
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
    paare = [f for f in PRAXIS if lk in f["leistungen"]][:2]
    if paare:
        a(f'<section>\n  <h2>{e(l["name"])}: vorher und nachher</h2>\n  <p class="fall-mehr">Fotos aus unseren eigenen Einsätzen.</p>')
        a("\n".join(fall_html(f, "../") for f in paare))
        a('  <p class="fall-mehr"><a href="../vorher-nachher.html">Alle Vorher/Nachher-Fotos ansehen &rarr;</a></p>\n</section>')
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
    a('<footer>\n  <a href="../">Clean Connect Gebäudereinigung UG</a> &middot;\n  <a href="../impressum.html">Impressum</a> &middot;\n  <a href="../datenschutz.html">Datenschutz</a> &middot;\n  <a href="../agb.html">AGB</a> &middot;\n  <a href="../widerruf.html">Widerruf</a>\n  <div style="margin-top:8px">&copy; 2026 Clean Connect Gebäudereinigung UG</div>\n  <div style="margin-top:8px">Forststraße 33, 51107 Köln &middot; <a href="tel:+4922195490625">0221 95490625</a> &middot; Mo–Fr 8–18 Uhr, Sa 8–16 Uhr</div>\n</footer>')
    a('<script src="../maps-consent.js" defer></script>\n<script src="rechner.js" defer></script>\n</body>\n</html>\n')
    return "\n".join(teile)


# Bei neuen Stundensaetzen hier und auf preise.html nachziehen.
PREISSTAND = ("2026-11-04", "November 2026")


def fall_html(f, prefix="", h="h3"):
    """Eine Vorher/Nachher-Karte aus praxis.py; prefix = "../" auf den Standortseiten."""
    w, hh = (800, 600) if f["format"] == "quer" else (800, 1067)
    zeile = " &middot; ".join(e(x) for x in (f["objekt"], f["ort"], f["leistung"], f"seit {f['seit']}" if f["seit"] else None) if x)
    bilder = fall_bilder(f)
    html = "".join(
        f'<figure class="{k}"><img src="{prefix}images/praxis/{e(datei)}" alt="{e(BILD_ART[k])}: {e(f["bildtext"])}" '
        f'loading="lazy" width="{w}" height="{hh}"><figcaption>{e(BILD_ART[k])}</figcaption></figure>'
        for datei, k in bilder)
    klassen = "fall" + (" quer" if f["format"] == "quer" else "")
    return (f'  <div class="{klassen}">\n    <{h}>{e(f["titel"])}</{h}>\n    <p>{zeile}</p>\n'
            f'    <p><strong>Vorher:</strong> {e(f["aufgabe"])} <strong>{e(f.get("ergebnis_label", "Nachher"))}:</strong> {e(f["ergebnis"])}</p>\n'
            f'    <div class="bilder{" drei" if len(bilder) == 3 else ""}">{html}</div>\n  </div>')


BILD_ART = {"vorher": "Vorher", "nachher": "Nachher", "einsatz": "Im Einsatz"}


def fall_bilder(f):
    """[(datei, art)]; "bilder" in praxis.py ersetzt das Standardpaar vorher/nachher."""
    return f.get("bilder") or [(f["vorher"], "vorher"), (f["nachher"], "nachher")]


def kopf(titel, meta, canonical, schema, basis_css, zurueck=("preise.html", "Alle Preise"), og_typ="website", extra_css=CSS_SEITEN):
    """Gemeinsamer Seitenkopf der Seiten im Hauptverzeichnis (rechner, fragen, preisspiegel, team)."""
    teile = []
    a = teile.append
    a('<!DOCTYPE html>\n<html lang="de-DE">\n<head>\n<meta charset="UTF-8">')
    a('<meta name="viewport" content="width=device-width, initial-scale=1.0, viewport-fit=cover">')
    a(f"<title>{e(titel)}</title>")
    a(f'<meta name="description" content="{e(meta)}">')
    a('<meta name="robots" content="index, follow, max-image-preview:large, max-snippet:-1">')
    a(f'<link rel="canonical" href="{canonical}">')
    a(f'<meta property="og:type" content="{og_typ}">')
    a(f'<meta property="og:url" content="{canonical}">')
    a(f'<meta property="og:title" content="{e(titel)}">')
    a(f'<meta property="og:description" content="{e(meta)}">')
    a('<meta property="og:locale" content="de_DE">\n<meta property="og:site_name" content="Clean Connect Gebäudereinigung">')
    a(f'<meta property="og:image" content="{BASE}/og-image.jpg">\n<meta name="twitter:card" content="summary_large_image">')
    a('<link rel="icon" type="image/x-icon" href="favicon.ico">\n<link rel="icon" type="image/png" sizes="32x32" href="favicon-32x32.png">\n<link rel="apple-touch-icon" sizes="180x180" href="apple-touch-icon.png">')
    a('<script type="application/ld+json">\n' + json.dumps(schema, ensure_ascii=False, indent=1) + "\n</script>")
    a('<link rel="preload" href="fonts/inter-400-latin.woff2" as="font" type="font/woff2" crossorigin>\n<link rel="preload" href="fonts/plus-jakarta-sans-400-latin.woff2" as="font" type="font/woff2" crossorigin>\n<link rel="stylesheet" href="fonts.css">')
    a("<style>\n" + basis_css + CSS_EXTRA + extra_css + "</style>\n</head>\n<body>")
    a('<a href="#main" class="skip-link">Zum Inhalt springen</a>')
    a(f'<nav aria-label="Hauptnavigation">\n  <a href="./"><img src="images/clean-connect-logo-96.webp" alt="Clean Connect Logo" width="96" height="96"></a>\n  <a class="back" href="{zurueck[0]}">&larr; {zurueck[1]}</a>\n</nav>')
    return teile


def fuss(skript=None):
    """Gemeinsamer Seitenfuss; schliesst main, das in jeder Seite in einem wrap-div endet."""
    teile = []
    a = teile.append
    a("</div>\n</main>")
    a('<footer>\n  <a href="./">Clean Connect Gebäudereinigung UG</a> &middot;\n  <a href="impressum.html">Impressum</a> &middot;\n  <a href="datenschutz.html">Datenschutz</a> &middot;\n  <a href="agb.html">AGB</a> &middot;\n  <a href="widerruf.html">Widerruf</a> &middot;\n  <a href="fragen.html">Häufige Fragen</a> &middot;\n  <a href="team.html">Team</a>\n  <div style="margin-top:8px">&copy; 2026 Clean Connect Gebäudereinigung UG</div>\n  <div style="margin-top:8px">Forststraße 33, 51107 Köln &middot; <a href="tel:+4922195490625">0221 95490625</a> &middot; Mo–Fr 8–18 Uhr, Sa 8–16 Uhr</div>\n</footer>')
    a((f'<script src="{skript}" defer></script>\n' if skript else "") + "</body>\n</html>\n")
    return teile


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
    kurz = ("Eine Büroreinigung von 200 m² zweimal pro Woche braucht rund eine Stunde je Einsatz zu 32 € netto, das sind "
            "rund 277 € im Monat. Weil das unter unserem Mindestpreis liegt, berechnen wir dafür 280 € netto im Monat. Ein Treppenhaus mit vier Etagen, wöchentlich gereinigt, liegt bei rund 195 € netto im Monat. "
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
    teile = kopf(titel, meta, canonical, schema, basis_css, extra_css="")
    a = teile.append
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
    teile += fuss("standorte/rechner.js")
    schreibe(os.path.join(ROOT, "rechner.html"), "\n".join(teile), geaendert)


def anker(text):
    t = text.lower().replace("ä", "ae").replace("ö", "oe").replace("ü", "ue").replace("ß", "ss")
    return re.sub(r"[^a-z0-9]+", "-", t).strip("-")[:60]


# Autor der Ratgeber und des Preisspiegels: die Firma, keine Einzelperson (05.11.2026)
AUTOR = {"@type": "Organization", "@id": f"{BASE}/#business", "name": "Clean Connect Gebäudereinigung", "url": f"{BASE}/"}


def hero(kicker, h1, lead, stand=None):
    teile = ['<main id="main">\n<div class="wrap hero">',
             f'  <div class="kicker"><span style="width:6px;height:6px;border-radius:50%;background:var(--teal);display:inline-block"></span>{e(kicker)}</div>',
             f"  <h1>{h1}</h1>", f'  <p class="lead">{lead}</p>']
    if stand:
        teile.append(f'  <p class="stand">{stand}</p>')
    teile.append('  <div class="cta-row">\n    <a href="./#kontakt" class="btn btn-p">Kostenloses Angebot &rarr;</a>\n    <a href="tel:022195490625" class="btn btn-g">&#128222; 0221 95490625</a>\n  </div>')
    teile.append("</div>")
    teile.append('<div class="wrap">')
    return teile


def cta_box():
    return ('<section>\n  <div class="cta-box">\n    <h2>Ihre Frage war nicht dabei?</h2>\n    <p>Schreiben Sie uns kurz, worum es geht. '
            'Sie bekommen innerhalb von 24 Stunden eine Antwort, auf Wunsch mit Angebot.</p>\n'
            '    <a href="./#kontakt" class="btn btn-p">Frage oder Anfrage senden &rarr;</a>\n  </div>\n</section>')


def fragen_seite(basis_css, geaendert):
    """fragen.html: gesammelte Kundenfragen, Antwort jeweils zuerst (04.11.2026)."""
    canonical = f"{BASE}/fragen.html"
    titel = "Häufige Fragen zur Gebäudereinigung Köln | Clean Connect"
    meta = ("Was kostet eine Reinigungsfirma in Köln, was ist im Preis enthalten, wie schnell geht es los? "
            "Antworten auf die Fragen, die uns Kunden wirklich stellen.")
    alle = [(f, a, l) for _, liste in FRAGEN for f, a, l, _q in liste]
    schema = {"@context": "https://schema.org", "@graph": [
        {"@type": "FAQPage", "name": titel, "url": canonical, "inLanguage": "de-DE", "dateModified": FRAGEN_STAND[0],
         "about": {"@id": f"{BASE}/#business"}, "isPartOf": {"@type": "WebSite", "url": f"{BASE}/"},
         "mainEntity": [{"@type": "Question", "name": f, "acceptedAnswer": {"@type": "Answer", "text": a}} for f, a, _ in alle]},
        {"@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Start", "item": f"{BASE}/"},
            {"@type": "ListItem", "position": 2, "name": "Häufige Fragen", "item": canonical}]},
    ]}
    teile = kopf(titel, meta, canonical, schema, basis_css, zurueck=("./", "Startseite"))
    a = teile.append
    teile += hero("Häufige Fragen", "Fragen und Antworten zur <em>Gebäudereinigung</em> in Köln",
                  "Diese Fragen stellen uns Interessenten und Kunden immer wieder, per Mail und über die Suche. Die Antwort "
                  "steht jeweils im ersten Satz, Details und Links folgen danach.",
                  f"Stand: {FRAGEN_STAND[1]} &middot; {len(alle)} Fragen")
    a('<section>\n  <h2>Themen</h2>\n  <div class="inhalt">')
    for gruppe, _ in FRAGEN:
        a(f'    <a href="#{anker(gruppe)}">{e(gruppe)}</a>')
    a("  </div>\n</section>")
    for gruppe, liste in FRAGEN:
        a(f'<section id="{anker(gruppe)}">\n  <h2>{e(gruppe)}</h2>')
        for f, antwort, link, _q in liste:
            mehr = f' <a href="{e(link[0])}">{e(link[1])} &rarr;</a>' if link else ""
            a(f'  <div class="frage" id="{anker(f)}">\n    <h3>{e(f)}</h3>\n    <p>{e(antwort)}{mehr}</p>\n  </div>')
        a("</section>")
    a(cta_box())
    teile += fuss()
    schreibe(os.path.join(ROOT, "fragen.html"), "\n".join(teile), geaendert)


RHYTHMUS = {"1x": "1× pro Woche", "2x": "2× pro Woche", "3x": "3× pro Woche", "5x": "5× pro Woche (werktäglich)",
            "7x": "7× pro Woche (täglich)", "14t": "alle 14 Tage"}
ART = {"unterhalt": "Unterhaltsreinigung", "treppenhaus": "Treppenhausreinigung"}


def tausend(n):
    return f"{n:,}".replace(",", ".") + " €"


def monat_de(iso):
    monate = ["Januar", "Februar", "März", "April", "Mai", "Juni", "Juli", "August", "September", "Oktober", "November", "Dezember"]
    return f"{monate[int(iso[5:7]) - 1]} {iso[:4]}"


def preisspiegel_seite(basis_css, geaendert):
    """preisspiegel.html: Monatspreise aus unseren eigenen Angeboten (04.11.2026).
    Zahlen kommen aus preisspiegel_daten.json, erzeugt von preisspiegel_auswertung.py."""
    d = json.load(open(os.path.join(os.path.dirname(__file__), "preisspiegel_daten.json"), encoding="utf-8"))
    z = {(r["art"], r["intervall"]): r for r in d["zeilen"]}
    u1, u2, u5 = z[("unterhalt", "1x")], z[("unterhalt", "2x")], z[("unterhalt", "5x")]
    canonical = f"{BASE}/preisspiegel.html"
    titel = "Preisspiegel Unterhaltsreinigung Köln 2026 | Clean Connect"
    meta = (f"Was kostet Unterhaltsreinigung in Köln wirklich? Monatspreise aus {d['objekte']} Angeboten: "
            f"Median {tausend(u1['median'])} netto bei einer Reinigung pro Woche.")
    zeitraum = f"{monat_de(d['von'])} bis {monat_de(d['bis'])}"
    kurz = (f"Bei einer Reinigung pro Woche lag die Hälfte unserer Angebote für Büros, Praxen und Gewerbeflächen zwischen "
            f"{tausend(u1['p25'])} und {tausend(u1['p75'])} netto im Monat, der Median bei {tausend(u1['median'])}. Bei zwei "
            f"Terminen pro Woche lag der Median bei {tausend(u2['median'])}, bei werktäglicher Reinigung bei {tausend(u5['median'])}. "
            f"Grundlage sind {d['objekte']} Objekte, für die wir von {zeitraum} ein Angebot geschrieben haben.")
    schema = {"@context": "https://schema.org", "@graph": [
        {"@type": "Article", "headline": "Preisspiegel Unterhaltsreinigung Köln: Was unsere Angebote zeigen",
         "description": meta, "url": canonical, "inLanguage": "de-DE", "datePublished": "2026-11-04", "dateModified": d["stand"],
         "author": AUTOR, "publisher": {"@id": f"{BASE}/#business"}, "mainEntityOfPage": canonical,
         "image": f"{BASE}/og-image.jpg"},
        {"@type": "Dataset", "name": "Monatspreise Unterhalts- und Treppenhausreinigung aus Angeboten von Clean Connect",
         "description": kurz, "url": canonical, "creator": {"@id": f"{BASE}/#business"}, "isAccessibleForFree": True,
         "temporalCoverage": f"{d['von']}/{d['bis']}", "dateModified": d["stand"],
         "spatialCoverage": {"@type": "Place", "name": "Köln und Umgebung"},
         "variableMeasured": ["Monatspreis netto (Median)", "Monatspreis netto (25. bis 75. Perzentil)", "Anzahl Objekte"]},
        {"@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Start", "item": f"{BASE}/"},
            {"@type": "ListItem", "position": 2, "name": "Preise", "item": f"{BASE}/preise.html"},
            {"@type": "ListItem", "position": 3, "name": "Preisspiegel", "item": canonical}]},
    ]}
    teile = kopf(titel, meta, canonical, schema, basis_css, og_typ="article")
    a = teile.append
    teile += hero("Eigene Auswertung", "Was kostet <em>Unterhaltsreinigung</em> in Köln? Unser Preisspiegel",
                  f"Wir haben ausgewertet, welche Monatspreise wir in {d['objekte']} Angeboten genannt haben. Das zeigt, "
                  "was Reinigung in Köln tatsächlich kostet, ohne Rechenbeispiel und ohne Lockpreis.",
                  f'Stand: {monat_de(d["stand"])} &middot; Auswertung: <a href="team.html">Clean Connect</a>')
    a(f'<section>\n  <div class="kurz">\n    <h2>Kurz gesagt</h2>\n    <p>{e(kurz)}</p>\n  </div>\n</section>')
    a('<section>\n  <h2>Monatspreise nach Reinigungsrhythmus</h2>\n  <div class="tabelle"><table>\n'
      '    <thead><tr><th>Leistung</th><th>Rhythmus</th><th>Objekte</th><th>Median</th><th>Mittlere Hälfte</th></tr></thead>\n    <tbody>')
    for r in sorted(d["zeilen"], key=lambda r: (r["art"] != "unterhalt", list(RHYTHMUS).index(r["intervall"]))):
        hinweis = "*" if r["anzahl"] < 10 else ""
        a(f'      <tr><td>{ART[r["art"]]}</td><td>{RHYTHMUS[r["intervall"]]}</td><td>{r["anzahl"]}{hinweis}</td>'
          f'<td><b>{tausend(r["median"])}</b></td><td>{tausend(r["p25"])} bis {tausend(r["p75"])}</td></tr>')
    a("    </tbody>\n  </table></div>")
    a('  <p class="rechner-fuss">Alle Preise netto pro Monat und Objekt. * Weniger als zehn Angebote, nur ein grober Anhaltspunkt.</p>\n</section>')
    a('<section class="text">\n  <h2>So lesen Sie die Tabelle</h2>')
    a(f'  <p><strong>Median</strong> heißt: Die Hälfte der Angebote lag darunter, die andere Hälfte darüber. Einzelne sehr große '
      f'Objekte verzerren ihn kaum, anders als einen Durchschnitt. <strong>Mittlere Hälfte</strong> heißt: Jedes zweite Angebot '
      f'lag in diesem Bereich, bei einer Reinigung pro Woche also zwischen {tausend(u1["p25"])} und {tausend(u1["p75"])}.</p>')
    a('  <p>Den größten Einfluss auf den Preis hat die Fläche, danach kommen Nutzung und Rhythmus. Ein kleines Büro mit '
      'einem Termin pro Woche liegt am unteren Rand, eine Praxis mit viel Publikumsverkehr eher am oberen.</p>')
    a('  <p>Dass zwei Termine pro Woche mehr als das Doppelte kosten, liegt nicht am Rhythmus selbst: Objekte, die öfter '
      'gereinigt werden, sind meist auch größer. In den Zeilen stecken also unterschiedliche Objekte, nicht dasselbe Büro '
      'mit mehr Terminen. Für Ihr Objekt rechnet unser <a href="rechner.html">Rechner</a> mit den Stundensätzen aus der '
      '<a href="preise.html">Preisliste</a>.</p>\n</section>')
    a('<section class="text">\n  <h2>Was im Preis enthalten ist</h2>')
    a('  <p>Alle Preise sind netto. Reinigungsmittel, Wasseraufbereitung und die Anfahrt sind enthalten, Verbrauchsmaterial wie '
      'Toilettenpapier, Seife und Handtücher stellt in der Regel der Kunde. Seit November 2026 nehmen wir Unterhaltsreinigung '
      'erst ab 280 € netto im Monat je Objekt an. Einige ältere Angebote in der Auswertung liegen darunter.</p>\n</section>')
    a('<section class="text">\n  <h2>So haben wir gerechnet</h2>\n  <ul>')
    for punkt in [
        f"Grundlage sind alle Angebote aus unserer Buchhaltung (sevDesk) von {zeitraum}, ohne Entwürfe.",
        "Gezählt haben wir nur monatliche Pauschalpreise der Hauptleistung, ohne Zusatz-, Bedarfs- und Optionspositionen.",
        f"Je Objekt zählt nur das neueste Angebot, insgesamt {d['objekte']} Objekte. Gezählt sind angebotene Preise, nicht nur beauftragte.",
        f"{d['plz_koeln_umland']} der {d['plz_mit_angabe']} Objekte mit Postleitzahl liegen im Raum Köln (PLZ 50 und 51), "
        f"{d['plz_bonn']} im Raum Bonn (PLZ 53).",
        "Rhythmen mit weniger als fünf Angeboten zeigen wir nicht. Kundennamen und Adressen stehen nicht in der Auswertung.",
    ]:
        a(f"    <li>{e(punkt)}</li>")
    a("  </ul>\n  <p>Wir aktualisieren den Preisspiegel, wenn genug neue Angebote dazugekommen sind. Wer die Zahlen zitiert, "
      "nennt bitte Clean Connect und den Stand.</p>\n</section>")
    a('<section>\n  <div class="cta-box">\n    <h2>Was kostet es für Ihr Objekt?</h2>\n    <p>Mit Fläche, Nutzung und Rhythmus '
      'schreiben wir Ihnen innerhalb von 24 Stunden ein Angebot, auf Wunsch nach einer kostenlosen Besichtigung.</p>\n'
      '    <a href="./#kontakt" class="btn btn-p">Kostenloses Angebot &rarr;</a>\n  </div>\n</section>')
    teile += fuss()
    schreibe(os.path.join(ROOT, "preisspiegel.html"), "\n".join(teile), geaendert)


REFERENZEN = ["Harley-Davidson Köln-Bonn", "Rettig GmbH", "Kraus Bäckereien", "SAE Institute", "Novalis", "Bullhaus Köln"]


def team_seite(basis_css, geaendert):
    """team.html: wer hinter Clean Connect steht, Autorenprofil der Ratgeber (04.11.2026)."""
    canonical = f"{BASE}/team.html"
    titel = "Team und Geschäftsführung | Clean Connect Köln"
    meta = ("Clean Connect wurde 2024 von Fynn Laubkermeier in Köln gegründet. Wer das Unternehmen führt, wer Sie betreut "
            "und wer bei Ihnen reinigt.")
    fynn = {"@type": "Person", "@id": f"{BASE}/team.html#fynn-laubkermeier", "name": "Fynn Laubkermeier",
            "jobTitle": "Gründer und Geschäftsführer", "image": f"{BASE}/images/fynn-laubkermeier-geschaeftsfuehrer-clean-connect.webp", "worksFor": {"@id": f"{BASE}/#business"}}
    schema = {"@context": "https://schema.org", "@graph": [
        {"@type": "AboutPage", "name": titel, "url": canonical, "inLanguage": "de-DE", "dateModified": "2026-11-04",
         "mainEntity": {"@id": f"{BASE}/#business"}, "isPartOf": {"@type": "WebSite", "url": f"{BASE}/"}},
        fynn,
        {"@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Start", "item": f"{BASE}/"},
            {"@type": "ListItem", "position": 2, "name": "Team", "item": canonical}]},
    ]}
    teile = kopf(titel, meta, canonical, schema, basis_css, zurueck=("./", "Startseite"))
    a = teile.append
    teile += hero("Über uns", "Wer hinter <em>Clean Connect</em> steht",
                  "Clean Connect ist ein inhabergeführter Reinigungsdienst aus Köln. Gegründet 2024 von Fynn Laubkermeier, "
                  "heute mit mehr als 20 fest angestellten, deutschsprachigen Mitarbeitenden und einem Büro mit Lager in Köln-Rath/Heumar.")
    a('<section>\n  <h2>Geschäftsführung und Kundenbetreuung</h2>')
    a('  <div class="person" id="fynn-laubkermeier">\n    <img src="images/fynn-laubkermeier-geschaeftsfuehrer-clean-connect.webp" width="500" height="500" alt="Fynn Laubkermeier" loading="lazy">\n'
      '    <div><h3>Fynn Laubkermeier</h3><span class="rolle">Gründer und Geschäftsführer</span>\n'
      '    <p>Fynn hat Clean Connect 2024 gegründet. Vorher hat das Team als Subunternehmer bei verschiedenen Reinigungsdienstleistern '
      'gearbeitet und gesehen, woran es dort oft hakt: wenig Kommunikation, wechselndes Personal, keine echte Kontrolle. Als '
      'Geschäftsführer steht Fynn persönlich für jeden Auftrag ein.</p></div>\n  </div>')
    a('  <div class="person" id="kundenbetreuung">\n    <div class="ico"><svg viewBox="0 0 24 24" width="52" height="52" fill="none" stroke="#00C5C4" '
      'stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M3 14v-2a9 9 0 0 1 18 0v2"/>'
      '<path d="M21 15a2 2 0 0 1-2 2h-1v-6h1a2 2 0 0 1 2 2z"/><path d="M3 15a2 2 0 0 0 2 2h1v-6H5a2 2 0 0 0-2 2z"/>'
      '<path d="M18 17v1a3 3 0 0 1-3 3h-3"/></svg></div>\n    <div><h3>Kundenbetreuung</h3><span class="rolle">Angebote, Verträge, laufende Objekte</span>\n'
      '    <p>Von der ersten Anfrage bis zum laufenden Vertrag haben Sie einen festen Ansprechpartner im Büro. Er schreibt '
      'Ihr Angebot und das Leistungsverzeichnis und ist direkt erreichbar unter <a href="tel:+4915792492755">0157 92492755</a> '
      'oder <a href="mailto:service@cleanconnect.de">service@cleanconnect.de</a>. Unsere <a href="blog/index.html">Ratgeber</a> '
      'und den <a href="preisspiegel.html">Preisspiegel</a> schreibt das Büroteam aus der eigenen Praxis.</p></div>\n  </div>\n</section>')
    a('<section class="text">\n  <h2>Das Team</h2>\n  <ul>')
    for punkt in ["Mehr als 20 Mitarbeitende, alle fest und sozialversicherungspflichtig angestellt, keine Subunternehmer.",
                  "Alle deutschsprachig und persönlich eingearbeitet.",
                  "Jedes Objekt hat ein festes Team. Fällt jemand aus, übernimmt eine Vertretung aus demselben Team.",
                  "Mitarbeitende und Unternehmen sind haftpflichtversichert."]:
        a(f"    <li>{e(punkt)}</li>")
    a("  </ul>\n</section>")
    if PRAXIS:
        a('<section id="praxis">\n  <h2>Aus der Praxis</h2>')
        a("\n".join(fall_html(f) for f in PRAXIS[:3]))
        a(f'  <p class="fall-mehr"><a href="vorher-nachher.html">Alle {len(PRAXIS)} Vorher/Nachher-Beispiele ansehen &rarr;</a></p>\n</section>')
    a('<section class="text">\n  <h2>Standort, Kunden und Engagement</h2>')
    a('  <p>Unser Büro und Lager liegen in der <strong>Forststraße 33, 51107 Köln</strong> (Rath/Heumar). Firmensitz laut '
      '<a href="impressum.html">Impressum</a> ist die Berliner Straße 957 in Köln, eingetragen beim Amtsgericht Köln unter HRB 119725.</p>')
    a(f'  <p>Zu unseren Kunden zählen {e(", ".join(REFERENZEN[:-1]))} und {e(REFERENZEN[-1])}. Bei Google haben wir 27 Bewertungen, '
      'im Schnitt 4,96 von 5 Sternen (Stand November 2026, <a href="https://www.google.com/maps?cid=6656574569178855580">Google-Profil</a>).</p>')
    a('  <p>Wir unterstützen den Jugendfußball beim RSV Rath/Heumar 1920 e.V.</p>\n</section>')
    a(cta_box().replace("Ihre Frage war nicht dabei?", "Lernen Sie uns kennen"))
    teile += fuss()
    schreibe(os.path.join(ROOT, "team.html"), "\n".join(teile), geaendert)


def vorher_nachher_seite(basis_css, geaendert):
    """vorher-nachher.html: alle Vorher/Nachher-Paare aus praxis.py, nach Leistung (06.11.2026)."""
    canonical = f"{BASE}/vorher-nachher.html"
    titel = "Vorher und nachher: Reinigung in Köln | Clean Connect"
    meta = (f"{len(PRAXIS)} Vorher/Nachher-Beispiele aus unseren eigenen Einsätzen: Bauendreinigung, Grundreinigung, "
            "Gastronomie, Glas, Sanitär und Fassade. Echte Fotos, keine Bilddatenbank.")
    gruppen = {}
    for f in PRAXIS:
        gruppen.setdefault(f["leistung"], []).append(f)
    bilder = [{"@type": "ImageObject", "contentUrl": f"{BASE}/images/praxis/{datei}", "name": f"{f['titel']} ({BILD_ART[k]})",
               "caption": f"{BILD_ART[k]}: {f['bildtext']}", "creator": {"@id": f"{BASE}/#business"},
               "copyrightHolder": {"@id": f"{BASE}/#business"}} for f in PRAXIS for datei, k in fall_bilder(f)]
    schema = {"@context": "https://schema.org", "@graph": [
        {"@type": "CollectionPage", "name": titel, "description": meta, "url": canonical, "inLanguage": "de-DE",
         "dateModified": "2026-11-06", "about": {"@id": f"{BASE}/#business"}, "isPartOf": {"@type": "WebSite", "url": f"{BASE}/"},
         "primaryImageOfPage": bilder[1]["contentUrl"], "hasPart": bilder},
        {"@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Start", "item": f"{BASE}/"},
            {"@type": "ListItem", "position": 2, "name": "Vorher und nachher", "item": canonical}]},
    ]}
    teile = kopf(titel, meta, canonical, schema, basis_css, zurueck=("./", "Startseite"))
    a = teile.append
    teile += hero("Aus unserer Arbeit", "Vorher und <em>nachher</em>",
                  "Diese Fotos haben unsere Teams bei eigenen Einsätzen gemacht. Kundennamen und Adressen zeigen wir nicht, "
                  "die Fotos sind unbearbeitet und nur verkleinert.")
    a('<section>\n  <div class="chips">' + "".join(f'<a href="#{anker(g)}">{e(g)}</a>' for g in gruppen) + "</div>\n</section>")
    for g, faelle in gruppen.items():
        a(f'<section id="{anker(g)}">\n  <h2>{e(g)}</h2>')
        a("\n".join(fall_html(f) for f in faelle))
        a("</section>")
    a(cta_box().replace("Ihre Frage war nicht dabei?", "Wie sieht es bei Ihnen aus?"))
    teile += fuss()
    schreibe(os.path.join(ROOT, "vorher-nachher.html"), "\n".join(teile), geaendert)


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


EIGENE_SEITEN = ["rechner.html", "fragen.html", "preisspiegel.html", "team.html", "vorher-nachher.html"]


def bilder_in_sitemap(s):
    """Bild-Sitemap fuer Google Bilder: je Seite die eingebundenen Fotos (ohne Logos),
    gelesen aus der fertigen HTML-Datei. Wird bei jedem Lauf neu geschrieben (09.11.2026)."""
    s = re.sub(r"\s*<image:image>.*?</image:image>", "", s, flags=re.S)
    if "xmlns:image" not in s:
        s = s.replace('<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">',
                      '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" '
                      'xmlns:image="http://www.google.com/schemas/sitemap-image/1.1">')

    def fuellen(m):
        block = m.group(0)
        loc = re.search(r"<loc>([^<]+)</loc>", block).group(1)
        rel = loc[len(BASE) + 1:] or "index.html"
        pfad = os.path.join(ROOT, rel)
        if not os.path.isfile(pfad):
            return block
        html = open(pfad, encoding="utf-8").read()
        urls = []
        for src in re.findall(r'<img[^>]+?src="([^"]+)"', html):
            if src.startswith(("data:", "http")) or "logo" in src:
                continue
            ziel = os.path.normpath(os.path.join(os.path.dirname(rel), src))
            gross = ziel.replace("-560.", ".")
            if gross != ziel and os.path.isfile(os.path.join(ROOT, gross)):
                ziel = gross
            url = f"{BASE}/{ziel}"
            if url not in urls:
                urls.append(url)
        if not urls:
            return block
        bilder = "".join(f"\n    <image:image><image:loc>{u}</image:loc></image:image>" for u in urls)
        return block.replace("\n  </url>", bilder + "\n  </url>")

    return re.sub(r"  <url>.*?\n  </url>", fuellen, s, flags=re.S)


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
    for rel in EIGENE_SEITEN:
        loc = f"{BASE}/{rel}"
        if loc in s:
            s = re.sub(r"(<loc>" + re.escape(loc) + r"</loc>\s*<lastmod>)[^<]+", lambda m: m.group(1) + datum(rel), s)
        else:
            s = s.replace("</urlset>", f"  <url>\n    <loc>{loc}</loc>\n    <lastmod>{heute}</lastmod>\n    <changefreq>monthly</changefreq>\n    <priority>0.8</priority>\n  </url>\n</urlset>")
    s = bilder_in_sitemap(s)
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
    fragen_seite(basis_css, geaendert)
    preisspiegel_seite(basis_css, geaendert)
    team_seite(basis_css, geaendert)
    vorher_nachher_seite(basis_css, geaendert)
    aktualisiere_hub(geaendert)
    aktualisiere_sitemap(heute, geaendert)
    print(f"{n} Seiten gebaut, davon {len(geaendert)} Dateien geaendert, sitemap.xml aktualisiert")


if __name__ == "__main__":
    main()
