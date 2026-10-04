"""Build static multilingual CME modules without runtime fetch or dependencies."""
import ast
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MODULES = ('cme-seminom-IIAB', 'cme-hodentumor-heft-teil3', 'cme-peniskarzinom', 'cme-salvage-operationen')


def load(name):
    return json.loads((ROOT / 'translations' / name).read_text(encoding='utf-8'))


def localized_literals(source, dictionary):
    # Scan JS strings conservatively. Quotes inside regex character classes and
    # comments are not string delimiters; a regex-only substitution is unsafe.
    result, i, previous = [], 0, ''
    while i < len(source):
        start = i
        char = source[i]
        if source.startswith('//', i):
            i = source.find('\n', i)
            if i < 0:
                i = len(source)
            result.append(source[start:i])
            continue
        if source.startswith('/*', i):
            end = source.find('*/', i + 2)
            i = len(source) if end < 0 else end + 2
            result.append(source[start:i])
            continue
        if char == '/' and previous in '(=:[,;!&|?{':
            i += 1
            bracket = False
            while i < len(source):
                if source[i] == '\\':
                    i += 2
                    continue
                if source[i] == '[':
                    bracket = True
                elif source[i] == ']':
                    bracket = False
                elif source[i] == '/' and not bracket:
                    i += 1
                    while i < len(source) and source[i].isalpha():
                        i += 1
                    break
                i += 1
            result.append(source[start:i])
            previous = '/'
            continue
        if char in "'\"":
            i += 1
            while i < len(source):
                if source[i] == '\\':
                    i += 2
                elif source[i] == char:
                    i += 1
                    break
                else:
                    i += 1
            literal = source[start:i]
            try:
                value = ast.literal_eval(literal)
            except (SyntaxError, ValueError):
                value = None
            is_key = previous in '{,' and source[i:].lstrip().startswith(':')
            if not is_key and isinstance(value, str) and any(term in value for term in dictionary):
                result.append('UroCme.t(' + literal + ')')
            else:
                result.append(literal)
            previous = char
            continue
        result.append(char)
        if not char.isspace():
            previous = char
        i += 1
    return ''.join(result)


def main():
    common = load('common.ui.json')
    # Preserve the score model and version keys from the existing German modules.
    engine = (ROOT / 'templates/cme/cme.js.in').read_text(encoding='utf-8')
    old = "h += '<p class=\"note\">Aktueller Lernstand: ' + wrong.length + ' zuletzt falsch beantwortete Frage' + (wrong.length === 1 ? '' : 'n') + '.</p><div class=\"actions\">';"
    new = "h += '<p class=\"note\">' + cmeText(wrong.length === 1 ? 'currentWrongOne' : 'currentWrong', {n: wrong.length}) + '</p><div class=\"actions\">';"
    if old not in engine:
        raise ValueError('CME score template changed; review the localized status sentence.')
    engine = engine.replace(old, new)
    semantic_keys = {'currentWrong', 'currentWrongOne', 'scoreOne', 'scoreMany', 'weakOne', 'weakMany'}
    engine = localized_literals(engine, {key: value for key, value in common.items() if key not in semantic_keys}).replace('UroCme.t(', 'cmeText(')
    language = (ROOT / 'templates/cme/language.js').read_text(encoding='utf-8')
    language = re.sub(r'\bt\(', 'cmeText(', language)
    language = '  var commonDictionary = ' + json.dumps(common, ensure_ascii=False) + ';\n' + language
    engine = engine.replace("  function own(", language + '\n  function own(', 1)
    engine = engine.replace('    render();\n    return session;', "    try { if (new URLSearchParams(global.location.search).get('continue') === '1' && saved && session.restore(saved)) saved = null; } catch (_) {}\n    render();\n    return session;")
    engine = engine.replace('global.UroCme = {mount:', 'global.UroCme = {t: cmeText, initialize: initialize, language: language, number: number, mount:')
    (ROOT / 'assets/cme.js').write_text(engine, encoding='utf-8')
    for module in MODULES:
        dictionary = {**common, **load(module + '.ui.json')}
        # Shared wording is consistent across modules, including score labels.
        dictionary.update(common)
        bundle = {'data': {lc: load(module + '.' + lc + '.json') for lc in ('en', 'es')}, 'ui': dictionary}
        asset = 'assets/' + module + '-languages.js'
        (ROOT / asset).write_text('window.CME_I18N = ' + json.dumps(bundle, ensure_ascii=False, separators=(',', ':')).replace('<', '\\u003c') + ';\n', encoding='utf-8')
        html = (ROOT / 'templates/cme' / (module + '.html.in')).read_text(encoding='utf-8')
        html = html.replace('<script src="assets/cme.js"></script>', '<script src="' + asset + '"></script>\n<script src="assets/cme.js"></script>')
        def script(match):
            code = match.group(1)
            data_match = re.search(r'var DATA = (.*?);\s*\n', code)
            if not data_match:
                return match.group()
            original = code[:data_match.end()]
            logic = code[data_match.end():]
            logic = logic.replace("return x.toFixed(1).replace('.', ',') + ' cm';", "return UroCme.number(x, 1) + ' cm';")
            logic = localized_literals(logic, dictionary)
            return '<script>' + original + 'var CME_BASE_DATA = DATA;\nDATA = UroCme.initialize(DATA);\n' + logic + '</script>'
        html = re.sub(r'<script>(.*?)</script>', script, html, flags=re.S)
        (ROOT / (module + '.html')).write_text(html, encoding='utf-8')
    print('Four CME modules built in German, English and Spanish.')


if __name__ == '__main__':
    main()
