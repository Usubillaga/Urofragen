"""Check complete CME translations, answer parity, citations and numeric values."""
import collections
import json
import re
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from tools.build_cme import MODULES


def leaves(value, path=()):
    if isinstance(value, dict):
        for key, child in value.items():
            yield from leaves(child, path + (key,))
    elif isinstance(value, list):
        for i, child in enumerate(value):
            yield from leaves(child, path + (i,))
    else:
        yield path, value


def numbers(text):
    # Citation numbers are checked separately as exact tokens.
    text = re.sub(r'\[(?:Q|X|LL [^\]]+)\]', '', text)
    return collections.Counter(x.replace(',', '.') for x in re.findall(r'\d+(?:[.,]\d+)*', text))


# Independently inspected equivalent word/number renderings. All other numerical
# values must match exactly; these adjustments do not excuse dropped doses.
WORD_NUMBER_VARIANTS = {
    ('cme-seminom-IIAB', 'en', ('questions', 3, 'ev')): {'5': 1},  # fünf Jahre → 5-year
    ('cme-seminom-IIAB', 'en', ('questions', 4, 'ev')): {'2': 1},  # Zweijahres → 2-year
    ('cme-salvage-operationen', 'en', ('sources', 2)): {'2': -1},  # phase 2 → phase II
    ('cme-salvage-operationen', 'es', ('sources', 2)): {'2': -1},  # fase 2 → fase II
    ('cme-salvage-operationen', 'en', ('hcg', 1, 'data')): {'4': 1},  # vier Jahre → 4-year
}


class CmeLanguages(unittest.TestCase):
    def test_complete_structure_and_answer_parity(self):
        for module in MODULES:
            html = (ROOT / (module + '.html')).read_text(encoding='utf-8')
            original = json.loads(re.search(r'var DATA = (.*?);\s*\n', html).group(1))
            base = dict(leaves(original))
            for lc in ('en', 'es'):
                with self.subTest(module=module, language=lc):
                    translated = json.loads((ROOT / 'translations' / (module + '.' + lc + '.json')).read_text(encoding='utf-8'))
                    local = dict(leaves(translated))
                    self.assertEqual(base.keys(), local.keys())
                    for path, value in base.items():
                        actual = local[path]
                        self.assertIs(type(actual), type(value), path)
                        if not isinstance(value, str) or path[-1] in {'correct', 'axis'}:
                            self.assertEqual(value, actual, path)
                        else:
                            self.assertTrue(actual.strip(), path)
                    self.assertEqual(len(translated['questions']), len(original['questions']))
                    for q, other in zip(original['questions'], translated['questions']):
                        self.assertEqual((q['n'], q['axis'], q['diff'], q['correct']),
                                         (other['n'], other['axis'], other['diff'], other['correct']))

    def test_medical_numbers_and_citations(self):
        for module in MODULES:
            original = json.loads(re.search(r'var DATA = (.*?);\s*\n', (ROOT / (module + '.html')).read_text(encoding='utf-8')).group(1))
            base = dict(leaves(original))
            for lc in ('en', 'es'):
                local = dict(leaves(json.loads((ROOT / 'translations' / (module + '.' + lc + '.json')).read_text(encoding='utf-8'))))
                for path, value in base.items():
                    if isinstance(value, str):
                        with self.subTest(module=module, language=lc, path=path):
                            markers = lambda s: collections.Counter(re.findall(r'\[(?:Q|X|LL [^\]]+)\]', s))
                            self.assertEqual(markers(value), markers(local[path]))
                            expected = numbers(value)
                            for number, count in WORD_NUMBER_VARIANTS.get((module, lc, path), {}).items():
                                expected[number] += count
                            self.assertEqual(+expected, numbers(local[path]))

    def test_language_assets(self):
        for module in MODULES:
            text = (ROOT / (module + '.html')).read_text(encoding='utf-8')
            asset = 'assets/' + module + '-languages.js'
            self.assertIn('src="' + asset + '"', text)
            self.assertTrue((ROOT / asset).is_file())
            dictionary = json.loads((ROOT / 'translations' / (module + '.ui.json')).read_text(encoding='utf-8'))
            for key, value in dictionary.items():
                self.assertTrue(key.strip(), (module, key))
                self.assertEqual(set(value), {'en', 'es'}, (module, key))
                self.assertTrue(value['en'].strip() and value['es'].strip(), (module, key))


if __name__ == '__main__':
    unittest.main()
