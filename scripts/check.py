#!/usr/bin/env python3
from __future__ import annotations
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlparse
import json, re, sys

ROOT = Path(__file__).resolve().parents[1]
DIST = ROOT / "dist"

class Parser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links=[]; self.title=False; self.description=False; self.h1=0
    def handle_starttag(self, tag, attrs):
        a=dict(attrs)
        if tag == 'a' and a.get('href'): self.links.append(a['href'])
        if tag == 'title': self.title=True
        if tag == 'meta' and a.get('name') == 'description' and a.get('content'): self.description=True
        if tag == 'h1': self.h1 += 1

def target_for(href: str) -> Path | None:
    if href.startswith(('mailto:', 'tel:', '#', 'https://', 'http://')): return None
    path = urlparse(href).path
    if not path.startswith('/'): return None
    rel = path.lstrip('/')
    if not rel: return DIST / 'index.html'
    candidate = DIST / rel
    if path.endswith('/'): candidate = candidate / 'index.html'
    return candidate

errors=[]
for page in sorted(DIST.rglob('*.html')):
    parser=Parser(); parser.feed(page.read_text(encoding='utf-8'))
    if not parser.title: errors.append(f'{page}: missing title')
    if not parser.description: errors.append(f'{page}: missing description')
    if parser.h1 != 1: errors.append(f'{page}: expected 1 h1, found {parser.h1}')
    for href in parser.links:
        target=target_for(href)
        if target and not target.exists(): errors.append(f'{page}: broken link {href} -> {target}')
    text=page.read_text(encoding='utf-8').lower()
    for forbidden in ('google-analytics.com','googletagmanager.com','facebook.net','doubleclick.net'):
        if forbidden in text: errors.append(f'{page}: tracker reference {forbidden}')
required=['index.html','work/index.html','appliances/index.html','pilot/index.html','patterns/index.html','discovery/index.html','method/index.html','field/index.html','about/index.html','privacy/index.html','robots.txt','sitemap.xml','site.webmanifest']
for rel in required:
    if not (DIST/rel).exists(): errors.append(f'missing {rel}')
if errors:
    print('\n'.join(errors), file=sys.stderr); raise SystemExit(1)
print(f'PASS: {len(list(DIST.rglob("*.html")))} HTML files validated')
print('PASS: internal links resolve')
print('PASS: one H1 and description per page')

layout=(ROOT/'src/layout.html').read_text(encoding='utf-8')
css=(ROOT/'src/assets/site.css').read_text(encoding='utf-8')
if 'document.documentElement.classList.add("has-js")' not in layout:
    errors.append('layout: missing progressive enhancement marker')
if '[data-reveal] { opacity: 1; transform: none; }' not in css:
    errors.append('css: content is not visible by default')
if errors:
    print('\n'.join(errors), file=sys.stderr); raise SystemExit(1)
print('PASS: no common advertising trackers')
print('PASS: content remains visible without JavaScript')

discovery = DIST / 'discovery'
discovery_html = (discovery / 'index.html').read_text(encoding='utf-8')
discovery_js = (discovery / 'discovery.js').read_text(encoding='utf-8')
corpus_js = (discovery / 'data/water-treatment-en-v1.js').read_text(encoding='utf-8')
corpus = json.loads(corpus_js.removeprefix('window.QW_DISCOVERY_SURVEY = ').removesuffix(';\n'))
question_ids = [
    question['id']
    for section in corpus['sections']
    for question in section['questions']
]
if len(corpus['sections']) != 30:
    errors.append(f'discovery: expected 30 sections, found {len(corpus["sections"])}')
if len(question_ids) != 333:
    errors.append(f'discovery: expected 333 questions, found {len(question_ids)}')
if len(set(question_ids)) != 333:
    errors.append('discovery: question IDs are not unique')
if len(corpus['quick_question_ids']) != 17 or len(set(corpus['quick_question_ids'])) != 17:
    errors.append('discovery: expected 17 unique Quick-path question IDs')
if not set(corpus['quick_question_ids']).issubset(question_ids):
    errors.append('discovery: quick path contains an unknown question ID')
for directive in ("connect-src 'none'", "form-action 'none'"):
    if directive not in discovery_html:
        errors.append(f'discovery: CSP missing {directive}')
if re.search(r'<form(?:\s|>)', discovery_html, re.IGNORECASE):
    errors.append('discovery: form element is prohibited')
prohibited_patterns = {
    'fetch': r'\bfetch\s*\(',
    'XMLHttpRequest': r'\bnew\s+XMLHttpRequest\b',
    'sendBeacon': r'\bsendBeacon\s*\(',
    'WebSocket': r'\bnew\s+WebSocket\b',
    'EventSource': r'\bnew\s+EventSource\b',
    'localStorage': r'\blocalStorage\s*[.\[]',
    'sessionStorage': r'\bsessionStorage\s*[.\[]',
    'IndexedDB': r'\bindexedDB\s*[.(\[]',
    'cookies': r'\bdocument\.cookie\s*=',
    'service worker': r'\bserviceWorker\s*\.',
}
for label, pattern in prohibited_patterns.items():
    if re.search(pattern, discovery_js):
        errors.append(f'discovery: prohibited {label} API use')
for relative in ('./discovery.css', './report.css', './data/water-treatment-en-v1.js', './discovery.js'):
    if relative not in discovery_html:
        errors.append(f'discovery: missing local asset reference {relative}')
if 'https://www.quietwire.ai/discovery/' not in (DIST / 'sitemap.xml').read_text(encoding='utf-8'):
    errors.append('discovery: missing sitemap URL')
if errors:
    print('\n'.join(errors), file=sys.stderr)
    raise SystemExit(1)
print('PASS: Discovery has 30 sections, 333 questions, and 333 unique IDs')
print('PASS: Discovery CSP and local-only API boundary validated')
