"""Exercise native report publication against real source reports and edge cases."""
import importlib.util
import re
import shutil
import subprocess
import sys
import tempfile
import unittest
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BUILDER = ROOT / 'tools' / 'build_reports.py'


class Page(HTMLParser):
    def __init__(self, content):
        super().__init__()
        self.links, self.ids, self.text = [], [], []
        self.feed(content)

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if 'href' in attrs:
            self.links.append(attrs['href'])
        if 'id' in attrs:
            self.ids.append(attrs['id'])

    def handle_data(self, data):
        self.text.append(data)


class NativeReportsTest(unittest.TestCase):
    def build(self, root, output):
        result = subprocess.run([sys.executable, str(BUILDER), '--root', str(root),
                                 '--output-dir', str(output)], capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_full_real_reports_have_native_links_in_each_language(self):
        self.check_full_reports(ROOT)

    def check_full_reports(self, source_root):
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp)
            self.build(source_root, out)
            sources = sorted((source_root / 'weekly-reports').glob('*/*.md'))
            self.assertEqual(len(list(out.rglob('*.html'))), 3 + len(sources))
            for source in sources:
                kind, issue = source.parent.name, source.name[:10]
                lang = 'es' if source.stem.endswith('-es') else 'en' if source.stem.endswith('-en') else 'de'
                web_suffix = {'es': '-es', 'en': '', 'de': '-de'}[lang]
                page = out / 'reports' / kind / (issue + web_suffix + '.html')
                html = page.read_text(encoding='utf-8')
                parsed = Page(html)
                markdown = source.read_text(encoding='utf-8')
                self.assertIn('<html lang="' + lang + '">', html)
                self.assertEqual(len(parsed.ids), len(set(parsed.ids)))
                # Every original external source and confidence tag survives.
                for url in re.findall(r'\]\((https://[^\s)]+)\)', markdown):
                    self.assertIn(url, parsed.links)
                plain = ''.join(parsed.text)
                for tag in ('[Sicher]', '[Wahrscheinlich]', '[Vermutung]'):
                    self.assertEqual(plain.count(tag), markdown.count(tag), (source.name, tag))
                for href in parsed.links:
                    if href.startswith(('https://', 'http://')):
                        continue
                    target, _, anchor = href.partition('#')
                    self.assertNotIn('.md', target)
                    resolved = (page.parent / target).resolve() if target else page
                    if resolved.name in ('index.html', 'reports.css'):
                        continue
                    self.assertTrue(resolved.is_file(), href)
                    if anchor:
                        self.assertIn(anchor, Page(resolved.read_text(encoding='utf-8')).ids)
                if re.search(r'^\|[-| :]+\|$', markdown, re.M):
                    self.assertIn('<table>', html)
                self.assertFalse(any('weekly-reports/README' in href for href in parsed.links))
            de = (out / 'reports/maintenance/2026-10-17-de.html').read_text(encoding='utf-8')
            self.assertIn('id="monitoring_state"', de)
            self.assertIn('checked_default_sha', ''.join(Page(de).text))

    def test_deterministic_archive_orders_newest_issue_first(self):
        with tempfile.TemporaryDirectory() as tmp:
            root, out = Path(tmp) / 'source', Path(tmp) / 'site'
            shutil.copytree(ROOT / 'weekly-reports', root / 'weekly-reports')
            for kind in ('research', 'maintenance'):
                for suffix in ('', '-es', '-en'):
                    source = root / 'weekly-reports' / kind / ('2026-10-17' + suffix + '.md')
                    shutil.copy(source, source.with_name('2026-10-24' + suffix + '.md'))
            self.check_full_reports(root)
            self.build(root, out)
            before = {p.relative_to(out): p.read_bytes() for p in out.rglob('*.html')}
            self.build(root, out)
            self.assertEqual(before, {p.relative_to(out): p.read_bytes() for p in out.rglob('*.html')})
            html = (out / 'reports-de.html').read_text(encoding='utf-8')
            self.assertLess(html.index('2026-10-24-de.html'), html.index('2026-10-17-de.html'))

    def test_incomplete_translation_fails_before_any_output_changes(self):
        with tempfile.TemporaryDirectory() as tmp:
            root, out = Path(tmp) / 'source', Path(tmp) / 'site'
            folder = root / 'weekly-reports/research'
            folder.mkdir(parents=True)
            (folder / '2026-10-17.md').write_text('# Deutsch\n\nVolltext.', encoding='utf-8')
            out.mkdir()
            sentinel = out / 'reports.html'
            sentinel.write_text('previous complete edition', encoding='utf-8')
            result = subprocess.run([sys.executable, str(BUILDER), '--root', str(root), '--output-dir', str(out)], capture_output=True, text=True)
            self.assertNotEqual(result.returncode, 0)
            self.assertEqual(sentinel.read_text(), 'previous complete edition')
            self.assertEqual(list(out.rglob('*.html')), [sentinel])

    def test_safe_markdown_preserves_tables_code_emphasis_and_parenthesized_links(self):
        self.assertTrue(BUILDER.is_file(), 'Native report builder is missing')
        spec = importlib.util.spec_from_file_location('build_reports', BUILDER)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        md = '# Prüfbericht\n\n**Relevant** und *belegt*, `A < B`.\n\n[Sicher] Befund mit [Quelle](https://example.org/Trial_(2026)).\n\n| Wert | Befund |\n|---|---|\n| 1 | **relevant** |\n\n```json\n{"stage": "<script>"}\n```\n\n<script>alert(1)</script> [böse](javascript:alert(1)) [böse](//example.org)'
        html = module.render_markdown(md, Path('weekly-reports/research/2026-10-17.md'), {})
        self.assertIn('<strong>Relevant</strong>', html)
        self.assertIn('<em>belegt</em>', html)
        self.assertIn('<code>A &lt; B</code>', html)
        self.assertIn('href="https://example.org/Trial_(2026)"', html)
        self.assertIn('<table>', html)
        self.assertIn('[Sicher] Befund mit <a ', html)
        self.assertIn('&lt;script&gt;', html)
        self.assertNotIn('<script>', html)
        self.assertNotIn('href="javascript:', html)
        self.assertNotIn('href="//', html)

    def test_home_navigation_targets_local_language_archives(self):
        source = (ROOT / 'build.py').read_text(encoding='utf-8')
        self.assertTrue("reportsLink.href = {es:'reports-es.html',en:'reports.html',de:'reports-de.html'}[lang]" in source, "Homepage report link must open the native language archive")
        self.assertNotIn("reportsLink.target = '_blank'", source)


if __name__ == '__main__':
    unittest.main(verbosity=2)
