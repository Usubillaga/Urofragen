"""Verify import integrity, deduplication, drafts, and approval isolation."""
import copy,hashlib,json,shutil,subprocess,sys,tempfile,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path[:0]=[str(ROOT),str(ROOT/'tools')]
from approval import valid_approval,fingerprint
from import_blocks import prepare
import build
class Update(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.docs=[json.loads(p.read_text(encoding='utf-8')) for p in (ROOT/'data/fragen').glob('*.json')]
        cls.qs={q['id']:q for d in cls.docs for q in d['fragen']}
        cls.report=json.loads((ROOT/'review/import-2026-10-04.json').read_text(encoding='utf-8'))
    def test_counts_languages_and_unique_ids(self):
        self.assertEqual(len(self.qs),291)
        self.assertEqual(sum(len(d['fragen']) for d in self.docs),291)
        self.assertEqual(sum(q['status']=='published' for q in self.qs.values()),281)
        self.assertEqual(sum(q['status']=='draft' for q in self.qs.values()),10)
        self.assertTrue(all(set(q['content'])=={'de','en','es'} for q in self.qs.values()))
    def test_residency_additions_preserve_provenance_and_pending_review(self):
        mapping={
            'uro-and-00011':'q-pri-ischaemic-40h-mri-necrosis-early-prosthesis',
            'uro-and-00012':'q-pri-prolonged-erection-after-ici-terbutaline-first',
            'uro-pca-00024':'q-pca-baseline-psa-intermediate-interval',
            'uro-pca-00025':'q-pca-brca2-carrier-confirmed-psa-mri',
            'uro-rcc-00013':'q-rcc-sestamibi-positive-biopsy-before-surveillance',
        }
        self.assertTrue(set(mapping)<=set(self.qs),'Five adapted Residency cases are missing')
        for qid,source_id in mapping.items():
            with self.subTest(question=qid):
                q=self.qs[qid]
                self.assertEqual(q['version'],1)
                self.assertEqual(q['status'],'published')
                self.assertEqual(q['import_record']['source_case_id'],source_id)
                self.assertEqual(q['import_record']['source_commit'],'a853851ef6afdc34861dde63daf422eb2e1a86f8')
                self.assertEqual(sum(bool(o['correct']) for o in q['options']),1)
                self.assertFalse(valid_approval(q))
                self.assertIsNone(q['review']['last_reviewed'])
                self.assertTrue(q['review']['revision']['requires_review'])
                self.assertEqual(set(q['translation']),{'en','es'})
                self.assertTrue(all(v['clinical_signoff'] is False for v in q['translation'].values()))
                self.assertTrue(all(source.get('url','').startswith('https://') for source in q['sources']))
    def test_urodynamics_section_shows_tracings_and_stays_linked_to_residency(self):
        config=json.loads((ROOT/'data/domains.json').read_text(encoding='utf-8'))
        slugs=[d['slug'] for d in config['domains']]
        self.assertEqual(slugs[slugs.index('funktionell')+1],'urodynamik')
        domain=config['domains'][slugs.index('urodynamik')]
        self.assertEqual(domain['label'],{'de':'Urodynamik','en':'Urodynamics','es':'Urodinámica'})
        doc=json.loads((ROOT/'data/fragen/urodynamik.json').read_text(encoding='utf-8'))
        self.assertEqual(doc['gebiet'],'urodynamik')
        tracings=json.loads((ROOT/'data/urodynamik-kurven.json').read_text(encoding='utf-8'))['tracings']
        ids=[q['id'] for q in doc['fragen']]
        self.assertEqual(ids,[f'uro-udy-{n:05d}' for n in range(1,20)])
        companions=set()
        for n,q in enumerate(doc['fragen'],1):
            with self.subTest(question=q['id']):
                # The ten questions of 20 October gained their tracing (version 2); nine tracing questions are new.
                self.assertEqual((q['version'],q['status'],q['taxonomy']['domain']),(2 if n<=10 else 1,'published','urodynamik'))
                self.assertEqual(sum(bool(o['correct']) for o in q['options']),1)
                self.assertEqual(len(q['options']),5 if n<=10 else 4)
                self.assertEqual(set(q['content']),{'de','en','es'})
                # No approval is invented; marking happens in the review page.
                self.assertFalse(valid_approval(q))
                self.assertIsNone(q['review']['reviewer'])
                self.assertEqual(q['review']['clinical_review_status'],'pending_independent_review')
                self.assertTrue(q['review']['revision']['requires_review'])
                self.assertTrue(all(v['clinical_signoff'] is False for v in q['translation'].values()))
                notes=' '.join([q['review']['editorial_review']['method'],q['review']['review_note']]+[v['method'] for v in q['translation'].values()])
                self.assertNotIn('fachärztliche Freigabe',notes)
                self.assertNotIn('ausstehend',notes)
                self.assertTrue(any(s.get('url','').startswith('https://') for s in q['sources']))
                self.assertTrue(all(s.get('url','https://').startswith('https://') for s in q['sources']))
                self.assertEqual(q['companion_case']['repository'],'Usubillaga/Residency-Game-DE')
                case=q['companion_case']['case_id']
                self.assertTrue(case.startswith('udy-'))
                companions.add(case)
                ref,tr=q['tracing'],tracings[case]
                self.assertEqual(ref['case'],case)
                self.assertIn(ref['view'],[v['id'] for v in tr['views']])
                self.assertTrue(set(ref['after'])<=set(tr['steps']))
                self.assertEqual(ref['sha256'],build.tracing_sha(tr))
                if n>10:
                    self.assertIn(q['companion_case']['step'],tr['steps'])
                if q['evidence']['flag']:
                    self.assertTrue(all(q['content'][lc]['flag_note'] for lc in ('de','en','es')))
        self.assertEqual(len(companions),19)
        self.assertEqual(set(tracings),companions)
        first=json.loads((ROOT/'updates/2026-10-20/urodynamik-abschnitt.json').read_text(encoding='utf-8'))
        self.assertEqual([r['id'] for r in first['questions']],ids[:10])
        record=json.loads((ROOT/'updates/2026-10-27/urodynamik-messkurven.json').read_text(encoding='utf-8'))
        self.assertEqual([r['id'] for r in record['questions']],ids)
        self.assertRegex(record['source_commit'],r'^[0-9a-f]{40}$')
        for path,entry in record['files'].items():
            self.assertEqual(hashlib.sha256((ROOT/path).read_bytes()).hexdigest(),entry['sha256'],path)
    def test_tracing_checks_reject_changed_curves_and_hidden_sections(self):
        build.TRACINGS.clear();build.TRACINGS.update(json.loads((ROOT/'data/urodynamik-kurven.json').read_text(encoding='utf-8'))['tracings'])
        def problems(q):
            found=[];build.check_tracing(q,found.append);return found
        q=copy.deepcopy(self.qs['uro-udy-00008'])
        self.assertEqual(problems(q),[])
        for change,expected in [({'sha256':'0'*64},'sha256'),({'view':'fill2'},'verborgen'),({'after':['unbekannt']},'tracing.after'),
                                ({'case':'udy-fehlt'},'fehlt'),({'view_after':'keiner'},'kein Ausschnitt'),({'extra':1},'unbekannte Felder')]:
            with self.subTest(change=change):
                bad=copy.deepcopy(q);bad['tracing'].update(change)
                self.assertTrue(any(expected in p for p in problems(bad)),problems(bad))
    def test_tracing_is_part_of_the_approval_fingerprint(self):
        q=copy.deepcopy(self.qs['uro-udy-00011']);shown=fingerprint(q,['de'])
        q['tracing']['sha256']='0'*64
        self.assertNotEqual(fingerprint(q,['de']),shown)
        q.pop('tracing')
        self.assertNotEqual(fingerprint(q,['de']),shown)
    def test_revised_citrate_explanation_uses_male_eau_threshold(self):
        q=self.qs['uro-lit-00003']
        self.assertEqual(q['version'],3)
        for lc,threshold in [('de','1,7 mmol/d'),('en','1.7 mmol/day'),('es','1,7 mmol/día')]:
            with self.subTest(language=lc):
                text=q['content'][lc]['options']['D']['rationale']
                self.assertIn(threshold,text)
                self.assertNotRegex(text,r'2[,.]5')
        self.assertFalse(valid_approval(q))
        self.assertTrue(any('/metabolic-evaluation-and-recurrence-prevention' in s.get('url','') for s in q['sources']))
    def test_ureteroenteric_stricture_correction_is_versioned_and_sourced(self):
        q=self.qs['uro-rek-00012']
        self.assertEqual(q['version'],2)
        self.assertFalse(valid_approval(q))
        self.assertIn('links häufiger als rechts',q['content']['de']['options']['B']['rationale'])
        self.assertTrue(any(s.get('doi')=='10.21037/tau.2019.09.05' for s in q['sources']))
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
