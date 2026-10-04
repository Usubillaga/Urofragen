#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Übernimmt Fragenblöcke in die passende Gebietsdatei unter data/fragen/ der Website Urofragen.

Jeder Block nennt sein Gebiet selbst; das Skript sucht die zugehörige Datei und vergibt die IDs
nach dem Präfix, das in dieser Datei bereits verwendet wird.

Blöcke in diesem Ordner:
  hodentumor-seminom-IIAB-block.json         Seminom IIA/B (Che & Papachristofilou 2025), Ersatz 00007
  hodentumor-nachsorge-block.json            Nachsorge (Dieckmann et al. 2025)
  hodentumor-heft3-block.json                Schwerpunktheft 10/2025, Teil 3
  operationskenntnisse-salvage-block.json    Salvage-Operationen (Heidenreich et al. 2026)

Aufruf im Projektordner der Website (dort, wo build.py liegt):
    python3 pfad/zu/merge-hodentumor.py            Vorschau aller Blöcke, schreibt nichts
    python3 pfad/zu/merge-hodentumor.py --apply    schreiben und build.py ausführen
Optionen:
    --block DATEI      nur diesen Block (mehrfach möglich); ohne Angabe alle *-block.json im Ordner
    --datei PFAD       Zieldatei ausdrücklich angeben, falls der Gebietsname nicht passt
    --status review    neue Fragen als Entwurf statt veröffentlicht
    --ohne-ersatz      bestehende Fragen nicht verändern (betrifft nur Block Seminom IIA/B)

Verhalten:
  * Bereits übernommene Fragen werden erkannt und übersprungen; mehrfaches Ausführen ist unschädlich.
  * Sind vorgeschlagene IDs belegt, werden die neuen Fragen fortlaufend neu nummeriert.
  * Tags außerhalb des Vokabulars in domains.json werden weggelassen und angezeigt.
  * Schlägt build.py fehl, wird die Gebietsdatei auf den alten Stand zurückgesetzt.
  * Geänderte und neue Fragen verlieren bzw. haben keine Freigabe; Freigabe über pruefung.html.
"""
import argparse
from collections import Counter
import json
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
# Voreinstellungen für Blöcke ohne eigene Angaben (Block Seminom IIA/B vom 19.09.2026)
DEFAULT_GEGENLESEN = {'alle': ['Seminom'], 'eines': r'Stadium II(?!I)|IIA|IIB|Lymphadenektomie|\bRLA\b|RPLND|Carboplatin|Radiotherapie|Bestrahlung'}
DEFAULT_PRUEFUNG = [r'Lymphadenektomie|RLA|RPLND', 'Seminom']


def fail(msg):
    print('Abbruch: ' + msg)
    sys.exit(1)


def norm(text):
    return re.sub(r'\s+', ' ', text or '').strip().lower()


def de_text(q):
    de = (q.get('content') or {}).get('de') or {}
    opts = de.get('options') or {}
    return ' '.join([de.get('vignette', ''), de.get('lead_in', '')] +
                    [(o or {}).get('text', '') for o in opts.values()])


def related_filter(spec):
    alle = [re.compile(p) for p in spec.get('alle', [])]
    eines = re.compile(spec['eines']) if spec.get('eines') else None
    return lambda t: all(p.search(t) for p in alle) and (eines is None or bool(eines.search(t)))


def merge_block(block, qs, vocab, args, pool):
    """Wendet einen Block auf qs an. pool: fortlaufende Nummernvergabe über alle Blöcke."""
    changed, touched = False, set()
    print(f"== Block: {block.get('titel') or block.get('quelle', '')}")
    # 1) Ersatz bestehender Fragen
    for rid, rep in (block.get('ersatz') or {}).items():
        old = next((q for q in qs if q.get('id') == rid), None)
        checks = rep.get('pruefung', DEFAULT_PRUEFUNG)
        if args.ohne_ersatz:
            print(f'{rid}: bleibt unverändert (--ohne-ersatz)')
        elif old is None:
            print(f'{rid}: nicht gefunden, übersprungen')
        elif norm(de_text(old)) == norm(' '.join([rep['content']['de']['vignette'], rep['content']['de']['lead_in']] +
                                                  [o['text'] for o in rep['content']['de']['options'].values()])):
            print(f'{rid}: bereits aktualisiert')
        elif not all(re.search(p, de_text(old)) for p in checks):
            print(f'{rid}: Inhalt passt nicht zum erwarteten Thema, übersprungen. Bitte ID prüfen.')
        else:
            de_old = (old.get('content') or {}).get('de') or {}
            ck_old = next((o.get('key') for o in old.get('options', []) if o.get('correct')), None)
            ck_new = next(o['key'] for o in rep['options'] if o['correct'])
            print(f'{rid}: wird aktualisiert, Version {old.get("version", 1)} → {int(old.get("version", 1)) + 1}')
            print(f'   bisher: {de_old.get("lead_in", "")}')
            print(f'           richtig {ck_old}: {((de_old.get("options") or {}).get(ck_old) or {}).get("text", "")}')
            print(f'   neu:    {rep["content"]["de"]["lead_in"]}')
            print(f'           richtig {ck_new}: {rep["content"]["de"]["options"][ck_new]["text"]}')
            for key in ('options', 'evidence', 'sources', 'content'):
                old[key] = rep[key]
            old['version'] = int(old.get('version', 1)) + 1
            old.setdefault('review', {})['expires'] = rep['review_expires']
            tags = (old.get('taxonomy') or {}).get('tags')
            if tags is not None:
                old['taxonomy']['tags'] = [t for t in tags if t in vocab]
            touched.add(rid)
            changed = True

    # 2) Neue Fragen anhängen
    existing = {q.get('id') for q in qs}
    seen_vignettes = {norm(((q.get('content') or {}).get('de') or {}).get('vignette')) for q in qs}
    new_items = [q for q in block.get('neu', []) if norm(q['content']['de']['vignette']) not in seen_vignettes]
    skipped = len(block.get('neu', [])) - len(new_items)
    if skipped:
        print(f'{skipped} neue Fragen sind bereits vorhanden und werden übersprungen')
    renumber = any(q['id'] in existing for q in new_items) or \
        any(not q['id'].startswith(pool[1]) for q in new_items)
    if new_items:
        print(f'Neue Fragen ({len(new_items)}), Status "{args.status}":')
    for q in new_items:
        if renumber:
            q['id'] = f'{pool[1]}{pool[0]:0{pool[2]}d}'
            pool[0] += 1
        else:
            pool[0] = max(pool[0], int(q['id'].rsplit('-', 1)[1]) + 1)
        q['status'] = args.status
        tags = q['taxonomy'].get('tags', [])
        kept = [t for t in tags if t in vocab]
        dropped = [t for t in tags if t not in vocab]
        q['taxonomy']['tags'] = kept
        note = f'   (Tags weggelassen: {", ".join(dropped)})' if dropped else ''
        if tags and not kept:
            note += '   ACHTUNG: kein gültiger Tag übrig'
        print(f'   {q["id"]}  {q["content"]["de"]["lead_in"]}{note}')
        qs.append(q)
        touched.add(q['id'])
        changed = True
    if renumber and new_items:
        print('   Vorgeschlagene IDs waren belegt; fortlaufend neu vergeben.')

    print()
    return changed, touched


def main():
    ap = argparse.ArgumentParser(description='Fragenblöcke in die Gebietsdatei übernehmen')
    ap.add_argument('--apply', action='store_true', help='Änderungen schreiben und build.py ausführen')
    ap.add_argument('--status', choices=['published', 'review'], default='published')
    ap.add_argument('--ohne-ersatz', action='store_true', help='bestehende Fragen nicht verändern')
    ap.add_argument('--block', action='append', help='Blockdatei; mehrfach möglich. Standard: alle *-block.json neben diesem Skript')
    ap.add_argument('--datei', help='Zieldatei ausdrücklich angeben, etwa data/fragen/operationskenntnisse.json')
    args = ap.parse_args()

    root = Path.cwd()
    if not (root / 'build.py').exists():
        fail('build.py nicht gefunden. Bitte im Projektordner der Website ausführen.')
    data = root / 'data' if (root / 'data' / 'domains.json').exists() else root
    fragen = data / 'fragen' if data != root else root
    paths = [Path(b) for b in args.block] if args.block else sorted(HERE.glob('*-block.json'))
    if not paths:
        fail('Keine Blockdatei gefunden.')
    for p in paths:
        if not p.exists():
            fail(f'Blockdatei {p} nicht gefunden.')
    blocks = [json.loads(p.read_text(encoding='utf-8')) for p in paths]
    order = sorted(range(len(blocks)), key=lambda i: (blocks[i].get('erstellt', ''), paths[i].name))
    blocks = [blocks[i] for i in order]
    gebiete = {b.get('gebiet') for b in blocks}
    if len(gebiete) != 1 or None in gebiete:
        fail(f'Blöcke ohne oder mit verschiedenen Gebieten: {sorted(str(g) for g in gebiete)}')
    gebiet = gebiete.pop()
    namen = [gebiet] + [n for b in blocks for n in b.get('gebiet_alternativen', [])]

    if args.datei:
        target = Path(args.datei)
        if not target.exists():
            fail(f'{target} nicht gefunden.')
    else:
        treffer = [fragen / f'{n}.json' for n in namen if (fragen / f'{n}.json').exists()]
        if not treffer:
            vorhanden = sorted(f.name for f in fragen.glob('*.json') if f.name != 'domains.json')
            fail(f'Keine Datei für das Gebiet "{gebiet}" gefunden. Vorhanden sind: {", ".join(vorhanden)}.\n'
                 f'       Passende Datei mit --datei angeben oder das Gebiet in der Blockdatei korrigieren.')
        target = treffer[0]
    doc = json.loads(target.read_text(encoding='utf-8'))
    qs = doc.get('fragen')
    if not isinstance(qs, list):
        fail(f'{target.name}: Feld "fragen" fehlt.')
    vocab = set(json.loads((data / 'domains.json').read_text(encoding='utf-8')).get('tags', []))

    print(f'Datei: {target.relative_to(root)} mit {len(qs)} Fragen\n')
    teile = [m.groups() for m in (re.fullmatch(r'(.*?)(\d+)', q.get('id') or '') for q in qs) if m]
    if teile:
        praefix = Counter(p for p, _ in teile).most_common(1)[0][0]
        breite = max(len(z) for p, z in teile if p == praefix)
        nummern = [int(z) for p, z in teile if p == praefix]
    else:
        erste = next((q['id'] for b in blocks for q in b.get('neu', []) if q.get('id')), 'uro-xxx-00001')
        m = re.fullmatch(r'(.*?)(\d+)', erste)
        praefix, breite, nummern = m.group(1), len(m.group(2)), []
    pool = [max(nummern, default=0) + 1, praefix, breite]
    print(f'ID-Präfix der Datei: {praefix}, nächste freie Nummer: {pool[0]:0{breite}d}')
    changed, touched = False, set()
    for b in blocks:
        c, t = merge_block(b, qs, vocab, args, pool)
        changed, touched = changed or c, touched | t

    # Bestand zum Gegenlesen: nur Fragen, die in diesem Lauf nicht neu oder geändert sind
    own = {norm(q['content']['de']['vignette']) for b in blocks for q in b.get('neu', [])} | \
          {norm(r['content']['de']['vignette']) for b in blocks for r in (b.get('ersatz') or {}).values()}
    for b in blocks:
        match = related_filter(b.get('gegenlesen', DEFAULT_GEGENLESEN))
        related = [q for q in qs if q.get('id') not in touched and match(de_text(q))
                   and norm(((q.get('content') or {}).get('de') or {}).get('vignette')) not in own]
        if related:
            print(f"Bitte im Bestand gegen den Block \"{b.get('titel') or b.get('quelle', '')}\" gegenlesen:")
            for q in related:
                print(f'   {q.get("id")}  {((q.get("content") or {}).get("de") or {}).get("lead_in", "")}')
            print()

    if not changed:
        print('Keine Änderungen nötig.')
        return
    if not args.apply:
        print('Vorschau: nichts geschrieben. Übernehmen mit:  python3 merge-hodentumor.py --apply')
        return

    backup = target.with_name(target.name + '.vor-merge')
    shutil.copy2(target, backup)
    target.write_text(json.dumps(doc, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    env = dict(os.environ, PYTHONIOENCODING='utf-8')
    run = subprocess.run([sys.executable, 'build.py'], cwd=root, capture_output=True,
                         text=True, encoding='utf-8', errors='replace', env=env)
    out = (run.stdout or '') + '\n' + (run.stderr or '')
    if run.returncode != 0:
        shutil.copy2(backup, target)
        print(f'build.py ist fehlgeschlagen. {target.name} wurde auf den alten Stand zurückgesetzt.')
        lines = [l for l in out.splitlines() if l.startswith('Fehler') or 'Abbruch' in l]
        print('\n'.join(lines[-40:]) or out[-3000:])
        sys.exit(1)
    print('build.py erfolgreich.')
    pending = 0
    for line in out.splitlines():
        if any(i in line for i in touched) and 'Freigabe ausstehend' in line:
            pending += 1
        elif any(i in line for i in touched) or line.startswith(('index.html', 'richtige Antwort')) or 'verfuegbare Lernfragen' in line:
            print('   ' + line.strip())
    if pending:
        print(f'   {pending} neue oder geänderte Fragen warten auf deine fachärztliche Freigabe (pruefung.html)')
    print(f'Sicherung der alten Datei: {backup.name}')
    print('Hochladen: index.html, pruefung.html und data/fragen/' + target.name)


if __name__ == '__main__':
    main()
