"""Vorher/Nachher aus eigenen Einsätzen für vorher-nachher.html, /team.html und die Standortseiten (06.11.2026).

Nur eigene Fotos, von Julian freigegeben, ohne Kundennamen, Personen oder Firmenschilder.
Bilder als WebP ohne Metadaten (kein GPS) nach images/praxis/ legen, 800 px breit:
  cwebp -q 78 -metadata none -resize 800 0 <quelle> -o images/praxis/<name>.webp
Texte beschreiben nur, was auf den Fotos zu sehen ist. Ort und Zeitraum nur eintragen,
wenn sie belegt sind, sonst None lassen.

Felder je Fall:
  titel       kurze Überschrift
  objekt      Art des Objekts
  leistung    Leistung als Text
  leistungen  Schlüssel aus leistungen.py; dort erscheint das Paar auf allen Standortseiten
  ort, seit   Stadt bzw. Zeitpunkt oder None
  aufgabe     1-2 Sätze: Was war vorher?
  ergebnis    1-2 Sätze: Was ist nachher anders?
  vorher, nachher  Dateiname in images/praxis/
  bilder      optional statt vorher/nachher: [(datei, "vorher"|"nachher"|"einsatz"), ...], bis zu drei
  ergebnis_label  optional, Standard "Nachher" (z. B. "Im Einsatz", wenn kein Nachher-Foto da ist)
  format      "hoch" oder "quer" (Seitenverhältnis der Fotos)
  bildtext    ehrliche Beschreibung, was auf den Fotos zu sehen ist
"""

PRAXIS = [
    # Mitarbeitende auf den Fotos haben eingewilligt (laut Julian 06.11.2026, AV und Datenschutzerklärung unterschrieben)
    {"titel": "Grundreinigung im Café", "objekt": "Gastraum eines Cafés mit Boden in Betonoptik", "leistung": "Grundreinigung",
     "leistungen": ["grundreinigung"], "ort": None, "seit": None,
     "aufgabe": "Flecken, Laufspuren und ein grauer Schmutzfilm auf dem ganzen Boden im Gastraum.",
     "ergebnis_label": "Im Einsatz",
     "ergebnis": "Boden mit der Einscheibenmaschine geschrubbt, Schmutzwasser mit dem Nasssauger aufgenommen. Ein Nachher-Foto gibt es von diesem Einsatz nicht.",
     "bilder": [("grundreinigung-cafe-boden-vorher.webp", "vorher"), ("grundreinigung-cafe-boden-einscheibenmaschine.webp", "einsatz"), ("grundreinigung-cafe-boden-nasssauger.webp", "einsatz")],
     "format": "hoch",
     "bildtext": "Café-Boden in Betonoptik, vorher fleckig, dann bei der Grundreinigung mit Einscheibenmaschine und Nasssauger"},
    {"titel": "Bürofläche nach dem Umbau", "objekt": "Bürofläche mit Teppichboden", "leistung": "Bauendreinigung",
     "leistungen": ["bauendreinigung"], "ort": None, "seit": None,
     "aufgabe": "Nach den Malerarbeiten lagen Abdeckvlies, Bauschutt, Werkzeug und Putzreste auf dem Teppich.",
     "ergebnis": "Fläche geräumt, Reste entsorgt, Teppich gründlich gesaugt. Die Räume waren danach bezugsfertig.",
     "vorher": "bauendreinigung-bueroflur-vorher.webp", "nachher": "bauendreinigung-bueroflur-nachher.webp", "format": "hoch",
     "bildtext": "Büroflur mit Glaswänden, vorher mit Abdeckvlies und Bauresten, nachher leer und gesaugt"},
    {"titel": "Teppich voller Putz- und Farbreste", "objekt": "Büroeingang mit dunklem Teppichboden", "leistung": "Bauendreinigung",
     "leistungen": ["bauendreinigung"], "ort": None, "seit": None,
     "aufgabe": "Weiße Putz- und Farbspritzer, Staub und Kabelreste im ganzen Eingangsbereich.",
     "ergebnis": "Spritzer entfernt und Teppich gesaugt, die Fläche wirkt wieder einheitlich dunkel.",
     "vorher": "bauendreinigung-teppichboden-buero-vorher.webp", "nachher": "bauendreinigung-teppichboden-buero-nachher.webp", "format": "quer",
     "bildtext": "Dunkler Teppich an einer Glastür, vorher mit weißen Putzresten, nachher sauber"},
    {"titel": "Granittreppe nach den Bauarbeiten", "objekt": "Treppenhaus in einem Bürogebäude", "leistung": "Bauendreinigung",
     "leistungen": ["bauendreinigung", "treppenhausreinigung"], "ort": None, "seit": None,
     "aufgabe": "Baustaub, Bauabfall und Schmutzstreifen auf Stufen und Setzstufen.",
     "ergebnis": "Stufen nass gereinigt, Setzstufen abgewischt. Der Granit glänzt wieder.",
     "vorher": "bauendreinigung-granittreppe-vorher.webp", "nachher": "bauendreinigung-granittreppe-nachher.webp", "format": "hoch",
     "bildtext": "Granittreppe mit grauen Setzstufen, vorher staubig mit Abfall, nachher sauber und glänzend"},
    {"titel": "Atrium vor der Übergabe", "objekt": "Atrium eines Bürogebäudes mit grünem Bodenbelag", "leistung": "Bauendreinigung",
     "leistungen": ["bauendreinigung"], "ort": None, "seit": None,
     "aufgabe": "Folienreste, Klebeband, Papier und Kleinteile verteilt über die ganze Fläche.",
     "ergebnis": "Alles aufgesammelt und entsorgt, Belag gesaugt. Die Fotos sind zu unterschiedlichen Tageszeiten entstanden.",
     "vorher": "bauendreinigung-atrium-buerogebaeude-vorher.webp", "nachher": "bauendreinigung-atrium-buerogebaeude-nachher.webp", "format": "hoch",
     "bildtext": "Großes Atrium mit grünem Belag, vorher mit Abfall, nachher leer"},
    {"titel": "Fliesenboden in einer Gewerbeküche", "objekt": "Spülküche eines Gastronomiebetriebs", "leistung": "Grundreinigung",
     "leistungen": ["grundreinigung"], "ort": None, "seit": None,
     "aufgabe": "Grauer Schmutzfilm auf den Fliesen, dunkle Fugen, Essensreste unter den Regalen.",
     "ergebnis": "Boden gründlich gereinigt, auch unter den Regalen. Die Fugen sind wieder hell.",
     "vorher": "grundreinigung-gewerbekueche-fliesenboden-vorher.webp", "nachher": "grundreinigung-gewerbekueche-fliesenboden-nachher.webp", "format": "hoch",
     "bildtext": "Rutschhemmender Fliesenboden einer Küche, vorher verschmutzt, nachher frisch gereinigt"},
    {"titel": "WC mit Ablagerungen", "objekt": "Sanitärraum in einem Büro", "leistung": "Sanitärreinigung",
     "leistungen": ["grundreinigung", "unterhaltsreinigung", "bueroreinigung"], "ort": None, "seit": None,
     "aufgabe": "Dunkle Ablagerungen in der Spülrinne unter dem Rand.",
     "ergebnis": "Ablagerungen entfernt, die Keramik ist wieder durchgehend weiß.",
     "vorher": "sanitaerreinigung-wc-buero-vorher.webp", "nachher": "sanitaerreinigung-wc-buero-nachher.webp", "format": "hoch",
     "bildtext": "Wand-WC von oben, vorher mit dunklen Streifen in der Spülrinne, nachher sauber"},
    {"titel": "Spüle in der Teeküche", "objekt": "Teeküche in einem Büro", "leistung": "Büroreinigung",
     "leistungen": ["unterhaltsreinigung", "bueroreinigung"], "ort": None, "seit": None,
     "aufgabe": "Kalk- und Rostränder um den Abfluss, Ablagerungen im Becken.",
     "ergebnis": "Becken und Sieb von Kalk und Rost befreit, Edelstahl trocken gewischt.",
     "vorher": "bueroreinigung-teekueche-spuele-vorher.webp", "nachher": "bueroreinigung-teekueche-spuele-nachher.webp", "format": "hoch",
     "bildtext": "Edelstahlspüle mit Mischbatterie, vorher mit Kalk- und Rosträndern, nachher sauber"},
    {"titel": "Glasdach mit Belag", "objekt": "Glasdach über einem Eingang", "leistung": "Glasreinigung",
     "leistungen": ["glasreinigung"], "ort": None, "seit": None,
     "aufgabe": "Schmutzbelag und Wasserflecken auf allen Scheiben, kaum noch durchsichtig.",
     "ergebnis": "Scheiben und Profile gereinigt. Das Glas ist wieder klar und spiegelt.",
     "vorher": "glasdachreinigung-eingang-vorher.webp", "nachher": "glasdachreinigung-eingang-nachher.webp", "format": "hoch",
     "bildtext": "Glasdach mit Aluminiumprofilen, vorher trüb und fleckig, nachher klar"},
    {"titel": "Fenster mit Schlieren", "objekt": "Fenster in einem Bürogebäude", "leistung": "Glasreinigung",
     "leistungen": ["glasreinigung"], "ort": None, "seit": None,
     "aufgabe": "Schlieren und Schmutz auf der Scheibe, gegen die Sonne deutlich sichtbar.",
     "ergebnis": "Scheibe streifenfrei gereinigt, der Blick nach draußen ist wieder klar.",
     "vorher": "fensterreinigung-buerofenster-vorher.webp", "nachher": "fensterreinigung-buerofenster-nachher.webp", "format": "hoch",
     "bildtext": "Blick durch ein Bürofenster in einen Innenhof, vorher mit Schlieren, nachher klar"},
    {"titel": "Klinkerfassade mit dunklen Verfärbungen", "objekt": "Wohnhaus mit Klinkerfassade", "leistung": "Fassadenreinigung",
     "leistungen": ["fassadenreinigung"], "ort": None, "seit": None,
     "aufgabe": "Großflächige schwarze Verfärbungen auf dem Klinker.",
     "ergebnis": "Fassade gereinigt, der rote Klinker ist wieder sichtbar. Das Nachher-Foto zeigt dieselbe Wand aus einem etwas anderen Winkel.",
     "vorher": "fassadenreinigung-klinkerfassade-vorher.webp", "nachher": "fassadenreinigung-klinkerfassade-nachher.webp", "format": "hoch",
     "bildtext": "Klinkerwand neben einem Tor, vorher schwarz verfärbt, nachher rot"},
]
