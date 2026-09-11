# Facharztfragen Urologie · Preguntas de Urología

214 fallbasierte Fragen in 16 Gebieten, vollständig auf Deutsch, Englisch und
Spanisch. Die Website besteht aus einer eigenständigen `index.html`.
Jedes Gebiet enthält mindestens zehn Fragen; NMIBC und MIBC jeweils genau zehn.

## Bearbeiten und bauen

Die Gebietsarchive und `domains.json` können wie im bisherigen Repository neben
`build.py` liegen. Alternativ wird `data/domains.json` mit `data/fragen/*.json`
unterstützt; falls vorhanden, hat diese Struktur Vorrang. Nicht beide pflegen.

```text
python build.py
python tests/validate_bank.py
node tests/app.test.cjs
```

Python 3.8+ und für den Anwendungstest Node.js mit Blob-Unterstützung erforderlich.
Keine zusätzlichen Bibliotheken nötig. `index.html` ist die veröffentlichte Datei.
Der Build lädt weder Fragen noch Übersetzungen aus externen Diensten nach.

Jedes Archiv hat `gebiet` und `fragen`. IDs bleiben stabil. Richtige Antworten,
Quellen und Prüfdaten existieren einmal; Texte stehen unter `content.de`,
`content.en` und `content.es`. Bei inhaltlichen Änderungen die Version erhöhen,
damit frühere Antworten erneut geübt werden können.

Veröffentlichte Fragen benötigen alle drei vollständigen Sprachfassungen,
genau eine richtige Antwort, Begründungen, Merksatz und gültiges Ablaufdatum.
Bei Fehlern bleibt die bisherige `index.html` erhalten. Entwürfe und abgelaufene
Fragen werden in der Oberfläche nicht angeboten.

## Bedienung

DE / EN / ES wechselt die Sprache; Auswahl und Lernfortschritt bleiben lokal im
Browser. Antworten werden pro Sitzung gemischt. Der Sprachwechsel erhält auch
die Ergebnisseite. Ergebnisbögen können gedruckt oder als HTML gespeichert werden.
Im Browserdruckdialog ist „Als PDF speichern“ möglich.
Offizielle Quellentitel bleiben in ihrer Originalsprache zitierfähig.

Die Übersicht zeigt Trefferquote und Bearbeitungsstand getrennt, insgesamt,
pro Gruppe und pro Gebiet. Jede Frage zählt dabei einmal mit ihrer letzten Antwort.
Erstversuche seit dieser Version bleiben separat erhalten; ältere Erstversuche
werden nicht geschätzt. Eine Stärke wird ab fünf verschiedenen Fragen und 80 %
Trefferquote angezeigt, 60–79 % als „Weiter festigen“, darunter „Übungsbedarf“.
Diese Orientierung ist keine klinische Kompetenzprüfung.

Runden gleichen zunächst die Gebiete aus und bevorzugen bislang weniger
bearbeitete Gebiete. Innerhalb eines Gebiets wechseln Fehler, neue Fragen und
ältere richtige Antworten; fehlende Kategorien werden aufgefüllt. Pro Runde
erscheint jede Frage höchstens einmal. „Fehler gezielt üben“ nutzt die aktuell
falschen Antworten; am Rundenende können die Fehler dieser Runde wiederholt werden.
Laufende Runde, Ergebnis und Export zeigen richtige, falsche und offene Fragen.
Der Ergebnisbogen enthält außerdem eine Auswertung nach Gebiet und Lernhinweise.

## Inhaltsprüfung

Siehe [Prüfbericht](REVIEW.md). Die Ergänzungen sind KI-gestützt redigiert,
einschließlich maschineller spanischer Vorübersetzung. 32 Fragen erhielten
inhaltliche oder redaktionelle Änderungen am Ausgangstext.
Eine unabhängige fachärztliche Zweitfreigabe steht aus und wird nicht behauptet.
Die 27 neuen Fälle vom 11. September wurden direkt dreisprachig verfasst und
an den verlinkten EAU-Kapiteln abgeglichen. Der Build verhindert Gebiete mit
weniger als zehn aktiven Fragen. Ablaufende Inhalte müssen daher ersetzt werden.
Quellenverweise ersetzen nicht die Prüfung aktueller Fachinformationen.

Die Schriftarten werden wie bisher von Google Fonts angefragt. Ohne Zugriff
werden Systemschriften verwendet. Der gesamte Fragenbestand ist eingebettet;
für den Fragenbetrieb sind weder Konto noch Backend erforderlich.
