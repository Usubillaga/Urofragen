"""Editorial checks; warnings do not certify medical accuracy."""
import re
from difflib import SequenceMatcher
def norm(s):return re.sub(r'\s+',' ',s.strip()).casefold()
GENERIC={'welche antwort trifft am besten zu?','which answer is most appropriate?','¿cuál es la respuesta más adecuada?','welche aussage trifft zu?','which statement is correct?','¿qué afirmación es correcta?'}
def issues(q):
    out=[];correct=[o['key'] for o in q.get('options',[]) if o.get('correct')]
    for lc,b in q.get('content',{}).items():
        if norm(b.get('lead_in','')) in GENERIC:out.append((lc,'generic_lead','unspezifische Fragestellung'))
        if b.get('vignette','').rstrip().endswith('?'):out.append((lc,'mixed_stem','Frage in der Vignette'))
        opts=b.get('options',{});texts=[norm(o.get('text','')) for o in opts.values()];reasons=[norm(o.get('rationale','')) for o in opts.values()]
        if len(set(texts))!=len(texts):out.append((lc,'duplicate_option','doppelte Antwortoption'))
        if len(set(reasons))!=len(reasons):out.append((lc,'duplicate_rationale','wiederholte Einzelbegründung'))
        elif any(SequenceMatcher(None,a,c).ratio()>=.85 for i,a in enumerate(reasons) for c in reasons[i+1:]):out.append((lc,'near_duplicate_rationale','fast wortgleiche Begründungen prüfen'))
        for r in reasons:
            if len(r)>=140 and r.find(r[:70],70)>=0:out.append((lc,'repeated_block','wiederholten Textblock prüfen'));break
        if len(correct)==1 and correct[0] in opts and len(opts)>1:
            n={k:len(o.get('text','')) for k,o in opts.items()};avg=sum(v for k,v in n.items() if k!=correct[0])/(len(n)-1)
            if avg and n[correct[0]]/avg<.7:out.append((lc,'short_cue','auffällig kurze richtige Option'))
    def numbers(b):
        parts=[b.get('vignette',''),b.get('lead_in','')]
        for o in b.get('options',{}).values():parts += [o.get('text',''),o.get('rationale','')]
        parts += [b.get('explanation',{}).get('core',''),b.get('explanation',{}).get('teaching_point','')]
        text=' '.join(parts).replace('\u202f','').replace('\u00a0','')
        text=re.sub(r'(?<=\d)[.,\s](?=\d{3}(?!\d))','',text)
        text=re.sub(r'(?<=\d),(?=\d)','. ',text).replace('. ','.')
        return {n for n in re.findall(r'\d+(?:\.\d+)?',text) if len(n.split('.')[0])>=2 or '.' in n}
    content=q.get('content',{})
    if 'de' in content:
        ref=numbers(content['de'])
        for lc,b in content.items():
            if lc!='de' and numbers(b)!=ref:out.append((lc,'number_mismatch','Zahlenvergleich mit Deutsch prüfen (Schreibweisen können abweichen)'))
    return out
def corpus_issues(questions,language='de'):
    sig=[]
    for q in questions:
        c=[o['key'] for o in q.get('options',[]) if o.get('correct')];b=q.get('content',{}).get(language)
        if b and len(c)==1:sig.append((q['id'],norm(b.get('lead_in','')+' '+b['options'][c[0]]['text'])))
    out=[]
    for i,(a,x) in enumerate(sig):
        for c,y in sig[i+1:]:
            match=SequenceMatcher(None,x,y)
            if match.real_quick_ratio()<.85 or match.quick_ratio()<.85:continue
            ratio=match.ratio()
            if ratio>=.85:out.append((a,c,round(ratio,2)))
    return out
