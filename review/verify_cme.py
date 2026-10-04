"""Check static packaging and preserve all supplied medical module data."""
import json
import re
import unittest
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MODULES = {
    'cme-seminom-IIAB.html': 10,
    'cme-hodentumor-heft-teil3.html': 14,
    'cme-peniskarzinom.html': 16,
    'cme-salvage-operationen.html': 10,
}


def data(text):
    return json.loads(re.search(r'var DATA = (.*?);\s*\n', text).group(1))


class References(HTMLParser):
    def __init__(self):
        super().__init__()
        self.local = []

    def handle_starttag(self, tag, attrs):
        for name, value in attrs:
            if name in {'href', 'src'} and value and not value.startswith(('#', 'http:', 'https:', 'mailto:', 'data:')):
                self.local.append(value.split('#')[0].split('?')[0])


class CmeIntegration(unittest.TestCase):
    def test_medical_data_unchanged(self):
        for filename, count in MODULES.items():
            with self.subTest(module=filename):
                current = data((ROOT / filename).read_text(encoding='utf-8'))
                original = data((ROOT / 'updates/2026-10-04/cme-originals' / filename).read_text(encoding='utf-8'))
                self.assertEqual(current, original)
                self.assertEqual(len(current['questions']), count)
                self.assertEqual(len({q['n'] for q in current['questions']}), count)
                for q in current['questions']:
                    self.assertEqual(set(q['opts']), set('ABCDE'))
                    self.assertIn(q['correct'], q['opts'])
                    self.assertIn(q['axis'], current['axes'])

    def test_relative_links_and_assets(self):
        for filename in MODULES:
            text = (ROOT / filename).read_text(encoding='utf-8')
            refs = References()
            refs.feed(text)
            with self.subTest(module=filename):
                for ref in refs.local:
                    self.assertTrue((ROOT / ref).is_file(), ref)
                self.assertIn('index.html', refs.local)
                self.assertIn('pruefung.html', refs.local)
                self.assertIn('assets/cme.js', refs.local)
                self.assertIn('assets/cme.css', refs.local)

    def test_generated_home_and_question_bank(self):
        text = (ROOT / 'index.html').read_text(encoding='utf-8')
        for filename in MODULES:
            self.assertIn(filename, text)
        self.assertIn('Alemán, inglés y español', text)
        bank = json.loads(re.search(r'<script id="bank" type="application/json">(.*?)</script>',
                                   (ROOT / 'pruefung.html').read_text(encoding='utf-8'), re.S).group(1))
        self.assertEqual(len(bank['questions']), 267)
        self.assertEqual(sum(q['status'] == 'published' for q in bank['questions']), 257)


if __name__ == '__main__':
    unittest.main()
