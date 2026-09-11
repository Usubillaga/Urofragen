# Prüfbericht – aktualisiert am 11. September 2026

## Erweiterung und Lernfortschritt vom 11. September

214 Fragen mit 642 vollständigen Sprachfassungen in 16 Gebieten. Alle 187
ursprünglichen IDs bleiben erhalten. Ergänzt wurden NMIBC 00003–00010,
MIBC 00005–00010, Peniskarzinom 00005–00010 und Urolithiasis 00004–00010.
Damit hat jedes Gebiet mindestens zehn Fragen. Die Ergänzungen stehen mit
Einzelquellen und Abrufdatum in den Gebietsdateien; das redaktionelle Hilfsskript
liegt unter `review/expand_bank.py`. Es gehört nicht zum normalen Buildablauf.

Die neuen Fälle wurden direkt auf Deutsch, Englisch und Spanisch formuliert.
Quellenabgleich: [EAU NMIBC](https://uroweb.org/guidelines/non-muscle-invasive-bladder-cancer/chapter/disease-management),
[NMIBC Diagnostik](https://uroweb.org/guidelines/non-muscle-invasive-bladder-cancer/chapter/diagnosis),
[NMIBC Nachsorge](https://uroweb.org/guidelines/non-muscle-invasive-bladder-cancer/chapter/followup-of-patients-with-nmibc),
[MIBC Therapie](https://uroweb.org/guidelines/muscle-invasive-and-metastatic-bladder-cancer/chapter/disease-management),
[MIBC Diagnostik](https://uroweb.org/guidelines/muscle-invasive-and-metastatic-bladder-cancer/chapter/diagnostic-evaluation),
[Peniskarzinom Diagnostik](https://uroweb.org/guidelines/penile-cancer/chapter/diagnostic-evaluation-and-staging),
[Peniskarzinom Therapie](https://uroweb.org/guidelines/penile-cancer/chapter/disease-management)
und [Urolithiasis](https://uroweb.org/guidelines/urolithiasis/chapter/guidelines).
Zusätzlich wurde in uro-nmi-00001 die zu enge Beschränkung der Frühinstillation
auf Low Risk korrigiert und der Merksatz zur möglichen zusätzlichen Muskelinvasion
präzisiert. Die Fragenversion wurde dafür erhöht.

Die neue Auswertung trennt Trefferquote (letzte Antwort pro Frage), Abdeckung,
Erstversuche und Anzahl der Versuche. Wiederholung überschreibt keinen bekannten
Erstversuch. Alte Daten ohne Erstversuchsangabe bleiben ausdrücklich unbekannt.
Die Lernkategorien beruhen auf transparenten Schwellen: mindestens fünf verschiedene
Fragen, ≥80 % Stärke, 60–79 % weiter festigen, darunter Übungsbedarf. Kleinere
Stichproben erhalten keine Stärke-/Schwäche-Einstufung. Diese Schwellen sind
redaktionelle Lernhilfen und nicht klinisch validiert.

Geprüft wurden Auswahl ohne Duplikate, ausgeglichene Gebiete, Fehler-/Neu-/Alt-Mix,
Erhalt der Erstversuche, Migration älterer Fortschrittsdaten, beschädigter Speicher,
Zurücksetzen, ungültige Fragenversionen, Kategoriengrenzen, gezielte Fehlerübung,
Doppelklickschutz, laufende Zähler, abgebrochene Runden, Gebietsaufschlüsselung
und spanischer Export. Python- und JavaScript-Tests erfolgreich.
Keine visuelle Browserprüfung oder unabhängige fachärztliche Freigabe erfolgt.

## Vorheriger Prüfstand vom 10. September

Ausgangspunkt ist die Live-Seite mit 187 Fragen in 16 Gebieten. Alle ursprünglichen
IDs bleiben erhalten. Die Spanischabdeckung steigt von 10 auf 187 Fragen:
Fall, Fragestellung, Optionen, Begründungen, Merksätze und Evidenzhinweise.
Offizielle bibliografische Titel bleiben in ihrer Originalsprache.

Spanisch wurde maschinell vorübersetzt und anschließend KI-gestützt redigiert.
Korrigiert wurden unter anderem Bosniak, Boari, Gefäße, venöse Sinus, PSA,
Stadium IS und IMDC-Risikogruppen. Ein ganz unübersetzter Block wurde ersetzt.
Der Zahlenabgleich erkannte nur eine zulässige Formatänderung: 4 pm → 16:00.

## Wichtigste fachliche Korrekturen

| Fragen | Änderung | Referenz |
|---|---|---|
| uro-lit-00002 | Keine routinemäßige L-Methionin-Empfehlung bei Brushit | [EAU](https://uroweb.org/guidelines/urolithiasis/chapter/metabolic-evaluation-and-recurrence-prevention) |
| uro-lit-00003 | NOSTONE-Population korrigiert; keine automatische Zitratgabe | [Originalstudie](https://www.nejm.org/doi/abs/10.1056/NEJMoa2209275) |
| uro-pca-00020 | Frakturrisiko statt automatischer Denosumab-Gabe unter ADT | [EAU](https://uroweb.org/guidelines/prostate-cancer/chapter/followup) |
| uro-rek-00005 | Prostatisches CIS schließt Neoblase nicht pauschal aus; richtige Antwort C → B | [EAU](https://uroweb.org/guidelines/muscle-invasive-and-metastatic-bladder-cancer/chapter/disease-management) |
| uro-kin-00006 | Asymptomatische physiologische Vorhautenge: Aufklärung und Abwarten | [EAU](https://uroweb.org/guidelines/paediatric-urology/chapter/phimosis-and-other-abnormalities-of-the-penile-skin) |
| uro-kin-00004 | MCU-Erwägung bei febrilem Harnwegsinfekt unter einem Jahr ergänzt | [EAU](https://uroweb.org/guidelines/paediatric-urology/chapter/urinary-tract-infections-in-children) |
| uro-hod-00005, 00013 | PET-Abstand und Interpretation positiver Befunde präzisiert | [EAU](https://uroweb.org/guidelines/testicular-cancer/chapter/followup-after-curative-therapy) |
| uro-hod-00002, 00006 | EP/VIP-Indikationen getrennt; eindeutiges Lymphknotenwachstum ergänzt | [EAU](https://uroweb.org/guidelines/testicular-cancer/chapter/disease-management) |
| uro-hod-00019 | Keine starre Sauerstoffrestriktion nach Bleomycin | [Studie](https://pmc.ncbi.nlm.nih.gov/articles/PMC3987121/) |
| uro-rcc-00002 | Fallvignette mit günstigem IMDC-Risiko vereinbar gemacht | [EAU](https://uroweb.org/guidelines/renal-cell-carcinoma/chapter/prognostic-factors) |
| uro-rek-00001 | Urethroplastiktechnik individualisiert | [EAU](https://uroweb.org/guidelines/urethral-strictures/chapter/disease-management-in-males) |
| uro-rek-00013 | Stabile KHK kein automatischer Ausschluss; Tumorrisiko genauer beurteilen | [KDIGO](https://pmc.ncbi.nlm.nih.gov/articles/PMC7147399/) |
| uro-ope-00018 | Neurologisch symptomatische Hyponatriämie: Akuttherapie von Korrekturgrenzen unterscheiden | [Notfallleitlinie](https://www.endocrinology.org/media/xhrhxhxm/emergency-management-of-severe-and-moderately-severely-symptomatic-hyponatraemia-in-adult-patients-2022.pdf) |
| uro-tra-00013 | Dringliche Exploration statt vermeintlichem Wartefenster | [EAU](https://uroweb.org/guidelines/urological-trauma/chapter/urogenital-trauma-guidelines) |
| uro-nmi-00001, 00002 | Nachresektion auch therapeutisch; BCG-Erhaltung ein bis drei Jahre | [EAUN](https://nurses-new.uroweb.org/guidelines/intravesical-instillation/chapter/common-treatment-schedules) |
| uro-pca-00011 | Ungünstiges intermediäres Risiko ausdrücklich definiert | [EAU](https://uroweb.org/guidelines/prostate-cancer/chapter/treatment) |
| uro-pca-00018 | PSMA- und Vortherapiekriterien präzisiert | [EMA](https://www.ema.europa.eu/en/medicines/human/EPAR/pluvicto) |
| uro-mib-00002, 00003 | Neoadjuvante Zyklen benannt; DKA-Ursache offen; unbelegte behandlungsbedingte Todesfallangaben entfernt | [EMA](https://www.ema.europa.eu/en/medicines/human/EPAR/padcev) |
| uro-utu-00002 | Starke und schwächere Risikomerkmale getrennt | [EAU](https://uroweb.org/guidelines/upper-urinary-tract-urothelial-cell-carcinoma/chapter/risk-stratification) |
| uro-ure-00001, 00005, 00008 | Histologie nicht allein aus Epithel ableiten; definitive Radiochemotherapie und begrenzte Evidenz kenntlich | [EAU](https://uroweb.org/guidelines/primary-urethral-carcinoma/chapter/disease-management) |
| uro-ope-00008 | Jejunumfolgen nicht pauschal als Gegenteil ilealer Azidose beschrieben | [EAUN](https://nurses.uroweb.org/wp-content/uploads/0628EAUN_Guideline_2010_HR.pdf) |

Zusätzlich wurden Satzduplikate in uro-ope-00005, uro-ope-00019, uro-pca-00003,
uro-utu-00004 und uro-utu-00005 entfernt. Insgesamt betreffen die Änderungen am
Ausgangstext 32 Fragen; `review/editorial-changes.json` enthält die Felderliste.
Spanische Fachterminologie und missverständliche Formulierungen wurden darüber
hinaus im gesamten Bestand redigiert.

Die unterschiedliche EU-/US-Indikation in uro-mib-00004 wurde anhand
von [EMA](https://www.ema.europa.eu/en/medicines/human/EPAR/padcev) und
[FDA vom 10. Juli 2026](https://www.fda.gov/drugs/resources-information-approved-drugs/fda-approves-pembrolizumab-or-pembrolizumab-and-berahyaluronidase-alfa-pmph-each-enfortumab-vedotin)
abgeglichen und beibehalten.

## Technische Prüfung

- 187 eindeutige IDs erhalten; 561 vollständige Sprachfassungen.
- Genau eine richtige Antwort; identische Schlüssel über Sprachen.
- Fehlendes Spanisch bei veröffentlichten Fragen verhindert den Build.
- Sprachwechsel erhält Antworten und die Ergebnisseite.
- Seitentitel, Evidenzbegriffe, Quellenhinweise und Ergebnisexport lokalisiert.
- Alte Antworten auf geänderte Fragenversionen werden erneut fällig.
- Ablaufdatum in Builder und Anwendung konsistent behandelt.
- JavaScript-Syntax und Abläufe mit simuliertem Dokument getestet.
- Kein visueller Browsertest oder physischer Druckdialogtest durchgeführt.

## Umfang und Grenzen

Alle Fragen wurden auf Struktur, Schlüssel und Übersetzungsabdeckung geprüft.
Medizinische Quellenabgleiche erfolgten gezielt bei gefundenen Auffälligkeiten.
Dies bestätigt nicht jede Dosierung, Evidenzstufe, Registernummer oder Aussage
im gesamten Bestand. Die ursprünglichen Evidenzstufen wurden überwiegend
übernommen und bedürfen gesonderter Validierung.

Eine unabhängige fachärztliche Zweitprüfung steht aus, auch für die Korrekturen.
Bestehende Autoren- und Prüferfelder wurden nicht durch erfundene Freigaben
ersetzt. Dieser Status wird nun auch in der Anwendung und im Export angezeigt.
Das Material bleibt zur Prüfungsvorbereitung bestimmt.
