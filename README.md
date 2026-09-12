# Urofragen – zusammengeführte Arbeitsfassung

Stand: 12. September 2026. Zum Öffnen: `index.html`.

214 Lernfragen in 16 Abschnitten, vollständig auf Deutsch, Englisch und Spanisch. Jeder Abschnitt enthält mindestens 10 Fragen; NMIBC und MIBC jeweils 10. Die vorhandene adaptive Fragenauswahl und Auswertung mit Stärken, Schwächen und bearbeiteten Fragen wurden übernommen.

## Freigabestand

**0 von 214 Fragen sind fachärztlich freigegeben.** Die Verfügbarkeit zum Lernen bedeutet keine Freigabe.

Der unberechtigte importierte Freigabeeintrag für `uro-mib-00004` wurde nach ausdrücklicher Rückmeldung des Nutzers entfernt. Die ursprünglichen Importkopien und personenbezogenen Auditdetails sind nicht Teil dieses Uploadpakets.

## Änderungen

- Beide gelieferten Dateistände zusammengeführt. Das separate Hodentumor-JSON stimmt mit dem neueren Import überein.
- Elf importierte Änderungen an Begründungen mit neuen Fragenversionen versehen.
- Zwei Hodentumor-Fragen fachlich und sprachlich korrigiert: unpassende Rezidivzahl entfernt, Bildgebung in der Surveillance ergänzt, absolute Aussagen über adjuvantes BEP korrigiert. Quellen: [EAU Behandlung](https://uroweb.org/guidelines/testicular-cancer/chapter/disease-management), [EAU Nachsorge](https://uroweb.org/guidelines/testicular-cancer/chapter/followup-after-curative-therapy).
- Freigaben werden erst nach ausdrücklicher Entscheidung gespeichert und an Name, Datum, Ablaufdatum, Version und ausgewählte Sprachen gebunden. Ein Textvergleich über einen Prüffingerabdruck erkennt nachträgliche Änderungen. Das ist keine Identitätsprüfung oder digitale Signatur.
- Jede Entscheidung wird unmittelbar gespeichert. Ein Abbruch verliert bereits bestätigte Entscheidungen nicht. Das Protokoll lässt sich aus gespeicherten Entscheidungen wiederherstellen.
- Website und Druckansicht zeigen einen bloßen Prüfernamen nicht mehr als gültige Freigabe an. Eine deutsche Freigabe gilt nicht automatisch für Spanisch oder Englisch.
- Das Kürzungswerkzeug zeigt standardmäßig nur eine Vorschau, bewahrt einzigartige Folgesätze und hebt nach einer Änderung die alte Freigabe auf.

## Eigene fachärztliche Prüfung

Am einfachsten: **`pruefung.html` öffnen**, oben den eigenen Namen, Sprache und Abschnitt wählen. Unter jeder Frage **✓ Fachlich korrekt** oder **✗ Korrektur nötig** anklicken. Bei ✗ eine kurze Fehlerbeschreibung eintragen. Entscheidungen lassen sich zurücknehmen. Mit „Weiter“ zur nächsten Frage gehen.

Nach jeder Sitzung **„Prüfungen als Datei sichern“** anklicken. Diese JSON-Datei enthält die Entscheidungen mit Name, Version, Sprache und Datum. Sie kann später über „Gesicherte Prüfungen laden“ wieder eingelesen oder zur Übernahme in die Fragendaten weitergegeben werden. Die Website selbst erhält durch das Anklicken noch keine veröffentlichte Freigabe. Die lokale Speicherung gilt nur für den verwendeten Browser und die jeweilige Adresse; die exportierte Datei dient zur Sicherung und Übertragung.

Der Prüfmodus wurde im Browser auf Deutsch und Spanisch angesehen. Die isolierten Funktionstests prüfen Pflichtfelder, Korrektur, Freigabe, Ablaufdatum, getrennte Sprachen, Rücknahme, Speicherfehler, Export, Wiederherstellung und geänderte Versionen. Dabei wurden keine tatsächlichen Fragen freigegeben.

Alternativ über das bisherige Prüfwerkzeug:

Im Projektordner mit installiertem Python:

```text
python tools/freigabe.py --stand
python tools/freigabe.py --reviewer "Eigener vollständiger Name" --gebiet mibc --sprachen de --limit 10
python build.py
```

Das Werkzeug zeigt die Frage, alle Antworten und Begründungen, Quellen und Merksätze. Erst `j` und das bestätigte Ablaufdatum erteilen die Freigabe. `ä` fordert Änderungen an, `n` lehnt ab, `s` überspringt, `b` beendet. Für eine bestimmte Frage `--id uro-mib-00004` verwenden. Für die gemeinsame Prüfung aller Fassungen `--sprachen de,en,es` wählen. Eine erneute Freigabe ersetzt den aktuellen Sprachumfang; die vorherige bleibt im Verlauf dokumentiert.

Nach jeder Freigabe oder Textänderung `build.py` ausführen, damit die Website den neuen Stand enthält. Abgelehnte Fragen werden nicht als aktive Lernfragen ausgeliefert. Sinkt ein Abschnitt dadurch unter 10, verlangt der Aufbau Ersatzfragen.

## Geprüft und noch offen

Der Aufbau ist erfolgreich. Acht Regressionstests für Freigaben und Speichern sowie fünf Prüfungen der sprachabhängigen Anzeige bestehen. Die JavaScript-Syntax wurde geprüft. Es fand in diesem Durchgang keine vollständige visuelle Browserprüfung statt.

Die automatische Prüfung meldet neben 214 ausstehenden Freigaben vier sprachliche Zahlenhinweise und ein ähnliches Fragenpaar (`uro-ope-00017` / `uro-rek-00004`). Zahlenhinweise sind Suchhilfen; beispielsweise können „16 Uhr“, „4 pm“ und „16:00“ fälschlich als unterschiedlich erscheinen. Der Zahlenprüfer erfasst noch nicht alle einstelligen Zahlen zuverlässig. Die komplette fachärztliche Prüfung aller 214 Fragen ist offen. Erfolgreiche technische Tests bestätigen keine medizinische Richtigkeit.

Details: `review/build-check.txt`, `review/change-log.json`. Tests: `python review/check_release.py`.

Diese Fassung wurde lokal erstellt und nicht auf GitHub veröffentlicht.
