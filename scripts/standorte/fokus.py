# Eigene Inhalte fuer die Standortseiten mit der meisten Nachfrage (04.11.2026).
#
# Auswahl nach Search Console (Einblendungen und Position, Aug.-Nov. 2026).
# Jede Seite bekommt Text, den es nur dort gibt:
#   kurz      die Antwort zuerst, in zwei bis drei Saetzen
#   beispiel  Rechenbeispiel mit denselben Formeln wie standorte/rechner.js
#   fragen    Fragen, die Kunden uns so oder sehr aehnlich gestellt haben
#   praxis    echte Erfahrungen und Objekte aus dieser Stadt - NUR mit
#             Freigabe von Julian/Fynn eintragen, nichts erfinden
#
# Preise nur wie auf preise.html: Unterhalt 32 €, Grund 38 €, Glas 45 € netto
# pro Stunde, Treppenhaus 120-300 € netto pro Monat.

FOKUS = {
    ("treppenhausreinigung", "koeln"): {
        "kurz": "Eine Treppenhausreinigung in Köln kostet bei uns zwischen 120 und 300 € netto im Monat, je nach Etagen, Turnus und Kellerflur. Wir arbeiten vor allem für Hausverwaltungen und Eigentümergemeinschaften, mit festem Reinigungstag und festem Team. Die Besichtigung ist kostenlos, das Angebot kommt innerhalb von 24 Stunden.",
        "beispiel": "Ein Mehrfamilienhaus in Ehrenfeld mit vier Etagen und wöchentlicher Reinigung liegt bei uns bei rund 195 € netto im Monat. Soll der Kellerflur mitgereinigt werden, sind es rund 215 €. Reicht eine Reinigung alle zwei Wochen, landet dasselbe Haus am unteren Ende der Spanne bei 120 €.",
        "fragen": [],
        "praxis": [],
    },
    ("unterhaltsreinigung", "koeln"): {
        "kurz": "Unterhaltsreinigung in Köln kostet bei uns 32 € netto pro Stunde, die Anfahrt ist inklusive. Wie viele Stunden Ihr Objekt braucht, legen wir nach einer kostenlosen Besichtigung oder einer Erstreinigung fest, danach zahlen Sie jeden Monat denselben Betrag. Wir reinigen Büros, Praxen, Läden und Showrooms in allen Kölner Stadtbezirken.",
        "beispiel": "Ein Büro mit 300 m² in der Innenstadt, zweimal pro Woche gereinigt, braucht bei uns etwa 1,75 Stunden je Einsatz. Das sind rund 56 € netto pro Einsatz und rund 485 € netto im Monat.",
        "fragen": [
            ("Wie hoch sind Ihre Stundensätze, und gibt es Zuschläge für Sonn- und Feiertage?",
             "Die Unterhaltsreinigung kostet 32 € netto pro Stunde, die Grundreinigung 38 € und die Glasreinigung 45 €. Für Einsätze nachts oder an Sonn- und Feiertagen gibt es einen Zuschlag. Wie hoch er ist, steht vorher im Angebot, damit Sie nicht überrascht werden."),
        ],
        "praxis": [],
    },
    ("grundreinigung", "koeln"): {
        "kurz": "Eine Grundreinigung in Köln kostet bei uns 38 € netto pro Stunde. Wir übernehmen sie einmalig, etwa vor einer Neueröffnung oder nach einem Mieterwechsel, und auch regelmäßig, zum Beispiel einmal im Quartal. Den Aufwand schätzen wir nach einer Besichtigung oder anhand von Fotos und Quadratmetern.",
        "beispiel": "Eine Ladenfläche mit 300 m² Fliesenboden, die vor einer Neueröffnung stark verschmutzt ist, braucht bei uns etwa 14 Arbeitsstunden. Das sind rund 532 € netto. Bei normaler Verschmutzung wären es etwa 10 Stunden und rund 380 € netto.",
        "fragen": [
            ("Geht eine Grundreinigung auch regelmäßig, zum Beispiel einmal im Quartal oder im Halbjahr?",
             "Ja. Das passt gut, wenn die laufende Reinigung jemand anderes übernimmt oder gar nicht nötig ist, aber zwei- bis viermal im Jahr gründlich sauber gemacht werden soll. Die Termine legen wir gemeinsam im Voraus fest."),
            ("Was brauchen Sie für ein Angebot?",
             "Am schnellsten geht es mit ein paar Fotos, der Quadratmeterzahl und dem Bodenbelag. Wenn möglich, schauen wir uns die Fläche vorher kurz an. Das ist kostenlos."),
        ],
        "praxis": [],
    },
    ("winterdienst", "koeln"): {
        "kurz": "Mit unserem Winterdienst in Köln übernehmen wir die Räum- und Streupflicht für Ihren Gehweg, Zugänge und Parkflächen und dokumentieren jeden Einsatz. Laut Stadt Köln muss der Gehweg in 1,5 Metern Breite geräumt sein, werktags bis 7 Uhr. Den Saisonpreis nennen wir nach einer kurzen Besichtigung.",
        "beispiel": "Ein Grundstück mit 25 Metern Gehweg und 10 m² Zugang zur Haustür ergibt eine Vertragsfläche von rund 48 m². Das erledigen wir in Handarbeit. Erst ab einer größeren Parkfläche setzen wir zusätzlich Maschinen ein.",
        "fragen": [
            ("Können Sie uns ein Beispielangebot für den Winterdienst schicken?",
             "Ja. Schicken Sie uns die Adresse und sagen Sie uns, welche Flächen dazugehören, also Gehweg, Zugänge und eventuell Parkplatz. Dann bekommen Sie ein Angebot mit Bereitschaft und Einsätzen für die ganze Saison."),
        ],
        "praxis": [],
    },
    ("glasreinigung", "koeln"): {
        "kurz": "Glasreinigung in Köln kostet bei uns 45 € netto pro Stunde. Wir reinigen Fenster, Rahmen, Schaufenster und Glasfronten, regelmäßig oder als einzelnen Termin, auch ohne laufenden Reinigungsvertrag. Wie lange es dauert, hängt von der Zahl der Fensterflügel und ihrer Höhe ab.",
        "beispiel": "Eine Anfrage, wie wir sie oft bekommen: 43 Glasflächen im Erdgeschoss, innen und außen. Ohne Rahmen sind das bei uns etwa 4,25 Stunden und rund 191 € netto. Mit Rahmen und Fensterbänken etwa 6 Stunden und rund 270 € netto.",
        "fragen": [
            ("Bieten Sie auch reine Fensterreinigung an, ohne laufende Reinigung?",
             "Ja. Die Glasreinigung buchen Sie bei uns auch einzeln, zum Beispiel ein- oder zweimal im Jahr. Einen Vertrag für die Unterhaltsreinigung brauchen Sie dafür nicht."),
            ("Reinigen Sie auch die Fensterrahmen und Glasdächer, etwa über der Terrasse?",
             "Rahmen und Fensterbänke reinigen wir auf Wunsch mit. Bei Glasdächern hängt es davon ab, wie wir sicher herankommen. Schicken Sie uns am besten ein Foto, dann sagen wir Ihnen, ob es geht und was es kostet."),
        ],
        "praxis": [],
    },
    ("unterhaltsreinigung", "bergheim"): {
        "kurz": "Unterhaltsreinigung in Bergheim kostet bei uns 32 € netto pro Stunde, die Anfahrt aus Köln ist inklusive. Wir reinigen Büros, Praxen und Gewerbeflächen in Bergheim-Mitte, Quadrath-Ichendorf, Kenten und den übrigen Stadtteilen, mit festem Reinigungstag und festem Team. Den Stundenumfang legen wir nach einer kostenlosen Besichtigung fest.",
        "beispiel": "Eine Arztpraxis mit 150 m², dreimal pro Woche gereinigt, braucht bei uns etwa 1,25 Stunden je Einsatz. Das sind rund 40 € netto pro Einsatz und rund 520 € netto im Monat.",
        "fragen": [
            ("Kommen Sie für eine Reinigung extra aus Köln nach Bergheim?",
             "Ja, und die Anfahrt kostet Sie nichts extra. Wir planen Einsätze in Bergheim so, dass dasselbe Team immer an festen Tagen kommt."),
        ],
        "praxis": [],
    },
    ("bueroreinigung", "leverkusen"): {
        "kurz": "Büroreinigung in Leverkusen kostet bei uns 32 € netto pro Stunde, die Anfahrt ist inklusive. Wir reinigen Büros in Wiesdorf, Opladen, Schlebusch und den anderen Stadtteilen, abends oder zu Zeiten, in denen Sie nicht gestört werden. Nach einer kostenlosen Besichtigung bekommen Sie einen festen Monatspreis.",
        "beispiel": "Ein Büro mit 400 m², zweimal pro Woche gereinigt, braucht bei uns etwa 2,25 Stunden je Einsatz. Das sind rund 72 € netto pro Einsatz und rund 624 € netto im Monat.",
        "fragen": [],
        "praxis": [],
    },
    ("polsterreinigung", "wuppertal"): {
        "kurz": "Polsterreinigung in Wuppertal bieten wir nach Stückzahl und Material an, für Bürostühle, Sitzbänke, Sofas und Wartezimmer. Wir reinigen vor Ort mit Sprühextraktion, nach zwei bis vier Stunden sind die Polster wieder trocken. Ab mehreren Möbeln an einem Ort wird es pro Stück günstiger.",
        "beispiel": "Ein Wartezimmer mit zwölf Stühlen und einer Sitzbank braucht bei uns etwa drei Stunden Arbeitszeit. Danach trocknen die Polster zwei bis vier Stunden, am nächsten Morgen ist alles wieder nutzbar.",
        "fragen": [],
        "praxis": [],
    },
    ("treppenhausreinigung", "wuppertal"): {
        "kurz": "Eine Treppenhausreinigung in Wuppertal kostet bei uns zwischen 120 und 300 € netto im Monat, je nach Etagen, Turnus und Kellerflur. In den hohen Altbauten in Elberfeld und Barmen planen wir mehr Zeit für Geländer, Stufen und Podeste ein. Die Anfahrt aus Köln ist im Preis enthalten.",
        "beispiel": "Ein Altbau mit fünf Etagen, wöchentlicher Reinigung und Kellerflur liegt bei uns bei rund 240 € netto im Monat. Ohne Kellerflur sind es rund 220 €.",
        "fragen": [],
        "praxis": [],
    },
    ("teppichreinigung", "bergisch-gladbach"): {
        "kurz": "Teppichreinigung in Bergisch Gladbach bieten wir nach Fläche und Verschmutzung an, für Büros, Praxen und Treppenhäuser mit Teppichboden. Wir arbeiten mit Sprühextraktion, der Boden ist nach vier bis sechs Stunden trocken und am selben Tag wieder begehbar. Zusammen mit einer laufenden Reinigung wird es meist günstiger.",
        "beispiel": "Ein Büro mit 80 m² Teppichboden und deutlichen Laufstraßen braucht bei uns etwa 2,6 Stunden Arbeitszeit. Reinigen wir am Freitagnachmittag, ist der Boden am Montag längst trocken.",
        "fragen": [],
        "praxis": [],
    },
    ("bauendreinigung", "huerth"): {
        "kurz": "Eine Bauendreinigung in Hürth kalkulieren wir nach Aufwand, denn Feinstaub, Farbreste und Folien sind auf jeder Baustelle anders. Das Angebot bekommen Sie nach einer Besichtigung oder anhand von Fotos. Wir planen den Termin so, dass Sie pünktlich übergeben oder einziehen können.",
        "beispiel": "Eine Wohnung oder Büroeinheit mit 120 m² nach dem Innenausbau braucht bei uns etwa 11 bis 16 Arbeitsstunden. Das schafft ein kleines Team an einem Tag.",
        "fragen": [],
        "praxis": [],
    },
    ("unterhaltsreinigung", "wesseling"): {
        "kurz": "Unterhaltsreinigung in Wesseling kostet bei uns 32 € netto pro Stunde, die Anfahrt ist inklusive. Wir reinigen Büros, Praxen und Läden in Wesseling-Mitte, Berzdorf, Keldenich und Urfeld mit festem Reinigungstag und festem Team. Nach einer kostenlosen Besichtigung bekommen Sie einen festen Monatspreis.",
        "beispiel": "Ein Laden mit 200 m², der an fünf Tagen pro Woche gereinigt wird, braucht bei uns etwa eine Stunde je Einsatz. Das sind 32 € netto pro Einsatz und rund 693 € netto im Monat.",
        "fragen": [],
        "praxis": [],
    },
    ("glasreinigung", "wesseling"): {
        "kurz": "Glasreinigung in Wesseling kostet bei uns 45 € netto pro Stunde. Wir reinigen Fenster, Rahmen und Schaufenster, regelmäßig oder einmalig, auch ohne laufenden Reinigungsvertrag.",
        "beispiel": "Zwölf Fensterflügel im Obergeschoss, innen und außen, ohne Rahmen brauchen bei uns etwa 1,5 Stunden. Das sind rund 68 € netto.",
        "fragen": [],
        "praxis": [],
    },
    ("treppenhausreinigung", "wesseling"): {
        "kurz": "Eine Treppenhausreinigung in Wesseling kostet bei uns zwischen 120 und 300 € netto im Monat. Für Hausverwaltungen und Eigentümergemeinschaften reinigen wir wöchentlich oder alle zwei Wochen an einem festen Tag. Die Anfahrt ist im Preis enthalten.",
        "beispiel": "Ein Haus mit drei Etagen und Reinigung alle zwei Wochen liegt bei uns am unteren Ende der Spanne, bei 120 € netto im Monat. Wöchentlich gereinigt sind es rund 170 €.",
        "fragen": [],
        "praxis": [],
    },
}
