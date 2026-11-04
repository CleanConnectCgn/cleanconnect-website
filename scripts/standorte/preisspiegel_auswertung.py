#!/usr/bin/env python3
"""Wertet unsere sevDesk-Angebote für /preisspiegel.html aus (04.11.2026).

Eingabe: zwei Exporte der sevDesk-API (nur lesen), lokal gespeichert:
  GET /api/v1/Order?orderType=AN&limit=1000        -> orders.json
  GET /api/v1/OrderPos?limit=10000&embed=unity     -> orderpos.json
Aufruf:  python3 scripts/standorte/preisspiegel_auswertung.py orders.json orderpos.json
Ausgabe: scripts/standorte/preisspiegel_daten.json (enthält nur Zahlen, keine Kunden)

Regeln: keine Entwürfe (Status 100), Angebote ab 2025, nur Positionen mit
„Monatlicher Pauschalpreis“, ohne Zusatz-, Options- und Bedarfspositionen.
Je Objekt (Adresse aus dem Positionstext) zählt nur das neueste Angebot.
"""
import collections
import datetime
import json
import os
import re
import statistics
import sys


def intervall(t):
    t = t.lower()
    m = re.search(r"(\d)\s*x\s*(wöchentlich|pro woche)", t)
    if m:
        return f"{m.group(1)}x"
    if re.search(r"14-tägig|14 tägig|zweiwöchentlich|alle 2 wochen|alle zwei wochen", t):
        return "14t"
    if re.search(r"wöchentlich|einmal pro woche", t):
        return "1x"
    return None


def quantil(xs, f):
    xs = sorted(xs)
    i = (len(xs) - 1) * f
    lo = int(i)
    return xs[lo] + (xs[min(lo + 1, len(xs) - 1)] - xs[lo]) * (i - lo)


def main(orders_pfad, pos_pfad):
    orders = {o["id"]: o for o in json.load(open(orders_pfad))["objects"]}
    angebote = collections.defaultdict(lambda: {"summe": 0.0})
    for p in json.load(open(pos_pfad))["objects"]:
        o = orders.get(p["order"]["id"])
        if not o or o["status"] == "100" or (o["orderDate"] or "")[:4] < "2025":
            continue
        text = re.sub(r"\s+", " ", p.get("text") or "")
        tl = ((p.get("name") or "") + " " + text).lower()
        if "monatlicher pauschalpreis" not in tl or re.search(r"nur in verbindung|zusatz|optional|bedarf", tl):
            continue
        art = "treppenhaus" if "treppenh" in tl else ("unterhalt" if re.search(r"unterhalt|büro|praxis", tl) else None)
        if not art:
            continue
        obj = re.search(r"Objekt:\s*([^→]+)", text)
        obj = obj.group(1).strip().lower()[:50] if obj else o["orderNumber"]
        a = angebote[(art, obj, o["id"])]
        a["summe"] += float(p.get("sumNet") or 0)
        a["datum"] = o["orderDate"][:10]
        a["intervall"] = a.get("intervall") or intervall(text)
        plz = re.search(r"\b(\d{5})\b", obj)
        a["plz"] = plz.group(1) if plz else None
    neueste = {}
    for (art, obj, _), a in angebote.items():
        if a["summe"] > 0 and ((art, obj) not in neueste or a["datum"] > neueste[(art, obj)]["datum"]):
            neueste[(art, obj)] = a
    gruppen = collections.defaultdict(list)
    for (art, _), a in neueste.items():
        gruppen[(art, a["intervall"])].append(a["summe"])
    zeilen = []
    for (art, iv), werte in sorted(gruppen.items(), key=lambda kv: (kv[0][0], str(kv[0][1]))):
        if iv is None or len(werte) < 5:
            continue
        zeilen.append({"art": art, "intervall": iv, "anzahl": len(werte), "median": round(statistics.median(werte)),
                       "p25": round(quantil(werte, .25)), "p75": round(quantil(werte, .75))})
    alle = list(neueste.values())
    plz = collections.Counter((a["plz"] or "")[:2] for a in alle if a["plz"])
    daten = {
        "stand": datetime.date.today().isoformat(),
        "objekte": len(alle),
        "von": min(a["datum"] for a in alle),
        "bis": max(a["datum"] for a in alle),
        "plz_mit_angabe": sum(plz.values()),
        "plz_koeln_umland": plz["50"] + plz["51"],
        "plz_bonn": plz["53"],
        "zeilen": zeilen,
    }
    ziel = os.path.join(os.path.dirname(__file__), "preisspiegel_daten.json")
    json.dump(daten, open(ziel, "w"), ensure_ascii=False, indent=1)
    print(json.dumps(daten, ensure_ascii=False, indent=1))


if __name__ == "__main__":
    main(*sys.argv[1:3])
