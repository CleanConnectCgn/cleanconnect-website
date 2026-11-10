# cleanconnect-website
## Bilder

Neue Bilder mit sprechendem Namen und `cwebp -metadata none` anlegen, Titel in `scripts/standorte/bilder.py` eintragen, dann `python3 scripts/bild_metadaten.py` (setzt Titel, Urheber, Copyright als XMP). Beim Umbenennen eine `RedirectMatch 301`-Zeile in `.htaccess` ergänzen und `build.py` laufen lassen.

## Neue Seiten

Neue Seiten auf oberster Ebene in `deploy.yml` (put) und in der `RedirectMatch`-Zeile für Adressen ohne Endung in `.htaccess` eintragen.
