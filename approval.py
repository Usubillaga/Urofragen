"""Content-bound review records; not identity verification or a digital signature.
Approvals have no expiry date; a new question version or changed content ends them."""
import hashlib,json
from datetime import date
def fingerprint(q,languages):
    body={k:q.get(k) for k in ('id','version','taxonomy','type','options','evidence','sources')}
    body['content']={lc:q['content'][lc] for lc in sorted(languages)}
    return hashlib.sha256(json.dumps(body,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode('utf-8')).hexdigest()
def valid_approval(q,today=None):
    r=q.get('review') or {};a=r.get('approval') or {};langs=a.get('languages')
    try:
        return bool(r.get('reviewer') and r.get('clinical_review_status')=='approved' and a.get('reviewer')==r['reviewer'] and a.get('question_version')==q.get('version') and isinstance(langs,list) and langs and len(set(langs))==len(langs) and all(lc in q.get('content',{}) for lc in langs) and date.fromisoformat(r['last_reviewed']) <= (today or date.today()) and a.get('date')==r['last_reviewed'] and a.get('content_sha256')==fingerprint(q,langs))
    except (KeyError,TypeError,ValueError):return False
def invalidate(q,reason):
    r=q.setdefault('review',{})
    if r.get('approval'):r.setdefault('approval_history',[]).append(r.pop('approval'))
    r['reviewer']=None;r['last_reviewed']=None;r['clinical_review_status']='pending_independent_review'
    r.setdefault('editorial_review',{})['clinical_signoff']=False;r['review_note']=reason
    r.pop('approval_valid',None)
