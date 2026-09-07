#!/usr/bin/env python3
from __future__ import annotations

import json
from datetime import datetime, timezone
from html import escape
from pathlib import Path

from authors import load_manifest as load_authors_manifest, render_author, render_authors_landing
from build import CONFIG, DIST, ROOT, canonical_url, locales, render_document, single_locale_language_data
from publications import load_manifest as load_publications_manifest

AUTHORS_MANIFEST = ROOT / "data" / "authors.v1.json"
AUTHORS_OUTPUT = Path("library/authors/index.html")
AUTHORS_MARKER = "<!-- quietwire-authors-shelf -->"


def _library_shelf(authors: list[dict]) -> str:
    cards = []
    for author in authors:
        cards.append(
            f'<article class="library-card" data-library-author-id="{escape(author["author_id"])}">'
            '<div class="publication-meta"><span>Author</span></div>'
            f'<h3>{escape(author["name"])}</h3><p>{escape(author["affiliation"])}</p>'
            f'<p>{escape(author["summary"])}</p>'
            f'<a class="text-link" href="/library/authors/{escape(author["author_id"], quote=True)}/">Explore author <span aria-hidden="true">→</span></a>'
            '</article>'
        )
    return (
        '<section class="section section-soft" data-library-authors-shelf><div class="shell library-shelf" data-reveal>'
        '<div class="section-heading"><div><p class="section-kicker">People &amp; perspectives</p><h2>Authors</h2></div>'
        '<a class="text-link" href="/library/authors/">All authors →</a></div>'
        f'<div class="library-grid">{"".join(cards)}</div></div></section>'
    )


def build_authors() -> None:
    authors = load_authors_manifest(AUTHORS_MANIFEST)
    publications = load_publications_manifest(ROOT / CONFIG["publications_collection"]["manifest"])
    locale = next(item for item in locales() if item["id"] == CONFIG["default_locale"])
    shell = json.loads((ROOT / locale["shell"]).read_text(encoding="utf-8"))
    layout = (ROOT / "src" / "layout.html").read_text(encoding="utf-8")
    year = str(datetime.now(timezone.utc).year)

    landing_page = {
        "output": str(AUTHORS_OUTPUT),
        "key": "authors",
        "title": "Authors — QuietWire Library",
        "description": "Author spaces for QuietWire writing, conversations, field notes, and public work.",
    }
    landing_output = DIST / AUTHORS_OUTPUT
    landing_output.parent.mkdir(parents=True, exist_ok=True)
    landing_html = render_document(
        layout, landing_page, locale, shell,
        render_authors_landing(authors, publications), year,
        single_locale_language_data(landing_page, locale),
    )
    landing_output.write_text(landing_html.rstrip() + "\n", encoding="utf-8")

    author_urls = [canonical_url(landing_page, locale)]
    for author in authors:
        relative = Path("library/authors") / author["author_id"] / "index.html"
        page = {
            "output": str(relative),
            "key": "author",
            "title": f'{author["name"]} — QuietWire Library',
            "description": author["summary"],
        }
        output = DIST / relative
        output.parent.mkdir(parents=True, exist_ok=True)
        html = render_document(
            layout, page, locale, shell,
            render_author(author, publications), year,
            single_locale_language_data(page, locale),
        )
        output.write_text(html.rstrip() + "\n", encoding="utf-8")
        author_urls.append(canonical_url(page, locale))

    library_path = DIST / "library" / "index.html"
    library_html = library_path.read_text(encoding="utf-8")
    if AUTHORS_MARKER not in library_html:
        raise ValueError("Library is missing the author shelf marker")
    library_path.write_text(library_html.replace(AUTHORS_MARKER, _library_shelf(authors), 1), encoding="utf-8")

    sitemap_path = DIST / "sitemap.xml"
    sitemap = sitemap_path.read_text(encoding="utf-8")
    insertion = "\n".join(f"  <url><loc>{escape(url)}</loc></url>" for url in author_urls)
    if insertion and author_urls[0] not in sitemap:
        sitemap = sitemap.replace("\n</urlset>\n", f"\n{insertion}\n</urlset>\n")
        sitemap_path.write_text(sitemap, encoding="utf-8")


if __name__ == "__main__":
    build_authors()
    print("Built QuietWire Library author spaces")
