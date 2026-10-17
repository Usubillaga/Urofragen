# Wochenberichte und gezielte Residency-Übernahmen – 17.10.2026

Die Lernstartseite verlinkt das dauerhafte [Archiv der Wochenberichte](weekly-reports/README.md#ausgaben). Dort stehen Studien- und Wartungsberichte vollständig auf Spanisch, Englisch und Deutsch. Die Beschriftung des Links folgt der gewählten Lernsprache. Das Öffnen in einem neuen Tab erhält die Lernseite.

## Fragenänderungen

Fünf ergänzende Fälle wurden aus dem geprüften Korrekturstand von [Residency-Game-DE](https://github.com/Usubillaga/Residency-Game-DE/tree/a853851ef6afdc34861dde63daf422eb2e1a86f8/data) angepasst. Quelle ist die wirksame Fallfassung **nach** Anwendung von `data/case-updates.json`, kein neuer Rohimport der Urofragen-Daten. Die neue Bank hat **262 verfügbare Lernfragen und 10 bestehende OP-Entwürfe, zusammen 272 Datensätze**. Alle 267 bisherigen IDs bleiben erhalten; die vier CME-Module mit 50 Fragen bleiben separat.

| Urofragen-ID | Version | Inhalt und ursprünglicher Residency-Fall |
|---|---|---|
| `uro-and-00011` | neu, 1 | Refraktärer ischämischer Priapismus mit MRT-Nekrosehinweisen: Beratung über frühe Prothese; `q-pri-ischaemic-40h-mri-necrosis-early-prosthesis` |
| `uro-and-00012` | neu, 1 | Frühe orale EAU-Option nach Schwellkörperinjektion; keine Verzögerung der Ischämiebehandlung; `q-pri-prolonged-erection-after-ici-terbutaline-first` |
| `uro-pca-00024` | neu, 1 | Basis-PSA 2,1 ng/ml: ausdrücklich S3-Version 8.1, Empfehlung 4.4; `q-pca-baseline-psa-intermediate-interval` |
| `uro-pca-00025` | neu, 1 | Spezieller BRCA2-Risikopfad einschließlich Biopsieberatung trotz unauffälliger MRT; `q-pca-brca2-carrier-confirmed-psa-mri` |
| `uro-rcc-00013` | neu, 1 | Grenzen von Sestamibi und onkozytärer Stanzbiopsie vor Überwachung/Ablation; `q-rcc-sestamibi-positive-biopsy-before-surveillance` |
| `uro-rek-00012` | 1 → 2 | Ureteroenterische Strikturen häufiger links als rechts; Seitenverteilung und Originalquelle berichtigt. Antwortschlüssel unverändert. |
| `uro-lit-00003` | 2 → 3 | EAU-Grenzwert ausdrücklich: Hypozitraturie bei Männern unter 1,7 mmol/Tag; 2,2 mmol/Tag erfüllt ihn nicht. Zwei aufeinanderfolgende 24-Stunden-Sammlungen zur spezifischen Stoffwechselbeurteilung. Antwortschlüssel unverändert. |

Alle Fragen enthalten vollständige Texte, Optionen und Einzelbegründungen in DE/EN/ES. Die neuen Fragen übernehmen keine Spielpunkte, Patientennamen oder Freigaben aus Residency. Zu lange richtige Antworten wurden verkürzt; die medizinischen Einschränkungen bleiben in den Begründungen. `import_record` und [Adaptationsprotokoll](updates/2026-10-17/residency-adaptations.json) halten Herkunft, Commit und ID-Zuordnung fest.

## Quellenabgleich und Grenzen

- [EAU 2026, Priapism](https://uroweb.org/guidelines/sexual-and-reproductive-health/chapter/priapism), 10.1.2–10.1.4 und Tabelle 10.4: Ischämie ist ein Notfall. Orales Terbutalin ist eine begrenzt belegte frühe Option nach Injektion, kein verpflichtender erster Behandlungsschritt. Hinweise auf Nekrose unterstützen spezialisierte Prothesenberatung; die Evidenz ist überwiegend retrospektiv. Keine automatische Implantationspflicht nach 40 Stunden.
- [Deutsche Bricanyl-Fachinformation, März 2022](https://www.fachinfo.de/fi/pdf/004867/bricanyl-r-0-5-mg), 4.1/4.4: Atemwegsindikation und kardiovaskuläre Risiken. Diese Injektions-Fachinformation belegt weder eine Priapismuszulassung noch eine orale Dosis oder aktuelle Verfügbarkeit eines oralen Präparats. Die orale Dosisangabe stammt allein aus der EAU-Tabelle.
- [S3 Prostatakarzinom, Kurzversion 8.1, August 2025](https://www.leitlinienprogramm-onkologie.de/fileadmin/user_upload/Downloads/Leitlinien/Prostatatkarzinom/Version_8/22_05_2026_Prostatakarzinom_Kurzversion_8.1_final_KL.pdf), S. 21–22: Empfehlung 4.4, Empfehlungsgrad A, für PSA-Intervalle; 4.8–4.10 sind konsensbasierte Empfehlungen für pathogene Varianten. Dokumentversion und Abrufdatum werden nicht als neue Leitlinienveröffentlichung ausgegeben.
- [EAU RCC: Diagnostik](https://uroweb.org/guidelines/renal-cell-carcinoma/chapter/diagnostic-evaluation), 5.2.3/5.3/5.4; [Pathologie](https://uroweb.org/guidelines/renal-cell-carcinoma/chapter/epidemiology-aetiology-and-pathology), 3.5.4–3.5.5; [Therapie](https://uroweb.org/guidelines/renal-cell-carcinoma/chapter/disease-management), 7.2.4: Sestamibi noch unzureichend extern validiert; keine definitive Onkozytomdiagnose in der Stanzbiopsie; Biopsie vor Ablation starke, Auswahl zur Überwachung schwache Empfehlung.
- [Yang et al., Originalkohorte, 2020](https://tau.amegroups.org/article/view/29662/html), DOI 10.21037/tau.2019.09.05: Linksbetonung ureteroenterischer Strikturen. Retrospektiver Einzelzentrumsbefund; die vermutete Ischämie nach Mobilisierung ist keine gesicherte individuelle Ursache.
- [EAU Urolithiasis, 4.1.2 und Tabelle 4.2](https://uroweb.org/guidelines/urolithiasis/chapter/metabolic-evaluation-and-recurrence-prevention): geschlechtsspezifische Citratgrenzen. Der Residency-Korrekturtext mit einem behaupteten EAU-Grenzwert von 2,5 mmol/Tag wurde **nicht** übernommen; diese Abweichung wurde beim Quellenabgleich erkannt. Der NOSTONE-Antwortschlüssel bleibt erhalten.

Quellen geprüft am **17.10.2026**. Bei den neuen und medizinisch veränderten Fragen ist die unabhängige fachärztliche Prüfung jeder Sprache ausstehend. Die **51 bestehenden deutschen Freigaben bleiben inhaltlich und hinsichtlich ihrer Fingerprints unverändert**; technische Prüfungen schaffen keine neue Freigabe.
