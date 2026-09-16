#!/usr/bin/env python3
"""Explicit per-question review, saved before advancing. --stand is read-only."""
import argparse,copy,json,os,sys,tempfile,uuid
from datetime import date
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from approval import fingerprint,valid_approval,invalidate
FRAGEN=ROOT/'data/fragen';PROTOKOLL=ROOT/'review/freigabe-protokoll.jsonl'
UMFANG='''Die Freigabe gilt nur für die angezeigte Fragenversion und die gewählten
Sprachfassungen. Du bestätigst Lösung, Eindeutigkeit im beschriebenen Fall,
Begründungen, Quellen und medizinische Zahlenangaben. Die anderen Optionen
müssen im konkreten Fall nicht die beste Antwort sein, nicht überall falsch.
Nicht angezeigte Sprachen und andere Fragen sind nicht mitfreigegeben.
Jede Entscheidung wird sofort gespeichert. Kein Name wird voreingetragen.
'''
def atomic_json(path,obj):
    path=Path(path);path.parent.mkdir(parents=True,exist_ok=True)
    fd,name=tempfile.mkstemp(prefix=path.name+'.',suffix='.tmp',dir=path.parent)
    try:
        with os.fdopen(fd,'w',encoding='utf-8') as f:
            json.dump(obj,f,ensure_ascii=False,indent=2);f.write('\n');f.flush();os.fsync(f.fileno())
        os.replace(name,path)
    finally:
        if os.path.exists(name):os.unlink(name)
def lade():
    paths=sorted(FRAGEN.glob('*.json'))
    if not paths:raise ValueError('Keine Fragendateien gefunden: '+str(FRAGEN))
    return {p:json.loads(p.read_text(encoding='utf-8')) for p in paths}
def sync_log(dateien):
    # Embedded events repair a crash between saving the question and updating the log.
    entries={}
    if PROTOKOLL.exists():
        for line in PROTOKOLL.read_text(encoding='utf-8').splitlines():
            try:e=json.loads(line)
            except json.JSONDecodeError:continue
            if e.get('event_id'):entries[e['event_id']]=e
    for doc in dateien.values():
        for q in doc['fragen']:
            for e in q.get('review',{}).get('decision_history',[]):entries[e['event_id']]=e
    PROTOKOLL.parent.mkdir(parents=True,exist_ok=True)
    fd,name=tempfile.mkstemp(prefix='freigabe-log.',suffix='.tmp',dir=PROTOKOLL.parent)
    try:
        with os.fdopen(fd,'w',encoding='utf-8') as f:
            for e in sorted(entries.values(),key=lambda e:(e['date'],e['event_id'])):f.write(json.dumps(e,ensure_ascii=False)+'\n')
            f.flush();os.fsync(f.fileno())
        os.replace(name,PROTOKOLL)
    finally:
        if os.path.exists(name):os.unlink(name)
def entscheiden(path,doc,qid,reviewer,languages,decision,expires=None,note=''):
    if not reviewer.strip():raise ValueError('Prüfername fehlt.')
    if decision not in {'approved','changes_requested','rejected'}:raise ValueError('Unbekannte Entscheidung.')
    work=copy.deepcopy(doc);q=next(q for q in work['fragen'] if q['id']==qid)
    if not languages or not set(languages)<=set(q['content']):raise ValueError('Ungültiger Sprachumfang.')
    now=date.today().isoformat();r=q.setdefault('review',{})
    if decision=='approved':
        if not expires or date.fromisoformat(expires)<date.today():raise ValueError('Gültiges Ablaufdatum erforderlich.')
        if r.get('approval'):r.setdefault('approval_history',[]).append(r['approval'])
        r.update(reviewer=reviewer.strip(),last_reviewed=now,expires=expires,clinical_review_status='approved')
        r.setdefault('editorial_review',{})['clinical_signoff']=True
        r['approval']={'reviewer':reviewer.strip(),'date':now,'expires':expires,'languages':sorted(languages),'question_version':q['version'],'content_sha256':fingerprint(q,languages),'scope':'Medical correctness of displayed languages; explicit reviewer decision'}
        r.pop('review_note',None);q['status']='published'
    else:
        invalidate(q,note);r['clinical_review_status']=decision;q['status']='review' if decision=='changes_requested' else 'retired'
    event={'event_id':str(uuid.uuid4()),'date':now,'question_id':qid,'question_version':q['version'],'reviewer':reviewer.strip(),'languages':sorted(languages),'decision':decision,'expires':expires if decision=='approved' else None,'note':note,'content_sha256':fingerprint(q,languages)}
    r.setdefault('decision_history',[]).append(event)
    atomic_json(path,work)
    doc.clear();doc.update(work)
    return event
def stand(dateien):
    total=approved=0;print('Gebiet                      gültig freigegeben / gesamt')
    for p,doc in dateien.items():
        qs=doc['fragen'];n=sum(valid_approval(q) for q in qs)
        print(f'{p.stem:<28}{n:>4} / {len(qs)}');total+=len(qs);approved+=n
    print(f'Gesamt: {approved}/{total}; {total-approved} ohne aktuelle Freigabe.')
def zeige(q,languages):
    print('\n'+q['id']+' · Version '+str(q['version']));ck=next(o['key'] for o in q['options'] if o['correct'])
    for lc in languages:
        b=q['content'][lc];print('\n'+lc.upper()+'\n'+b['vignette']+'\n\n'+b['lead_in'])
        for key,o in b['options'].items():print(f"\n{'✓' if key==ck else ' '} {key}: {o['text']}\n{o['rationale']}")
        print('\nKernaussage: '+b['explanation']['core']);print('Merksatz: '+b['explanation']['teaching_point'])
        if b.get('flag_note'):print('Vorbehalt: '+b['flag_note'])
    for s in q['sources']:print('\nQuelle:',s.get('title',s.get('citation','')),s.get('year',''),s.get('url',''))
    print('Evidenz:',q.get('evidence'));print('Ablaufdatum:',q['review'].get('expires'));print('Prüffingerabdruck:',fingerprint(q,languages))
def main(argv=None):
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--reviewer');p.add_argument('--gebiet');p.add_argument('--id');p.add_argument('--limit',type=int,default=0)
    p.add_argument('--sprachen',default='de');p.add_argument('--stand',action='store_true');p.add_argument('--erneut',action='store_true')
    args=p.parse_args(argv);docs=lade()
    if args.stand:stand(docs);return
    if not args.reviewer or not args.reviewer.strip():p.error('--reviewer mit dem eigenen Namen ist erforderlich.')
    langs=args.sprachen.split(',')
    if not langs or len(set(langs))!=len(langs) or not set(langs)<={'de','en','es'}:p.error('--sprachen muss de, en, es oder eine Kommaliste enthalten.')
    if args.limit<0:p.error('--limit darf nicht negativ sein.')
    tasks=[(path,q['id']) for path,doc in docs.items() for q in doc['fragen'] if (not args.gebiet or path.stem==args.gebiet) and (not args.id or q['id']==args.id) and (args.erneut or not valid_approval(q) or not set(langs)<=set(q['review'].get('approval',{}).get('languages',[])))]
    if not tasks:print('Keine passenden offenen Fragen. Filter und Prüfstand kontrollieren.');return
    def priority(item):
        path,qid=item;q=next(q for q in docs[path]['fragen'] if q['id']==qid)
        return (not q['evidence'].get('flag'),not bool({'dosierung','zulassung'}&set(q['taxonomy'].get('tags',[]))),q['review'].get('expires','9999'),qid)
    tasks.sort(key=priority);sync_log(docs);print(UMFANG);print('Prüfer:',args.reviewer,'· Sprachen:',','.join(langs));saved=0
    try:
        for path,qid in tasks:
            if args.limit and saved>=args.limit:break
            q=next(q for q in docs[path]['fragen'] if q['id']==qid);zeige(q,langs)
            while True:
                answer=input('\n[j] freigeben, [ä] Änderung, [n] ablehnen, [s] überspringen, [b] beenden: ').strip().lower()
                if answer in {'j','ä','ae','n','s','b'}:break
            if answer=='b':break
            if answer=='s':continue
            note='';expires=None
            if answer=='j':
                while True:
                    default=q['review'].get('expires','');expires=input('Freigabe gültig bis YYYY-MM-DD ['+default+']: ').strip() or default
                    try:
                        if date.fromisoformat(expires)>=date.today():break
                    except ValueError:pass
                    print('Bitte ein gültiges Datum ab heute eingeben.')
                decision='approved'
            else:
                decision='changes_requested' if answer in {'ä','ae'} else 'rejected'
                while not note:note=input('Begründung: ').strip()
            entscheiden(path,docs[path],qid,args.reviewer,langs,decision,expires,note);saved+=1;sync_log(docs);print('Entscheidung gespeichert.')
    except (KeyboardInterrupt,EOFError):print('\nAbgebrochen. Alle zuvor bestätigten Entscheidungen sind gespeichert.')
    stand(docs)
if __name__=='__main__':
    try:main()
    except (ValueError,OSError) as error:print(str(error),file=sys.stderr);sys.exit(1)
