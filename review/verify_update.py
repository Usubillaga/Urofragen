"""Verify import integrity, deduplication, drafts, and approval isolation."""
import copy,json,shutil,subprocess,sys,tempfile,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path[:0]=[str(ROOT),str(ROOT/'tools')]
from approval import valid_approval,fingerprint
from import_blocks import prepare
class Update(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.docs=[json.loads(p.read_text(encoding='utf-8')) for p in (ROOT/'data/fragen').glob('*.json')]
        cls.qs={q['id']:q for d in cls.docs for q in d['fragen']}
        cls.report=json.loads((ROOT/'review/import-2026-10-04.json').read_text(encoding='utf-8'))
    def test_counts_languages_and_unique_ids(self):
        self.assertEqual(len(self.qs),267)
        self.assertEqual(sum(len(d['fragen']) for d in self.docs),267)
        self.assertEqual(sum(q['status']=='published' for q in self.qs.values()),257)
        self.assertEqual(sum(q['status']=='draft' for q in self.qs.values()),10)
        self.assertTrue(all(set(q['content'])=={'de','en','es'} for q in self.qs.values()))
    def test_exactly_once_import(self):
        changes,report=prepare(list((ROOT/'updates/2026-10-04').glob('*-block.json')))
        self.assertEqual(changes,{})
        self.assertEqual(report['added'],[]);self.assertEqual(report['replaced'],[])
        self.assertEqual(len(self.report['added']),43)
    def test_approvals(self):
        self.assertEqual(sum(valid_approval(q) for q in self.qs.values()),51)
        for item in self.report['added']:
            q=self.qs[item['id']];self.assertFalse(valid_approval(q));self.assertIsNone(q['review']['reviewer'])
        q=self.qs['uro-hod-00007'];old=self.report['replaced'][0]['previous_question']
        self.assertTrue(valid_approval(old));self.assertFalse(valid_approval(q));self.assertEqual(q['version'],old['version']+1)
        self.assertTrue(q['review']['approval_history'])
    def test_source_content_and_mapping(self):
        for entry in self.report['added']:
            block=json.loads((ROOT/'updates/2026-10-04'/entry['block']).read_text(encoding='utf-8'))
            original=next(q for q in block['neu'] if q['id']==entry['source_id'])
            q=self.qs[entry['id']]
            for field in ['content','sources','options','evidence']:self.assertEqual(q[field],original[field])
            self.assertIn(q['taxonomy']['domain'],{'hodentumor','operativ'})
    def test_restored_drafts(self):
        original=json.loads((ROOT/'updates/2026-10-04/operativ-originalformat.json').read_text(encoding='utf-8'))['gebiete']['operativ']
        for q in original:
            (q.get('review') or {}).pop('expires',None)  # expiry dates were removed from the bank; the source file stays as delivered
            self.assertEqual(self.qs[q['id']],q)
    def test_failed_import_restores_all_generated_outputs(self):
        # Exercise the real importer and builder in an isolated project. A late
        # CME failure happens after the main pages and earlier CME files write.
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp)/'project'
            shutil.copytree(ROOT,root,ignore=shutil.ignore_patterns('.git','node_modules','__pycache__','*.png'))
            original=copy.deepcopy(self.qs['uro-hod-00031'])
            original['id']='uro-hod-90099'
            original['taxonomy']['tags'].append('import-rollback-test')
            block=root/'new-block.json'
            block.write_text(json.dumps({'gebiet':'hodentumor','neu':[original]}),encoding='utf-8')
            modules=['cme-seminom-IIAB','cme-hodentumor-heft-teil3','cme-peniskarzinom','cme-salvage-operationen']
            outputs=[root/'index.html',root/'pruefung.html',root/'assets/cme.js']
            outputs += [root/(name+'.html') for name in modules]
            outputs += [root/'assets'/(name+'-languages.js') for name in modules]
            for path in outputs:path.write_bytes(b'previous generated output\n')
            # These will be newly created before the later module fails.
            (root/(modules[0]+'.html')).unlink()
            (root/'assets'/(modules[0]+'-languages.js')).unlink()
            before={path:path.read_bytes() if path.exists() else None for path in outputs}
            data={path:path.read_bytes() for path in (root/'data').rglob('*.json')}
            (root/'translations'/(modules[-1]+'.es.json')).unlink()
            run=subprocess.run([sys.executable,'-X','utf8',str(root/'tools/import_blocks.py'),'--apply','--block',str(block)],capture_output=True,encoding='utf-8')
            self.assertNotEqual(run.returncode,0)
            self.assertIn('Build failed',run.stderr)
            self.assertIn(modules[-1]+'.es.json',run.stderr)
            self.assertEqual(data,{path:path.read_bytes() for path in data})
            self.assertEqual(before,{path:path.read_bytes() if path.exists() else None for path in outputs})
if __name__=='__main__':unittest.main()
