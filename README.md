# Urofragen – Aktualisierung 04.10.2026

Die ZIP enthält die komplette Website und alle zum erneuten Aufbau benötigten Projektdateien. Die fertigen HTML-Dateien können direkt hochgeladen werden; Python wird auf GitHub Pages nicht benötigt.

## Inhalt

- 257 verfügbare Lernfragen in 16 Abschnitten, jeweils Deutsch, Englisch und Spanisch.
- 43 neue Fragen: 9 Seminom IIA/B, 10 Hodentumor-Nachsorge, 14 Schwerpunktheft Teil 3, 10 Salvage-Operationen.
- Hodentumor jetzt 53, Operative Urologie 30 verfügbare Fragen. NMIBC und MIBC weiterhin jeweils 10.
- 10 zusätzliche dreisprachige OP-Entwürfe aus dem bestehenden Repository erhalten; im Prüfmodus verfügbar, im Lernmodus nicht ausgeliefert. Insgesamt 267 Datensätze.
- `uro-hod-00007` ersetzt und versioniert. Die alte Freigabe ist im Verlauf erhalten; die neue Fassung muss erneut geprüft werden. 51 übrige deutsche Freigaben unverändert erhalten.
- Alle neuen Fragen ohne fachärztliche Freigabe. Es wurde keine pauschale Freigabe aus Autorennamen oder Dateiinhalten abgeleitet.
- `cme-seminom-IIAB.html`: mitgelieferte eigenständige CME-Lerneinheit auf Deutsch, von der Startseite verlinkt. Ihre separate Auswertung wird nicht mit dem Urofragen-Lernkonto zusammengeführt. Die integrierten Fragenblöcke sind vollständig dreisprachig.

## Hochladen

ZIP entpacken. **Den Inhalt**, nicht die ZIP und nicht den äußeren Ordner, in den bisherigen Website-Ordner des Repositorys `Usubillaga/Urofragen` hochladen. Vorhandene gleichnamige Dateien durch diese zusammengehörige Fassung ersetzen.

Diese drei Dateien müssen nebeneinander liegen:

- `index.html` – Lernwebsite
- `pruefung.html` – fachärztliche Prüfung
- `cme-seminom-IIAB.html` – CME-Lerneinheit

Die Ordner `data`, `tools`, `review` und `updates` sowie die Python-Dateien gehören zum vollständigen Projekt. Die bisherige GitHub-Pages-Konfiguration bleibt verwendbar. Diese Fassung wurde nur lokal vorbereitet, nicht in das Repository geschrieben.

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

Ohne `--apply` nur Vorschau. Wiederholtes Einspielen erzeugt keine Duplikate. Ein fehlgeschlagener Aufbau stellt Fragendateien und HTML-Ausgaben wieder her. Veränderte Quelldateien bereits importierter Blöcke verlangen einen ausdrücklichen Abgleich statt stillen Überschreibens.

## Prüfung

Aufbau erfolgreich; fünf Importtests, acht Freigabe-/Speichertests, fünf Anzeigeprüfungen und die isolierten Prüfmodus-Tests bestanden. JavaScript-Syntax aller drei HTML-Dateien geprüft. Keine vollständige visuelle Browserprüfung in diesem Durchgang.

Die gelieferten medizinischen Fragen wurden inhaltlich übernommen; dies ist keine vollständige neue Leitlinienprüfung sämtlicher 43 Fragen. Der Seminom-IIA/B-Rahmen wurde mit der EAU-Therapieseite und der Nachsorge-Rahmen mit der EAU-Nachsorgeseite abgeglichen. Artikelbezogene Aussagen, Zahlen und Einzelfallempfehlungen benötigen deine fachärztliche Prüfung. Formale Hinweise sind unter `review/build-check.txt` dokumentiert; Tests bestätigen keine medizinische Richtigkeit.

Quellen für den orientierenden Abgleich (04.10.2026):
- https://uroweb.org/guidelines/testicular-cancer/chapter/disease-management
- https://uroweb.org/guidelines/testicular-cancer/chapter/followup-after-curative-therapy

Importbericht einschließlich vorheriger Ersatzfrage: `review/import-2026-10-04.json`. Mitgelieferte Quelldateien: `updates/2026-10-04/`.
