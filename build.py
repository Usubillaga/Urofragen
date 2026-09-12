#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Facharztfragen Urologie — baut aus data/domains.json und data/fragen/*.json
eine einzelne index.html.

    python3 build.py

Pro Gebiet eine Datei unter data/fragen/, benannt wie der Slug in domains.json.
Richtigkeit, Quellen und Ablaufdatum existieren pro Frage genau einmal,
uebersetzt werden nur die Texte unter "content".

Keine Bibliotheken noetig, Python 3.8 oder neuer.
"""

import json
import sys
from datetime import date, timedelta
from pathlib import Path
from quality import issues as quality_issues
from quality import corpus_issues as quality_corpus_issues
from approval import valid_approval
from review_ui import write_review_page

ROOT = Path(__file__).resolve().parent
DATA = ROOT / "data" if (ROOT / 'data' / 'domains.json').exists() else ROOT
FRAGEN = DATA / "fragen" if DATA != ROOT else ROOT
OUT = ROOT / "index.html"

STATUS = {"draft", "review", "published", "retired", "expired"}
CERTAINTY = {"etabliert", "kontrovers", "ohne_phase_III", "expertenkonsens"}

errors = []
warnings = []


def load(path):
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        errors.append(f"{path.name} fehlt")
    except json.JSONDecodeError as e:
        errors.append(f"{path.name}: kein gueltiges JSON — Zeile {e.lineno}, Spalte {e.colno}: {e.msg}")
    return None


def check(q, slug, tags, languages, seen, today, soon, length_cue, longest_correct, coverage):
    qid = q.get("id") or "(ohne id)"

    def bad(msg):
        errors.append(f"{qid}: {msg}")

    if not q.get("id"):
        bad("id fehlt")
    elif q["id"] in seen:
        bad("id doppelt vergeben")
    else:
        seen.add(q["id"])

    if not isinstance(q.get("version"), int):
        bad("version fehlt oder ist keine Zahl")
    if q.get("status") not in STATUS:
        bad(f"status \"{q.get('status')}\" unbekannt")

    tax = q.get("taxonomy") or {}
    if tax.get("domain") and tax["domain"] != slug:
        bad(f"taxonomy.domain \"{tax['domain']}\" widerspricht der Datei {slug}.json")
    for tag in tax.get("tags", []):
        if tag not in tags:
            bad(f"Tag \"{tag}\" nicht im kontrollierten Vokabular")

    if q.get("type") != "single_best_answer":
        bad(f"Fragetyp \"{q.get('type')}\" wird nicht unterstuetzt")

    opts = q.get("options") or []
    if len(opts) < 4:
        bad(f"nur {len(opts)} Antwortoptionen, mindestens 4 gefordert")

    correct = [o for o in opts if o.get("correct")]
    if len(correct) != 1:
        bad(f"{len(correct)} als richtig markierte Optionen, genau 1 gefordert")

    keys = []
    for o in opts:
        if o.get("key") in keys:
            bad(f"Optionsschluessel \"{o.get('key')}\" doppelt")
        keys.append(o.get("key"))

    ev = q.get("evidence") or {}
    if ev.get("certainty") not in CERTAINTY:
        bad(f"evidence.certainty \"{ev.get('certainty')}\" unbekannt")
    if ev.get("certainty") != "etabliert" and ev.get("flag") is not True:
        bad("nicht etablierte Evidenz muss flag: true tragen")

    if not q.get("sources"):
        bad("keine Quelle angegeben")

    content = q.get("content") or {}
    for lc in languages:
        body = content.get(lc)
        if not body:
            if lc == languages[0] or q.get('status') == 'published':
                bad(f"Sprache \"{lc}\" fehlt vollstaendig")
            else:
                coverage.setdefault(lc, [0, 0])[1] += 1
            continue
        coverage.setdefault(lc, [0, 0])
        coverage[lc][0] += 1
        coverage[lc][1] += 1
        if not body.get("vignette"):
            bad(f"[{lc}] vignette fehlt")
        if not body.get("lead_in"):
            bad(f"[{lc}] lead_in fehlt")
        if lc == 'es' and body.get('lead_in') == (content.get('en') or {}).get('lead_in'):
            bad('[es] lead_in ist unuebersetzt aus Englisch uebernommen')
        if not (body.get("explanation") or {}).get("core"):
            bad(f"[{lc}] explanation.core fehlt")
        if not (body.get("explanation") or {}).get("teaching_point"):
            bad(f"[{lc}] explanation.teaching_point fehlt")
        texts = body.get("options") or {}
        for k in keys:
            entry = texts.get(k) or {}
            if not entry.get("text"):
                bad(f"[{lc}] Option {k}: text fehlt")
            if not entry.get("rationale"):
                bad(f"[{lc}] Option {k}: rationale fehlt")
        extra = [k for k in texts if k not in keys]
        if extra:
            bad(f"[{lc}] unbekannte Optionsschluessel: {', '.join(extra)}")
        if ev.get("flag") is True and not body.get("flag_note"):
            bad(f"[{lc}] flag: true ohne flag_note")
        lengths = {k: len((texts.get(k) or {}).get("text") or "") for k in keys}
        ck = correct[0].get("key") if correct else None
        if lc == languages[0] and ck in lengths and len(lengths) > 1:
            longest_correct[1] += 1
            if lengths[ck] == max(lengths.values()):
                longest_correct[0] += 1
        if ck in lengths and len(lengths) > 1:
            others = [v for k, v in lengths.items() if k != ck]
            avg = sum(others) / len(others)
            if avg > 0 and lengths[ck] / avg >= 1.5:
                warnings.append(
                    f"{qid} [{lc}]: richtige Option {lengths[ck]/avg:.1f}-mal so lang wie die Distraktoren "
                    f"— die Laenge verraet die Antwort")
                length_cue.append(qid)
            elif lengths[ck] == max(lengths.values()) and lengths[ck] / avg >= 1.25:
                warnings.append(
                    f"{qid} [{lc}]: richtige Option ist die laengste ({lengths[ck]/avg:.2f}x)")

    review = q.get("review") or {}
    expires = review.get("expires")
    live = False
    if not expires:
        bad("review.expires fehlt (Pflichtfeld)")
    else:
        try:
            d = date.fromisoformat(expires)
        except ValueError:
            bad(f"review.expires \"{expires}\" ist kein gueltiges Datum")
        else:
            if d < today:
                warnings.append(f"{qid}: abgelaufen am {expires}, wird nicht ausgeliefert")
            else:
                if d < soon:
                    warnings.append(f"{qid}: laeuft am {expires} ab")
                live = q.get("status") == "published"

    if q.get("status") == "published" and not valid_approval(q):
        warnings.append(f"{qid}: fachärztliche Freigabe ausstehend")
    review['approval_valid'] = valid_approval(q)

    for lc, kind, description in quality_issues(q):
        if kind in {'generic_lead','mixed_stem','duplicate_rationale','duplicate_option'}:
            bad(f'[{lc}] {description}')
        elif kind != 'long_cue':
            warnings.append(f'{qid} [{lc}]: {description}')

    return live


def main():
    config = load(DATA / "domains.json")
    if config is None:
        for e in errors:
            print("Fehler   " + e, file=sys.stderr)
        return 1

    languages = config.get("languages", ["de"])
    if not languages or len(set(languages)) != len(languages) or any(lc not in {'de','en','es'} for lc in languages):
        errors.append('languages muss eine eindeutige Liste aus de, en, es sein')
        return 1
    for item in config.get('groups', []) + config.get('domains', []):
        for lc in languages:
            if not (item.get('label') or {}).get(lc):
                errors.append(f"{item.get('slug')}: label.{lc} fehlt")
            if 'hint' in item and not item['hint'].get(lc):
                errors.append(f"{item.get('slug')}: hint.{lc} fehlt")
    domains = {d["slug"] for d in config["domains"]}
    tags = set(config.get("tags", []))
    today = date.today()
    soon = today + timedelta(days=90)
    seen = set()
    counts = {slug: 0 for slug in domains}
    length_cue = []
    longest_correct = [0, 0]
    coverage = {}

    if not FRAGEN.is_dir():
        errors.append("Ordner data/fragen fehlt")
        for e in errors:
            print("Fehler   " + e, file=sys.stderr)
        return 1

    # Dateien, die zu keinem deklarierten Gebiet gehoeren
    for f in sorted(FRAGEN.glob("*.json")):
        if FRAGEN == ROOT and f.name == 'domains.json':
            continue
        if f.stem not in domains:
            errors.append(f"data/fragen/{f.name}: \"{f.stem}\" ist in domains.json nicht deklariert")

    questions = []
    for d in config["domains"]:
        slug = d["slug"]
        path = FRAGEN / f"{slug}.json"
        if not path.exists():
            warnings.append(f"data/fragen/{slug}.json fehlt, Gebiet bleibt leer")
            continue
        doc = load(path)
        if doc is None:
            continue
        if doc.get("gebiet") != slug:
            errors.append(f"data/fragen/{slug}.json: Feld \"gebiet\" ist \"{doc.get('gebiet')}\", erwartet \"{slug}\"")
            continue
        for q in doc.get("fragen", []) or []:
            q.setdefault("taxonomy", {})["domain"] = slug
            questions.append(q)
            if check(q, slug, tags, languages, seen, today, soon, length_cue, longest_correct, coverage):
                counts[slug] += 1

    minimum = config.get('min_questions_per_domain', 10)
    for slug, count in counts.items():
        if count < minimum:
            errors.append(f'{slug}: {count} aktive Fragen, mindestens {minimum} erforderlich')
    for w in warnings:
        print("Hinweis  " + w, file=sys.stderr)
    for e in errors:
        print("Fehler   " + e, file=sys.stderr)

    if errors:
        print(f"\nAbbruch: {len(errors)} Fehler. index.html wurde nicht geschrieben.", file=sys.stderr)
        return 1

    bank = {
        "generated": today.isoformat(),
        "session_size": config.get("session_size", 10),
        "languages": languages,
        "groups": config.get("groups", []),
        "domains": config["domains"],
        "questions": questions,
    }

    payload = json.dumps(bank, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")
    html = (HTML_TEMPLATE
            .replace("@@CSS@@", CSS)
            .replace("@@BANK@@", payload)
            .replace("@@STORE@@", STORE_JS)
            .replace("@@APP@@", APP_JS))
    OUT.write_text(html, encoding="utf-8")
    write_review_page(bank, ROOT)

    live = sum(counts.values())
    size_kb = round(len(html.encode("utf-8")) / 1024)

    print()
    print(f"index.html geschrieben — {size_kb} KB, Sprachen: {', '.join(languages)}")
    print(f"{live} verfuegbare Lernfragen von {len(questions)} in {len(config['domains'])} Dateien")
    pending = sum(not valid_approval(q) for q in questions)
    print(f'{pending} Fragen ohne unabhaengige fachaerztliche Freigabe; Verfuegbarkeit ist keine Freigabe.')
    for g in config.get("groups", []):
        total = sum(counts[d["slug"]] for d in config["domains"] if d.get("group") == g["slug"])
        print(f"  {total:>4}  {g['label'][languages[0]]}")
        for d in config["domains"]:
            if d.get("group") == g["slug"]:
                print(f"  {counts[d['slug']]:>4}      {d['label'][languages[0]]}")
    for d in config["domains"]:
        if not d.get("group"):
            print(f"  {counts[d['slug']]:>4}  {d['label'][languages[0]]}")
    for lc in languages:
        ok, ges = coverage.get(lc, [0, 0])
        if ges and ok < ges:
            print(f"Sprache {lc}: {ok}/{ges} Fragen uebersetzt ({ok/ges*100:.0f} %), "
                  f"der Rest faellt auf {languages[0]} zurueck")
    paare = quality_corpus_issues(questions)
    for a, b, r in paare:
        warnings.append(f"{a} und {b}: Fragestellung und richtige Antwort fast gleich ({r})")
        print(f"Hinweis  {a} / {b}: ähnliche Fragestellung ({r}); klinischen Kontext vergleichen")
    if paare:
        print(f"{len(paare)} ähnliche Fragenpaare zur manuellen Prüfung")
    if longest_correct[1]:
        share = longest_correct[0] / longest_correct[1] * 100
        mark = "  <-- Zufallserwartung liegt bei 25 %" if share > 40 else ""
        print(f"richtige Antwort ist die laengste Option: {longest_correct[0]}/{longest_correct[1]} "
              f"({share:.0f} %){mark}")
    if length_cue:
        print(f"{len(set(length_cue))} Fragen, in denen die Optionslaenge die Antwort verraet")
    if warnings:
        print(f"{len(warnings)} Hinweise (siehe oben)")
    print()
    print("Für Lern- und Prüfmodus beide Dateien hochladen: index.html und pruefung.html")
    return 0


CSS = r'''@import url('https://fonts.googleapis.com/css2?family=Archivo:wght@400;500;600;700&family=Spectral:ital,wght@0,400;0,500;0,600;1,400&display=swap');

:root {
  --paper: #f2f4f1;
  --card: #ffffff;
  --ink: #17201c;
  --muted: #646d68;
  --rule: #d9ded8;
  --rule-soft: #e8ebe6;
  --accent: #2e4b7a;
  --accent-soft: #e7ecf4;
  --correct: #1e5b3e;
  --correct-soft: #e6f0e9;
  --wrong: #8c2f2a;
  --wrong-soft: #f5e7e6;
  --flag: #8a5e14;
  --flag-soft: #f6efdf;
  --serif: 'Spectral', Georgia, serif;
  --sans: 'Archivo', system-ui, -apple-system, sans-serif;
}

* { box-sizing: border-box; }
html { -webkit-text-size-adjust: 100%; }

body {
  margin: 0;
  background: var(--paper);
  color: var(--ink);
  font-family: var(--serif);
  font-size: 17px;
  line-height: 1.62;
}

:focus-visible { outline: 2px solid var(--accent); outline-offset: 3px; }

.wrap { max-width: 47rem; margin: 0 auto; padding: 0 1.25rem 5rem; }

.masthead { border-bottom: 1px solid var(--rule); padding: 2rem 0 1rem; margin-bottom: 2rem; }

.masthead-row {
  display: flex; align-items: baseline; justify-content: space-between;
  gap: 1rem; flex-wrap: wrap;
}

.masthead h1 {
  font-family: var(--sans); font-weight: 700; font-size: 1.35rem;
  letter-spacing: -0.015em; margin: 0;
}

.lang { display: flex; gap: 0.15rem; }

.lang button {
  font-family: var(--sans); font-size: 0.78rem; font-weight: 600;
  letter-spacing: 0.03em; padding: 0.3rem 0.6rem;
  border: 1px solid var(--rule); background: none; color: var(--muted);
  cursor: pointer; border-radius: 3px;
}

.lang button.on { background: var(--ink); border-color: var(--ink); color: var(--paper); }

.inventory { font-family: var(--sans); font-size: 0.82rem; color: var(--muted); display: block; margin-top: 0.4rem; }

.intro { font-size: 1.05rem; margin: 0 0 2rem; max-width: 34rem; }

.board { border-top: 1px solid var(--rule); }

.domain {
  display: block; width: 100%; text-align: left; background: none; border: none;
  border-bottom: 1px solid var(--rule); padding: 1rem 0; cursor: pointer;
  font: inherit; color: inherit;
}

.domain:hover:not(:disabled) .domain-name { color: var(--accent); }
.domain:disabled { cursor: default; }

.domain-head { display: flex; align-items: baseline; justify-content: space-between; gap: 1rem; }

.domain-name { font-family: var(--sans); font-weight: 600; font-size: 1.05rem; letter-spacing: -0.01em; }
.domain-count { font-family: var(--sans); font-size: 0.8rem; color: var(--muted); white-space: nowrap; }
.domain-hint { font-size: 0.9rem; color: var(--muted); margin-top: 0.1rem; }

.domain.locked .domain-name, .domain.locked .domain-hint { color: #a8b0ac; }

.domain.group { padding: 1.2rem 0 1rem; }
.domain.group .domain-name { font-size: 1.15rem; }
.domain.nested { padding-left: 1.1rem; border-left: 2px solid var(--rule-soft); }
.domain.nested .domain-name { font-size: 0.98rem; font-weight: 500; }

.bar { height: 3px; background: var(--rule); margin-top: 0.65rem; max-width: 14rem; }
.bar span { display: block; height: 100%; background: var(--accent); }

.legend {
  margin-top: 2.25rem; padding-top: 1.25rem; border-top: 1px solid var(--rule);
  font-size: 0.88rem; color: var(--muted);
}
.legend .flagmark { color: var(--flag); }

.session-bar {
  display: flex; align-items: baseline; justify-content: space-between; gap: 1rem;
  font-family: var(--sans); font-size: 0.82rem; color: var(--muted); margin-bottom: 0.6rem;
}

.navstrip { display: flex; gap: 0.3rem; flex-wrap: wrap; margin-bottom: 1.5rem; }

.navstrip button {
  width: 1.9rem; height: 1.9rem; padding: 0;
  font-family: var(--sans); font-size: 0.78rem; font-weight: 600;
  border: 1px solid var(--rule); background: var(--card); color: var(--muted);
  border-radius: 3px; cursor: pointer;
}

.navstrip button.done-ok { border-color: var(--correct); color: var(--correct); background: var(--correct-soft); }
.navstrip button.done-no { border-color: var(--wrong); color: var(--wrong); background: var(--wrong-soft); }
.navstrip button.here { border-color: var(--ink); color: var(--ink); box-shadow: inset 0 0 0 1px var(--ink); }

.card { background: var(--card); border: 1px solid var(--rule); border-radius: 4px; padding: 1.75rem; }

.vignette { margin: 0 0 1.25rem; }
.lead-in { font-weight: 600; margin: 0 0 1.4rem; }

.options { display: grid; gap: 0.55rem; }

.option {
  display: grid; grid-template-columns: 1.7rem 1fr; gap: 0.85rem; align-items: start;
  width: 100%; text-align: left; font: inherit; color: inherit; background: var(--card);
  border: 1px solid var(--rule); border-left: 3px solid var(--rule);
  border-radius: 3px; padding: 0.85rem 1rem; cursor: pointer;
}

.option:hover:not(:disabled) { border-color: var(--accent); }
.option:disabled { cursor: default; }

.option .key { font-family: var(--sans); font-weight: 600; font-size: 0.85rem; color: var(--muted); padding-top: 0.15rem; }

.option.is-correct { border-left-color: var(--correct); background: var(--correct-soft); }
.option.is-correct .key { color: var(--correct); }
.option.is-wrong { border-left-color: var(--wrong); background: var(--wrong-soft); }
.option.is-wrong .key { color: var(--wrong); }

.rationale { display: block; font-size: 0.88rem; color: var(--muted); margin-top: 0.4rem; }

.explain { margin-top: 1.6rem; padding-top: 1.4rem; border-top: 1px solid var(--rule); }
.explain p { margin: 0 0 1rem; }

.teaching {
  border-left: 3px solid var(--accent); background: var(--accent-soft);
  padding: 0.75rem 1rem; margin: 0 0 1rem; font-style: italic;
}

.flagline {
  background: var(--flag-soft); border-left: 3px solid var(--flag); color: var(--flag);
  padding: 0.7rem 1rem; font-size: 0.9rem; margin: 0 0 1rem;
}

.sourceline { font-family: var(--sans); font-size: 0.78rem; color: var(--muted); line-height: 1.5; }

@media (prefers-reduced-motion: no-preference) {
  .explain { animation: reveal 0.22s ease-out; }
  @keyframes reveal { from { opacity: 0; transform: translateY(-4px); } to { opacity: 1; transform: none; } }
}

.actions { display: flex; gap: 0.6rem; flex-wrap: wrap; margin-top: 1.75rem; }

.btn {
  font-family: var(--sans); font-weight: 600; font-size: 0.92rem;
  padding: 0.65rem 1.25rem; border-radius: 3px;
  border: 1px solid var(--accent); background: var(--accent); color: #fff; cursor: pointer;
}

.btn.ghost { background: none; color: var(--accent); }
.btn.quiet { background: none; color: var(--muted); border-color: var(--rule); }
.btn:disabled { opacity: 0.4; cursor: default; }

.score { font-family: var(--sans); font-size: 1.45rem; font-weight: 700; margin: 0 0 0.3rem; }
.score-note { color: var(--muted); margin: 0 0 2rem; }
.learning-panel { border:1px solid var(--rule); background:var(--card); padding:1.2rem; margin:1.5rem 0; border-radius:6px; }
.learning-panel h2 { font-size:1.15rem; margin:0 0 .75rem; }
.learning-panel h3 { font-size:.86rem; margin:.3rem 0 .5rem; }
.learning-summary, .live-score { font-family:var(--sans); font-size:.9rem; line-height:1.7; }
.live-score { padding:.7rem 0; border-bottom:1px solid var(--rule); }
.learning-grid { display:grid; grid-template-columns:repeat(auto-fit,minmax(200px,1fr)); gap:1rem; margin:1rem 0; }
.learning-link { display:block; border:0; background:transparent; color:var(--ink); text-align:left; font:inherit; font-size:.85rem; padding:.35rem 0; cursor:pointer; text-decoration:underline; text-underline-offset:3px; }
.learning-link:focus-visible { outline:2px solid var(--accent); outline-offset:3px; }
.learning-panel .domain-hint { line-height:1.65; margin:.65rem 0; }

.review-list { border-top: 1px solid var(--rule); }

.review-item {
  border-bottom: 1px solid var(--rule); padding: 0.85rem 0;
  display: grid; grid-template-columns: 1.5rem 1fr; gap: 0.75rem;
}

.mark { font-family: var(--sans); font-weight: 700; }
.mark.ok { color: var(--correct); }
.mark.no { color: var(--wrong); }

.review-item .stem { font-size: 0.95rem; }
.review-item .meta { font-family: var(--sans); font-size: 0.78rem; color: var(--muted); margin-top: 0.2rem; }

.notice {
  background: var(--card); border: 1px solid var(--rule); border-left: 3px solid var(--flag);
  border-radius: 4px; padding: 1.25rem 1.5rem;
}

.footnote {
  margin-top: 3rem; padding-top: 1.25rem; border-top: 1px solid var(--rule);
  font-family: var(--sans); font-size: 0.76rem; color: var(--muted);
}

@media (max-width: 34rem) {
  body { font-size: 16px; }
  .card { padding: 1.25rem; }
  .wrap { padding: 0 1rem 4rem; }
  .navstrip button { width: 1.7rem; height: 1.7rem; }
}
'''

STORE_JS = r'''(function () {
  'use strict';
  var KEY = 'urofragen.progress.v1';
  var CODE_KEY = 'urofragen.code.v1';

  /* ---------- localStorage (Standard) ---------- */

  function LocalProgressStore() {
    this.state = this._load();
    var versions = {};
    var today = new Date(), day = today.getFullYear() + '-' + String(today.getMonth()+1).padStart(2,'0') + '-' + String(today.getDate()).padStart(2,'0');
    window.QUESTION_BANK.questions.forEach(function (q) {
      if(q.status === 'published' && q.review && q.review.expires >= day) versions[q.id] = q.version;
    });
    Object.keys(this.state.answers).forEach(function (id) {
      var a = this.state.answers[id];
      if (!a || a.version !== versions[id] || !versions[id] || typeof a.correct !== 'boolean') delete this.state.answers[id];
    }, this);
  }

  LocalProgressStore.prototype._load = function () {
    try {
      var raw = window.localStorage.getItem(KEY);
      if (!raw) return { answers: {} };
      var parsed = JSON.parse(raw);
      return parsed && parsed.answers && typeof parsed.answers === 'object' && !Array.isArray(parsed.answers) ? parsed : { answers: {} };
    } catch (e) {
      return { answers: {} };
    }
  };

  LocalProgressStore.prototype._save = function () {
    try {
      window.localStorage.setItem(KEY, JSON.stringify(this.state));
    } catch (e) {
      /* Privater Modus oder voller Speicher: Sitzung laeuft weiter, nichts wird persistiert. */
    }
  };

  LocalProgressStore.prototype.recordAnswer = function (event) {
    var old = this.state.answers[event.questionId];
    this.state.answers[event.questionId] = {
      domain: event.domain,
      version: event.questionVersion,
      correct: event.correct,
      selected: event.selected,
      attempts: (old ? old.attempts || 1 : 0) + 1,
      firstCorrect: old ? (typeof old.firstCorrect === 'boolean' ? old.firstCorrect : null) : event.correct,
      lastSeen: new Date().toISOString()
    };
    this._save();
    return Promise.resolve();
  };

  LocalProgressStore.prototype.getDomainProgress = function () {
    var out = {};
    var answers = this.state.answers;
    for (var id in answers) {
      if (!Object.prototype.hasOwnProperty.call(answers, id)) continue;
      var a = answers[id];
      if (!out[a.domain]) out[a.domain] = { seen: 0, correct: 0, firstCorrect: 0, firstKnown: 0, attempts: 0 };
      out[a.domain].seen += 1;
      if (a.correct) out[a.domain].correct += 1;
      out[a.domain].attempts += a.attempts || 1;
      if (typeof a.firstCorrect === 'boolean') {
        out[a.domain].firstKnown += 1;
        if (a.firstCorrect) out[a.domain].firstCorrect += 1;
      }
    }
    return Promise.resolve(out);
  };

  LocalProgressStore.prototype.getAnswered = function () {
    return Promise.resolve(new Set(Object.keys(this.state.answers)));
  };

  LocalProgressStore.prototype.reset = function () {
    this.state = { answers: {} };
    this._save();
    return Promise.resolve();
  };

  window.LocalProgressStore = LocalProgressStore;
  // Balance domains first, then interleave errors, unseen questions and old successes.
  // Pure function so selection can be checked without rendering a session.
  window.selectLearningQuestions = function (questions, size, answers, random) {
    random = random || Math.random;
    var buckets = {}, seenIds = {}, chosen = [], turns = {};
    questions.forEach(function(q) {
      if(seenIds[q.id]) return;
      seenIds[q.id] = true;
      var slug = q.taxonomy.domain;
      if(!buckets[slug]) buckets[slug] = [];
      buckets[slug].push(q);
    });
    var domains = Object.keys(buckets).map(function(slug) {
      var qs = buckets[slug];
      return {slug:slug, coverage:qs.filter(function(q){return !!answers[q.id];}).length/qs.length, tie:random()};
    }).sort(function(a,b){return a.coverage-b.coverage || a.tie-b.tie;});
    domains.forEach(function(d) {
      buckets[d.slug] = buckets[d.slug].map(function(q){return {q:q,tie:random()};});
      turns[d.slug] = 0;
    });
    while(chosen.length < size) {
      var added = false;
      domains.forEach(function(d) {
        var qs = buckets[d.slug];
        if(!qs.length || chosen.length >= size) return;
        var mode = turns[d.slug]++ % 4;
        function rank(q) {
          var a = answers[q.id];
          var kind = !a ? 'new' : a.correct ? 'review' : 'wrong';
          return (mode === 0 ? ['wrong','new','review'] : mode === 3 ? ['review','new','wrong'] : ['new','wrong','review']).indexOf(kind);
        }
        qs.sort(function(a,b) {
          var diff = rank(a.q)-rank(b.q);
          if(diff) return diff;
          var aa=answers[a.q.id], bb=answers[b.q.id];
          return (aa && bb ? (Date.parse(aa.lastSeen)||0)-(Date.parse(bb.lastSeen)||0) : 0) || a.tie-b.tie;
        });
        chosen.push(qs.shift().q); added = true;
      });
      if(!added) break;
    }
    return chosen;
  };
})();
'''

APP_JS = r'''(function () {
  'use strict';

  var UI = {
    de: {
      title: 'Facharztfragen Urologie',
      section: 'Abschnitt', version: 'Version', reviewed: 'Letzte fachliche Prüfung',
      unreviewed: 'Unabhängige fachärztliche Prüfung ausstehend',
      certainty: { etabliert: 'etabliert', kontrovers: 'kontrovers', ohne_phase_III: 'ohne Phase-III-Bestätigung', expertenkonsens: 'Expertenkonsens' },
      intro: 'Fallbasierte Fragen auf Facharztniveau. Jede Antwortoption ist begründet, jede Frage nennt ihre Quelle und ihr Überprüfungsdatum. Der Lernfortschritt bleibt in diesem Browser.',
      inventory: function (n, d) { return n + ' Fragen in ' + d + ' Gebieten'; },
      questions: 'Fragen',
      empty: 'in Vorbereitung',
      allEntities: 'alle Entitäten',
      mixed: 'Gemischte Sitzung über alle Gebiete',
      mixedSession: 'Gemischte Sitzung',
      progress: function (s, t, c) { return s + ' von ' + t + ' bearbeitet, ' + c + ' richtig'; },
      question: function (i, n) { return 'Frage ' + i + ' von ' + n; },
      next: 'Nächste Frage',
      back: 'Zurück',
      finish: 'Auswertung ansehen',
      stop: 'Sitzung beenden',
      score: function (c, t) { return c + ' von ' + t + ' richtig'; },
      repeat: 'Falsche wiederholen',
      home: 'Zur Übersicht',
      printPdf: 'Als PDF drucken',
      download: 'Als Datei speichern',
      reset: 'Fortschritt löschen',
      resetConfirm: 'Gesamten Lernfortschritt löschen?',
      legend: function () {
        return '⚠ markiert Fragen zu Themen mit uneinheitlicher Datenlage oder ohne randomisierte Bestätigung.';
      },
      evidence: 'Evidenz',
      yourAnswer: 'Ihre Antwort',
      correctAnswer: 'Richtige Antwort',
      sheetTitle: 'Ergebnis',
      sheetDate: 'Datum',
      sheetArea: 'Gebiet',
      sheetResult: 'Ergebnis',
      stand: 'Stand der Fragen',
      disclaimer: 'Lehrmaterial zur Prüfungsvorbereitung. Keine Handlungsanweisung für die Behandlung einzelner Patienten. Arzneimitteldosierungen sind vor jeder Anwendung gegen die Fachinformation zu prüfen.'
    },
    en: {
      title: 'Urology Board Questions',
      section: 'Section', version: 'Version', reviewed: 'Last clinical review',
      unreviewed: 'Independent specialist review pending',
      certainty: { etabliert: 'established', kontrovers: 'controversial', ohne_phase_III: 'without phase III confirmation', expertenkonsens: 'expert consensus' },
      intro: 'Case-based questions at board level. Every answer option is explained, every question states its source and review date. Your progress stays in this browser.',
      inventory: function (n, d) { return n + ' questions across ' + d + ' areas'; },
      questions: 'questions',
      empty: 'in preparation',
      allEntities: 'all entities',
      mixed: 'Mixed session across all areas',
      mixedSession: 'Mixed session',
      progress: function (s, t, c) { return s + ' of ' + t + ' done, ' + c + ' correct'; },
      question: function (i, n) { return 'Question ' + i + ' of ' + n; },
      next: 'Next question',
      back: 'Back',
      finish: 'See results',
      stop: 'End session',
      score: function (c, t) { return c + ' of ' + t + ' correct'; },
      repeat: 'Retry incorrect',
      home: 'Back to overview',
      printPdf: 'Print as PDF',
      download: 'Save as file',
      reset: 'Clear progress',
      resetConfirm: 'Clear all stored progress?',
      legend: function () {
        return '⚠ marks questions on topics with inconsistent evidence or without randomised confirmation.';
      },
      evidence: 'Evidence',
      yourAnswer: 'Your answer',
      correctAnswer: 'Correct answer',
      sheetTitle: 'Result',
      sheetDate: 'Date',
      sheetArea: 'Area',
      sheetResult: 'Score',
      stand: 'Questions as of',
      disclaimer: 'Teaching material for board exam preparation. Not a treatment instruction for individual patients. Verify all drug doses against the current product information before use.'
    },
    es: {
      title: 'Preguntas de especialidad en Urología',
      section: 'Sección', version: 'Versión', reviewed: 'Última revisión clínica',
      unreviewed: 'Revisión independiente por un especialista pendiente',
      certainty: { etabliert: 'establecida', kontrovers: 'controvertida', ohne_phase_III: 'sin confirmación en fase III', expertenkonsens: 'consenso de expertos' },
      intro: 'Preguntas basadas en casos, de nivel de especialista. Cada opción lleva su justificación y cada pregunta indica su fuente y su fecha de revisión. El progreso queda en este navegador.',
      inventory: function (n, d) { return n + ' preguntas en ' + d + ' áreas'; },
      questions: 'preguntas',
      empty: 'en preparación',
      allEntities: 'todas las entidades',
      mixed: 'Sesión mixta de todas las áreas',
      mixedSession: 'Sesión mixta',
      progress: function (s, t, c) { return s + ' de ' + t + ' hechas, ' + c + ' correctas'; },
      question: function (i, n) { return 'Pregunta ' + i + ' de ' + n; },
      next: 'Siguiente pregunta',
      back: 'Atrás',
      finish: 'Ver resultado',
      stop: 'Terminar sesión',
      score: function (c, t) { return c + ' de ' + t + ' correctas'; },
      repeat: 'Repetir las falladas',
      home: 'Volver al índice',
      printPdf: 'Imprimir como PDF',
      download: 'Guardar como archivo',
      reset: 'Borrar el progreso',
      resetConfirm: '¿Borrar todo el progreso guardado?',
      legend: function () {
        return '⚠ señala preguntas sobre temas con datos heterogéneos o sin confirmación aleatorizada.';
      },
      evidence: 'Evidencia',
      yourAnswer: 'Su respuesta',
      correctAnswer: 'Respuesta correcta',
      sheetTitle: 'Resultado',
      sheetDate: 'Fecha',
      sheetArea: 'Área',
      sheetResult: 'Puntuación',
      stand: 'Preguntas actualizadas a',
      disclaimer: 'Material docente para la preparación de la especialidad. No es una indicación de tratamiento para pacientes concretos. Verifique toda dosis frente a la ficha técnica vigente antes de usarla.'
    }
  };

  var LEARNING = {
    de: {overview:'Dein Lernstand', latest:'Trefferquote · letzte Antwort je Frage', coverage:'Bearbeitet', first:'Erstversuche seit dieser Version', attempts:'Antwortversuche', strong:'Stärke', developing:'Weiter festigen', weak:'Übungsbedarf', little:'Noch wenig Daten', fresh:'Noch nicht begonnen', practice:'Fehler gezielt üben', adaptive:'Adaptive Runden: ausgewogene Gebiete, neue Fragen, Fehler und ältere richtige Antworten. Antworten werden jedes Mal neu angeordnet.', criteria:'Orientierung anhand letzter Antworten: ab 5 verschiedenen Fragen ≥80 % Stärke, 60–79 % weiter festigen, <60 % Übungsbedarf. Wiederholung kann die Quote erhöhen; keine Bewertung klinischer Kompetenz.', session:'Diese Runde nach Gebiet', wrong:'Falsch', open:'Offen', answered:'Beantwortet', noWrong:'Aktuell keine falsch beantworteten Fragen.', local:'Lernstand bleibt in diesem Browser. Frühere Erstversuche werden nicht rückwirkend geschätzt.'},
    en: {overview:'Your learning progress', latest:'Accuracy · latest answer per question', coverage:'Completed', first:'First attempts since this version', attempts:'Answer attempts', strong:'Strength', developing:'Keep consolidating', weak:'Needs practice', little:'Limited data so far', fresh:'Not started', practice:'Practise incorrect answers', adaptive:'Adaptive rounds balance domains, new questions, errors and older correct answers. Answer positions are shuffled each time.', criteria:'Guide based on latest answers: at least 5 distinct questions and ≥80% strength, 60–79% keep consolidating, <60% needs practice. Repetition can raise accuracy; this does not assess clinical competence.', session:'This round by domain', wrong:'Incorrect', open:'Unanswered', answered:'Answered', noWrong:'No currently incorrect answers.', local:'Progress stays in this browser. Earlier first attempts are not retrospectively estimated.'},
    es: {overview:'Tu progreso de aprendizaje', latest:'Aciertos · última respuesta por pregunta', coverage:'Completadas', first:'Primeros intentos desde esta versión', attempts:'Intentos de respuesta', strong:'Fortaleza', developing:'Seguir consolidando', weak:'Necesita práctica', little:'Aún hay pocos datos', fresh:'Sin empezar', practice:'Practicar los errores', adaptive:'Las rondas adaptativas equilibran áreas, preguntas nuevas, errores y aciertos antiguos. Las opciones cambian de posición en cada ronda.', criteria:'Orientación según últimas respuestas: al menos 5 preguntas distintas y ≥80 % fortaleza, 60–79 % seguir consolidando, <60 % necesita práctica. Repetir puede elevar los aciertos; no evalúa competencia clínica.', session:'Esta ronda por área', wrong:'Incorrectas', open:'Sin responder', answered:'Respondidas', noWrong:'Actualmente no hay respuestas incorrectas.', local:'El progreso se guarda en este navegador. No se estiman retrospectivamente los primeros intentos anteriores.'}
  };
  var LANG_KEY = 'urofragen.lang.v1';
  var root = document.getElementById('app');
  var inventoryEl = document.getElementById('inventory');
  var langBox = document.getElementById('lang');
  var store = new window.LocalProgressStore();

  var bank = window.QUESTION_BANK;
  var pool = [];
  var counts = {};
  var session = null;
  var screen = 'home';
  var lang = readLang();
  var t = UI[lang];

  function readLang() {
    var saved = null;
    try { saved = window.localStorage.getItem(LANG_KEY); } catch (e) { /* egal */ }
    var erlaubt = (window.QUESTION_BANK.languages || ['de']);
    if (erlaubt.indexOf(saved) !== -1) return saved;
    var nav = ((window.navigator && window.navigator.language) || 'de').slice(0, 2);
    return erlaubt.indexOf(nav) !== -1 ? nav : erlaubt[0];
  }

  function setLang(next) {
    lang = next;
    t = UI[lang];
    try { window.localStorage.setItem(LANG_KEY, next); } catch (e) { /* egal */ }
    document.documentElement.lang = next;
    renderLangSwitch();
    updateInventory();
    if (screen === 'result' && session) renderResult();
    else if (session) renderQuestion(); else renderHome();
  }

  function el(tag, className, text) {
    var n = document.createElement(tag);
    if (className) n.className = className;
    if (text != null) n.textContent = text;
    return n;
  }

  function shuffle(list) {
    var a = list.slice();
    for (var i = a.length - 1; i > 0; i--) {
      var j = Math.floor(Math.random() * (i + 1));
      var x = a[i]; a[i] = a[j]; a[j] = x;
    }
    return a;
  }

  function isLive(q) {
    if (q.status !== 'published') return false;
    var e = q.review && q.review.expires;
    var now = new Date();
    var today = now.getFullYear() + '-' + String(now.getMonth() + 1).padStart(2, '0') + '-' + String(now.getDate()).padStart(2, '0');
    return e ? e >= today : false;
  }

  /* Sprachabhängige Textfelder. Fällt auf Deutsch zurück, falls eine Übersetzung fehlt. */
  function c(q) { return (q.content && (q.content[lang] || q.content.de)) || {}; }
  function label(obj) { return (obj && (obj[lang] || obj.de)) || ''; }

  function domainOf(slug) {
    return bank.domains.filter(function (d) { return d.slug === slug; })[0];
  }
  function domainLabel(slug) {
    var d = domainOf(slug);
    return d ? label(d.label) : slug;
  }
  function optionByKey(q, key) {
    return q.options.filter(function (o) { return o.key === key; })[0];
  }

  function questionsOf(slug) {
    return pool.filter(function (q) { return q.taxonomy.domain === slug; });
  }

  function sourceLine(q) {
    return q.sources.map(function (s) {
      var p = [];
      if (s.title) p.push(s.title);
      if (s.citation) p.push(s.citation);
      if (s.code) p.push(s.code);
      if (s.version) p.push(t.version + ' ' + s.version);
      if (s.year) p.push(String(s.year));
      if (s.section) p.push(t.section + ' ' + s.section);
      return p.join(', ');
    }).join(' · ');
  }

  /* ---------- Kopf ---------- */

  function renderLangSwitch() {
    document.title = t.title;
    document.querySelector('.masthead h1').textContent = t.title;
    document.querySelector('meta[name="description"]').content = t.intro;
    langBox.innerHTML = '';
    (bank.languages || ['de']).forEach(function (code) {
      var b = el('button', code === lang ? 'on' : null, code.toUpperCase());
      b.type = 'button';
      b.setAttribute('aria-pressed', code === lang ? 'true' : 'false');
      b.setAttribute('aria-label', {de:'Deutsch',en:'English',es:'Español'}[code]);
      b.addEventListener('click', function () { if (code !== lang) setLang(code); });
      langBox.appendChild(b);
    });
  }

  function updateInventory() {
    var withContent = bank.domains.filter(function (d) { return counts[d.slug] > 0; }).length;
    inventoryEl.textContent = t.inventory(pool.length, withContent) + ' · ' + t.stand + ' ' + bank.generated;
  }

  /* ---------- Übersicht ---------- */

  function pct(correct, seen) { return seen ? Math.round(100 * correct / seen) + '%' : '—'; }
  function learningStatus(p) {
    var l=LEARNING[lang];
    return !p.seen ? l.fresh : p.seen < 5 ? l.little : p.correct/p.seen >= .8 ? l.strong : p.correct/p.seen >= .6 ? l.developing : l.weak;
  }
  function metric(p, total) {
    var l=LEARNING[lang];
    return l.latest + ': ' + pct(p.correct,p.seen) + ' (' + p.correct + '/' + p.seen + ') · ' + l.coverage + ': ' + p.seen + '/' + total;
  }
  function sumProgress(progress, slugs) {
    var total={seen:0,correct:0,firstKnown:0,firstCorrect:0,attempts:0};
    slugs.forEach(function(slug) {
      var p=progress[slug] || {};
      Object.keys(total).forEach(function(key){total[key] += p[key] || 0;});
    });
    return total;
  }
  function learningDashboard(progress) {
    var l=LEARNING[lang], box=el('section','learning-panel');
    box.appendChild(el('h2',null,l.overview));
    var total=sumProgress(progress,bank.domains.map(function(d){return d.slug;}));
    box.appendChild(el('p','learning-summary',metric(total,pool.length)));
    box.appendChild(el('p','domain-hint',l.first + ': ' + pct(total.firstCorrect,total.firstKnown) + ' ('+total.firstCorrect+'/'+total.firstKnown+') · '+l.attempts+': '+total.attempts));
    var grid=el('div','learning-grid');
    [l.strong,l.developing,l.weak,l.little,l.fresh].forEach(function(status) {
      var members=bank.domains.filter(function(d){return learningStatus(progress[d.slug] || {seen:0,correct:0})===status;});
      if(!members.length) return;
      var group=el('div','learning-category');
      group.appendChild(el('h3',null,status+' ('+members.length+')'));
      members.slice(0,3).forEach(function(d){
        var p=progress[d.slug] || {seen:0,correct:0};
        var b=el('button','learning-link',label(d.label)+' · '+pct(p.correct,p.seen)+' ('+p.correct+'/'+p.seen+')');
        b.type='button';b.addEventListener('click',function(){startSession(d.slug,questionsOf(d.slug));});
        group.appendChild(b);
      });
      grid.appendChild(group);
    });
    box.appendChild(grid);
    var wrong=pool.filter(function(q){var a=store.state.answers[q.id];return a && !a.correct;});
    if(wrong.length) {
      var practice=el('button','btn ghost',l.practice+' ('+wrong.length+')');
      practice.type='button';practice.addEventListener('click',function(){startSession(null,wrong);});
      box.appendChild(practice);
    }
    box.appendChild(el('p','domain-hint',l.criteria));
    box.appendChild(el('p','domain-hint',l.local));
    return box;
  }
  function sessionProgress() {
    var progress={};
    answeredItems().forEach(function(a){
      var slug=a.question.taxonomy.domain;
      if(!progress[slug]) progress[slug]={seen:0,correct:0};
      progress[slug].seen++;if(a.given.correct)progress[slug].correct++;
    });
    return progress;
  }
  function sessionSummary() {
    var done=answeredItems(), right=done.filter(function(a){return a.given.correct;}).length, l=LEARNING[lang];
    return l.answered+': '+done.length+'/'+session.items.length+' · '+t.sheetResult+': '+right+'/'+done.length+' ('+pct(right,done.length)+') · '+l.wrong+': '+(done.length-right)+' · '+l.open+': '+(session.items.length-done.length);
  }
  function sessionBreakdown() {
    var box=el('section','learning-panel'), progress=sessionProgress();
    box.appendChild(el('h2',null,LEARNING[lang].session));
    var slugs=[];session.items.forEach(function(q){if(slugs.indexOf(q.taxonomy.domain)<0)slugs.push(q.taxonomy.domain);});
    slugs.forEach(function(slug){
      var p=progress[slug] || {seen:0,correct:0};
      var n=session.items.filter(function(q){return q.taxonomy.domain===slug;}).length;
      box.appendChild(el('p','domain-hint',domainLabel(slug)+' · '+p.correct+'/'+p.seen+' ('+pct(p.correct,p.seen)+') · '+LEARNING[lang].answered+': '+p.seen+'/'+n+' · '+learningStatus(p)));
    });
    box.appendChild(el('p','domain-hint',LEARNING[lang].criteria));
    return box;
  }

  function renderHome() {
    screen = 'home';
    session = null;
    store.getDomainProgress().then(function (progress) {
      root.innerHTML = '';
      root.appendChild(el('p', 'intro', t.intro));
      root.appendChild(el('p','notice',t.unreviewed));
      var reviewLink = el('a', 'btn ghost', {de:'✓ Fragen fachlich prüfen',en:'✓ Review questions',es:'✓ Revisar preguntas'}[lang]);
      reviewLink.href = 'pruefung.html';
      root.appendChild(reviewLink);
      root.appendChild(learningDashboard(progress));
      root.appendChild(el('p','domain-hint',LEARNING[lang].adaptive));

      var board = el('div', 'board');

      function row(domain, nested) {
        var count = counts[domain.slug];
        var open = count > 0;
        var done = progress[domain.slug] || { seen: 0, correct: 0 };

        var btn = el('button', 'domain' + (open ? '' : ' locked') + (nested ? ' nested' : ''));
        btn.type = 'button';
        btn.disabled = !open;

        var head = el('div', 'domain-head');
        head.appendChild(el('span', 'domain-name', label(domain.label)));
        head.appendChild(el('span', 'domain-count', open ? count + ' ' + t.questions : t.empty));
        btn.appendChild(head);
        if (domain.hint) btn.appendChild(el('div', 'domain-hint', label(domain.hint)));

        if (open && done.seen > 0) {
          var bar = el('div', 'bar');
          var fill = el('span');
          fill.style.width = Math.min(100, Math.round((done.seen / count) * 100)) + '%';
          bar.appendChild(fill);
          btn.appendChild(bar);
        }
        btn.appendChild(el('div','domain-hint',metric(done,count)+' · '+learningStatus(done)));

        if (open) {
          btn.addEventListener('click', function () {
            startSession(domain.slug, questionsOf(domain.slug));
          });
        }
        return btn;
      }

      (bank.groups || []).forEach(function (group) {
        var members = bank.domains.filter(function (d) { return d.group === group.slug; });
        if (!members.length) return;

        var total = 0;
        members.forEach(function (m) { total += counts[m.slug]; });

        var head = el('button', 'domain group' + (total ? '' : ' locked'));
        head.type = 'button';
        head.disabled = !total;
        var hr = el('div', 'domain-head');
        hr.appendChild(el('span', 'domain-name', label(group.label)));
        hr.appendChild(el('span', 'domain-count',
          total ? total + ' ' + t.questions + ', ' + t.allEntities : t.empty));
        head.appendChild(hr);
        head.appendChild(el('div','domain-hint',metric(sumProgress(progress,members.map(function(m){return m.slug;})),total)));
        if (total) {
          head.addEventListener('click', function () {
            var all = [];
            members.forEach(function (m) { all = all.concat(questionsOf(m.slug)); });
            startSession(null, all);
          });
        }
        board.appendChild(head);
        members.forEach(function (m) { board.appendChild(row(m, true)); });
      });

      bank.domains.forEach(function (d) {
        if (!d.group) board.appendChild(row(d, false));
      });

      root.appendChild(board);

      var populated = bank.domains.filter(function (d) { return counts[d.slug] > 0; });
      if (populated.length > 1) {
        var all = [];
        populated.forEach(function (d) { all = all.concat(questionsOf(d.slug)); });
        var mixed = el('button', 'btn', t.mixed);
        mixed.type = 'button';
        mixed.style.marginTop = '1.75rem';
        mixed.addEventListener('click', function () { startSession(null, all); });
        root.appendChild(mixed);
      }

      root.appendChild(el('div', 'legend', t.legend()));

      var reset = el('button', 'btn quiet', t.reset);
      reset.type = 'button';
      reset.style.marginTop = '1.25rem';
      reset.addEventListener('click', function () {
        if (window.confirm(t.resetConfirm)) store.reset().then(renderHome);
      });
      root.appendChild(reset);

      root.appendChild(el('div', 'footnote', t.disclaimer));
    });
  }

  /* ---------- Sitzung ---------- */

  function pick(questions, size) {
    return Promise.resolve(window.selectLearningQuestions(questions,size,store.state.answers));
  }

  function startSession(slug, questions) {
    pick(questions, bank.session_size).then(function (items) {
      if (!items.length) { renderHome(); return; }
      session = {
        domain: slug,
        items: items,
        index: 0,
        given: new Array(items.length).fill(null),
        /* Anzeigereihenfolge der Optionen, pro Frage einmal gewuerfelt und dann stabil.
           Verhindert, dass man sich beim Wiederholen die Position statt der Sache merkt. */
        order: items.map(function (q) { return shuffle(q.options.map(function (o) { return o.key; })); }),
        startedAt: new Date()
      };
      renderQuestion();
      window.scrollTo(0, 0);
    });
  }

  function answeredCount() {
    return session.given.filter(function (g) { return g; }).length;
  }

  function renderQuestion() {
    screen = 'question';
    var q = session.items[session.index];
    var body = c(q);
    var given = session.given[session.index];
    var shownAt = Date.now();

    root.innerHTML = '';

    var bar = el('div', 'session-bar');
    bar.appendChild(el('span', null, session.domain ? domainLabel(session.domain) : domainLabel(q.taxonomy.domain)));
    bar.appendChild(el('span', null, t.question(session.index + 1, session.items.length)));
    root.appendChild(bar);
    var liveScore=el('p','live-score',sessionSummary());
    liveScore.setAttribute('aria-live','polite');
    root.appendChild(liveScore);

    /* Navigationsleiste: zeigt den Stand und erlaubt den Sprung zurück. */
    var strip = el('div', 'navstrip');
    session.items.forEach(function (item, i) {
      var g = session.given[i];
      var cls = i === session.index ? 'here' : g ? (g.correct ? 'done-ok' : 'done-no') : null;
      var b = el('button', cls, String(i + 1));
      b.type = 'button';
      b.setAttribute('aria-label', t.question(i + 1, session.items.length));
      /* Vorwärts nur bis zur ersten unbeantworteten Frage. */
      var reachable = i <= session.index || session.given[i] !== null;
      b.disabled = !reachable;
      b.addEventListener('click', function () {
        if (i === session.index) return;
        session.index = i;
        renderQuestion();
        window.scrollTo(0, 0);
      });
      strip.appendChild(b);
    });
    root.appendChild(strip);

    var card = el('div', 'card');
    card.appendChild(el('p', 'vignette', body.vignette));
    card.appendChild(el('p', 'lead-in', body.lead_in));

    var list = el('div', 'options');
    var buttons = {};
    var order = session.order[session.index];

    order.forEach(function (key, pos) {
      var opt = optionByKey(q, key);
      var text = (body.options && body.options[key]) || {};
      var letter = String.fromCharCode(65 + pos);
      var b = el('button', 'option');
      b.type = 'button';
      b.appendChild(el('span', 'key', letter));
      var inner = el('span');
      inner.appendChild(el('span', null, text.text));
      b.appendChild(inner);
      b.addEventListener('click', function () {
        if (session.given[session.index]) return;
        session.given[session.index] = { key: key, letter: letter, correct: !!opt.correct };
        store.recordAnswer({
          questionId: q.id,
          questionVersion: q.version,
          domain: q.taxonomy.domain,
          selected: key,
          correct: !!opt.correct,
          msSpent: Date.now() - shownAt
        });
        reveal(q, body, buttons, card);
        liveScore.textContent=sessionSummary();
      });
      buttons[key] = { button: b, inner: inner, option: opt, text: text, letter: letter };
      list.appendChild(b);
    });

    card.appendChild(list);
    root.appendChild(card);

    if (given) reveal(q, body, buttons, card);
  }

  function reveal(q, body, buttons, card) {
    var given = session.given[session.index];

    Object.keys(buttons).forEach(function (key) {
      var e = buttons[key];
      e.button.disabled = true;
      if (e.option.correct) e.button.classList.add('is-correct');
      else if (key === given.key) e.button.classList.add('is-wrong');
      if (e.text.rationale) {
        e.inner.appendChild(el('span', 'rationale', e.text.rationale));
      }
    });

    var explain = el('div', 'explain');

    if (q.evidence && q.evidence.flag) {
      explain.appendChild(el('p', 'flagline',
        '⚠ ' + t.evidence + ': ' + t.certainty[q.evidence.certainty] + ' — ' + (body.flag_note || '')));
    }

    explain.appendChild(el('p', null, body.explanation.core));
    if (body.explanation.teaching_point) {
      explain.appendChild(el('p', 'teaching', body.explanation.teaching_point));
    }
    explain.appendChild(el('p', 'sourceline', sourceLine(q)));
    q.sources.forEach(function (s) {
      if (s.url && /^https:\/\//.test(s.url)) {
        var a = el('a', 'sourceline', s.title || s.url);
        a.href = s.url; a.target = '_blank'; a.rel = 'noopener noreferrer';
        explain.appendChild(a); explain.appendChild(el('br'));
      }
    });
    explain.appendChild(el('p', 'sourceline', approvalLine(q)));

    var actions = el('div', 'actions');

    if (session.index > 0) {
      var back = el('button', 'btn ghost', t.back);
      back.type = 'button';
      back.addEventListener('click', function () {
        session.index -= 1;
        renderQuestion();
        window.scrollTo(0, 0);
      });
      actions.appendChild(back);
    }

    var last = session.index === session.items.length - 1;
    var next = el('button', 'btn', last ? t.finish : t.next);
    next.type = 'button';
    next.addEventListener('click', function () {
      if (last) { renderResult(); return; }
      session.index += 1;
      renderQuestion();
      window.scrollTo(0, 0);
    });
    actions.appendChild(next);

    if (!last) {
      var stop = el('button', 'btn quiet', t.stop);
      stop.type = 'button';
      stop.addEventListener('click', renderResult);
      actions.appendChild(stop);
    }

    explain.appendChild(actions);
    card.appendChild(explain);
    next.focus();
  }

  /* ---------- Auswertung ---------- */

  function answeredItems() {
    var out = [];
    session.items.forEach(function (q, i) {
      if (session.given[i]) out.push({ question: q, given: session.given[i], order: session.order[i] });
    });
    return out;
  }

  function renderResult() {
    screen = 'result';
    var done = answeredItems();
    var correct = done.filter(function (a) { return a.given.correct; }).length;

    root.innerHTML = '';
    root.appendChild(el('p', 'score', t.score(correct, done.length)));
    root.appendChild(el('p', 'score-note',
      session.domain ? domainLabel(session.domain) : t.mixedSession));
    root.appendChild(el('p','live-score',sessionSummary()));
    root.appendChild(sessionBreakdown());

    var list = el('div', 'review-list');
    done.forEach(function (a) {
      var item = el('div', 'review-item');
      item.appendChild(el('span', 'mark ' + (a.given.correct ? 'ok' : 'no'), a.given.correct ? '✓' : '✕'));
      var b = el('div');
      var body=c(a.question);
      b.appendChild(el('div', 'stem', body.vignette));
      b.appendChild(el('p','domain-hint',t.yourAnswer+': '+body.options[a.given.key].text));
      var right=a.question.options.find(function(o){return o.correct;}).key;
      b.appendChild(el('p','domain-hint',t.correctAnswer+': '+body.options[right].text));
      b.appendChild(el('p','domain-hint',body.explanation.core));
      b.appendChild(el('div', 'meta', domainLabel(a.question.taxonomy.domain) + ' · ' + a.question.id));
      item.appendChild(b);
      list.appendChild(item);
    });
    root.appendChild(list);

    var actions = el('div', 'actions');

    var pdf = el('button', 'btn', t.printPdf);
    pdf.type = 'button';
    pdf.addEventListener('click', function () { printSheet(done, correct); });
    actions.appendChild(pdf);

    var dl = el('button', 'btn ghost', t.download);
    dl.type = 'button';
    dl.addEventListener('click', function () { downloadSheet(done, correct); });
    actions.appendChild(dl);

    var wrong = done.filter(function (a) { return !a.given.correct; })
      .map(function (a) { return a.question; });

    if (wrong.length) {
      var again = el('button', 'btn ghost', t.repeat);
      again.type = 'button';
      again.addEventListener('click', function () {
        var items = shuffle(wrong);
        session = {
          domain: session.domain, items: items, index: 0,
          given: new Array(items.length).fill(null),
          order: items.map(function (q) { return shuffle(q.options.map(function (o) { return o.key; })); }),
          startedAt: new Date()
        };
        renderQuestion();
        window.scrollTo(0, 0);
      });
      actions.appendChild(again);
    }

    var home = el('button', 'btn quiet', t.home);
    home.type = 'button';
    home.addEventListener('click', function () { renderHome(); window.scrollTo(0, 0); });
    actions.appendChild(home);

    root.appendChild(actions);
    root.appendChild(el('div', 'footnote', t.disclaimer));
  }

  /* ---------- Ergebnis als Datei ---------- */

  function approvalLine(q) {
    var r = q.review || {}, a = r.approval || {};
    var today = new Date().toISOString().slice(0,10);
    return r.approval_valid === true && (a.languages || []).indexOf(lang) >= 0 && r.expires >= today
      ? UI[lang].reviewed + ': ' + r.last_reviewed + ' · ' + r.reviewer + ' · ' + a.languages.join(', ').toUpperCase()
      : UI[lang].unreviewed;
  }
  function esc(s) {
    return String(s == null ? '' : s)
      .replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
  }

  function sheetHtml(done, correct) {
    var when = new Date();
    var area = session.domain ? domainLabel(session.domain) : t.mixedSession;

    var p = [];
    p.push('<!DOCTYPE html><html lang="' + lang + '"><head><meta charset="utf-8">');
    p.push('<title>' + esc(t.sheetTitle) + ' — ' + esc(area) + ' — ' + when.toISOString().slice(0, 10) + '</title>');
    p.push('<style>' +
      '@page{size:A4;margin:18mm 16mm}' +
      'body{font-family:Georgia,"Times New Roman",serif;max-width:44rem;margin:2rem auto;padding:0 1.5rem;color:#17201c;line-height:1.55;font-size:11.5pt}' +
      'h1{font-size:1.25rem;margin:0 0 .2rem}' +
      '.meta{color:#555f59;font-size:.85em;margin-bottom:1.8rem;padding-bottom:.8rem;border-bottom:1px solid #d9ded8}' +
      '.q{border-bottom:1px solid #e8ebe6;padding:1rem 0;break-inside:avoid;page-break-inside:avoid}' +
      '.qhead{color:#646d68;font-size:.78em;margin-bottom:.35rem}' +
      '.lead{font-weight:bold;margin:.5rem 0}' +
      '.opt{margin:.15rem 0 .15rem 1.1rem}' +
      '.ok{color:#1e5b3e}.no{color:#8c2f2a}' +
      '.rat{color:#646d68;font-size:.85em;margin:0 0 .3rem 2.2rem}' +
      '.note{color:#646d68;font-size:.85em}' +
      '.flag{color:#8a5e14}' +
      '.tp{font-style:italic;border-left:2px solid #2e4b7a;padding-left:.7rem;margin:.5rem 0}' +
      'footer{margin-top:2rem;border-top:1px solid #d9ded8;padding-top:.8rem;font-size:.78em;color:#646d68}' +
      '@media print{body{margin:0;max-width:none}}' +
      '</style></head><body>');
    p.push('<h1>' + esc(t.title) + ' — ' + esc(t.sheetTitle) + '</h1>');
    p.push('<div class="meta">' +
      esc(t.sheetDate) + ': ' + esc(when.toLocaleString(lang)) + '<br>' +
      esc(t.sheetArea) + ': ' + esc(area) + '<br>' +
      esc(t.sheetResult) + ': ' + correct + ' / ' + done.length + '</div>');
    p.push('<p>'+esc(sessionSummary())+'</p>');
    p.push('<h2>'+esc(LEARNING[lang].session)+'</h2>');
    var breakdown=sessionProgress();
    var slugs=[];session.items.forEach(function(q){if(slugs.indexOf(q.taxonomy.domain)<0)slugs.push(q.taxonomy.domain);});
    slugs.forEach(function(slug){
      var s=breakdown[slug] || {seen:0,correct:0};
      var n=session.items.filter(function(q){return q.taxonomy.domain===slug;}).length;
      p.push('<p>'+esc(domainLabel(slug))+' · '+s.correct+'/'+s.seen+' ('+pct(s.correct,s.seen)+') · '+esc(LEARNING[lang].answered)+': '+s.seen+'/'+n+' · '+esc(learningStatus(s))+'</p>');
    });
    p.push('<p>'+esc(LEARNING[lang].criteria)+'</p>');

    done.forEach(function (a, i) {
      var q = a.question;
      var body = c(q);
      var order = a.order;
      var rightLetter = '';
      p.push('<div class="q">');
      p.push('<div class="qhead">' + (i + 1) + ' · ' + esc(domainLabel(q.taxonomy.domain)) +
        ' · ' + esc(q.id) + ' · ' + (a.given.correct ? '✓' : '✕') + '</div>');
      p.push('<p>' + esc(body.vignette) + '</p>');
      p.push('<p class="lead">' + esc(body.lead_in) + '</p>');
      order.forEach(function (key, pos) {
        var o = optionByKey(q, key);
        var letter = String.fromCharCode(65 + pos);
        if (o.correct) rightLetter = letter;
        var txt = (body.options && body.options[key]) || {};
        var mark = o.correct ? '✓' : (key === a.given.key ? '✕' : '·');
        var cls = o.correct ? 'ok' : (key === a.given.key ? 'no' : '');
        p.push('<div class="opt ' + cls + '">' + mark + ' ' + esc(letter) + ') ' + esc(txt.text) + '</div>');
        if (txt.rationale) {
          p.push('<div class="rat">' + esc(txt.rationale) + '</div>');
        }
      });
      p.push('<p class="note">' + esc(t.yourAnswer) + ': ' + esc(a.given.letter) +
        ' · ' + esc(t.correctAnswer) + ': ' + esc(rightLetter) + '</p>');
      if (q.evidence && q.evidence.flag) {
        p.push('<p class="flag">⚠ ' + esc(t.evidence) + ': ' + esc(t.certainty[q.evidence.certainty]) +
          ' — ' + esc(body.flag_note) + '</p>');
      }
      p.push('<p>' + esc(body.explanation.core) + '</p>');
      if (body.explanation.teaching_point) {
        p.push('<p class="tp">' + esc(body.explanation.teaching_point) + '</p>');
      }
      p.push('<p class="note">' + esc(sourceLine(q)) + '</p>');
      q.sources.forEach(function (s) {
        if (s.url && /^https:\/\//.test(s.url)) p.push('<p class="note"><a href="' + esc(s.url) + '">' + esc(s.title || s.url) + '</a></p>');
      });
      p.push('<p class="note">' + esc(approvalLine(q)) + '</p>');
      p.push('</div>');
    });

    p.push('<footer>' + esc(t.disclaimer) + '</footer>');
    p.push('</body></html>');
    return p.join('\n');
  }

  function sheetName() {
    var slug = (session.domain || 'gemischt').replace(/[^a-z0-9]+/gi, '-');
    return 'urofragen-' + slug + '-' + new Date().toISOString().slice(0, 10);
  }

  /* Druckt über ein verstecktes Fenster. Im Druckdialog steht bei jedem Browser
     "Als PDF speichern" bzw. "Save as PDF" zur Verfügung. */
  function printSheet(done, correct) {
    var html = sheetHtml(done, correct);
    var frame = document.createElement('iframe');
    frame.setAttribute('aria-hidden', 'true');
    frame.style.position = 'fixed';
    frame.style.right = '0';
    frame.style.bottom = '0';
    frame.style.width = '0';
    frame.style.height = '0';
    frame.style.border = '0';
    document.body.appendChild(frame);

    var win = frame.contentWindow;
    try {
      win.document.open();
      win.document.write(html);
      win.document.close();
      win.focus();
      setTimeout(function () {
        try { win.print(); } catch (e) { openInTab(html); }
        setTimeout(function () {
          if (frame.parentNode) document.body.removeChild(frame);
        }, 2000);
      }, 250);
    } catch (e) {
      if (frame.parentNode) document.body.removeChild(frame);
      openInTab(html);
    }
  }

  /* Rückfalllösung, etwa wenn der Browser das Drucken aus einem Rahmen sperrt. */
  function openInTab(html) {
    var tab = window.open('', '_blank');
    if (!tab) { downloadBlob(html); return; }
    tab.document.open();
    tab.document.write(html);
    tab.document.close();
  }

  function downloadBlob(html) {
    var blob = new Blob([html], { type: 'text/html;charset=utf-8' });
    var url = URL.createObjectURL(blob);
    var a = document.createElement('a');
    a.href = url;
    a.download = sheetName() + '.html';
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    setTimeout(function () { URL.revokeObjectURL(url); }, 1000);
  }

  function downloadSheet(done, correct) {
    downloadBlob(sheetHtml(done, correct));
  }

  /* ---------- Start ---------- */

  pool = bank.questions.filter(isLive);
  bank.domains.forEach(function (d) { counts[d.slug] = questionsOf(d.slug).length; });

  document.documentElement.lang = lang;
  renderLangSwitch();
  updateInventory();
  renderHome();
})();
'''

HTML_TEMPLATE = r'''<!DOCTYPE html>
<html lang="de">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Facharztfragen Urologie</title>
<meta name="description" content="Fallbasierte Fragen zur Facharztprüfung Urologie. Deutsch, Englisch und Spanisch.">
<style>
@@CSS@@
</style>
</head>
<body>
<div class="wrap">
  <header class="masthead">
    <div class="masthead-row">
      <h1>Facharztfragen Urologie</h1>
      <div class="lang" id="lang"></div>
    </div>
    <span class="inventory" id="inventory"></span>
  </header>
  <main id="app"></main>
</div>
<script>window.QUESTION_BANK=@@BANK@@;</script>
<script>
@@STORE@@
</script>
<script>
@@APP@@
</script>
</body>
</html>
'''

if __name__ == "__main__":
    sys.exit(main())
