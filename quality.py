"""Editorial checks are not a substitute for independent clinical review.

Erweiterung: fast gleiche Begruendungen, Zahlenabgleich ueber die Sprachen,
und Dubletten ueber Fragen hinweg.
"""
import re
from difflib import SequenceMatcher

RATIONALE_SIMILARITY = 0.85
QUESTION_SIMILARITY = 0.85


def _numbers(text):
    """Zahlen mit Bedeutung; Tausendertrenner werden vereinheitlicht."""
    t = text.replace("\u202f", "").replace("\u00a0", "")
    t = re.sub(r"(?<=\d)[.,\s](?=\d{3}(?!\d))", "", t)   # Tausendertrenner
    t = re.sub(r"(?<=\d),(?=\d)", ".", t)                  # Dezimalkomma
    return {n for n in re.findall(r"\d+(?:\.\d+)?", t)
            if len(n.split(".")[0]) >= 2 or "." in n}


def _body_text(body):
    parts = [body.get("vignette", ""), body.get("lead_in", "")]
    for o in body.get("options", {}).values():
        parts += [o.get("text", ""), o.get("rationale", "")]
    exp = body.get("explanation", {})
    parts += [exp.get("core", ""), exp.get("teaching_point") or ""]
    return " ".join(parts)


def corpus_issues(questions, language="de"):
    """Fragen, die sich in Fragestellung und richtiger Antwort kaum unterscheiden."""
    sig = []
    for q in questions:
        korrekt = [o["key"] for o in q.get("options", []) if o.get("correct")]
        b = q.get("content", {}).get(language)
        if not b or len(korrekt) != 1:
            continue
        opt = b.get("options", {}).get(korrekt[0], {})
        sig.append((q["id"], norm(b.get("lead_in", "") + " " + opt.get("text", ""))))
    found = []
    for i, (id_a, a) in enumerate(sig):
        for id_b, c in sig[i + 1:]:
            r = SequenceMatcher(None, a, c).ratio()
            if r >= QUESTION_SIMILARITY:
                found.append((id_a, id_b, round(r, 2)))
    return found
GENERIC={
 'welche antwort trifft am besten zu?', 'which answer is most appropriate?',
 '¿cuál es la respuesta más adecuada?', 'welche aussage trifft zu?',
 'which statement is correct?', '¿qué afirmación es correcta?'
}
def norm(s):return re.sub(r'\s+',' ',s.strip()).casefold()
def issues(q):
    result=[]
    correct=[o['key'] for o in q.get('options',[]) if o.get('correct')]
    for lc,b in q.get('content',{}).items():
        if norm(b.get('lead_in','')) in GENERIC:result.append((lc,'generic_lead','unspezifische Fragestellung'))
        if b.get('vignette','').rstrip().endswith('?'):result.append((lc,'mixed_stem','Frage in der Vignette'))
        opts=b.get('options',{})
        reasons=[norm(o.get('rationale','')) for o in opts.values()]
        if len(set(reasons))!=len(reasons):result.append((lc,'duplicate_rationale','wiederholte Einzelbegründung'))
        else:
            paare=[(SequenceMatcher(None,a,c).ratio(),a,c) for i,a in enumerate(reasons) for c in reasons[i+1:]]
            if paare and max(paare)[0]>=RATIONALE_SIMILARITY:
                result.append((lc,'near_duplicate_rationale',f'zwei Begründungen fast wortgleich ({max(paare)[0]:.2f})'))
        texts=[norm(o.get('text','')) for o in opts.values()]
        if len(set(texts))!=len(texts):result.append((lc,'duplicate_option','doppelte Antwortoption'))
        if len(correct)==1 and correct[0] in opts and len(opts)>1:
            lengths={k:len(o['text']) for k,o in opts.items()}
            ratio=lengths[correct[0]]/(sum(v for k,v in lengths.items() if k!=correct[0])/(len(opts)-1))
            if ratio<.7:result.append((lc,'short_cue',f'auffällig kurze richtige Option ({ratio:.2f})'))
            elif ratio>=1.25 and lengths[correct[0]]==max(lengths.values()):result.append((lc,'long_cue',f'auffällig lange richtige Option ({ratio:.2f})'))
    content=q.get('content',{})
    if len(content)>1:
        leit=sorted(content)[0]; ref=_numbers(_body_text(content[leit]))
        for lc in sorted(content):
            if lc==leit: continue
            hier=_numbers(_body_text(content[lc]))
            fehlt,extra=ref-hier,hier-ref
            if fehlt or extra:
                teile=[]
                if fehlt: teile.append('fehlt '+', '.join(sorted(fehlt)))
                if extra: teile.append('zusätzlich '+', '.join(sorted(extra)))
                result.append((lc,'number_mismatch',f'Zahlen weichen von {leit} ab ({"; ".join(teile)})'))
    return result
