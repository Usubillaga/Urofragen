# Abschnitt Urodynamik – 20.10.2026

Neuer 17. Abschnitt **Urodynamik** mit zehn dreisprachigen Fallfragen (`data/fragen/urodynamik.json`). Die Bank hat damit **272 verfügbare Lernfragen und 10 bestehende OP-Entwürfe, zusammen 282 Datensätze**. Alle bisherigen IDs, Freigaben und CME-Module bleiben unverändert.

## Fälle

| ID | Thema | Richtige Antwort | Evidenzhinweis | Fall in Residency-Game-DE (Entscheidungen) |
|---|---|---|---|---|
| `uro-udy-00001` | Druck-Fluss-Messung | Obstruktion bei normaler Kontraktilität – Desobstruktion ist gut begründet | – | `udy-bpo-pressure-flow-indices` (3) |
| `uro-udy-00002` | Detrusorunteraktivität | Intermittierender Katheterismus; für den Drang bevorzugt Beta-3-Agonist | ⚠ eingeschränkt | `udy-dhic-elderly-man-no-turp` (3) |
| `uro-udy-00003` | Videourodynamik | Primäre Blasenhalsobstruktion; zunächst ein Alphablocker | ⚠ eingeschränkt | `udy-pbno-young-man-vuds` (3) |
| `uro-udy-00004` | Neurourologie | Keine Resektion: Verdacht auf MSA, Katheterismus und Neurologie | ⚠ eingeschränkt | `udy-msa-before-turp` (3) |
| `uro-udy-00005` | Weibliche Blasenauslassobstruktion | Bandrevision mit Aufklärung über ein Rezidiv der Belastungsinkontinenz | – | `udy-female-boo-after-sling` (3) |
| `uro-udy-00006` | Harnverhalt der Frau | Sakrale Neuromodulation nach erfolgreicher Testphase | ⚠ eingeschränkt | `udy-fowler-retention-young-woman` (3) |
| `uro-udy-00007` | Okkulte Belastungsinkontinenz | Gemeinsame Entscheidung: weniger Inkontinenz, aber mehr Komplikationen | – | `udy-occult-sui-prolapse-reduction` (3) |
| `uro-udy-00008` | Compliance | Compliance 6,5 ml/cmH2O; mit physiologischer Füllrate wiederholen | – | `udy-low-compliance-sci-filling-rate` (3) |
| `uro-udy-00009` | Kinderurologie | Urotherapie mit Obstipationsbehandlung, bei Persistenz Biofeedback | ⚠ Expertenkonsens | `udy-paediatric-dysfunctional-voiding` (3) |
| `uro-udy-00010` | Qualitätskontrolle und Artefakte | Rektumkontraktionen; vesikale Leitung spülen, Hustentest wiederholen | – | `udy-artefacts-rectal-contraction-transmission` (3) |

Jede Frage hat fünf Optionen mit Einzelbegründungen, Kernaussage, Merksatz und Quellen in DE/EN/ES. Die Antwortpositionen werden in jeder Runde gemischt; die richtige Option ist in keiner Sprache die längste. Fragen mit ⚠ zeigen den Evidenzhinweis nach der Antwort.

In Residency-Game-DE sind dieselben Fälle Mehrschrittfälle mit je drei Entscheidungen, Oberarzt-Hinweisen und verknüpfter Lernzeichnung. `companion_case` verknüpft jede Frage mit ihrem Fall; `updates/2026-10-20/urodynamik-abschnitt.json` hält Zuordnung und Quellen fest.

## Quellenabgleich

Geprüft am **20.10.2026**:

- [EAU 2026, Management of Non-neurogenic Male LUTS – Diagnostic Evaluation](https://uroweb.org/guidelines/management-of-non-neurogenic-male-luts/chapter/diagnostic-evaluation), 4.12: Urodynamik nur bei gezielter Indikation vor invasiver Therapie, darunter Qmax über 10 ml/s, Miktionsvolumen unter 150 ml, Alter unter 50 oder über 80 Jahre, erfolglose invasive Vorbehandlung (jeweils schwach); BOOI und BCI mit Grenzwerten; UPSTREAM 38 % gegenüber 36 % operiert.
- [EAU 2026, Male LUTS – Disease Management](https://uroweb.org/guidelines/management-of-non-neurogenic-male-luts/chapter/disease-management), 5.2.1/5.2.3/5.2.4: Ejakulationsstörung unter selektiven Alphablockern, häufiger bei jüngeren Männern, mit Aufklärungspflicht; keine Antimuskarinika bei Restharn über 150 ml (schwach); Mirabegron ohne Verschlechterung der Miktionsparameter bei Obstruktion.
- [EAU 2026, Neuro-Urology](https://uroweb.org/guidelines/neuro-urology/chapter/the-guideline), 3.3.7/3.3.8/3.4: physiologische Füllrate mit körperwarmer Lösung und Wiederholungsmessung (stark), Videourodynamik als optimales Verfahren, Gefährdung des oberen Harntrakts durch hohen Füllungsdruck, Leckagedruck nicht als alleiniges Diagnostikum, Augmentation bei niedriger Compliance nach Versagen weniger invasiver Verfahren.
- [EAU 2026, Non-neurogenic Female LUTS – Pocket Guidelines](https://d56bochluxqnz.cloudfront.net/documents/pocket-guidelines/EAU-Pocket-on-Non-Neurogenic-Female-LUTS-2026_2026-03-12-155317_rckt.pdf) und [Diagnosis](https://uroweb.org/guidelines/non-neurogenic-female-luts/chapter/diagnosis): Obstruktion nicht allein aus der Uroflowmetrie, Urodynamik möglichst mit Durchleuchtung und Urethrozystoskopie (stark); keine Dilatation oder Urethrotomie nach synthetischem Band wegen des theoretischen Risikos einer Netzextrusion (schwach); Bandrevision und Aufklärung über erneute Belastungsinkontinenz (stark); Katheterismus und sakrale Nervenstimulation bei unteraktiver Blase (stark) und funktioneller Obstruktion (schwach); Prolaps-Repositionstest bei kontinenten Frauen und kombinierte Operation nur nach ausführlicher Aufklärung (stark); kein allgemein akzeptierter Obstruktionsgrenzwert bei Frauen.
- Originalarbeiten: OPUS ([N Engl J Med 2012](https://doi.org/10.1056/NEJMoa1111967)), Druck-Fluss-Indizes ([BJU Int 1999](https://doi.org/10.1046/j.1464-410x.1999.00121.x)), Detrusorunteraktivität vor transurethraler Chirurgie ([J Urol 2018](https://doi.org/10.1016/j.juro.2017.07.079)), Mirabegron bei Obstruktion ([J Urol 2013](https://doi.org/10.1016/j.juro.2013.05.062)), primäre Blasenhalsobstruktion ([Urol Res Pract 2024](https://doi.org/10.5152/tud.2024.23155); [Eur Urol Focus 2025](https://uroluts.uroweb.org/publication/management-of-primary-bladder-beck-obstruction-and-dysfunctional-voiding-in-young-men-a-systematic-review-and-meta-analysis/)), MSA ([J Neurol Neurosurg Psychiatry 2001](https://jnnp.bmj.com/content/71/5/600); [Br J Urol 1997](https://doi.org/10.1046/j.1464-410X.1997.00249.x); [MDS-Kriterien 2022](https://doi.org/10.1002/mds.29005)), Fowler-Syndrom ([Eur Urol 2000](https://pubmed.ncbi.nlm.nih.gov/11025383/)), ICCS ([Terminologie 2016](https://doi.org/10.1002/nau.22751); [dysfunktionelle Miktion 2010](https://doi.org/10.1016/j.juro.2009.12.059)).
- ICS-Lehrmaterial zur Qualitätskontrolle ([Teaching-Modul auf Basis von ICS-GUP 2016](https://www.ics.org/Workshops/HandoutFiles/001011.pdf); [Workshop Basic Urodynamics](https://www.ics.org/Workshops/HandoutFiles/000601.pdf)): Ruhedruckbereiche, Hustentests, 70-%-Regel, Rektumkontraktionen.

## Gegenprüfung und Nachprüfung am 24.10.2026

Ein unabhängiger KI-Reviewer hat alle zehn Fälle geprüft: keine falsch verschlüsselte Antwort, keine Rechenfehler, aber zwei inhaltlich relevante und mehrere kleinere Präzisierungen. Jeder Befund wurde vor der Übernahme an der Originalquelle nachgeprüft und in allen drei Sprachen umgesetzt:

| Frage | Befund | Nachgeprüft an | Änderung |
|---|---|---|---|
| `uro-udy-00003` | Ejakulationsstörung auch unter Alphablockern fehlte | Eur Urol Focus 2025 (Abstract), EAU Male LUTS 5.2.1, [BMC Urol 2012](https://doi.org/10.1186/1471-2490-12-29) | Alphablocker als Erstlinie mit Ejakulationsstörung bei 47–50 %, nach Absetzen in der Regel reversibel; Inzision mit möglicherweise bleibender Störung; Evidenzhinweis mit 0–88,8 % nach operativer Therapie und gemeinsamer Entscheidung. Zwei Quellen ergänzt. |
| `uro-udy-00007` | NNT 6,3 gilt für alle kontinenten Frauen, nicht für die Untergruppe mit positivem Test | OPUS-Abstract (NEJM), ICS-Kongressabstract, Fachbericht zur Subgruppe | NNT ausdrücklich dem Gesamtkollektiv zugeordnet (etwa ein Drittel mit positivem Test); Subgruppe nach drei Monaten 29,6 % vs. 71,9 %, Interaktion nicht signifikant. Die frühere Aussage „nach zwölf Monaten statistisch nicht mehr gesichert“ ist entfernt, weil die Quelle sie nicht eindeutig trägt. |
| `uro-udy-00002` | Mirabegron-Daten stammen aus einer 12-Wochen-Studie bei Obstruktion, nicht bei DHIC | J Urol 2013 (Abstract), EAU Male LUTS 5.2.4 | Extrapolation benannt; fehlende anticholinerge Wirkung als Argument im Alter; Hinweis und Fazit präzisiert. |
| `uro-udy-00004` | „Blasenstörung vor der Motorik“ war aus der Vignette nicht ablesbar | – | Zeitachse ergänzt: Blasensymptome seit drei Jahren, erste motorische Symptome vor zwei Jahren, Diagnose vor 18 Monaten. |
| `uro-udy-00005` | Begründung der EAU gegen Dilatation | EAU-Pocket Female LUTS | „theoretisches Risiko einer Netzextrusion“, schwache Empfehlung. |
| `uro-udy-00006` | „Therapie der Wahl“ und „belegt“ zu stark; EAU-Haltung zu Medikamenten | EAU-Pocket Female LUTS, Übersichten zum Fowler-Syndrom | Alphablocker nur off-label bei funktioneller Obstruktion (schwach), Parasympathomimetika nicht routinemäßig (stark); Neuromodulation mit etwa 70 % Spontanmiktion in Fallserien; Prostaglandine nur in Studien (schwach). |
| `uro-udy-00009` | Biofeedback ist die zweite Stufe, nicht Ergänzung | ICCS 2010 | Option: „bei Persistenz Biofeedback“. |
| `uro-udy-00010` | Erneutes Nullen verfälscht nur, wenn gegen Körperdruck genullt wird | ICS-basiertes Lehrmaterial | Begründung präzisiert: Null ist der Atmosphärendruck. |

Zusätzlich bestätigt: die physiologische Füllrate Körpergewicht/4 ml/min (ICS-Terminologie 2002), Hustentests etwa jede Minute oder alle 50 ml, alle elf Männer mit MSA nach TURP inkontinent, Restharnkriterium der MDS 2022, die Endpunkte der Metaanalyse 2018 (geringere Besserung von IPSS und Qmax, nicht von Lebensqualität und Restharn) und etwa 70 % Erfolg der Neuromodulation beim Fowler-Syndrom.

## Grenzen

- **Ohne fachärztliche Freigabe.** Die KI-Gegenprüfung ersetzt nicht deine Prüfung jeder Sprache im Prüfmodus.
- Fünf Fragen tragen bewusst einen Evidenzhinweis: DHIC (keine randomisierten Therapiestudien), primäre Blasenhalsobstruktion (kleine, nicht randomisierte Serien), MSA (Fallserien und Konsens), Fowler-Syndrom (Fallserien) und kindliche dysfunktionelle Miktion (überwiegend ICCS-Konsens).
- Grenzwerte ohne allgemeinen Konsens sind als solche benannt: Compliance-Normwerte, der historische Leckagedruck von 40 cmH2O und das Nomogramm für Frauen (BOOIf).
- Nicht im Volltext prüfbar: Der OPUS-Volltext war am 24.10.2026 nicht abrufbar; die Subgruppenwerte (29,6 % vs. 71,9 %, Interaktion p = 0,06) stammen aus einem Fachbericht über die Publikation, die übrigen OPUS-Zahlen aus dem Abstract. Die Zuordnung „0–88,8 % nach operativer Therapie“ folgt der Reihenfolge im Abstract von 2025.
- Die Formulierungen der EAU zu Alphablockern und Parasympathomimetika bei Frauen wurden im Wortlaut der Pocket-Ausgabe 2022 geprüft. Laut Änderungsübersichten sind 2024 und 2026 Nachdrucke, und 2025 nennt für diese Empfehlungen keine Änderung.
- Die MDS-Kriterien 2022 schreiben den Restharn in Tabelle 1 als „≥ 100 mL“, im Text und in Tabelle 3 als „> 100 mL“; die Fragen verwenden „über 100 ml“, die Fallwerte (180–190 ml) liegen in beiden Fällen darüber.
- Reversibilität der Ejakulationsstörung: belegt für Silodosin in einer kleinen Studie (alle Betroffenen erholten sich nach dem Absetzen); für andere Alphablocker übertragen.
- Ohne direkten Link zitiert: Fowler und Kirby 1985, Resnick und Yalla 1987, McGuire 1981, Solomon 2018 (BOOIf), ICS-Terminologie 2002 und ICS-GUP 2002/2016 als Originalarbeiten; die Aussagen daraus sind über die verlinkten Leitlinien, Übersichten oder ICS-Lehrmaterialien belegt.

## Technik

- `data/domains.json`: Abschnitt `urodynamik` direkt nach `funktionell`; der Hinweistext von `funktionell` lautet jetzt „LUTS, OAB, Inkontinenz, Neurourologie, Neuromodulation“.
- `python build.py` erzeugt `index.html` und `pruefung.html` neu; die CME-Dateien bleiben bytegleich.
- Tests: Fragenzahlen in `review/verify.py`, `review/verify_update.py`, `review/verify_cme.py` und `review/test_review_ui.cjs` auf 282/272 angepasst; neuer Test für Vollständigkeit, Prüfstatus und Verknüpfung des Abschnitts.
- Lokal bestanden: alle Schritte aus `.github/workflows/pruefung.yml` einschließlich der drei Browsertests sowie `review/verify.py` und `review/test_review_ui.cjs`.
