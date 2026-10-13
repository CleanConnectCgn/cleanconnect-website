# Zusaetzliche Fragen und Vorteile je Leistung (13.10.2026).
# build.py waehlt je Ort eine andere Auswahl aus faq + faq_extra bzw.
# vorteile + vorteile_extra, damit nicht jede Stadtseite dieselben Bloecke traegt.

FAQ_EXTRA = {
    "unterhaltsreinigung": [
        ("Arbeiten Sie mit eigenem Personal?", "Ja, mit festen Mitarbeitenden, die Ihr Objekt kennen. Wechsel im Team kündigen wir an und arbeiten neue Kräfte vor Ort ein."),
        ("Was passiert, wenn etwas nicht sauber ist?", "Sie melden es Ihrer Ansprechperson per E-Mail oder Telefon. Wir bessern beim nächsten Einsatz nach, bei Sanitärbereichen schon am nächsten Werktag."),
        ("Können wir den Umfang später ändern?", "Ja. Wenn sich Fläche oder Nutzung ändern, passen wir Leistungsverzeichnis und Stundenumfang an, schriftlich und mit neuem Preis."),
        ("Reinigen Sie auch Praxen mit Hygienevorgaben?", "Ja. In Praxen arbeiten wir nach einem Hygieneplan mit getrennten Tüchern für Sanitär und Behandlungsräume. Medizinprodukte bereiten wir nicht auf."),
    ],
    "bueroreinigung": [
        ("Wie wird der Zugang geregelt?", "Über Schlüssel, Transponder oder Code. Die Übergabe dokumentieren wir mit einem Protokoll, und nur das eingeteilte Team hat Zugang."),
        ("Reinigen Sie auch kleine Büros mit nur einem Raum?", "Ja. Auch kleine Büros reinigen wir regelmäßig, der Stundenumfang wird dann entsprechend klein angesetzt."),
        ("Kümmern Sie sich auch um Verbrauchsmaterial?", "Auf Wunsch füllen wir Seife, Papierhandtücher und Toilettenpapier nach. Das Material stellen Sie oder wir rechnen es separat ab."),
        ("Kann die Reinigung über Feiertage ausfallen?", "Ja. Termine an Feiertagen verschieben wir nach Absprache oder lassen sie ausfallen, je nachdem, was Ihnen lieber ist."),
    ],
    "glasreinigung": [
        ("Brauchen wir für die Glasreinigung Strom oder Wasser?", "Wasser bringen wir in der Regel selbst mit. Ein Stromanschluss in der Nähe hilft bei größeren Flächen, ist aber nicht immer nötig."),
        ("Reinigen Sie auch Oberlichter und Glasdächer?", "Ja, sofern wir sie sicher erreichen. Für Glasdächer prüfen wir vorher den Zugang und die nötige Sicherung."),
        ("Was ist mit Aufklebern und Farbspritzern?", "Aufkleber, Farbspritzer und Baurückstände entfernen wir mit Klinge und passenden Mitteln, ohne das Glas zu zerkratzen."),
        ("Müssen wir die Fensterbänke freiräumen?", "Bitte stellen Sie Pflanzen und empfindliche Dinge vor dem Termin zur Seite. Den Rest erledigen wir."),
    ],
    "grundreinigung": [
        ("Wann ist der beste Zeitpunkt für eine Grundreinigung?", "Wenn die Räume leer stehen: in den Ferien, zwischen zwei Mietern oder vor einer Neueröffnung."),
        ("Müssen Möbel ausgeräumt werden?", "Kleine Möbel stellen wir selbst um. Schränke und schwere Möbel sollten vorher leer oder verrückt sein, oder wir planen das Umräumen gesondert ein."),
        ("Riecht es nach der Grundreinigung nach Chemie?", "Kurz nach der Reinigung kann es leicht riechen. Nach dem Lüften ist davon nichts mehr zu merken."),
        ("Machen Sie auch eine Grundreinigung in Wohnungen?", "Ja, zum Beispiel beim Auszug oder vor der Neuvermietung, inklusive Küche und Bad."),
    ],
    "treppenhausreinigung": [
        ("Wer stellt die Reinigungsmittel?", "Wir. Reinigungsmittel und Geräte sind in der Pauschale enthalten. Für Wasser genügt ein Anschluss im Keller oder im Treppenhaus."),
        ("Was passiert bei Mängeln im Haus?", "Defekte Lampen, beschädigte Stufen oder abgestellter Sperrmüll fallen uns zuerst auf. Wir melden das direkt an die Verwaltung."),
        ("Reinigen Sie auch die Treppenhausfenster?", "Die Fenster im Treppenhaus reinigen wir innen nach Absprache mit, außen als Zusatzleistung."),
        ("Kann der Vertrag mit dem Verwalterwechsel weiterlaufen?", "Ja. Wechselt die Verwaltung, übertragen wir den Vertrag auf den neuen Ansprechpartner."),
    ],
    "bauendreinigung": [
        ("Wie viele Reinigungsdurchgänge sind nötig?", "Meist zwei: eine Grobreinigung nach dem Ende der Arbeiten und eine Feinreinigung kurz vor Übergabe. Bei kleinen Projekten reicht ein Durchgang."),
        ("Brauchen Sie Strom und Wasser auf der Baustelle?", "Ja. Ohne Strom und Wasser lässt sich eine Endreinigung nicht ordentlich machen; das klären wir vorher mit der Bauleitung."),
        ("Entfernen Sie auch Silikon- und Farbreste?", "Ja, von Fliesen, Fenstern und Sanitärobjekten. Bei empfindlichen Oberflächen testen wir vorher."),
        ("Können Sie kurzfristig einspringen?", "Oft ja, wenn der Termin sich verschiebt. Je früher wir das Datum kennen, desto sicherer ist es eingeplant."),
    ],
    "winterdienst": [
        ("Was kostet Winterdienst ungefähr?", "Das hängt von der Fläche und der Zahl der Einsätze ab. Üblich ist eine monatliche Bereitschaftspauschale plus ein Preis je Einsatz; das Angebot bekommen Sie nach Besichtigung."),
        ("Wann beginnt die Saison?", "In der Regel vom 1. November bis 31. März. Bei frühem Wintereinbruch können wir auch früher starten."),
        ("Räumen Sie auch am Wochenende und an Feiertagen?", "Ja. Schnee und Glätte richten sich nicht nach Bürozeiten, unsere Einsätze auch nicht."),
        ("Muss ich Streugut bereitstellen?", "Nein. Streugut bringen wir mit; es ist im Einsatzpreis enthalten."),
    ],
    "photovoltaikreinigung": [
        ("Wann im Jahr ist die Reinigung sinnvoll?", "Im Frühjahr nach Pollenflug und Winter, damit die Module zur ertragsstarken Zeit sauber sind. Bei starker Verschmutzung auch im Herbst."),
        ("Reinigen Sie auch große Gewerbeanlagen?", "Ja. Für große Flächen planen wir mehrere Tage und arbeiten abschnittsweise, damit der Betrieb weiterläuft."),
        ("Muss die Anlage abgeschaltet werden?", "Nein, eine Reinigung mit Wasser und weichen Bürsten ist im Betrieb möglich. Bei Schäden an Kabeln oder Modulen halten wir an und melden uns."),
        ("Merkt man den Unterschied im Ertrag?", "Bei stark verschmutzten Modulen ja. Ob sich die Reinigung lohnt, sehen Sie am besten am Ertrag vor und nach dem Termin."),
    ],
    "entruempelung": [
        ("Wie schnell kann geräumt werden?", "Nach der Besichtigung meist innerhalb von ein bis zwei Wochen, in dringenden Fällen auch schneller."),
        ("Übernehmen Sie Haushaltsauflösungen?", "Ja, auch komplette Wohnungen oder Häuser, zum Beispiel nach einem Umzug ins Pflegeheim."),
        ("Was ist mit Sondermüll wie Farben oder Chemikalien?", "Farben, Öle und Chemikalien trennen wir aus und geben sie bei den zuständigen Sammelstellen ab. Dafür kann ein Aufpreis anfallen."),
        ("Brauchen Sie eine Halteverbotszone?", "Wenn vor dem Haus kein Platz für Transporter oder Container ist, beantragen wir eine Halteverbotszone bei der Stadt."),
    ],
    "fassadenreinigung": [
        ("Wie lange dauert eine Fassadenreinigung?", "Ein Einfamilienhaus schaffen wir meist an einem Tag, größere Gebäude in mehreren Abschnitten."),
        ("Bleiben Fenster und Pflanzen geschützt?", "Ja. Fenster, Türen und Beete decken wir ab, bevor wir anfangen."),
        ("Reinigen Sie auch Graffiti?", "Graffiti entfernen wir je nach Untergrund. Ob die Fläche ohne Schatten sauber wird, zeigt eine Probefläche."),
        ("Welche Jahreszeit ist am besten?", "Frühjahr bis Herbst bei trockenem Wetter und Temperaturen über dem Gefrierpunkt."),
    ],
    "teppichreinigung": [
        ("Muss der Raum leer sein?", "Stühle und Papierkörbe räumen wir selbst um. Schwere Möbel bleiben stehen, darunter reinigen wir nur, wenn sie vorher verrückt werden."),
        ("Reinigen Sie auch einzelne Teppiche?", "Auf Wunsch ja, vor Ort. Sehr wertvolle Orientteppiche geben wir an eine Fachwäscherei."),
        ("Schadet die Reinigung dem Teppich?", "Nein. Wir prüfen vorher das Material und arbeiten mit passender Temperatur und mildem Reiniger."),
        ("Hilft die Reinigung gegen Allergene?", "Sprühextraktion holt Staub, Milbenrückstände und Pollen aus den Fasern, besser als normales Saugen."),
    ],
    "polsterreinigung": [
        ("Reinigen Sie auch Autositze oder Matratzen?", "Matratzen auf Anfrage. Autositze gehören nicht zu unserem Angebot."),
        ("Was ist mit Wasserflecken nach der Reinigung?", "Wir arbeiten mit kontrollierter Feuchtigkeit und saugen sie direkt wieder ab, damit keine Ränder entstehen."),
        ("Können Sie Gerüche wie Rauch entfernen?", "Gerüche lassen sich deutlich reduzieren. Ob sie ganz verschwinden, hängt davon ab, wie tief sie im Material sitzen."),
        ("Lohnt sich das statt neuer Stühle?", "Bei gut erhaltenen Möbeln fast immer. Eine Reinigung kostet nur einen Bruchteil von neuen Stühlen."),
    ],
}

VORTEILE_EXTRA = {
    "unterhaltsreinigung": [("Erstreinigung zum Testen", "Ein echter Einsatz zum Stundensatz, ohne Vertragsbindung."), ("Schriftliche Abnahme", "Monatliche Rechnung mit Leistungsübersicht.")],
    "bueroreinigung": [("Feste Teams", "Dieselben Gesichter, die Ihre Räume und Gewohnheiten kennen."), ("Zusatzleistungen", "Glas, Teppich und Grundreinigung aus einer Hand.")],
    "glasreinigung": [("Ohne Rückstände", "Kein Spülmittel auf dem Glas, das neuen Schmutz anzieht."), ("Fester Turnus", "Wir planen die nächsten Termine selbstständig ein.")],
    "grundreinigung": [("Probe vorab", "Wir testen an einer Stelle, bevor wir die ganze Fläche bearbeiten."), ("Am Stück", "Ein Termin, ein Team, bis alles fertig ist.")],
    "treppenhausreinigung": [("Umlagefähig", "Rechnungen passend für die Betriebskostenabrechnung."), ("Mit Winterdienst", "Auf Wunsch übernehmen wir auch Schnee und Glätte.")],
    "bauendreinigung": [("Mit Bauleitung abgestimmt", "Wir planen den Termin mit Ihrem Bauzeitenplan."), ("Fotodokumentation", "Auf Wunsch mit Fotos für die Abnahme.")],
    "winterdienst": [("Versichert", "Betriebshaftpflicht für Personen- und Sachschäden aus dem Winterdienst."), ("Feste Saison", "Laufzeit November bis März, ohne Kündigung.")],
    "photovoltaikreinigung": [("Vorher-Nachher-Fotos", "Sie sehen, was gereinigt wurde."), ("Schäden fallen auf", "Bei der Reinigung prüfen wir Module und Rahmen auf sichtbare Schäden.")],
    "entruempelung": [("Wertsachen gesichert", "Dokumente und Wertsachen legen wir beiseite."), ("Auch kurzfristig", "Termine oft innerhalb von ein bis zwei Wochen.")],
    "fassadenreinigung": [("Abgedeckt", "Fenster, Türen und Pflanzen werden vorher geschützt."), ("Mit Glasreinigung", "Fassade und Fenster in einem Einsatz.")],
    "teppichreinigung": [("Allergiker-freundlich", "Tiefenreinigung holt Staub und Pollen aus den Fasern."), ("Ehrliche Einschätzung", "Wir sagen vorher, welche Flecken rausgehen.")],
    "polsterreinigung": [("Auch Leder", "Reinigung und Pflege für Ledermöbel auf Anfrage."), ("Mit Teppich kombinierbar", "Polster und Teppich an einem Termin.")],
}

# Zweiter Ortsabschnitt: welche weiteren Facetten je Leistung zusaetzlich gezeigt werden
ZUSATZ_THEMEN = {
    "unterhaltsreinigung": ["handel", "gewerbe"],
    "bueroreinigung": ["lage", "bau"],
    "glasreinigung": ["buero", "bau"],
    "grundreinigung": ["buero", "lage"],
    "treppenhausreinigung": ["lage", "handel"],
    "bauendreinigung": ["wohnen", "besonders"],
    "winterdienst": ["besonders", "handel"],
    "photovoltaikreinigung": ["wohnen", "besonders"],
    "entruempelung": ["bau", "lage"],
    "fassadenreinigung": ["besonders", "wohnen"],
    "teppichreinigung": ["besonders", "gewerbe"],
    "polsterreinigung": ["besonders", "bau"],
}
