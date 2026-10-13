#!/usr/bin/env python3
"""Meldet URLs per IndexNow an Bing (und weitere Suchmaschinen), 13.10.2026.

Google nutzt IndexNow nicht - dort reicht die Sitemap in der Search Console.
Aufruf nach einem Deploy:
  python3 scripts/indexnow.py               # alle URLs aus sitemap.xml
  python3 scripts/indexnow.py standorte/    # nur URLs, die den Text enthalten
Der Schluessel liegt als 7a7c3578bc2fb01274f59ee760f00e2a.txt im Webroot (Deploy laedt ihn hoch).
"""
import json, re, sys, urllib.request
KEY = "7a7c3578bc2fb01274f59ee760f00e2a"
HOST = "cleanconnect.de"
urls = re.findall(r"<loc>([^<]+)</loc>", open("sitemap.xml", encoding="utf-8").read())
if len(sys.argv) > 1:
    urls = [u for u in urls if sys.argv[1] in u]
body = json.dumps({"host": HOST, "key": KEY, "keyLocation": f"https://{HOST}/{KEY}.txt", "urlList": urls[:10000]}).encode()
req = urllib.request.Request("https://api.indexnow.org/indexnow", data=body, headers={"Content-Type": "application/json; charset=utf-8"})
with urllib.request.urlopen(req, timeout=30) as r:
    print(r.status, len(urls), "URLs gemeldet")
