"""Rebuild and report generated files that no longer match the committed sources.

Only the build date ("generated") and line endings may differ; everything else
must be identical.
Typical cause of a failure: data/fragen, translations or templates were changed
or uploaded without running `python build.py` and uploading the rebuilt files.
"""
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BUILD_DATE = re.compile(rb'"generated":"\d{4}-\d{2}-\d{2}"')


def generated_files():
    return [ROOT / 'index.html', ROOT / 'pruefung.html', ROOT / 'assets' / 'cme.js',
            *sorted(ROOT.glob('cme-*.html')), *sorted((ROOT / 'assets').glob('*-languages.js'))]


def comparable(data):
    return BUILD_DATE.sub(b'"generated":""', data.replace(b'\r\n', b'\n'))


def main():
    before = {path: path.read_bytes() if path.exists() else None for path in generated_files()}
    run = subprocess.run([sys.executable, '-X', 'utf8', str(ROOT / 'build.py')], capture_output=True, encoding='utf-8')
    if run.returncode:
        print(run.stdout + run.stderr)
        print('Aufbau fehlgeschlagen.')
        return 1
    stale = [path.relative_to(ROOT).as_posix() for path in generated_files()
             if before.get(path) is None or comparable(before[path]) != comparable(path.read_bytes())]
    if stale:
        print('Nicht aktuell (python build.py ausführen und diese Dateien mit hochladen):')
        for name in stale:
            print('  ' + name)
        return 1
    print(f'{len(before)} erzeugte Dateien passen zu den Quelldaten.')
    return 0


if __name__ == '__main__':
    sys.exit(main())
