/* Rechner auf den Standortseiten (13.10.2026).
   Ein Skript fuer alle Leistungen; die Art steht in data-rechner, Stundensaetze
   nur wie auf preise.html veroeffentlicht. Alles ist eine grobe Schaetzung -
   das verbindliche Angebot gibt es nach Begehung oder Fotos. */
(function () {
  var STUNDE = { unterhalt: 32, grund: 38, glas: 45 };
  var fmt = function (n, d) { return n.toLocaleString('de-DE', { minimumFractionDigits: d || 0, maximumFractionDigits: d || 0 }); };
  var eur = function (n) { return fmt(Math.round(n), 0) + ' €'; };
  var viertel = function (h) { return Math.max(1, Math.round(h * 4) / 4); };

  var ARTEN = {
    unterhalt: {
      titel: 'Was kostet die Reinigung ungefähr?',
      felder: [
        ['flaeche', 'Fläche in m²', 'number', 200, 20, 10000],
        ['nutzung', 'Nutzung', 'select', [['180', 'Büro'], ['120', 'Praxis'], ['140', 'Kita / Schule'], ['200', 'Laden / Showroom']]],
        ['einsaetze', 'Einsätze pro Woche', 'select', [['1', '1×'], ['2', '2×'], ['3', '3×'], ['5', '5× (werktäglich)']]]
      ],
      rechne: function (v) {
        var h = viertel(v.flaeche / v.nutzung);
        var monat = h * v.einsaetze * 4.33 * STUNDE.unterhalt;
        return [['Zeit pro Einsatz', 'ca. ' + fmt(h, 2) + ' Std.'], ['Pro Einsatz', 'ca. ' + eur(h * STUNDE.unterhalt) + ' netto'], ['Pro Monat', 'ca. ' + eur(monat) + ' netto']];
      },
      fuss: 'Grundlage: 32 € netto pro Stunde und typische Reinigungsleistung je Nutzung. Den genauen Stundenumfang legen wir nach der Begehung fest.'
    },
    glas: {
      titel: 'Wie lange dauert die Glasreinigung?',
      felder: [
        ['fluegel', 'Anzahl Fensterflügel', 'number', 20, 1, 2000],
        ['seiten', 'Seiten', 'select', [['2', 'innen und außen'], ['1', 'nur außen']]],
        ['rahmen', 'Rahmen und Fensterbänke', 'select', [['1.4', 'mit Rahmen'], ['1', 'ohne Rahmen']]],
        ['hoehe', 'Höhe', 'select', [['1', 'Erdgeschoss / mit Stange erreichbar'], ['1.25', 'Obergeschosse']]]
      ],
      rechne: function (v) {
        var h = viertel(v.fluegel * 3 * v.seiten * v.rahmen * v.hoehe / 60);
        return [['Zeit', 'ca. ' + fmt(h, 2) + ' Std.'], ['Kosten', 'ca. ' + eur(h * STUNDE.glas) + ' netto']];
      },
      fuss: 'Grundlage: 45 € netto pro Stunde. Sehr große Scheiben oder eine Hebebühne kalkulieren wir gesondert.'
    },
    grund: {
      titel: 'Wie aufwendig ist die Grundreinigung?',
      felder: [
        ['flaeche', 'Bodenfläche in m²', 'number', 100, 10, 5000],
        ['belag', 'Bodenbelag', 'select', [['25', 'PVC / Linoleum'], ['30', 'Fliesen'], ['20', 'Naturstein'], ['35', 'Teppich (Sprühextraktion)']]],
        ['zustand', 'Verschmutzung', 'select', [['1', 'normal'], ['1.4', 'stark']]]
      ],
      rechne: function (v) {
        var h = viertel(v.flaeche / v.belag * v.zustand);
        return [['Zeit', 'ca. ' + fmt(h, 2) + ' Std.'], ['Kosten', 'ca. ' + eur(h * STUNDE.grund) + ' netto']];
      },
      fuss: 'Grundlage: 38 € netto pro Stunde. Eine neue Einpflege mit Schutzfilm ist nicht enthalten.'
    },
    treppenhaus: {
      titel: 'Wo liegt Ihr Treppenhaus in unserer Preisspanne?',
      felder: [
        ['etagen', 'Etagen', 'number', 4, 1, 15],
        ['turnus', 'Turnus', 'select', [['1', 'wöchentlich'], ['0.6', 'alle zwei Wochen']]],
        ['keller', 'Kellerflur', 'select', [['0', 'nein'], ['20', 'ja, mitreinigen']]]
      ],
      rechne: function (v) {
        var p = Math.min(300, Math.max(120, (95 + v.etagen * 25) * v.turnus + v.keller));
        return [['Einordnung', 'ca. ' + eur(p) + ' netto / Monat'], ['Spanne', '120–300 € netto / Monat']];
      },
      fuss: 'Unsere Pauschale liegt zwischen 120 und 300 € netto pro Treppenhaus und Monat. Wo genau, klären wir bei der Besichtigung.'
    },
    bauend: {
      titel: 'Wie viel Arbeit steckt in der Endreinigung?',
      felder: [
        ['flaeche', 'Fläche in m²', 'number', 120, 10, 20000],
        ['zustand', 'Zustand', 'select', [['14', 'nur Feinstaub'], ['9', 'normal nach Ausbau'], ['6', 'stark (Farbe, Mörtel, Folien)']]]
      ],
      rechne: function (v) {
        var h = v.flaeche / v.zustand;
        return [['Aufwand', 'ca. ' + fmt(Math.floor(h * 0.85)) + '–' + fmt(Math.ceil(h * 1.15)) + ' Arbeitsstunden'], ['Team', h > 40 ? 'mehrere Personen, 1–2 Tage' : 'kleines Team, 1 Tag']];
      },
      fuss: 'Bauendreinigungen kalkulieren wir nach Aufwand. Die Schätzung hilft bei der Terminplanung; den Preis nennen wir nach Besichtigung oder Fotos.'
    },
    winter: {
      titel: 'Wie groß ist Ihre Winterdienst-Fläche?',
      felder: [
        ['laenge', 'Gehweg entlang des Grundstücks in m', 'number', 25, 1, 2000],
        ['zugaenge', 'Zugänge und Wege auf dem Grundstück in m²', 'number', 10, 0, 5000],
        ['parkplatz', 'Parkplatz / Zufahrt in m²', 'number', 0, 0, 20000]
      ],
      rechne: function (v) {
        var gehweg = v.laenge * 1.5;
        var summe = gehweg + v.zugaenge + v.parkplatz;
        return [['Gehweg (1,5 m breit)', 'ca. ' + fmt(gehweg) + ' m²'], ['Vertragsfläche gesamt', 'ca. ' + fmt(summe) + ' m²'], ['Einsatzart', v.parkplatz > 300 ? 'Handarbeit + Maschine' : 'Handarbeit']];
      },
      fuss: 'Die räumpflichtige Breite regelt die Satzung Ihrer Stadt. Den Saisonpreis aus Bereitschaft und Einsätzen nennen wir nach Besichtigung.'
    },
    pv: {
      titel: 'Wie groß ist Ihre Solaranlage?',
      felder: [
        ['module', 'Anzahl Module', 'number', 30, 1, 20000],
        ['dach', 'Dach', 'select', [['flach', 'Flachdach'], ['schraeg', 'Schrägdach']]],
        ['umgebung', 'Umgebung', 'select', [['normal', 'Wohngebiet'], ['staub', 'Feld, Straße oder Industrie']]]
      ],
      rechne: function (v) {
        var flaeche = v.module * 1.8;
        var turnus = (v.dach === 'flach' || v.umgebung === 'staub') ? 'jährlich prüfen' : 'alle 2–3 Jahre prüfen';
        return [['Modulfläche', 'ca. ' + fmt(flaeche) + ' m²'], ['Leistung', 'ca. ' + fmt(v.module * 0.42, 1) + ' kWp'], ['Empfehlung', turnus]];
      },
      fuss: 'Annahme: ca. 1,8 m² und 420 W je Modul. Das Angebot richtet sich nach Modulanzahl, Neigung und Zugang.'
    },
    entruempelung: {
      titel: 'Wie viel muss raus?',
      felder: [
        ['zimmer', 'Zimmer / Büroräume', 'number', 2, 0, 100],
        ['keller', 'Keller- oder Dachbodenräume', 'number', 1, 0, 50],
        ['fuell', 'Füllgrad', 'select', [['0.4', 'locker'], ['0.7', 'normal möbliert'], ['1', 'sehr voll']]]
      ],
      rechne: function (v) {
        var m3 = (v.zimmer * 8 + v.keller * 5) * v.fuell;
        return [['Volumen', 'ca. ' + fmt(Math.round(m3)) + ' m³'], ['Containergröße', m3 <= 7 ? 'ca. 1 × 7 m³' : 'ca. ' + Math.ceil(m3 / 7) + ' × 7 m³'], ['Dauer', m3 > 40 ? '1–2 Tage' : 'meist 1 Tag']];
      },
      fuss: 'Grobe Volumenschätzung. Den Festpreis nennen wir nach der Besichtigung, je nach Material und Zugang.'
    },
    fassade: {
      titel: 'Wie groß ist die Fassade?',
      felder: [
        ['breite', 'Breite in m', 'number', 15, 1, 1000],
        ['hoehe', 'Höhe in m', 'number', 8, 1, 120],
        ['material', 'Material', 'select', [['putz', 'Putz'], ['klinker', 'Klinker / Stein'], ['glas', 'Glas / Metall']]]
      ],
      rechne: function (v) {
        var m2 = v.breite * v.hoehe;
        var technik = v.hoehe > 6 ? 'Hebebühne nötig' : 'vom Boden / Leiter';
        var verfahren = v.material === 'putz' ? 'Niederdruck + Reiniger' : v.material === 'glas' ? 'Reinwasser' : 'Heißwasser / Niederdruck';
        return [['Fläche', 'ca. ' + fmt(m2) + ' m²'], ['Technik', technik], ['Verfahren', verfahren]];
      },
      fuss: 'Vor der ganzen Fläche reinigen wir eine Probefläche. Den Preis nennen wir nach Besichtigung.'
    },
    teppich: {
      titel: 'Wie lange dauert die Teppichreinigung?',
      felder: [
        ['flaeche', 'Teppichfläche in m²', 'number', 80, 5, 10000],
        ['flecken', 'Flecken', 'select', [['1', 'wenige'], ['1.3', 'viele / Laufstraßen']]]
      ],
      rechne: function (v) {
        var h = Math.max(1, v.flaeche / 40 * v.flecken);
        return [['Arbeitszeit', 'ca. ' + fmt(h, 1) + ' Std.'], ['Trocknung', 'ca. 4–6 Std.'], ['Begehbar', 'am selben Tag']];
      },
      fuss: 'Annahme: Sprühextraktion mit ca. 40 m² pro Stunde. Das Angebot richtet sich nach Fläche und Verschmutzung.'
    },
    polster: {
      titel: 'Wie viel Zeit brauchen Ihre Polster?',
      felder: [
        ['stuehle', 'Stühle / Bürostühle', 'number', 10, 0, 1000],
        ['sofas', 'Sofas / Sitzbänke', 'number', 1, 0, 200]
      ],
      rechne: function (v) {
        var min = v.stuehle * 12 + v.sofas * 45;
        return [['Arbeitszeit', 'ca. ' + fmt(Math.max(1, min / 60), 1) + ' Std.'], ['Trocknung', 'ca. 2–4 Std.']];
      },
      fuss: 'Annahme: ca. 12 Minuten je Stuhl und 45 Minuten je Sofa. Das Angebot richtet sich nach Stückzahl und Material.'
    }
  };

  function baue(box) {
    var art = ARTEN[box.getAttribute('data-rechner')];
    if (!art) return;
    var form = document.createElement('form');
    form.className = 'rechner-form';
    form.setAttribute('aria-label', art.titel);
    art.felder.forEach(function (f) {
      var lab = document.createElement('label');
      lab.textContent = f[1];
      var el;
      if (f[2] === 'select') {
        el = document.createElement('select');
        f[3].forEach(function (o) { var op = document.createElement('option'); op.value = o[0]; op.textContent = o[1]; el.appendChild(op); });
      } else {
        el = document.createElement('input');
        el.type = 'number'; el.value = f[3]; el.min = f[4]; el.max = f[5]; el.inputMode = 'numeric';
      }
      el.name = f[0];
      lab.appendChild(el);
      form.appendChild(lab);
    });
    var out = document.createElement('div');
    out.className = 'rechner-out';
    out.setAttribute('aria-live', 'polite');
    var fuss = document.createElement('p');
    fuss.className = 'rechner-fuss';
    fuss.textContent = art.fuss;
    box.appendChild(form); box.appendChild(out); box.appendChild(fuss);
    function update() {
      var v = {};
      art.felder.forEach(function (f) {
        var raw = form.elements[f[0]].value;
        var n = parseFloat(raw);
        v[f[0]] = isNaN(n) ? raw : Math.min(f[2] === 'number' ? f[5] : n, Math.max(f[2] === 'number' ? 0 : n, n));
      });
      out.innerHTML = '';
      art.rechne(v).forEach(function (z) {
        var d = document.createElement('div');
        var s = document.createElement('span'); s.textContent = z[0];
        var b = document.createElement('b'); b.textContent = z[1];
        d.appendChild(s); d.appendChild(b); out.appendChild(d);
      });
    }
    form.addEventListener('input', update);
    form.addEventListener('submit', function (e) { e.preventDefault(); });
    update();
  }
  document.querySelectorAll('[data-rechner]').forEach(baue);
})();
