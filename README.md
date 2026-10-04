# Urofragen – Aktualisierung 04.10.2026

Die ZIP enthält die komplette Website und alle zum erneuten Aufbau benötigten Projektdateien. Die fertigen HTML-Dateien können direkt hochgeladen werden; Python wird auf GitHub Pages nicht benötigt.

## Inhalt

- 257 verfügbare Lernfragen in 16 Abschnitten, jeweils Deutsch, Englisch und Spanisch.
- 43 neue Fragen: 9 Seminom IIA/B, 10 Hodentumor-Nachsorge, 14 Schwerpunktheft Teil 3, 10 Salvage-Operationen.
- Hodentumor jetzt 53, Operative Urologie 30 verfügbare Fragen. NMIBC und MIBC weiterhin jeweils 10.
- 10 zusätzliche dreisprachige OP-Entwürfe aus dem bestehenden Repository erhalten; im Prüfmodus verfügbar, im Lernmodus nicht ausgeliefert. Insgesamt 267 Datensätze.
- `uro-hod-00007` ersetzt und versioniert. Die alte Freigabe ist im Verlauf erhalten; die neue Fassung muss erneut geprüft werden. 51 übrige deutsche Freigaben unverändert erhalten.
- Alle neuen Fragen ohne fachärztliche Freigabe. Es wurde keine pauschale Freigabe aus Autorennamen oder Dateiinhalten abgeleitet.
- Vier eigenständige CME-Lerneinheiten auf Deutsch, Englisch und Spanisch mit insgesamt 50 Fragen: Seminom IIA/B (10), Hodentumor Teil 3 (14), Peniskarzinom (16), Salvage-Operationen (10). Vollständig übersetzt sind Fragen, Optionen, Begründungen, Lernziele, Merkkästen, Entscheidungshilfen, Navigation, Auswertung und Druckfassung. Bibliografische Originaltitel bleiben als Quellenangabe erhalten. Die 50 CME-Fragen sind separate Übungen; sie erhöhen die Zahl der 257 Fragen im Hauptquiz nicht.
- Einheitliche Navigation mit DE/EN/ES-Schalter, getrennte Auswertung des ersten Durchgangs und der Fehlerwiederholung sowie Fortsetzen im selben Browser. Der Sprachwechsel erhält Antworten und Erstquote; die Startseite öffnet das Modul in der gewählten Sprache. Änderungen sind in `CME-AENDERUNGEN-2026-10-04.md` beschrieben. Deutsche medizinische Originaltexte und Antwortschlüssel bleiben unverändert; Übersetzungen vergeben keine neue fachärztliche Freigabe.

## Hochladen

ZIP entpacken. **Den Inhalt**, nicht die ZIP und nicht den äußeren Ordner, in den bisherigen Website-Ordner des Repositorys `Usubillaga/Urofragen` hochladen. Vorhandene gleichnamige Dateien durch diese zusammengehörige Fassung ersetzen.

Diese sechs Dateien müssen nebeneinander liegen; der Ordner `assets` muss daneben mit hochgeladen werden:

- `index.html` – Lernwebsite
- `pruefung.html` – fachärztliche Prüfung
- `cme-seminom-IIAB.html` – Seminom IIA/B
- `cme-hodentumor-heft-teil3.html` – Hodentumor Teil 3
- `cme-peniskarzinom.html` – Peniskarzinom
- `cme-salvage-operationen.html` – Salvage-Operationen
- `assets/` – gemeinsame Darstellung, Navigation und Fortschritt der CME-Module

Die Ordner `data`, `tools`, `review`, `updates`, `translations` und `templates` sowie die Python-Dateien gehören zum vollständigen Projekt. Die bisherige GitHub-Pages-Konfiguration bleibt verwendbar. Die Sprachdateien unter `assets` müssen mit hochgeladen werden.

## Weiterprüfen und Verlauf

Im Prüfmodus den Filter **„Neu oder überarbeitet – prüfen“** wählen. Er enthält die 44 neuen/geänderten Fragen dieses Updates und die 13 noch offenen Überarbeitungen aus September. Die anderen 51 deutschen Freigaben bleiben gültig. Englisch und Spanisch sind separat freizugeben.

Nach jeder Sitzung „Prüfungen als Datei sichern“ verwenden. Browserdaten sind nicht automatisch mit GitHub synchronisiert. Bei einem öffentlichen Repository sind die enthaltenen Prüfernamen und Kommentare öffentlich einsehbar.

## Technische Wiederherstellung

Im heruntergeladenen GitHub-Stand fehlten `approval.py` und `quality.py`; diese wurden wiederhergestellt. Die Gebietsdatei `operativ.json` enthielt nur 10 neue Entwürfe in einem anderen Format. Die 20 zuvor vorhandenen OP-Fragen wurden aus der ausgelieferten Website rekonstruiert und zusammen mit den Entwürfen in das unterstützte Format überführt.

Die beiden Heft-3-Dateien waren bytegleich und wurden nur einmal importiert. Salvage-IDs `uro-sal-90001` bis `uro-sal-90010` sind im vorhandenen operativen Bereich auf `uro-ope-00021` bis `uro-ope-00030` abgebildet. Die ursprünglichen IDs stehen in `import_record` und im Importbericht.

Das mitgelieferte ursprüngliche Merge-Skript unterstützte mehrere Gebiete nicht gemeinsam und entfernte vorhandene Freigabefelder nicht ausdrücklich. Es liegt unverändert unter `updates/2026-10-04/` zur Nachvollziehbarkeit. Für künftige Wiederholungen das neue Skript im Projektstamm verwenden:

```text
python merge-fragen.py
python merge-fragen.py --apply
python build.py
```

`build.py` baut auch die vier CME-Dateien und ihre Sprachdateien aus `templates/cme/` und `translations/` neu auf. Dafür werden keine zusätzlichen Pakete benötigt; auf GitHub Pages laufen die fertig erzeugten Dateien direkt und auch lokal ohne Webserver. Die deutschen Originaltexte stehen in den Vorlagen, die Übersetzungen in den Sprach-JSON-Dateien. Eigenständiger CME-Aufbau: `python tools/build_cme.py`.

Ohne `--apply` nur Vorschau. Wiederholtes Einspielen erzeugt keine Duplikate. Ein fehlgeschlagener Aufbau stellt Fragendateien und HTML-Ausgaben wieder her. Veränderte Quelldateien bereits importierter Blöcke verlangen einen ausdrücklichen Abgleich statt stillen Überschreibens.

## Keine Ablaufdaten

Seit dem 04.10.2026 haben Fragen und fachärztliche Freigaben kein Ablaufdatum mehr. Veröffentlichte Fragen bleiben dauerhaft sichtbar, und `python build.py` scheitert nicht mehr an Ablaufdaten. Eine Freigabe gilt unbefristet für die geprüfte Fragenversion und Sprache; sie endet nur, wenn sich Version oder Inhalt der Frage ändern. Nach einem Leitlinien-Update markiert die Seite betroffene Fragen deshalb nicht mehr von selbst als ungeprüft: Diese Fragen aktiv überarbeiten (neue Version) oder erneut prüfen. Frühere Ablaufdaten bleiben in Freigabe-Historie und Importbericht zur Nachvollziehbarkeit erhalten.

## Automatische Prüfung

Bei jedem Push auf `main` und bei jedem Pull Request führt GitHub Actions `.github/workflows/pruefung.yml` aus: Neuaufbau, Abgleich der hochgeladenen HTML- und `assets`-Dateien mit den Quelldaten, alle Python- und Node-Tests sowie die Browsertests mit Chromium. Ein rotes Kreuz am Commit bedeutet meist: Fragen, Übersetzungen oder Vorlagen geändert, aber die mit `python build.py` erzeugten Dateien nicht mit hochgeladen. Lokal:

```text
python tools/check_generated.py
python review/check_release.py
```

`build.py` schreibt alle erzeugten Dateien auf jedem Betriebssystem mit LF-Zeilenenden; ein Aufbau unter Windows ergibt dieselben Dateien wie unter Linux. Die Browsertests verwenden weiterhin Edge; mit leerer Umgebungsvariable `CME_BROWSER_CHANNEL` verwenden sie das Chromium von Playwright.

## Prüfung

Aufbau erfolgreich; fünf Importtests, acht Freigabe-/Speichertests, fünf Anzeigeprüfungen und die isolierten Prüfmodus-Tests bestanden. CME-Daten und lokale Verweise werden zusätzlich mit `review/verify_cme.py` geprüft. Ergebnisse der ergänzenden CME- und Browserprüfung stehen in `CME-AENDERUNGEN-2026-10-04.md`.

Die gelieferten medizinischen Fragen wurden inhaltlich übernommen; dies ist keine vollständige neue Leitlinienprüfung sämtlicher 43 Fragen. Der Seminom-IIA/B-Rahmen wurde mit der EAU-Therapieseite und der Nachsorge-Rahmen mit der EAU-Nachsorgeseite abgeglichen. Artikelbezogene Aussagen, Zahlen und Einzelfallempfehlungen benötigen deine fachärztliche Prüfung. Formale Hinweise sind unter `review/build-check.txt` dokumentiert; Tests bestätigen keine medizinische Richtigkeit.

Quellen für den orientierenden Abgleich (04.10.2026):
- https://uroweb.org/guidelines/testicular-cancer/chapter/disease-management
- https://uroweb.org/guidelines/testicular-cancer/chapter/followup-after-curative-therapy

Importbericht einschließlich vorheriger Ersatzfrage: `review/import-2026-10-04.json`. Mitgelieferte Quelldateien: `updates/2026-10-04/`.
