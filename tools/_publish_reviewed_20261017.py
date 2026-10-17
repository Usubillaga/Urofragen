"""Generate only the locally reviewed outputs on this exact feature branch."""
import importlib.util, json, os, subprocess, sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
CFG={"branch":"feat/weekly-report-residency-backports-20261017","base":"3d7d3034991323e5fbe4548e4c819562ad72550c","tree":"6dbd61370eec7ef6b8fe29e89a19372a3d822f3c","workflow":".github/workflows/pruefung.yml","repository":"Urofragen"}
def git(*args):
    return subprocess.run(['git',*args],cwd=ROOT,capture_output=True,text=True,check=True).stdout.strip()
assert os.environ.get('GITHUB_REF')=='refs/heads/'+CFG['branch']
assert git('branch','--show-current')==CFG['branch']
start=git('rev-parse','HEAD')
git('merge-base','--is-ancestor',CFG['base'],'HEAD')
original=subprocess.run(['git','show',CFG['base']+':'+CFG['workflow']],cwd=ROOT,capture_output=True,check=True).stdout
(ROOT/CFG['workflow']).write_bytes(original)
Path(__file__).unlink()
sys.path.insert(0,str(ROOT))
import build
from datetime import date
class EditionDate(date):
    @classmethod
    def today(cls): return cls(2026,10,17)
build.date=EditionDate
assert build.main()==0
git('add','--all')
actual=git('write-tree')
assert actual==CFG['tree'],f"Generated tree {actual} differs from reviewed tree {CFG['tree']}"
remote=git('ls-remote','origin','refs/heads/'+CFG['branch']).split()[0]
assert remote==start,'Feature branch moved concurrently; refusing to overwrite it'
git('-c','user.name=github-actions[bot]','-c','user.email=41898282+github-actions[bot]@users.noreply.github.com','commit','-m','Generate outputs identical to the reviewed local tree')
git('push','origin','HEAD:refs/heads/'+CFG['branch'])
print('Verified and published tree '+actual)
