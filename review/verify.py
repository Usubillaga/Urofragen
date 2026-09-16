"""Regression checks use temporary copies, never real clinical approvals."""
import copy,importlib.util,json,re,sys,tempfile,unittest
from pathlib import Path
from unittest.mock import patch
ROOT=Path(__file__).resolve().parents[1];sys.path[:0]=[str(ROOT),str(ROOT/'tools')]
from approval import valid_approval,invalidate,fingerprint
import freigabe
spec=importlib.util.spec_from_file_location('dedup',ROOT/'tools/entdoppeln-begruendungen.py');dedup=importlib.util.module_from_spec(spec);spec.loader.exec_module(dedup)
class Integrity(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory();self.addCleanup(self.tmp.cleanup)
        self.path=Path(self.tmp.name)/'mibc.json'
        self.doc=json.loads((ROOT/'data/fragen/mibc.json').read_text(encoding='utf-8'))
        for q in self.doc['fragen']:invalidate(q,'Isolated test fixture')
        self.q=self.doc['fragen'][0];self.qid=self.q['id']
        freigabe.atomic_json(self.path,self.doc)
    def approve(self):
        freigabe.entscheiden(self.path,self.doc,self.qid,'TEST ONLY',['de'],'approved','2099-12-31')
        return self.doc['fragen'][0]
    def test_imported_name_is_not_approval(self):
        self.q['review'].update(reviewer='TEST ONLY',clinical_review_status='approved')
        self.assertFalse(valid_approval(self.q))
    def test_content_version_and_language_scope(self):
        q=self.approve();self.assertTrue(valid_approval(q));self.assertEqual(q['review']['approval']['languages'],['de'])
        q['content']['es']['lead_in']+=' Cambio';self.assertTrue(valid_approval(q))
        q['content']['de']['lead_in']+=' Änderung';self.assertFalse(valid_approval(q))
        q=self.approve();q['version']+=1;self.assertFalse(valid_approval(q))
    def test_expiry_and_rejection(self):
        q=self.approve();q['review']['expires']='2000-01-01';self.assertFalse(valid_approval(q))
        freigabe.entscheiden(self.path,self.doc,self.qid,'TEST ONLY',['de'],'rejected',note='Test')
        q=self.doc['fragen'][0];self.assertFalse(valid_approval(q));self.assertIsNone(q['review']['reviewer']);self.assertEqual(q['status'],'retired')
    def test_atomic_failure_preserves_file_and_memory(self):
        before=self.path.read_bytes();old=copy.deepcopy(self.doc)
        with patch.object(freigabe.os,'replace',side_effect=OSError('test')):
            with self.assertRaises(OSError):self.approve()
        self.assertEqual(before,self.path.read_bytes());self.assertEqual(old,self.doc)
    def test_log_recovery(self):
        self.approve();log=Path(self.tmp.name)/'log.jsonl'
        with patch.object(freigabe,'PROTOKOLL',log):
            freigabe.sync_log({self.path:self.doc});freigabe.sync_log({self.path:self.doc})
        self.assertEqual(len(log.read_text(encoding='utf-8').splitlines()),1)
    def test_eof_preserves_confirmed_decision(self):
        with patch.object(freigabe,'FRAGEN',Path(self.tmp.name)),patch.object(freigabe,'PROTOKOLL',Path(self.tmp.name)/'log.jsonl'),patch('builtins.print'),patch('builtins.input',side_effect=['j','2099-12-31',EOFError()]):
            freigabe.main(['--reviewer','TEST ONLY'])
        saved=json.loads(self.path.read_text(encoding='utf-8'))
        self.assertEqual(sum(valid_approval(q) for q in saved['fragen']),1)
    def test_dedup_retains_unique_suffix(self):
        block='Dieser vollständige Satz enthält eine ausreichend lange medizinische Begründung zur Prüfung.'
        self.assertEqual(dedup.kuerze(block+' '+block+' Einzigartiger Zusatz.'),block+' Einzigartiger Zusatz.')
        self.assertEqual(dedup.kuerze(block+' '+block[:-12]+' anderer Schluss.'),block+' '+block[:-12]+' anderer Schluss.')
    def test_production_bank_preserves_explicit_approvals(self):
        docs=[json.loads(p.read_text(encoding='utf-8')) for p in (ROOT/'data/fragen').glob('*.json')]
        qs=[q for d in docs for q in d['fragen']]
        self.assertEqual(len(qs),214);self.assertTrue(all(len(d['fragen'])>=10 for d in docs))
        self.assertTrue(all(set(q['content'])=={'de','en','es'} for q in qs))
        approved=[q for q in qs if valid_approval(q)]
        self.assertEqual(len(approved),52)
        for q in approved:
            self.assertEqual(q['review']['approval']['languages'],['de'])
            d=q['review']['imported_decisions'][-1]
            self.assertEqual(d['decision'],'approved')
            self.assertEqual(fingerprint(q,['de']),d['content_sha256'])
            self.assertEqual(q['review']['last_reviewed'],d['date'])
        revised=[q for q in qs if q['review'].get('revision')]
        self.assertEqual(len(revised),13)
        self.assertFalse(any(valid_approval(q) for q in revised))
        self.assertEqual(sum(bool(q['review'].get('approval_history')) for q in revised),8)
if __name__=='__main__':unittest.main()
