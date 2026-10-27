# Urodynamik mit Messkurven – 27.10.2026

Alle Fragen des Abschnitts **Urodynamik** zeigen jetzt eine interaktive Messkurve aus dem Urodynamik-Labor von [Residency-Game-DE](https://github.com/Usubillaga/Residency-Game-DE), und neun Kurvenfälle des Labors sind als neue Fragen hinzugekommen. Der Abschnitt hat damit 19 Fragen; die Bank hat **281 verfügbare Lernfragen und 10 OP-Entwürfe, zusammen 291 Datensätze**. Alle übrigen Fragen, IDs, Freigaben und CME-Module bleiben unverändert.

## So sieht es aus

- **Lernmodus:** Die Kurve steht zwischen Vignette und Fragestellung: Pves, Pabd, Pdet, Fluss, infundiertes und entleertes Volumen sowie Beckenboden-EMG, mit Markern für Husten, Empfindungen, Drang, Leckage, Miktionserlaubnis und Qmax. Tippen, Ziehen oder die Pfeiltasten bewegen einen Cursor, der alle Kanäle zu diesem Zeitpunkt abliest; Ausschnitt-Schaltflächen zoomen auf Füllung, Miktion oder Hustentests.
- **Vor der Antwort** zeigt die Kurve keine Befunde. Teile einer Messung, die die Antwort verraten würden, bleiben bis dahin verborgen: die zweite, langsamere Füllung (`uro-udy-00008`), Spülung und Kontrollhusten nach gedämpfter Leitung (`00010`), das Vorgehen bei autonomer Dysreflexie (`00016`) und die Wiederholung nach herausgerutschtem Katheter (`00019`).
- **Nach der Antwort** erscheinen die nummerierten Befunde in der Kurve und als Liste darunter; bei den vier genannten Fragen wechselt die Ansicht auf den Teil, der jetzt sichtbar wird.
- **Telefon und Desktop:** eigene Layouts; wechselt die Breite, wird die Kurve neu gezeichnet. Kein seitliches Scrollen bei 390 px.
- **Ergebnisblatt (Drucken oder Speichern):** jede Kurve als ganze Messung mit allen Befunden, ohne Bedienelemente.
- **Prüfmodus:** Die Kurve steht ebenfalls zwischen Vignette und Fragestellung, umschaltbar zwischen „Wie vor der Antwort“ und „Nach der Antwort, mit Befunden“. Eine fehlerhafte Frage wird wie bisher mit „✗ Korrektur nötig“ und einem Kommentar markiert. Neue Fragen (Version 1) tragen im Hinweiskasten nicht mehr den Vorsatz „Überarbeitet nach deinem Hinweis“.

## Fragen und Kurven

| ID | Thema | Richtig | Ausschnitt vor der Antwort | danach | Befunde | verborgener Teil | Fall · Entscheidung im Spiel |
|---|---|---|---|---|---|---|---|
| `uro-udy-00001` | Druck-Fluss-Messung | A | Miktion | – | 3 | – | `udy-bpo-pressure-flow-indices` |
| `uro-udy-00002` | Detrusorunteraktivität | C | Gesamte Messung | – | 3 | – | `udy-dhic-elderly-man-no-turp` |
| `uro-udy-00003` | Videourodynamik | A | Miktion | – | 3 | – | `udy-pbno-young-man-vuds` |
| `uro-udy-00004` | Neurourologie | B | Gesamte Messung | – | 3 | – | `udy-msa-before-turp` |
| `uro-udy-00005` | Weibliche Blasenauslassobstruktion | B | Miktion | – | 3 | – | `udy-female-boo-after-sling` |
| `uro-udy-00006` | Harnverhalt der Frau | B | Gesamte Messung | – | 2 | – | `udy-fowler-retention-young-woman` |
| `uro-udy-00007` | Okkulte Belastungsinkontinenz | C | Hustentest bei 300 ml | – | 2 | – | `udy-occult-sui-prolapse-reduction` |
| `uro-udy-00008` | Compliance | A | Füllung 1 · 30 ml/min | Gesamte Messung | 2 | zweite Füllung mit 15 ml/min | `udy-low-compliance-sci-filling-rate` |
| `uro-udy-00009` | Kinderurologie | B | Flow 1 | – | 1 | – | `udy-paediatric-dysfunctional-voiding` |
| `uro-udy-00010` | Qualitätskontrolle und Artefakte | B | Gesamte Messung | – | 4 | Stopp, Spülung, Kontrollhusten | `udy-artefacts-rectal-contraction-transmission` |
| `uro-udy-00011` | Normalbefund | B | Füllphase | – | 3 | – | `udy-normal-study-man` · storage |
| `uro-udy-00012` | Überaktive Blase | C | Füllphase | – | 2 | – | `udy-normal-study-woman-oab` · storage |
| `uro-udy-00013` | Detrusorüberaktivität | D | Füllphase | – | 2 | – | `udy-detrusor-overactivity-incontinence` · filling |
| `uro-udy-00014` | Belastungsinkontinenz | A | Hustentests 200–300 ml | – | 3 | – | `udy-urodynamic-stress-incontinence` · lpp |
| `uro-udy-00015` | Mischinkontinenz | C | Füllphase | – | 2 | – | `udy-mixed-incontinence` · read |
| `uro-udy-00016` | Neurourologie | B | Gesamte Messung | Bei 140 ml | 3 | Füllung gestoppt, Blase abgelassen | `udy-neurogenic-overactivity-dsd` · read |
| `uro-udy-00017` | Detrusorunteraktivität | D | Miktion | – | 3 | – | `udy-acontractile-detrusor-straining` · void |
| `uro-udy-00018` | Uroflowmetrie | A | Uroflowmetrie | – | 1 | – | `udy-plateau-flow-stricture` · curve |
| `uro-udy-00019` | Qualitätskontrolle und Artefakte | C | Miktion 1 | Gesamte Messung | 3 | neuer Katheter, Wiederholung | `udy-catheter-loss-repeat` · artefact |

## Die zehn Fragen vom 20.10.2026

Version 2: Jede Frage zeigt die Kurve ihres Falls. Die Messwerte, die eine Vignette aus der Untersuchung nennt (etwa PdetQmax 82 cmH2O bei Qmax 9 ml/s in `00001`, Pves +38 gegenüber Pabd +100 cmH2O in `00010`), stimmen mit den Kurven überein; im Spiel sind sie als Ablesewerte hinterlegt und werden bei jeder Prüfung aus der Kurve nachgerechnet. Fragetexte, Optionen und Begründungen sind unverändert. Einzige Textänderung: Die Erklärung von `00008` beschreibt in allen drei Sprachen die nach der Antwort gezeigte Wiederholung („Die abgebildete Wiederholung mit 15 ml/min bestätigt die verminderte Compliance: Pdet erreicht 40 cmH2O bei 300 ml; die Kathetervolumina müssen darunter bleiben.“).

## Neun neue Kurvenfragen

Jede neue Frage übernimmt aus dem Spiel die Entscheidung, in der die Kurve gelesen wird (Spalte „Entscheidung“). Antwortoptionen und Begründungen sind unverändert die des Spiels, die zwei unabhängige KI-Prüfungen am 26.10. durchlaufen haben und deren Befunde am 27.10. an den Primärquellen nachgeprüft wurden; neu geordnet sind nur die Schlüssel, damit die richtige Antwort nicht immer A ist. Die neuen Fragen haben deshalb vier statt fünf Optionen. Vignette, Fragestellung, Kernerklärung und Merksatz sind für die eigenständige Frage geschrieben: Die Vignette nennt keine Patientennamen und verweist auf die abgebildete Kurve; die Erklärung beschreibt, wie die Kurve gelesen wird, und fasst die Konsequenz zusammen.

Quellen der neuen Fragen (alle verlinkt): EAU 2026 zu männlichen und weiblichen LUTS (Diagnostik, Management, Pocket-Ausgaben), Neuro-Urologie und Harnröhrenstrikturen; ICS Good Urodynamic Practices 2016; IUGA/ICS-Terminologie 2010 (normale Detrusorfunktion „trotz Provokation“, unwillkürliche Kontraktionen „spontan oder provoziert“, urodynamische Belastungsinkontinenz, abdominaler Leak-Point-Druck, akontraktiler Detrusor, Mischinkontinenz als Symptom; am 27.10. im Wortlaut nachgelesen); Cragg und Krassioukov, CMAJ 2012, und die CAN-SCIP-Empfehlung zur autonomen Dysreflexie bei urodynamischen Untersuchungen (PVA 2020: Blutdruck mindestens alle 2 Minuten, zuerst die Blase entleeren, nicht sofort aufsetzen; gelingt die Kontrolle nicht, Untersuchung beenden und aufsetzen), beide am 27.10. nachgelesen.

## Technik

- `data/urodynamik-kurven.json` und `assets/urodynamik-kurven.js` sind unveränderte Kopien von `data/urodynamic-tracings.json` und `assets/urodynamics.js` aus Residency-Game-DE (Commit `0306b41`, Prüfsummen in `updates/2026-10-27/urodynamik-messkurven.json`). Das Zeichenskript hat dafür ein Layout `medium` für Textspalten von etwa 650–750 px erhalten.
- Jede Frage trägt ein Feld `tracing`: Fall, Ausschnitt vor der Antwort (`view`), die Schritte, deren Befunde danach erscheinen (`after`), optional den Ausschnitt danach (`view_after`) und die Prüfsumme der Kurve (`sha256`).
- `python build.py` prüft jede Angabe: Kurve vorhanden, Prüfsumme gleich, Ausschnitte vorhanden und vor bzw. nach der Antwort sichtbar, mindestens ein Befund nach der Antwort. Ändert sich eine Kurve, bricht der Aufbau ab, bis die Frage geprüft, ihre Version erhöht und die Prüfsumme neu eingetragen ist. Danach bettet der Aufbau Zeichenskript und genutzte Kurven (ohne die Ablesewerte des Spiels) in `index.html` und `pruefung.html` ein; beide Seiten bleiben eigenständige Dateien.
- Der Freigabe-Fingerabdruck (`approval.py`) umfasst bei Fragen mit Kurve auch das Feld `tracing`; eine Freigabe endet also, wenn sich die gezeigte Kurve ändert. Für alle Fragen ohne Kurve bleibt der Fingerabdruck unverändert, die 51 deutschen Freigaben gelten weiter.
- `updates/2026-10-20/urodynamik-abschnitt.json` bleibt der Nachweis der ersten zehn Fragen; `updates/2026-10-27/urodynamik-messkurven.json` beschreibt diese Erweiterung.
- Der Hinweistext des Abschnitts lautet jetzt „Messkurven lesen: Druck-Fluss, Füllung, Inkontinenz, Artefakte“.

## Prüfung

- `review/verify_update.py`: 19 Fragen mit Version, Kurve, Prüfsumme, Ausschnitten und Verknüpfung zum Spiel; keine Freigabe ohne Prüfung; die Aufbauprüfung lehnt geänderte Kurven, verborgene Ausschnitte, unbekannte Schritte und Felder ab; der Fingerabdruck ändert sich mit der Kurve.
- `review/test_urodynamik_browser.cjs` (neu, auch in der GitHub-Prüfung): alle 19 Fragen im Lernmodus mit Cursor, Ausschnitten, keinen Befunden vor und allen Befunden nach der Antwort, verborgenen Teilen erst danach; Ergebnisblatt mit 19 Kurven und allen Befunden; Telefon-Layout bei 390 px ohne seitliches Scrollen und Rückwechsel auf Desktop; Englisch und Spanisch; Prüfmodus mit beiden Ansichten für alle 19 Fragen; keine JavaScript-Fehler.
- Fragenzahlen in `review/verify.py`, `review/verify_update.py`, `review/verify_cme.py` und `review/test_review_ui.cjs` auf 291/281 angepasst.
- Lokal bestanden: alle Schritte aus `.github/workflows/pruefung.yml` einschließlich aller Browsertests.
