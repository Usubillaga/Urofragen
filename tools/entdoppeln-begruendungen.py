#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Entfernt doppelte Textblöcke in Begründungen.

Beim Zusammenführen mehrerer Bearbeitungsschritte wurde derselbe Satzblock
zweimal an eine Begründung angehängt. Betroffen sind Begründungen, in denen
die ersten 70 Zeichen ein zweites Mal vorkommen. Entfernt wird nur eine
exakte vollständige Wiederholung. Einzigartige Folgesätze bleiben erhalten.

Vorschau: python3 tools/entdoppeln-begruendungen.py
Speichern: python3 tools/entdoppeln-begruendungen.py --apply
"""
import json
import re
import argparse
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from approval import invalidate
from freigabe import atomic_json

FRAGEN = Path(__file__).resolve().parent.parent / "data" / "fragen"


def norm(s):
    return re.sub(r"\s+", " ", s.strip()).casefold()


def kuerze(text):
    t = norm(text)
    if len(t) < 140:
        return text
    kopf = t[:70]
    if t.count(kopf) < 2:
        return text
    # Position der Wiederholung im Originaltext suchen
    flach = re.sub(r"\s+", " ", text.strip())
    pos = flach.casefold().find(kopf, 1)
    if pos <= 0:
        return text
    block = flach[:pos].strip()
    rest = flach[pos:]
    # Remove only an exact complete repetition; retain every unique suffix.
    if not block.endswith(('.', '!', '?')) or rest[:len(block)].casefold() != block.casefold():
        return text
    return (block + ' ' + rest[len(block):].strip()).strip()


def main():
    parser = argparse.ArgumentParser(description='Exakte Wiederholungen prüfen; ohne --apply werden keine Dateien geändert.')
    parser.add_argument('--apply', action='store_true')
    args = parser.parse_args()
    gesamt = 0
    for pfad in sorted(FRAGEN.glob("*.json")):
        doc = json.loads(pfad.read_text(encoding="utf-8"))
        n = 0
        for q in doc["fragen"]:
            changed = False
            for b in q["content"].values():
                for o in b["options"].values():
                    neu = kuerze(o.get("rationale", ""))
                    if neu != o.get("rationale"):
                        o["rationale"] = neu
                        n += 1
                        changed = True
            if changed:
                q['version'] += 1
                invalidate(q, 'Begründung geändert; erneute Prüfung erforderlich.')
        if n:
            if args.apply:
                atomic_json(pfad, doc)
            print(f"{pfad.stem:<22} {n:>3} Begründungen: " + ('gespeichert' if args.apply else 'Vorschau'))
            gesamt += n
    print(f"\n{gesamt} Begründungen bereinigt")


if __name__ == "__main__":
    main()
