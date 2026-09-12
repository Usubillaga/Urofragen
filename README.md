# Urofragen – überarbeitete Fragenqualität

Stand: 12. September 2026. 214 Fragen, 16 Gebiete, Deutsch/Englisch/Spanisch.
Jedes Gebiet mindestens zehn Fragen, NMIBC und MIBC jeweils zehn.

Die Anmerkungen aus `pruefprotokoll-original.txt` sind vollständig in
[review/ANTHROPIC-RESPONSE.md](review/ANTHROPIC-RESPONSE.md) zugeordnet.
68 Fragen wurden redaktionell oder inhaltlich geändert; alle 27 zuletzt ergänzten
Fragen erhielten eigene Antwortbegründungen und plausiblere Alternativen.
Die unveränderten Eingangsdaten liegen unter `review/baseline/`.

`index.html` ist die fertige Website. Zum ausführlichen Lesen aller Fragen und
aller Sprachfassungen dient [review/review-questions.html](review/review-questions.html).
Die Website zeigt nach einer Antwort jetzt die Begründungen aller vier Optionen.
Bestehende Lernfortschritte zu unveränderten Fragen bleiben erhalten; geänderte
Fragenversionen werden neu bewertet. Erstversuche und Wiederholungen bleiben getrennt.

## Bauen und prüfen

```text
python build.py
python tests/test_quality.py
node tests/app.test.cjs
python review/report.py
```

Keine Zusatzpakete erforderlich. Python 3.8+ und Node.js mit Blob-Unterstützung.
`build.py` benötigt die mitgelieferte `quality.py`. Nach manuellen Inhaltsänderungen
die betroffenen Fragenversionen erhöhen. Die Skripte `review/revise.py` und
`review/finalize.py` dokumentieren diesen konkreten Bearbeitungslauf; sie gehören
nicht zum regulären Build und würden spätere manuelle Textänderungen überschreiben.

## Grenzen

150 redaktionelle Protokollhinweise wurden bearbeitet. 214 Hinweise auf fehlende
unabhängige fachärztliche Zweitprüfung bleiben offen und werden nicht als behoben
ausgegeben. Die formalen Prüfungen sind kein Nachweis klinischer Richtigkeit oder
psychometrischer Validität. Quellen wurden gezielt für neu gefasste oder auffällige
Inhalte abgeglichen; eine externe Prüfung aller Angaben steht aus.

Die Dateien sind lokal bereitgestellt. Eine Veröffentlichung auf GitHub wurde in
diesem Bearbeitungslauf nicht durchgeführt. Die vorherige Verbindung verweigerte
Schreibzugriff. Die unveränderten Ausgangsdateien im Downloads-Ordner bleiben bestehen.
