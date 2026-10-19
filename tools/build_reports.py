#!/usr/bin/env python3
"""Render complete, trusted-in-repo Markdown reports as safe static web pages.

No external packages or browser scripts. Source reports stay authoritative;
question/CME builders and approval state are deliberately outside this tool.
"""
import argparse
import html
import os
import posixpath
import re
import sys
import tempfile
from datetime import date
from pathlib import Path
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parents[1]
LANGUAGES = ('es', 'en', 'de')
NAMES = {'es': 'Español', 'en': 'English', 'de': 'Deutsch'}
WEB_SUFFIX = {'es': '-es', 'en': '', 'de': '-de'}
SOURCE_SUFFIX = {'es': '-es', 'en': '-en', 'de': ''}
COPY = {
    'es': {'title': 'Informes semanales', 'intro': 'Estudios, novedades y mejoras de Urofragen. Informes completos en tres idiomas, con fuentes y límites de la evidencia.',
           'research': 'Estudios y novedades', 'maintenance': 'Revisión y mejoras', 'home': 'Volver a las preguntas',
           'archive': 'Todos los informes', 'read': 'Leer informe completo', 'empty': 'Todavía no hay ediciones publicadas.',
           'notice': 'Relevancia: 1 muy relevante · 2 relevante · 3 algo relevante · 4 poco relevante. La relevancia y las pruebas técnicas no equivalen a una aprobación médica.',
           'languages': 'Idioma del informe', 'skip': 'Ir al contenido', 'issue': 'Edición', 'latest': 'Más reciente'},
    'en': {'title': 'Weekly reports', 'intro': 'Urofragen studies, updates and improvements. Complete reports in three languages, with sources and evidence limitations.',
           'research': 'Research and updates', 'maintenance': 'Review and improvements', 'home': 'Back to questions',
           'archive': 'All reports', 'read': 'Read full report', 'empty': 'No editions have been published yet.',
           'notice': 'Relevance: 1 very relevant · 2 relevant · 3 somewhat relevant · 4 low relevance. Relevance and technical tests do not constitute clinical approval.',
           'languages': 'Report language', 'skip': 'Skip to content', 'issue': 'Edition', 'latest': 'Latest'},
    'de': {'title': 'Wochenberichte', 'intro': 'Studien, Updates und Verbesserungen für Urofragen. Vollständige Berichte in drei Sprachen, mit Quellen und Evidenzgrenzen.',
           'research': 'Studien und Updates', 'maintenance': 'Prüfung und Verbesserungen', 'home': 'Zurück zu den Fragen',
           'archive': 'Alle Berichte', 'read': 'Vollständigen Bericht lesen', 'empty': 'Es wurden noch keine Ausgaben veröffentlicht.',
           'notice': 'Relevanz: 1 sehr relevant · 2 relevant · 3 etwas relevant · 4 wenig relevant. Relevanz und technische Tests ersetzen keine fachärztliche Freigabe.',
           'languages': 'Berichtssprache', 'skip': 'Zum Inhalt', 'issue': 'Ausgabe', 'latest': 'Neueste Ausgabe'},
}
FILENAME = re.compile(r'^(\d{4}-\d{2}-\d{2})(-es|-en)?\.md$')


def overview(lang):
    return 'reports' + WEB_SUFFIX[lang] + '.html'


def relative(target, page):
    return posixpath.relpath(str(target), posixpath.dirname(str(page)) or '.')


def report_link(url, source, link_map):
    """Allow http(s) sources and resolve local Markdown to the native archive."""
    if any(ord(c) < 32 for c in url) or '\\' in url:
        return None
    parts = urlsplit(url)
    if parts.scheme:
        return url if parts.scheme in ('https', 'http') and parts.netloc else None
    if parts.netloc or url.startswith('/'):
        return None
    if not parts.path:
        return url if parts.fragment else None
    resolved = posixpath.normpath(posixpath.join(str(source.parent), parts.path))
    if resolved in link_map:
        target = relative(link_map[resolved], link_map[str(source)])
        return target + ('#' + parts.fragment if parts.fragment else '')
    if parts.path.endswith('.md'):
        raise ValueError('Unresolved report link: ' + str(source) + ': ' + url)
    return None


def inline(text, source, link_map):
    """Small non-HTML Markdown subset used by the report contract."""
    out, i = [], 0
    while i < len(text):
        if text[i] == '\\' and i + 1 < len(text):
            out.append(html.escape(text[i + 1])); i += 2; continue
        if text[i] == '`':
            end = text.find('`', i + 1)
            if end != -1:
                out.append('<code>' + html.escape(text[i + 1:end]) + '</code>'); i = end + 1; continue
        marker = '**' if text.startswith('**', i) else '*' if text[i] == '*' else None
        if marker:
            end = text.find(marker, i + len(marker))
            if end != -1:
                tag = 'strong' if marker == '**' else 'em'
                out.append('<' + tag + '>' + inline(text[i + len(marker):end], source, link_map) + '</' + tag + '>')
                i = end + len(marker); continue
        if text[i] == '[':
            label_end = text.find(']', i + 1)
            if label_end != -1 and text.startswith('](', label_end):
                end, depth = label_end + 2, 1
                while end < len(text) and depth:
                    if text[end] == '(':
                        depth += 1
                    elif text[end] == ')':
                        depth -= 1
                    end += 1
                if depth == 0:
                    label = inline(text[i + 1:label_end], source, link_map)
                    url = report_link(text[label_end + 2:end - 1], source, link_map)
                    out.append('<a href="' + html.escape(url, quote=True) + '">' + label + '</a>' if url else label)
                    i = end; continue
        out.append(html.escape(text[i])); i += 1
    return ''.join(out)


def cells(line):
    return [cell.strip() for cell in re.split(r'(?<!\\)\|', line.strip().strip('|'))]


def render_markdown(text, source, link_map):
    lines, out, used, i = text.splitlines(), [], {}, 0
    while i < len(lines):
        line = lines[i]
        if not line.strip():
            i += 1; continue
        # The native page header provides the same three-language navigation.
        if re.fullmatch(r'\[Español\]\([^\n]+\.md\) [·|] \[English\]\([^\n]+\.md\) [·|] \[Deutsch\]\([^\n]+\.md\)', line.strip()):
            i += 1; continue
        if line.startswith('```'):
            language, code = line[3:].strip(), []
            i += 1
            while i < len(lines) and not lines[i].startswith('```'):
                code.append(lines[i]); i += 1
            if i == len(lines):
                raise ValueError('Unclosed code block: ' + str(source))
            cls = ' class="language-' + language + '"' if re.fullmatch(r'[a-z0-9_-]+', language) else ''
            out.append('<pre><code' + cls + '>' + html.escape('\n'.join(code)) + '</code></pre>')
            i += 1; continue
        heading = re.match(r'^(#{1,6}) (.+)$', line)
        if heading:
            level, title = len(heading[1]), heading[2]
            slug = ''.join(c.lower() if c.isalnum() or c in '_-' else '-' if c.isspace() else '' for c in title)
            slug = re.sub('-+', '-', slug).strip('-') or 'section'
            n = used.get(slug, 0); used[slug] = n + 1
            anchor = slug + ('-' + str(n) if n else '')
            out.append('<h{0} id="{1}">{2}</h{0}>'.format(level, anchor, inline(title, source, link_map)))
            i += 1; continue
        if i + 1 < len(lines) and '|' in line and re.fullmatch(r'\s*\|?\s*:?-+:?\s*(\|\s*:?-+:?\s*)+\|?\s*', lines[i + 1]):
            header, rows = cells(line), []
            i += 2
            while i < len(lines) and '|' in lines[i] and lines[i].strip():
                row = cells(lines[i])
                if len(row) != len(header):
                    raise ValueError('Inconsistent table: ' + str(source))
                rows.append(row); i += 1
            out.append('<div class="table-scroll" tabindex="0"><table><thead><tr>' + ''.join('<th scope="col">' + inline(c, source, link_map) + '</th>' for c in header) + '</tr></thead><tbody>' + ''.join('<tr>' + ''.join('<td>' + inline(c, source, link_map) + '</td>' for c in row) + '</tr>' for row in rows) + '</tbody></table></div>')
            continue
        item = re.match(r'^\s*(?:([-*])|(\d+)\.) (.+)$', line)
        if item:
            tag = 'ol' if item[2] else 'ul'
            start = ' start="' + item[2] + '"' if tag == 'ol' and item[2] != '1' else ''
            entries = []
            while i < len(lines):
                found = re.match(r'^\s*(?:([-*])|(\d+)\.) (.+)$', lines[i])
                if not found or ('ol' if found[2] else 'ul') != tag:
                    break
                entries.append('<li>' + inline(found[3], source, link_map) + '</li>'); i += 1
            out.append('<' + tag + start + '>' + ''.join(entries) + '</' + tag + '>'); continue
        paragraph = [line]
        i += 1
        while i < len(lines) and lines[i].strip() and not re.match(r'^(?:#{1,6} |```|\s*[-*] |\s*\d+\. )', lines[i]):
            paragraph.append(lines[i]); i += 1
        out.append('<p>' + inline('\n'.join(paragraph), source, link_map) + '</p>')
    return '\n'.join(out)


def page_html(lang, title, body, page, alternates):
    text = COPY[lang]
    nav = ' '.join('<a lang="{0}" hreflang="{0}" href="{1}"{2}>{3}</a>'.format(other, relative(alternates[other], page), ' aria-current="page"' if other == lang else '', NAMES[other]) for other in LANGUAGES)
    alternate_tags = '\n'.join('<link rel="alternate" hreflang="' + other + '" href="' + relative(alternates[other], page) + '">' for other in LANGUAGES)
    return '''<!DOCTYPE html>
<html lang="{lang}">
<head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title} · Urofragen</title><meta name="description" content="{intro}">
<link rel="stylesheet" href="{css}">{alternates}</head>
<body><a class="skip" href="#content">{skip}</a><div class="wrap">
<header class="masthead"><a class="brand" href="{home}">Urofragen</a>
<nav class="languages" aria-label="{languages}">{nav}</nav></header>
<nav class="breadcrumbs"><a href="{home}">← {home_label}</a><a href="{archive}">{archive_label}</a></nav>
<main id="content">{body}</main><footer>{notice}</footer></div></body></html>
'''.format(lang=lang, title=html.escape(title), intro=html.escape(text['intro'], quote=True),
           css=relative('assets/reports.css', page), alternates=alternate_tags, skip=text['skip'],
           home=relative('index.html', page), languages=text['languages'], nav=nav,
           home_label=text['home'], archive=relative(overview(lang), page), archive_label=text['archive'], body=body, notice=text['notice'])


def build_reports(root, output):
    editions, link_map = {}, {}
    for kind in ('research', 'maintenance'):
        for path in sorted((root / 'weekly-reports' / kind).glob('*.md')):
            match = FILENAME.fullmatch(path.name)
            if not match:
                continue
            issue = match[1]
            date.fromisoformat(issue)
            lang = {'-es': 'es', '-en': 'en', None: 'de'}[match[2]]
            source = path.relative_to(root)
            editions.setdefault((kind, issue), {})[lang] = source
            link_map[str(source)] = 'reports/' + kind + '/' + issue + WEB_SUFFIX[lang] + '.html'
    rendered = {}
    for (kind, issue), sources in editions.items():
        if set(sources) != set(LANGUAGES):
            raise ValueError('Incomplete language edition: ' + kind + '/' + issue)
        alternates = {lang: link_map[str(source)] for lang, source in sources.items()}
        for lang, source in sources.items():
            text = (root / source).read_text(encoding='utf-8')
            heading = re.search(r'^# (.+)$', text, re.M)
            if not heading or not text.strip():
                raise ValueError('Missing report heading: ' + str(source))
            page = alternates[lang]
            body = '<p class="eyebrow">' + COPY[lang][kind] + ' · <time datetime="' + issue + '">' + issue + '</time></p>\n<article class="report">' + render_markdown(text, source, link_map) + '</article>'
            rendered[page] = page_html(lang, heading[1], body, page, alternates)
    for lang in LANGUAGES:
        text, sections = COPY[lang], []
        for kind in ('research', 'maintenance'):
            issues = sorted((issue for series, issue in editions if series == kind), reverse=True)
            cards = []
            for n, issue in enumerate(issues):
                target = link_map[str(editions[(kind, issue)][lang])]
                cards.append('<li class="edition"><div class="edition-meta"><time datetime="' + issue + '">' + issue + '</time>' + ('<span class="latest">' + text['latest'] + '</span>' if n == 0 else '') + '</div><h3><a href="' + target + '">' + text[kind] + ' · ' + text['issue'] + ' ' + issue + '</a></h3><span class="read">' + text['read'] + ' →</span></li>')
            sections.append('<section aria-labelledby="' + kind + '"><h2 id="' + kind + '">' + text[kind] + '</h2>' + ('<ul class="editions">' + ''.join(cards) + '</ul>' if cards else '<p>' + text['empty'] + '</p>') + '</section>')
        body = '<p class="eyebrow">Urofragen · ' + text['title'] + '</p><h1>' + text['title'] + '</h1><p class="intro">' + text['intro'] + '</p>' + ''.join(sections)
        page = overview(lang)
        rendered[page] = page_html(lang, text['title'], body, page, {other: overview(other) for other in LANGUAGES})
    # Validate every source/link before touching published outputs. Each replacement
    # is atomic; a failed CI run is never committed by the publisher.
    for name, content in sorted(rendered.items()):
        target = output / name
        target.parent.mkdir(parents=True, exist_ok=True)
        with tempfile.NamedTemporaryFile(dir=target.parent, delete=False) as temp:
            temp.write(content.encode('utf-8'))
            temporary = temp.name
        os.replace(temporary, target)
    return rendered


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, default=ROOT)
    parser.add_argument('--output-dir', type=Path)
    args = parser.parse_args()
    try:
        pages = build_reports(args.root.resolve(), (args.output_dir or args.root).resolve())
    except (OSError, ValueError) as error:
        print('Report build failed: ' + str(error), file=sys.stderr)
        return 1
    print(str(len(pages)) + ' native report pages generated.')
    return 0


if __name__ == '__main__':
    sys.exit(main())
