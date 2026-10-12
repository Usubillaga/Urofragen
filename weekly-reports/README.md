# Wöchentliche Urologie-Berichte

Hier werden die angeforderten Studienberichte und Repository-Prüfungen archiviert. Die erste geplante Ausgabe ist am **16. Oktober 2026**. Die Aufgaben laufen freitags in der Zeitzone **Europe/Berlin**: Studienbericht morgens, Repository-Prüfung nachmittags. Die Terminierung erfolgt über ChatGPT-Aufgaben; sie ist kein GitHub-Actions-Cronjob.

## Studien und Updates

Ablage: `weekly-reports/research/YYYY-MM-DD.md`.

Der deutschsprachige Bericht wird aus derselben recherchierten Evidenz in **Usubillaga/Urofragen** und **Usubillaga/Residency-Game-DE** veröffentlicht. Er enthält nur relevante neue Studien, Leitlinien- und Zulassungsänderungen seit der vorherigen Ausgabe, beim ersten Lauf aus den letzten sieben Tagen. Eine ruhige Woche wird ausdrücklich als solche dokumentiert.

Je Beitrag: Originalquelle und Veröffentlichungsdatum, Fragestellung und Studiendesign, Population, Vergleich, wichtigste Ergebnisse und Grenzen sowie konkrete Bedeutung für Fragen, Erklärungen, Klassifikationen oder Lernfälle. Neue Evidenz, geltende Leitlinien und Zulassungsstatus werden getrennt dargestellt. Auswirkungen auf die beiden Projekte werden anhand tatsächlich gelesener Inhalte beschrieben.

Die datierten Ausgaben bleiben erhalten. Ein Verzeichnis der erschienenen Berichte wird hier ergänzt. Vor der ersten Ausführung existiert noch kein Studienbericht.

## Repository-Prüfung und Verbesserungen

Ablage: `weekly-reports/maintenance/YYYY-MM-DD.md`.

Geprüft werden neue Commits und offene Pull Requests, Build und vorhandene Tests, Fragen-/Antwortkonsistenz, Quellenstand, Übersetzungen, Klassifikationen, lokale Verweise und die Funktionsfähigkeit der Lernoberfläche. Der erste Lauf schließt eine Ausgangsprüfung des aktuellen Stands ein.

Belegte Fehler und sinnvolle begrenzte Verbesserungen werden in nachvollziehbaren Branches und Pull Requests umgesetzt. Jeder Prüfbericht nennt Befund, betroffene Dateien oder Fragen-IDs, konkrete Maßnahme, PR-Link sowie tatsächlich ausgeführte Prüfungen und verbleibende Lücken. Eine Woche ohne Befund wird knapp dokumentiert. Doppelte PRs für dieselbe unveränderte Ursache werden vermieden.

Medizinische Änderungen erhalten eine überprüfbare Quelle. Eine technische Prüfung oder KI-Überarbeitung ersetzt keine vorhandene fachärztliche Freigabe; Reviewstatus und Provenienz müssen zur jeweiligen Inhaltsversion und Sprache passen. Persönliche Spielstände, Prüfernamen und private Gesprächsinhalte gehören nicht in diese öffentlichen Berichte.

## Besonderheiten von Urofragen

- Bestehende Fragen-IDs, Versionen, Quellen und Freigabehistorien erhalten.
- Deutsch, Englisch und Spanisch konsistent aktualisieren; keine Freigabe zwischen Sprachen übertragen.
- Fachlich veränderte Fragen versionieren und den Freigabestatus nach dem bestehenden Prüfmodell anpassen.
- Quelldaten bearbeiten und die zugehörigen Ausgaben mit `python build.py` erzeugen.

Die aktuellen Prüfungen stehen in `.github/workflows/pruefung.yml`: unter anderem `python tools/check_generated.py`, `python review/verify_update.py`, `python review/verify_cme.py`, `python review/verify_cme_languages.py`, `python review/check_release.py` sowie die dort genannten Node- und Browsertests. Vor jeder Ausführung die aktuelle Workflowfassung lesen.

## Ausgaben

Noch keine Ausgabe; erster geplanter Termin: 16.10.2026.
