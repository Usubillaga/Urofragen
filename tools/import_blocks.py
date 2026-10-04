"""Import multiple domains safely. Preview by default; --apply builds or rolls back."""
import argparse,copy,hashlib,json,re,subprocess,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from approval import invalidate,valid_approval,fingerprint
ALIASES={'operationskenntnisse':'operativ'}
def read(p):return json.loads(p.read_text(encoding='utf-8'))
def encoded(d):return (json.dumps(d,ensure_ascii=False,indent=2)+'\n').encode('utf-8')
def prepare(paths,root=ROOT):
    config=read(root/'data/domains.json');docs={p:read(p) for p in (root/'data/fragen').glob('*.json')}
    bydomain={d['gebiet']:(p,d) for p,d in docs.items()};allids={q['id'] for d in docs.values() for q in d['fragen']}
    report={'added':[],'replaced':[],'skipped':[],'date':'2026-10-04'};hashes=set()
    tags=set(config.get('tags',[]))
    for path in sorted(paths):
        digest=hashlib.sha256(path.read_bytes()).hexdigest()
        if digest in hashes:report['skipped'].append(path.name+' (identical file)');continue
        hashes.add(digest);block=read(path);domain=ALIASES.get(block['gebiet'],block['gebiet'])
        if domain not in bydomain:raise ValueError('Unknown domain: '+domain)
        p,doc=bydomain[domain];prefix='uro-hod-' if domain=='hodentumor' else 'uro-ope-'
        imported={q.get('import_record',{}).get('source_key') for q in doc['fragen']}
        for sourceid,rep in (block.get('ersatz') or {}).items():
            q=next((q for q in doc['fragen'] if q['id']==sourceid),None)
            if q is None:raise ValueError('Replacement target missing: '+sourceid)
            token=path.name+':'+sourceid
            if q.get('import_record',{}).get('source_key')==token:
                if q['import_record']['block_sha256']!=digest:raise ValueError('Source changed; explicit review needed: '+token)
                report['skipped'].append(token);continue
            old=copy.deepcopy(q);version=q['version'];signed=valid_approval(q)
            for field in ['options','evidence','sources','content']:q[field]=copy.deepcopy(rep[field])
            q['version']=version+1;invalidate(q,'Neue Seminom-IIA/B-Fassung; erneute fachärztliche Prüfung erforderlich.')
            q['review']['expires']=rep['review_expires']
            q['review']['revision']={'date':report['date'],'based_on_version':version,'reason':'Seminom IIA/B: Stellenwert der primären RLA aktualisiert.','requires_review':True}
            q['import_record']={'source_key':token,'block_sha256':digest,'source_id':sourceid}
            report['replaced'].append({'id':sourceid,'old_version':version,'new_version':q['version'],'old_approval':signed,'previous_question':old})
        for original in block.get('neu',[]):
            token=path.name+':'+original['id']
            if token in imported:
                old=next(q for q in doc['fragen'] if q.get('import_record',{}).get('source_key')==token)
                if old['import_record']['block_sha256']!=digest:raise ValueError('Source changed; explicit review needed: '+token)
                report['skipped'].append(token);continue
            q=copy.deepcopy(original);sourceid=q['id']
            if q['id'] in allids or not q['id'].startswith(prefix):
                n=max([int(x[len(prefix):]) for x in allids if x.startswith(prefix) and x[len(prefix):].isdigit()]+[0])+1
                q['id']=prefix+str(n).zfill(5)
            q['taxonomy']['domain']=domain;tags.update(q['taxonomy'].get('tags',[]))
            invalidate(q,'Neu importiert; fachärztliche Prüfung ausstehend.')
            q['status']='published'
            q['review']['revision']={'date':report['date'],'reason':'Neue Frage: '+block.get('titel',path.stem),'requires_review':True}
            q['import_record']={'source_key':token,'block_sha256':digest,'source_id':sourceid}
            assert set(q['content'])=={'de','en','es'}
            assert sum(bool(o['correct']) for o in q['options'])==1
            doc['fragen'].append(q);allids.add(q['id']);imported.add(token)
            report['added'].append({'id':q['id'],'source_id':sourceid,'block':path.name,'domain':domain})
    config['tags']=sorted(tags)
    changes={p:encoded(d) for p,d in docs.items() if encoded(d)!=p.read_bytes()}
    if encoded(config)!=(root/'data/domains.json').read_bytes():changes[root/'data/domains.json']=encoded(config)
    return changes,report
def main():
    a=argparse.ArgumentParser(description=__doc__);a.add_argument('--apply',action='store_true');a.add_argument('--block',action='append');args=a.parse_args()
    paths=[Path(p) for p in args.block] if args.block else sorted((ROOT/'updates/2026-10-04').glob('*-block.json'))
    if not paths:raise ValueError('No blocks found')
    changes,report=prepare(paths)
    print(f"{len(report['added'])} neue Fragen; {len(report['replaced'])} Ersatzfragen; {len(report['skipped'])} übersprungen.")
    if not args.apply:print('Vorschau; zum Übernehmen --apply.');return
    if not changes:print('Keine Änderungen.');return
    backups={p:p.read_bytes() for p in changes}
    outputs={ROOT/n:(ROOT/n).read_bytes() if (ROOT/n).exists() else None for n in ['index.html','pruefung.html']}
    try:
        for p,b in changes.items():p.write_bytes(b)
        run=subprocess.run([sys.executable,'-X','utf8',str(ROOT/'build.py')],cwd=ROOT,capture_output=True,encoding='utf-8')
        (ROOT/'review/build-2026-10-04.txt').write_text(run.stdout+'\n'+run.stderr,encoding='utf-8')
        if run.returncode:raise ValueError('Build failed: '+run.stderr[-4000:])
    except BaseException:
        for p,b in backups.items():p.write_bytes(b)
        for p,b in outputs.items():
            if b is not None:p.write_bytes(b)
            elif p.exists():p.unlink()
        raise
    (ROOT/'review/import-2026-10-04.json').write_bytes(encoded(report))
    print('Gespeichert und Website erstellt.')
if __name__=='__main__':main()
