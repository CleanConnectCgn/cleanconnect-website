"""Praxisbeispiele für /team.html, Abschnitt „Aus der Praxis“ (04.11.2026).

Solange die Liste leer ist, erscheint der Abschnitt nicht. Nur Fälle eintragen,
die Julian freigegeben hat (Kunde einverstanden oder ohne Namen), und nur eigene
Fotos aus dem Objekt. Bilder als WebP nach images/praxis/ legen, 800 px breit.

Felder je Fall:
  titel     kurze Überschrift, z. B. "Treppenhäuser einer Hausverwaltung in Köln-Kalk"
  objekt    Art des Objekts, z. B. "Mehrfamilienhaus, 4 Treppenhäuser"
  ort       Stadt oder Stadtteil
  leistung  z. B. "Treppenhausreinigung wöchentlich, Winterdienst"
  seit      z. B. "2025" (bei Einmalaufträgen das Datum)
  aufgabe   1-2 Sätze: Was war das Problem oder der Auftrag?
  ergebnis  1-2 Sätze: Was haben wir gemacht, was ist heute anders?
  vorher    Dateiname in images/praxis/ oder None
  nachher   Dateiname in images/praxis/ oder None
  bildtext  ehrliche Beschreibung, was auf den Fotos zu sehen ist
"""

PRAXIS = []
