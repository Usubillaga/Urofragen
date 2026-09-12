"""Editorial checks are not a substitute for independent clinical review."""
import re
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
        texts=[norm(o.get('text','')) for o in opts.values()]
        if len(set(texts))!=len(texts):result.append((lc,'duplicate_option','doppelte Antwortoption'))
        if len(correct)==1 and correct[0] in opts and len(opts)>1:
            lengths={k:len(o['text']) for k,o in opts.items()}
            ratio=lengths[correct[0]]/(sum(v for k,v in lengths.items() if k!=correct[0])/(len(opts)-1))
            if ratio<.7:result.append((lc,'short_cue',f'auffällig kurze richtige Option ({ratio:.2f})'))
            elif ratio>=1.25 and lengths[correct[0]]==max(lengths.values()):result.append((lc,'long_cue',f'auffällig lange richtige Option ({ratio:.2f})'))
    return result
