"""Safe multi-domain import: preview by default, --apply to commit and build."""
import runpy
from pathlib import Path
runpy.run_path(str(Path(__file__).resolve().parent/'tools/import_blocks.py'),run_name='__main__')
