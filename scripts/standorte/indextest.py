"""Index-Test Standortseiten (gestartet 26.11.2026).

Frage: Indexiert und zeigt Google die uebrigen Seiten besser, wenn die Standortseiten ohne
jede Nachfrage nicht mehr in Index und Sitemap stehen?

Testgruppe: Standortseiten ohne eine einzige Google-Impression in 16 Monaten
(Search Console, Stand 25.11.2026), ausser Koeln (Hauptmarkt) und Winterdienst
(Saison beginnt gerade). Die Seiten bleiben online und verlinkt, bekommen aber
"noindex, follow" und fliegen aus der sitemap.xml.

Ausgangswerte 25.11.2026 (Search Console):
- Seitenindexierung: 59 indexiert, 104 nicht (95 "Gefunden - zurzeit nicht indexiert")
- Standortseiten: 49 von 131 mit Impressionen in 16 Monaten (4.130 Impr., 24 Klicks, Pos. 27,5)
- Letzte 28 Tage ohne Markensuchen: 9 Klicks, 6.160 Impressionen, Pos. 34,1
- Externe Links: 12

Auswerten ab ca. 07.01.2027 (6 Wochen): dieselben Werte erneut ablesen.
Zurueckdrehen: TESTGRUPPE leeren, build.py laufen lassen, deployen.
"""

TESTGRUPPE = {
    ("bauendreinigung", "frechen"),
    ("bauendreinigung", "leverkusen"),
    ("bauendreinigung", "pulheim"),
    ("bueroreinigung", "bergheim"),
    ("bueroreinigung", "bruehl"),
    ("bueroreinigung", "frechen"),
    ("bueroreinigung", "huerth"),
    ("bueroreinigung", "troisdorf"),
    ("bueroreinigung", "wesseling"),
    ("bueroreinigung", "wuppertal"),
    ("entruempelung", "bergheim"),
    ("entruempelung", "bergisch-gladbach"),
    ("entruempelung", "bruehl"),
    ("entruempelung", "huerth"),
    ("entruempelung", "leverkusen"),
    ("entruempelung", "pulheim"),
    ("entruempelung", "troisdorf"),
    ("entruempelung", "wesseling"),
    ("fassadenreinigung", "bruehl"),
    ("fassadenreinigung", "frechen"),
    ("fassadenreinigung", "huerth"),
    ("fassadenreinigung", "leverkusen"),
    ("fassadenreinigung", "troisdorf"),
    ("fassadenreinigung", "wesseling"),
    ("fassadenreinigung", "wuppertal"),
    ("glasreinigung", "bruehl"),
    ("glasreinigung", "huerth"),
    ("glasreinigung", "leverkusen"),
    ("grundreinigung", "bergheim"),
    ("grundreinigung", "bruehl"),
    ("grundreinigung", "frechen"),
    ("grundreinigung", "huerth"),
    ("grundreinigung", "troisdorf"),
    ("grundreinigung", "wesseling"),
    ("photovoltaikreinigung", "bergheim"),
    ("photovoltaikreinigung", "bruehl"),
    ("photovoltaikreinigung", "frechen"),
    ("photovoltaikreinigung", "huerth"),
    ("photovoltaikreinigung", "leverkusen"),
    ("photovoltaikreinigung", "pulheim"),
    ("photovoltaikreinigung", "troisdorf"),
    ("photovoltaikreinigung", "wesseling"),
    ("photovoltaikreinigung", "wuppertal"),
    ("polsterreinigung", "bergheim"),
    ("polsterreinigung", "bruehl"),
    ("polsterreinigung", "frechen"),
    ("polsterreinigung", "huerth"),
    ("polsterreinigung", "leverkusen"),
    ("polsterreinigung", "troisdorf"),
    ("polsterreinigung", "wesseling"),
    ("teppichreinigung", "bruehl"),
    ("teppichreinigung", "frechen"),
    ("teppichreinigung", "huerth"),
    ("teppichreinigung", "leverkusen"),
    ("teppichreinigung", "pulheim"),
    ("teppichreinigung", "troisdorf"),
    ("teppichreinigung", "wesseling"),
    ("teppichreinigung", "wuppertal"),
    ("treppenhausreinigung", "bergheim"),
    ("treppenhausreinigung", "bergisch-gladbach"),
    ("treppenhausreinigung", "bruehl"),
    ("treppenhausreinigung", "huerth"),
    ("treppenhausreinigung", "leverkusen"),
    ("treppenhausreinigung", "troisdorf"),
    ("unterhaltsreinigung", "bruehl"),
    ("unterhaltsreinigung", "huerth"),
    ("unterhaltsreinigung", "pulheim"),
    ("unterhaltsreinigung", "troisdorf"),
}
