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
        self.lang=None; self.direction=None; self.alternates=[]; self.x_default=False; self.language_links=[]; self.canonical=None
    def handle_starttag(self, tag, attrs):
        a=dict(attrs)
        if tag == 'a' and a.get('href'): self.links.append(a['href'])
        if tag == 'a' and a.get('hreflang'): self.language_links.append((a['hreflang'], a['href']))
        if tag == 'html': self.lang, self.direction = a.get('lang'), a.get('dir')
        if tag == 'link' and a.get('rel') == 'canonical': self.canonical = a.get('href')
        if tag == 'link' and a.get('rel') == 'alternate' and a.get('hreflang'):
            self.alternates.append((a['hreflang'], a.get('href')))
            self.x_default = self.x_default or a['hreflang'] == 'x-default'
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
config = json.loads((ROOT / 'site.config.json').read_text(encoding='utf-8'))
locales = {locale['id']: locale for locale in config['locales']}
required=['robots.txt','sitemap.xml','site.webmanifest']
required += [
    str(Path(locale['url_prefix']) / page['output']) if locale['url_prefix'] else page['output']
    for locale in locales.values()
    for page in locale['pages']
]
required += [app['output'].rstrip('/') + '/index.html' for app in config.get('static_apps', [])]
for rel in required:
    if not (DIST/rel).exists(): errors.append(f'missing {rel}')
if errors:
    print('\n'.join(errors), file=sys.stderr); raise SystemExit(1)
print(f'PASS: {len(list(DIST.rglob("*.html")))} HTML files validated')
print('PASS: internal links resolve')
print('PASS: one H1 and description per page')

default_locale = locales.get(config['default_locale'])
if default_locale is None:
    errors.append(f"locale: configured default {config['default_locale']!r} is not enabled")
for locale_id, locale in locales.items():
    for page in locale['pages']:
        rel = Path(locale['url_prefix']) / page['output'] if locale['url_prefix'] else Path(page['output'])
        path = DIST / rel
        parser = Parser(); parser.feed(path.read_text(encoding='utf-8'))
        expected_lang, expected_dir = locale_id, locale['direction']
        if (parser.lang, parser.direction) != (expected_lang, expected_dir):
            errors.append(f'{path}: expected lang={expected_lang} dir={expected_dir}')
        routes = {other_id: next(p for p in other['pages'] if p['key'] == page['key']) for other_id, other in locales.items()}
        expected_alternates = {other_id for other_id in locales} | {'x-default'}
        if {item[0] for item in parser.alternates} != expected_alternates:
            errors.append(f'{path}: missing reciprocal hreflang or x-default')
        if not parser.x_default:
            errors.append(f'{path}: missing x-default')
        if len(parser.language_links) != len(locales):
            errors.append(f'{path}: language selector must contain one ordinary link per locale')
        expected_paths = {other_id: (('/' + other['url_prefix'].strip('/') if other['url_prefix'].strip('/') else '') + ('/' if routes[other_id]['output'] == 'index.html' else '/' + routes[other_id]['output'].removesuffix('index.html'))) for other_id, other in locales.items()}
        expected_links = {other_id: config['base_url'] + path for other_id, path in expected_paths.items()}
        if parser.canonical != expected_links[locale_id] or not parser.canonical.startswith(('http://', 'https://')):
            errors.append(f'{path}: locale-incorrect canonical URL')
        for other_id, href in expected_links.items():
            if (other_id, expected_paths[other_id]) not in parser.language_links:
                errors.append(f'{path}: language link for {other_id} must be root-relative {expected_paths[other_id]}')
            if (other_id, href) not in parser.alternates:
                errors.append(f'{path}: hreflang for {other_id} does not point to {href}')
        if default_locale is not None and ('x-default', expected_links[config['default_locale']]) not in parser.alternates:
            errors.append(f'{path}: x-default does not point to English route')
sitemap_text = (DIST / 'sitemap.xml').read_text(encoding='utf-8')
for locale_id, locale in locales.items():
    if locale_id == config['default_locale']:
        continue
    prefix = locale['url_prefix'].strip('/')
    if not prefix:
        errors.append(f'locale {locale_id}: non-default locale must have a URL prefix')
        continue
    prohibited_discovery = f'/{prefix}/discovery/'
    if (DIST / prefix / 'discovery').exists():
        errors.append(f'locale {locale_id}: accidental {prohibited_discovery} output')
    if prohibited_discovery in sitemap_text:
        errors.append(f'locale {locale_id}: sitemap contains accidental {prohibited_discovery}')
    for page in sorted((ROOT / locale['content_dir'] / 'pages').glob('*.html')):
        source = page.read_text(encoding='utf-8')
        if '{{' in source or '}}' in source:
            errors.append(f'{page}: untranslated template placeholder marker')
    manifest_path = ROOT / 'docs/i18n' / f'{locale_id}-translation-manifest.json'
    if not manifest_path.is_file():
        errors.append(f'locale {locale_id}: missing translation manifest {manifest_path}')
        continue
    manifest = json.loads(manifest_path.read_text(encoding='utf-8'))
    expected_routes = [
        ('/' + prefix + '/') if page['output'] == 'index.html'
        else '/' + prefix + '/' + page['output'].removesuffix('index.html')
        for page in locale['pages']
    ]
    if manifest.get('locale') != locale_id:
        errors.append(f'locale {locale_id}: manifest locale mismatch')
    if manifest.get('source_locale') != config['default_locale']:
        errors.append(f'locale {locale_id}: manifest source_locale mismatch')
    if not manifest.get('source_commit'):
        errors.append(f'locale {locale_id}: manifest source_commit is required')
    if manifest.get('routes') != expected_routes:
        errors.append(f'locale {locale_id}: manifest routes do not match configured routes')
    if not manifest.get('glossary_version'):
        errors.append(f'locale {locale_id}: manifest glossary_version is required')
    if not isinstance(manifest.get('human_reviewed'), bool):
        errors.append(f'locale {locale_id}: manifest human_reviewed must be boolean')
    review_status = manifest.get('review_status')
    reviewed_routes = manifest.get('reviewed_routes', [])
    if review_status == 'partial_human_review':
        if manifest.get('human_reviewed') is not False:
            errors.append(f'locale {locale_id}: partial review cannot mark the full locale human reviewed')
        if not reviewed_routes or not set(reviewed_routes).issubset(expected_routes):
            errors.append(f'locale {locale_id}: partial review routes must be a non-empty subset')
        if set(reviewed_routes) == set(expected_routes):
            errors.append(f'locale {locale_id}: partial review cannot cover every route')
        if not manifest.get('reviewers'):
            errors.append(f'locale {locale_id}: partial review must name its reviewers')
if errors:
    print('\n'.join(errors), file=sys.stderr); raise SystemExit(1)
print('PASS: locale output language attributes, reciprocal hreflang, x-default, and route links')
print('PASS: non-default locale manifests, review scope, and Discovery exclusions validated')

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
