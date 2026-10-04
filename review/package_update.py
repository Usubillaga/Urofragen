"""Package the complete static website, sources, review records and originals."""
from pathlib import Path
from zipfile import ZipFile, ZIP_DEFLATED

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT.parent / 'Urofragen-GitHub-DE-EN-ES-2026-10-04.zip'
SKIP = {'.git', '.agents', '.codex', '__pycache__', 'node_modules'}
files = sorted(p for p in ROOT.rglob('*') if p.is_file() and not SKIP.intersection(p.relative_to(ROOT).parts)
               and p.suffix not in {'.pyc', '.pyo'})
with ZipFile(OUTPUT, 'w', ZIP_DEFLATED, compresslevel=9) as archive:
    for item in files:
        archive.write(item, item.relative_to(ROOT).as_posix())
with ZipFile(OUTPUT) as archive:
    names = archive.namelist()
    required = {'index.html', 'pruefung.html', '.nojekyll', 'build.py', 'approval.py', 'quality.py',
                'cme-seminom-IIAB.html', 'cme-hodentumor-heft-teil3.html', 'cme-peniskarzinom.html',
                'cme-salvage-operationen.html', 'assets/cme.js', 'assets/cme.css',
                'README.md', 'GITHUB-UPLOAD.md', 'CME-AENDERUNGEN-2026-10-04.md'}
    required.update({'tools/build_cme.py', 'translations/common.ui.json', 'templates/cme/language.js'})
    required.update('assets/' + module + '-languages.js' for module in
                    ('cme-seminom-IIAB', 'cme-hodentumor-heft-teil3', 'cme-peniskarzinom', 'cme-salvage-operationen'))
    assert required.issubset(names), required - set(names)
    assert len(names) == len(set(names))
    assert archive.testzip() is None
    assert all(archive.read(p.relative_to(ROOT).as_posix()) == p.read_bytes() for p in files)
print(f'{OUTPUT}\n{len(files)} files, {OUTPUT.stat().st_size} bytes; archive integrity and contents verified.')
