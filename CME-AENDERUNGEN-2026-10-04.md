# CME-Ergänzung für Urofragen – 04.10.2026

Die drei neuen Seiten sind in das vollständige Projekt integriert. Auf der Startseite gibt es vier CME-Karten, einschließlich der bereits vorhandenen Seminom-Seite. Die Seiten führen zurück zur Startseite und zum Prüfmodus und bieten einen Wechsel zwischen den Modulen.

| Modul | Datei | Fragen |
| --- | --- | ---: |
| Seminom IIA/B | cme-seminom-IIAB.html | 10 |
| Hodentumor Teil 3 | cme-hodentumor-heft-teil3.html | 14 |
| Peniskarzinom | cme-peniskarzinom.html | 16 |
| Salvage-Operationen | cme-salvage-operationen.html | 10 |

Die gelieferten medizinischen Texte, Antwortoptionen, Begründungen, interaktiven Entscheidungshilfen und Quellenangaben sind erhalten. Die unveränderten Originaldateien liegen unter `updates/2026-10-04/cme-originals/`. Vorhandene Aussagen zur Quellenprüfung stammen aus diesen Dateien. Es wurde keine neue fachärztliche Freigabe vergeben.

## Auswertung und Fortsetzen

Der erste Durchgang und die aktuelle Übungsrunde werden getrennt ausgewertet. Das Wiederholen einer falschen Antwort verändert die Erstquote nicht. Pro Thema werden Treffer und Übungsbedarf sichtbar. Weil manche Themen nur eine oder zwei Fragen enthalten, ist dies eine Orientierung zu den bearbeiteten Aufgaben und kein belastbarer Nachweis klinischer Kompetenz.

Jedes Modul speichert seinen eigenen Fortschritt lokal im Browser. Ein erneutes Öffnen im selben Browser erlaubt das Fortsetzen. Ein ausdrücklich gewählter Neustart beginnt einen neuen Durchgang. Sind Browserdaten nicht speicherbar, kann die Sitzung weitergeführt werden; die Seite weist auf die fehlende Speicherung hin.

Die CME-Ergebnisse sind unabhängig vom Lernstand des Hauptquiz und von den fachärztlichen Prüfentscheidungen. Ein Wechsel des Browsers, des Geräts oder von einer lokalen Datei zu GitHub Pages übernimmt die Ergebnisse nicht automatisch. Es gibt keine automatische Speicherung des Lernverlaufs im GitHub-Repository.

## Sprache und weiterer Ausbau

Alle vier CME-Seiten sind vollständig auf Deutsch, Englisch und Spanisch verfügbar. Der DE/EN/ES-Schalter übersetzt die Fragen samt Antwortoptionen, Begründungen, Lernzielen, Merkkästen, interaktiven Hilfen, Quellen-Annotationen, Navigation, Auswertung und Druckfassung. Bibliografische Originaltitel und die Herkunftsmarker [Q], [X] und [LL ...] bleiben erhalten. Die 257 Fragen im Hauptquiz sind weiterhin dreisprachig.

Beim Sprachwechsel bleibt derselbe Modul-Durchgang bestehen: Position, Antworten und Erstquote bleiben erhalten. Eine übersetzte Antwort wird nicht als neuer Versuch gewertet. Die ursprünglichen Versionsschlüssel des lokalen Lernstands werden weiterverwendet. Die Startseite öffnet ein Modul mit ihrer gewählten Sprache; die Modulnavigation erhält diese Sprache.

Ein exportierbarer Verlauf der CME-Durchgänge und eine eigene fachärztliche Prüfung der einzelnen CME-Aufgaben bleiben sinnvolle weitere Ergänzungen. Ein gemeinsamer Lernstand müsste Aufgaben, die auch im Hauptquiz vorkommen, ausdrücklich zuordnen, damit sie nicht doppelt als unabhängige Fragen gezählt werden.

## Verifikation

- Vollständiger Neuaufbau der Website und bestehende Freigabe-/Prüfmodus-Tests bestanden. Die 267 Datensätze, 257 veröffentlichten Fragen und 51 bestehenden deutschen Freigaben bleiben erhalten.
- Drei Integrationstests vergleichen alle CME-Daten mit den Originalen, prüfen Fragenzahlen und relative Verweise und bestätigen die unveränderten Hauptbankzahlen.
- Isolierte CME-Tests prüfen mehrere Fehlerwiederholungen, Erstquote/Rundenquote, Fortsetzen, bestätigten beziehungsweise abgebrochenen Neustart, ungültige Speicherstände, Speicherfehler und getrennte Schlüssel. JavaScript-Syntax geprüft.
- Echter Browserdurchlauf in einer frischen Edge-Sitzung: Alle 50 CME-Aufgaben beantwortet, je Modul einen Fehler wiederholt, unveränderte Erstquote und eigene Rundenquote bestätigt, nach Neuladen fortgesetzt, Speichertrennung sowie Neustart geprüft. Bei verweigerter Speicherung bleiben die Fragen benutzbar. Keine JavaScript-Laufzeitfehler.
- Startseite und CME-Seiten bei Desktopbreite und 390 Pixeln geprüft; kein horizontaler Überlauf. Screenshots liegen unter `review/`.
- Übersetzungsprüfung: alle 100 EN/ES-Fragefassungen und sämtliche Zusatzdaten haben dieselbe Struktur, Antwortbuchstaben, Achsen und Schwierigkeiten. Quellenmarker sind pro Textfeld erhalten. Zahlen wurden verglichen; fünf gleichwertige Schreibweisen wie „fünf Jahre“/„5-year“ und „Phase 2“/„phase II“ sind ausdrücklich dokumentiert. Eine fehlende AUC-7-Angabe in einer spanischen Distraktoroption wurde ergänzt; bedingte Operation, achtmonatige Erholung und eine Prozent-Spanne präzisiert.
- Mehrsprachiger Browserdurchlauf: vier Module DE→EN→ES, Fortsetzen mitten im Durchgang, alle EN/ES-Vignetten und Fragestellungen in der Druckfassung, sämtliche auswählbaren Lernhilfen auf Spanisch, Scores in beiden Sprachen, Fehlerwiederholung und mobile Darstellung bestanden. Keine JavaScript-Laufzeitfehler. Die Prüfung lief in einem frischen Browserprofil.

Neuaufbau: `python build.py` für das vollständige Projekt, `python tools/build_cme.py` für die CME-Seiten. Übersetzungen liegen in `translations/`; Vorlagen in `templates/cme/`. Alle erzeugten Sprachdateien unter `assets` gehören zum Upload.

Diese Prüfungen bestätigen die technische Einbindung und Auswertung; die fachärztliche Inhaltsprüfung führst du weiterhin durch.
