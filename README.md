# Facharztfragen Urologie

Dreisprachig (Deutsch / Englisch / Spanisch). Alle Fragen liegen in **einer** Datei.
`build.py` prüft sie und baut daraus **eine einzige `index.html`** — das ist die
einzige Datei, die zu GitHub hochgeladen wird.

## Auf deinem Rechner

```
build.py
data/domains.json    Gruppen und Gebiete, zweisprachige Bezeichnungen
data/fragen/         ein Archiv pro Gebiet — hier arbeitest du
index.html           <- erzeugt
```

## Ablauf beim Ergänzen

1. Neue Datei für ein Gebiet erhalten, zum Beispiel `prostatakarzinom.json`
2. Sie in `data/fragen/` an dieselbe Stelle legen und die alte ersetzen
3. `python3 build.py`
4. Die neue `index.html` zu GitHub hochladen

## Bauen

```bash
python3 build.py
```

Bei einem Fehler wird `index.html` nicht überschrieben, die laufende Seite bleibt heil.
Zum Ansehen die erzeugte `index.html` doppelklicken; es wird nichts nachgeladen.

## Hochladen

Repository → **Add file** → **Upload files** → `index.html` → **Commit changes**.
Eine Datei, keine Ordner.

## Aufbau der Archive

Jedes Gebiet hat eine eigene Datei unter `data/fragen/`, benannt wie der Slug in
`domains.json`. Um Fragen zu einem Thema zu ergänzen, tauschst du genau eine Datei aus.

```
data/fragen/prostatakarzinom.json     13 Fragen
data/fragen/nmibc.json                 2
data/fragen/mibc.json                  4
data/fragen/nierenzellkarzinom.json   12
data/fragen/hodentumor.json           20
data/fragen/utuc.json                 11
data/fragen/kinderurologie.json       10
data/fragen/operativ.json             20
data/fragen/peniskarzinom.json         4
data/fragen/urethrakarzinom.json       leer
data/fragen/funktionell.json          13
data/fragen/infektiologie.json         leer
data/fragen/urolithiasis.json          3
data/fragen/andrologie.json            leer
data/fragen/rekonstruktion.json        leer
```

Aufbau einer Datei:

```json
{
  "gebiet": "prostatakarzinom",
  "fragen": [ … ]
}
```

Das Feld `gebiet` muss zum Dateinamen passen, sonst bricht der Build ab. Damit kann eine
Datei nicht versehentlich unter dem falschen Namen gespeichert werden. Das Gebiet steckt
im Dateinamen und muss in der einzelnen Frage nicht noch einmal stehen.

Fehlt eine Datei, bleibt das Gebiet leer und `build.py` gibt einen Hinweis aus, ohne
abzubrechen. Eine Datei, deren Name in `domains.json` nicht vorkommt, ist ein Fehler.

## Datenmodell

Richtigkeit, Quellen, Evidenzgrad und Ablaufdatum stehen pro Frage **einmal**.
Übersetzt werden nur die Texte unter `content`. Damit kann die richtige Antwort
zwischen den Sprachen nicht auseinanderlaufen.

```json
{
  "id": "uro-pca-00004",
  "version": 1,
  "status": "draft",
  "taxonomy": { "subdomain": "", "tags": ["leitlinie", "dosierung"] },
  "type": "single_best_answer",
  "difficulty_estimated": 3,
  "options": [
    { "key": "A", "correct": true },
    { "key": "B", "correct": false },
    { "key": "C", "correct": false },
    { "key": "D", "correct": false }
  ],
  "evidence": { "level": "IIA", "certainty": "etabliert", "flag": false },
  "sources": [{ "type": "leitlinie", "code": "", "title": "", "year": 2026 }],
  "review": { "author": "EK", "reviewer": null, "created": "", "last_reviewed": "", "expires": "" },
  "content": {
    "de": {
      "vignette": "",
      "lead_in": "",
      "options": {
        "A": { "text": "", "rationale": "" },
        "B": { "text": "", "rationale": "" },
        "C": { "text": "", "rationale": "" },
        "D": { "text": "", "rationale": "" }
      },
      "explanation": { "core": "", "teaching_point": "" },
      "flag_note": null
    },
    "en": { "…gleiche Struktur…": "" }
  }
}
```

`status` auf `published` setzen, sobald die Frage geprüft ist. Nur `published` mit
`expires` in der Zukunft wird ausgeliefert; abgelaufene Fragen verschwinden automatisch.

Fehlt `content.en`, bricht der Build nicht ab — die Frage erscheint in der englischen
Ansicht auf Deutsch, und `build.py` gibt einen Hinweis aus.

## Was build.py abbrechen lässt

Kaputtes JSON, doppelte `id`, unbekannte Datei in `data/fragen/`, unbekannter Tag,
`gebiet` passt nicht zum Dateinamen, `taxonomy.domain` widerspricht der Datei, weniger als vier Optionen,
mehr oder weniger als eine richtige Antwort, fehlendes `expires`, fehlende `rationale`
in einer Sprache, `flag: true` ohne `flag_note`, nicht etablierte Evidenz ohne `flag`.

Als Hinweis ohne Abbruch: fehlende Gebietsdatei, fehlende englische Fassung, ablaufende
Fragen, stark unterschiedliche Optionslängen, `published` ohne Zweitprüfer.

## Gebiete und Gruppen

Die Onkologie ist in acht Entitäten geteilt, die über das Feld `group` zur Zeile
**Uro-Onkologie** zusammengefasst sind. Die Gruppenzeile startet eine Sitzung über
alle Entitäten, jede Entität ist zusätzlich einzeln startbar. Es gibt keine
Freigabegrenze mehr: Ein Gebiet mit Fragen ist offen, ein leeres steht auf
„in Vorbereitung".

Neues Gebiet: Eintrag in `data/domains.json` mit `label` und `hint` in beiden Sprachen,
dann `data/fragen/<slug>.json` anlegen mit `{ "gebiet": "<slug>", "fragen": [] }`.

## Funktionen der Seite

- Umschalter DE / EN / ES oben rechts, Auswahl bleibt gespeichert. Welche Sprachen
  erscheinen, steht in `data/domains.json` unter `languages`. Fehlt eine Übersetzung,
  fällt die Frage auf die erste Sprache zurück, und `build.py` meldet die Abdeckung.
- Navigationsleiste über der Frage: zeigt richtig und falsch, erlaubt den Sprung zurück
- Zurück-Knopf zwischen den Fragen, bereits gegebene Antworten bleiben sichtbar
- **Als PDF drucken**: öffnet den Druckdialog des Browsers mit einem fertig gesetzten
  Ergebnisbogen (A4, Seitenumbruch nie mitten in einer Frage). Im Dialog steht bei jedem
  Browser „Als PDF speichern" bzw. „Save as PDF"; auf dem iPhone über Teilen → Drucken.
  Ein echtes PDF direkt zu erzeugen ginge nur mit einer eingebetteten Fremdbibliothek von
  mehreren hundert Kilobyte — der Druckweg nutzt stattdessen die PDF-Ausgabe des Browsers
  und liefert die bessere Typografie.
- **Als Datei speichern**: derselbe Bogen als eigenständige HTML-Datei
- Der Bogen enthält Datum, Gebiet, Punktzahl und je Frage die Vignette, alle Optionen mit
  Markierung, die Begründungen zur gewählten und zur richtigen Antwort, Merksatz, Quellen
  und den ⚠-Hinweis
- Die Antwortoptionen werden pro Sitzung neu gemischt, damit die Position keine Hilfe ist.
  Angezeigt wird ein Positionsbuchstabe; gespeichert wird der feste Schlüssel aus der
  JSON-Datei, damit die spätere Itemstatistik über Sitzungen hinweg vergleichbar bleibt.
- Nicht beantwortete Fragen werden bevorzugt ausgespielt
- Fortschritt im Browser, kein Konto, keine Serverdaten

## Größe

Rund 2,4 KB pro Frage und Sprache. 400 Fragen zweisprachig ergeben etwa 1,9 MB
unkomprimiert; GitHub Pages liefert komprimiert aus, übertragen wird ungefähr ein Drittel
davon, einmalig beim ersten Aufruf.

## Ungeprüft

Alle Fragen stehen auf `published`, aber `review.reviewer` ist leer. Besonders zu
bestätigen: Dosierungsangaben, AWMF-Registernummern, Jahreszahlen und der
Zulassungsstand in `uro-mib-00004`.

## Vor dem Öffentlichmachen

- Impressum nach § 5 DDG mit Berufsbezeichnung und zuständiger Kammer
- Datenschutzerklärung (der Fortschritt bleibt im Browser, das gehört hinein)
- Die zwei Google-Schriften lokal einbetten statt per `@import` zu laden
