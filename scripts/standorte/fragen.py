"""Fragen-Seite /fragen.html (04.11.2026).

Die Fragen sind nicht ausgedacht, sondern gesammelt aus:
  mail  = Rückfragen von Interessenten und Kunden im Inbox-Tool (Clean-Connect-Kampagnen, 2026)
  suche = Suchanfragen aus der Search Console, für die cleanconnect.de angezeigt wurde
  ki    = lange Suchanfragen im Stil von KI-Assistenten (Search Console)
Jede Antwort beginnt mit dem Kern in ein bis zwei Sätzen (Regel aus dem GEO-Vortrag
vom 04.11.2026). Nur Fakten, die auch auf der Website oder in unseren Angeboten
stehen. Neue Fragen hier eintragen und build.py laufen lassen.
"""

STAND = ("2026-11-04", "November 2026")

# (Gruppe, [(Frage, Antwort, (Link, Linktext) oder None, Quelle)])
FRAGEN = [
    ("Kosten und Preise", [
        ("Was kostet eine Reinigungsfirma pro Stunde in Köln?",
         "Bei uns kostet die Unterhalts- und Büroreinigung 32 € netto pro Stunde, die Grundreinigung 38 € und die "
         "Glasreinigung 45 €. Die Anfahrt ist immer inklusive. Für Einsätze nachts sowie an Sonn- und Feiertagen gibt es "
         "einen Zuschlag, der vorher im Angebot steht.",
         ("preise.html", "Alle Preise"), "suche"),
        ("Was kostet Unterhaltsreinigung im Monat?",
         "Bei einer Reinigung pro Woche lag die Hälfte unserer Angebote zwischen 303 und 694 € netto im Monat, der Median "
         "bei 404 €. Bei zwei Terminen pro Woche lag der Median bei 971 €. Unter 280 € netto im Monat je Objekt nehmen wir "
         "keine Unterhaltsreinigung an, weil Verwaltung, Material und Anfahrt sonst nicht gedeckt sind.",
         ("preisspiegel.html", "Preisspiegel aus 113 Angeboten"), "mail"),
        ("Was kostet Treppenhausreinigung?",
         "Für ein Treppenhaus berechnen wir eine feste Monatspauschale von 120 bis 300 € netto. Ein Treppenhaus mit vier "
         "Etagen, wöchentlich gereinigt, liegt bei rund 195 € netto im Monat. Wo Ihr Haus in der Spanne liegt, hängt "
         "von Etagen, Parteien und Rhythmus ab.",
         ("standorte/treppenhausreinigung-koeln.html", "Treppenhausreinigung in Köln"), "suche"),
        ("Was kostet Gebäudereinigung pro Quadratmeter?",
         "Wir rechnen nicht pro Quadratmeter, sondern nach Zeit. Unser Rechner geht bei Büros von rund 180 m² pro Stunde aus, "
         "bei Praxen von rund 120 m². Ein Büro mit 200 m² braucht also etwa eine Stunde pro Einsatz, das sind 32 € netto.",
         ("rechner.html", "Zum Rechner"), "suche"),
        ("Sind Reinigungsmittel und Anfahrt im Preis enthalten?",
         "Ja. Reinigungsmittel, Wasseraufbereitung und die Anfahrt sind im Preis enthalten. Verbrauchsmaterial wie "
         "Toilettenpapier, Seife und Handtücher stellen in der Regel Sie.",
         None, "mail"),
        ("Gibt es Zuschläge für Sonn- und Feiertage?",
         "Ja, für Einsätze nachts sowie an Sonn- und Feiertagen gibt es einen Zuschlag. Wie hoch er ist, steht vorher im "
         "Angebot, damit es auf der Rechnung keine Überraschung gibt.",
         None, "mail"),
        ("Was kosten Grundreinigung und Glasreinigung?",
         "Die Grundreinigung kostet 38 € netto pro Stunde, die Glasreinigung 45 €, jeweils mindestens 150 € netto pro Auftrag. "
         "Wie viele Stunden ein Einsatz braucht, klären wir vorher bei einer Besichtigung oder anhand von Fotos.",
         ("preise.html", "Alle Preise"), "suche"),
        ("Sind die Preise netto oder brutto?",
         "Alle Preise auf dieser Website sind Nettopreise. Dazu kommt die gesetzliche Umsatzsteuer, derzeit 19 %.",
         None, "suche"),
        ("Gibt es günstigere Preise für mehrere Objekte?",
         "Ja. Betreuen wir mehrere Häuser oder Standorte für Sie, zum Beispiel als Hausverwaltung, sprechen wir über "
         "Staffelpreise.",
         None, "mail"),
    ]),
    ("Angebot und Start", [
        ("Wie schnell bekomme ich ein Angebot?",
         "Innerhalb von 24 Stunden nach Ihrer Anfrage melden wir uns. Für größere Objekte vereinbaren wir eine kostenlose "
         "Besichtigung und schreiben danach ein Leistungsverzeichnis, in dem jede Leistung mit Rhythmus steht.",
         ("./#kontakt", "Angebot anfragen"), "mail"),
        ("Kann man die Reinigung erst einmal ausprobieren?",
         "Ja, mit einer einmaligen Erstreinigung zum regulären Stundensatz von 32 € netto, Anfahrt inklusive und ohne "
         "Vertrag. Danach wissen beide Seiten, wie viel Zeit Ihr Objekt wirklich braucht, und das Angebot wird genauer.",
         None, "mail"),
        ("Wie lange gilt ein Angebot?",
         "Das Datum steht im Angebot, meist sind es vier bis sechs Wochen.",
         None, "mail"),
        ("Gibt es eine Mindestlaufzeit?",
         "Nein. Die Kündigungsfrist steht im Vertrag, meist sind es drei Monate zum Monatsende. Wir wollen durch Leistung "
         "überzeugen, nicht durch eine lange Bindung.",
         None, "mail"),
        ("Kann man mit 14-täglich anfangen und später erhöhen?",
         "Ja. Viele Kunden starten mit einem Rhythmus und passen ihn nach den ersten Wochen an. Mehr oder weniger Termine "
         "lassen sich mit etwas Vorlauf umstellen, der Preis ändert sich entsprechend.",
         None, "mail"),
        ("Geht auch eine einmalige Reinigung ohne Vertrag?",
         "Ja, Glasreinigung, Grundreinigung und Bauendreinigung buchen Sie auch einmalig ohne Reinigungsvertrag. Der "
         "Mindestauftrag liegt bei 150 € netto.",
         None, "mail"),
    ]),
    ("Ablauf im Alltag", [
        ("Muss jemand anwesend sein, wenn gereinigt wird?",
         "Nein. Die meisten Kunden geben uns einen Schlüssel oder einen Zugangscode, danach reinigen wir eigenständig. "
         "Die Schlüsselübergabe stimmen wir vorher mit Ihnen oder Ihrem Ansprechpartner vor Ort ab.",
         None, "mail"),
        ("Reinigen Sie abends oder am Wochenende?",
         "Ja, bei Büros ist das der Normalfall. Wir kommen vor Arbeitsbeginn, nach Feierabend oder am Wochenende, damit "
         "niemand gestört wird.",
         ("bueroreinigung-koeln.html", "Büroreinigung in Köln"), "mail"),
        ("Was passiert, wenn die Reinigungskraft krank oder im Urlaub ist?",
         "Dann übernimmt eine Vertretung aus unserem festen Team. Ihr Objekt ist bei uns dokumentiert, deshalb weiß auch "
         "die Vertretung, was zu tun ist. Fällt ein Termin auf einen Feiertag, holen wir ihn nach Absprache nach.",
         None, "mail"),
        ("Was gehört zur Unterhaltsreinigung?",
         "Die Unterhaltsreinigung ist die regelmäßige Pflege: Böden wischen oder saugen, Sanitärräume und Küchen reinigen, "
         "Oberflächen abwischen und Müll leeren. Was genau und wie oft, steht im Leistungsverzeichnis Ihres Angebots.",
         ("blog/was-ist-unterhaltsreinigung.html", "Was ist Unterhaltsreinigung?"), "suche"),
        ("Was ist der Unterschied zwischen Unterhaltsreinigung und Grundreinigung?",
         "Die Unterhaltsreinigung hält den Alltag sauber und läuft regelmäßig. Die Grundreinigung ist eine gründliche "
         "Tiefenreinigung, bei der Böden maschinell gereinigt und Ablagerungen entfernt werden, etwa vor einer Eröffnung, "
         "bei einem Mieterwechsel oder einmal im Quartal.",
         ("blog/grundreinigung-wann-faellig.html", "Wann eine Grundreinigung fällig ist"), "suche"),
    ]),
    ("Leistungen", [
        ("Machen Sie auch reine Fenster- und Glasreinigung?",
         "Ja, auch ohne Reinigungsvertrag. Wir reinigen Fenster, Rahmen, Schaufenster und Glasfronten zu 45 € netto pro "
         "Stunde, mindestens 150 € pro Auftrag.",
         ("standorte/glasreinigung-koeln.html", "Glasreinigung in Köln"), "mail"),
        ("Reinigen Sie auch Arztpraxen und Therapieräume?",
         "Ja, Praxen gehören neben Büros, Kanzleien und Läden zu unseren regelmäßigen Objekten. Besondere Anforderungen an "
         "die Hygiene besprechen wir bei der Besichtigung und nehmen sie ins Leistungsverzeichnis auf.",
         None, "mail"),
        ("Was gehört zur Treppenhausreinigung?",
         "Üblich sind Stufen und Podeste kehren und feucht wischen, Handläufe abwischen, Eingangsbereich und Briefkästen "
         "reinigen sowie Fingerabdrücke an Türen und Glas entfernen. Fenster, Heizkörper, Keller oder Aufzug kommen oft "
         "zusätzlich dazu und sollten schriftlich festgehalten werden.",
         ("blog/treppenhausreinigung-leistungen.html", "Leistungen der Treppenhausreinigung"), "suche"),
        ("Wie oft sollte ein Treppenhaus gereinigt werden?",
         "In Mehrfamilienhäusern sind wöchentlich oder alle 14 Tage üblich. Wöchentlich lohnt sich bei vielen Parteien, "
         "Kindern, Haustieren oder Gewerbe im Haus, in kleinen, ruhigen Häusern reichen oft 14 Tage.",
         ("blog/treppenhausreinigung-wie-oft.html", "Wie oft das Treppenhaus reinigen?"), "suche"),
        ("Bieten Sie auch Hausmeisterdienst und Grünpflege an?",
         "Ja, zusätzlich zur Reinigung übernehmen wir Kontrollgänge, Reparaturen und den Winterdienst sowie Garten- und "
         "Grünpflege mit Mähen, Heckenschnitt und Beetpflege.",
         ("broschuere.html", "Unsere Broschüre"), "mail"),
    ]),
    ("Hausverwaltung und Winterdienst", [
        ("Arbeiten Sie für Hausverwaltungen und Eigentümergemeinschaften?",
         "Ja, das ist unser Kerngeschäft. Wir übernehmen Treppenhausreinigung, Unterhaltsreinigung und Winterdienst für "
         "Mehrfamilienhäuser und Wohnanlagen, mit festem Ansprechpartner und dokumentierten Einsätzen.",
         None, "mail"),
        ("Bis wann muss in Köln Schnee geräumt sein?",
         "Laut Kölner Satzung werktags bis 7 Uhr und an Sonn- und Feiertagen bis 9 Uhr, und zwar auf 1,5 Metern Breite. "
         "Fällt nach 20 Uhr Schnee, reicht in der Regel der Einsatz am nächsten Morgen.",
         ("blog/winterdienst-koeln-pflicht.html", "Winterdienst in Köln: Wer muss räumen?"), "suche"),
        ("Wird der Winterdienst dokumentiert, etwa für die Versicherung?",
         "Ja, bei jedem Einsatz dokumentieren wir Datum, Uhrzeit und Leistung. Kommt es zu einem Unfall, können Sie oder Ihre "
         "Versicherung so nachweisen, dass geräumt und gestreut wurde.",
         ("standorte/winterdienst-koeln.html", "Winterdienst in Köln"), "mail"),
    ]),
    ("Team und Vertrauen", [
        ("Arbeiten Sie mit Subunternehmern?",
         "Nein. Alle Mitarbeitenden sind bei uns fest und sozialversicherungspflichtig angestellt und haftpflichtversichert. "
         "Auch das Unternehmen selbst ist haftpflichtversichert.",
         None, "mail"),
        ("Sind alle Mitarbeitenden deutschsprachig?",
         "Ja. Absprachen vor Ort, Schlüsselübergaben und Rückmeldungen laufen deshalb ohne Missverständnisse.",
         None, "mail"),
        ("Wer steht hinter Clean Connect?",
         "Clean Connect wurde 2024 von Fynn Laubkermeier in Köln gegründet, er führt das Unternehmen bis heute. Ein fester "
         "Ansprechpartner im Büro betreut die Kunden und schreibt die Angebote. Dazu kommen mehr als 20 feste Mitarbeitende.",
         ("team.html", "Unser Team"), "mail"),
        ("Wie wird Clean Connect bewertet?",
         "Bei Google haben wir 27 Bewertungen, 26 mit fünf Sternen und eine mit vier, im Schnitt 4,96 von 5 "
         "(Stand November 2026).",
         ("https://www.google.com/maps?cid=6656574569178855580", "Bewertungen bei Google"), "ki"),
        ("Woran erkenne ich eine gute Reinigungsfirma?",
         "Fragen Sie nach einem festen Ansprechpartner, festem Personal und fest angestellten Mitarbeitenden ohne "
         "Subunternehmer. Ein gutes Angebot hat ein Leistungsverzeichnis, und eine Probereinigung zeigt die Qualität, "
         "bevor Sie sich binden.",
         ("blog/reinigungsfirma-finden.html", "Reinigungsfirma finden: die richtigen Fragen"), "ki"),
    ]),
    ("Einsatzgebiet", [
        ("Ist Clean Connect eine Firma aus Köln?",
         "Ja. Unser Büro und Lager liegen in der Forststraße 33 in 51107 Köln (Rath/Heumar), Firmensitz laut Impressum ist "
         "die Berliner Straße 957 in Köln.",
         ("impressum.html", "Impressum"), "mail"),
        ("In welchen Städten reinigen Sie?",
         "In ganz Köln und im Umland, unter anderem in Leverkusen, Bergisch Gladbach, Pulheim, Frechen, Hürth, Brühl, "
         "Wesseling, Troisdorf und Bergheim. Größere Objekte übernehmen wir auf Anfrage auch weiter weg, etwa in Wuppertal, "
         "Bonn und Aachen. Deutschlandweit arbeiten wir nicht.",
         ("standorte.html", "Alle Leistungen und Städte"), "mail"),
    ]),
]
