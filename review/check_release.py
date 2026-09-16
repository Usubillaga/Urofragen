import json,re,subprocess,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
import build
r=subprocess.run([sys.executable,'-X','utf8',str(ROOT/'build.py')],capture_output=True,encoding='utf-8')
(ROOT/'review/build-check.txt').write_text(r.stdout+'\n'+r.stderr,encoding='utf-8')
if r.returncode:raise SystemExit(r.stderr)
js=ROOT/'review/app-check.js'
function=re.search(r'  function approvalLine\(q\) \{.*?\n  \}',build.APP_JS,re.S).group(0)
js.write_text("const assert=require('node:assert/strict');\nvar UI={de:{reviewed:'YES',unreviewed:'NO'},es:{reviewed:'YES',unreviewed:'NO'},en:{reviewed:'YES',unreviewed:'NO'}};var lang='de';\n"+function+"\nlet q={review:{reviewer:'TEST ONLY',last_reviewed:'2026-09-12',expires:'2099-12-31',approval_valid:true,approval:{languages:['de']}}};assert.match(approvalLine(q),/^YES/);lang='es';assert.equal(approvalLine(q),'NO');lang='en';assert.equal(approvalLine(q),'NO');lang='de';q.review.approval_valid=false;assert.equal(approvalLine(q),'NO');q.review.approval_valid=true;q.review.expires='2000-01-01';assert.equal(approvalLine(q),'NO');console.log('5 approval display checks passed');",encoding='utf-8')
subprocess.run(['node',str(js)],check=True)
for name,source in [('app',build.APP_JS),('store',build.STORE_JS)]:
    path=ROOT/'review'/f'{name}-syntax.js';path.write_text(source,encoding='utf-8');subprocess.run(['node','--check',str(path)],check=True);path.unlink()
subprocess.run([sys.executable,'-X','utf8',str(ROOT/'review/verify.py')],check=True)
subprocess.run(['node',str(ROOT/'review/test_review_ui.cjs')],check=True)
print(r.stdout)
