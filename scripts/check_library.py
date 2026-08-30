#!/usr/bin/env python3
"""Focused contract checks for the English-only Library packaging layer."""
from __future__ import annotations

import json
import re
from html.parser import HTMLParser
from pathlib import Path

from editions import load_manifest as load_editions_manifest
from publications import load_manifest as load_publications_manifest

ROOT = Path(__file__).resolve().parents[1]
DIST = ROOT / "dist"
config = json.loads((ROOT / "site.config.json").read_text(encoding="utf-8"))
edition_config = json.loads((ROOT / "data/editions-site.v1.json").read_text(encoding="utf-8"))
editions = load_editions_manifest(ROOT / edition_config["manifest"])
publications = load_publications_manifest(ROOT / config["publications_collection"]["manifest"])
output_path = DIST / "library/index.html"
errors: list[str] = []


class LibraryParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.h1 = 0
        self.featured: list[str] = []
        self.editions = 0
        self.publications = 0
        self.links: list[str] = []
        self.scripts: list[str] = []
        self.nav_depth = 0
        self.details_depth = 0
        self.nav_links: list[tuple[str, str]] = []
        self._anchor: tuple[str, list[str]] | None = None

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        attrs_dict = dict(attrs)
        if tag == "nav":
            self.nav_depth += 1
        if tag == "details":
            self.details_depth += 1
        if tag == "h1":
            self.h1 += 1
        if tag == "a" and attrs_dict.get("href"):
            self.links.append(attrs_dict["href"])
            if self.nav_depth == 1 and self.details_depth == 0:
                self._anchor = (attrs_dict["href"], [])
        if tag == "script" and attrs_dict.get("src"):
            self.scripts.append(attrs_dict["src"])
        if "data-library-featured-edition" in attrs_dict:
            self.featured.append(attrs_dict["data-library-featured-edition"] or "")
        if "data-library-edition-id" in attrs_dict:
            self.editions += 1
        if "data-library-publication-id" in attrs_dict:
            self.publications += 1

    def handle_data(self, data: str) -> None:
        if self._anchor is not None:
            self._anchor[1].append(data)

    def handle_endtag(self, tag: str) -> None:
        if tag == "a" and self._anchor is not None:
            href, text = self._anchor
            self.nav_links.append((href, "".join(text).strip()))
            self._anchor = None
        if tag == "details":
            self.details_depth -= 1
        if tag == "nav":
            self.nav_depth -= 1


if not output_path.is_file():
    errors.append("library: missing generated /library/ route")
else:
    text = output_path.read_text(encoding="utf-8")
    parser = LibraryParser()
    parser.feed(text)
    if parser.h1 != 1:
        errors.append(f"library: expected exactly one H1, found {parser.h1}")
    if parser.featured != [editions[0]["edition_id"]]:
        errors.append("library: featured Edition is not the newest validated Edition")
    if parser.editions != min(3, max(0, len(editions) - 1)):
        errors.append("library: Editions shelf is not bounded or does not match remaining validated records")
    if parser.publications != min(3, len(publications)):
        errors.append("library: Publications shelf is not bounded or does not match validated records")
    if "/editions/" not in parser.links or "/publications/" not in parser.links:
        errors.append("library: missing Editions or Publications collection link")
    if (parser.nav_links != [
        ("/work/", "Work"), ("/advisory/", "Advisory"),
        ("/library/", "Library"), ("/about/", "About"),
        ("mailto:hello@quietwire.ai?subject=QuietWire%20conversation", "Start a conversation"),
    ]):
        errors.append("library: primary navigation topology is not Work, Advisory, Library, About, CTA")
    if 'aria-current="page"' not in text[text.find('href="/library/"') - 30:text.find('href="/library/"') + 100]:
        errors.append("library: primary Library link is missing aria-current=page")
    if "QuietWire Edition</span> · <time" not in text:
        errors.append("library: featured Edition metadata is missing its explicit separator")
    if any(script.startswith("http://") or script.startswith("https://") for script in parser.scripts):
        errors.append("library: external script source introduced")
    if any(token in text for token in ("google-analytics.com", "googletagmanager.com", "facebook.net", "doubleclick.net")):
        errors.append("library: tracker reference introduced")

sitemap = (DIST / "sitemap.xml").read_text(encoding="utf-8")
if "https://www.quietwire.ai/library/" not in sitemap:
    errors.append("library: sitemap is missing /library/")
for prefix in ("ar", "es", "fr"):
    if (DIST / prefix / "library").exists() or f"/{prefix}/library/" in sitemap:
        errors.append(f"library: localized route was generated for {prefix}")

for prefix in ("ar", "es", "fr"):
    for page in sorted((DIST / prefix).rglob("*.html")):
        text = page.read_text(encoding="utf-8")
        if re.search(r'<a href="/library/">Library</a>', text):
            errors.append(f"library: English footer label injected into {page}")

english_pages = sorted(path for path in DIST.rglob("*.html") if not any(part in {"ar", "es", "fr", "discovery"} for part in path.relative_to(DIST).parts))
expected_english_nav = [("/work/", "Work"), ("/advisory/", "Advisory"), ("/library/", "Library"), ("/about/", "About"), ("mailto:hello@quietwire.ai?subject=QuietWire%20conversation", "Start a conversation")]
for page in english_pages:
    text = page.read_text(encoding="utf-8")
    parser = LibraryParser(); parser.feed(text)
    if parser.nav_links != expected_english_nav:
        errors.append(f"library: English primary nav mismatch in {page}")
for prefix, shell_path in (("ar", "src/i18n/ar.json"), ("es", "src/i18n/es.json"), ("fr", "src/i18n/fr-CA.json")):
    shell = json.loads((ROOT / shell_path).read_text(encoding="utf-8"))
    expected_localized_nav = [("/" + prefix + "/work/", shell["navigation"]["labels"]["work"]), ("/" + prefix + "/advisory/", shell["navigation"]["labels"]["advisory"]), ("/" + prefix + "/about/", shell["navigation"]["labels"]["about"]), ("mailto:hello@quietwire.ai?subject=" + shell["navigation"]["cta_subject"], shell["navigation"]["cta"])]
    for page in sorted((DIST / prefix).rglob("*.html")):
        parser = LibraryParser(); parser.feed(page.read_text(encoding="utf-8"))
        if parser.nav_links != expected_localized_nav:
            errors.append(f"library: localized primary nav mismatch in {page}")

for route in ("appliances", "pilot", "patterns"):
    if not (DIST / route / "index.html").is_file():
        errors.append(f"library: durable route missing /{route}/")
work_text = (DIST / "work/index.html").read_text(encoding="utf-8")
for route in ("appliances", "pilot", "patterns"):
    if f'href="/{route}/"' not in work_text:
        errors.append(f"library: Work page no longer links to /{route}/")
if '<a href="/library/">Library</a>' not in (DIST / "index.html").read_text(encoding="utf-8"):
    errors.append("library: English footer Library link is missing")

layout = (ROOT / "src/layout.html").read_text(encoding="utf-8")
library_source = (ROOT / "scripts/library.py").read_text(encoding="utf-8")
if "{{library_link}}" not in layout or 'locale["id"] == CONFIG["default_locale"]' not in (ROOT / "scripts/build.py").read_text(encoding="utf-8"):
    errors.append("library: footer link is not explicitly gated to the default locale")
if re.search(r"\b(fetch|XMLHttpRequest|WebSocket|EventSource)\b|requests\.|urllib\.request|BeautifulSoup", library_source):
    errors.append("library: runtime API or scraping dependency introduced")

if errors:
    raise SystemExit("\n".join(errors))
print("PASS: Library route, single H1, validated featured Edition, and bounded shelves")
print("PASS: Library collection links, sitemap route, and no localized Library outputs")
print("PASS: English-only footer discovery and local-only, tracker-free Library boundary")
