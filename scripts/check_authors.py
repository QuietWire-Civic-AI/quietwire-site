#!/usr/bin/env python3
from __future__ import annotations

from html import escape
from pathlib import Path

from authors import author_publications, load_manifest as load_authors_manifest
from publications import load_manifest as load_publications_manifest

ROOT = Path(__file__).resolve().parents[1]
DIST = ROOT / "dist"
AUTHORS = load_authors_manifest(ROOT / "data" / "authors.v1.json")
PUBLICATIONS = load_publications_manifest(ROOT / "data" / "publications.dev.v1.json")

errors: list[str] = []
landing = DIST / "library" / "authors" / "index.html"
if not landing.is_file():
    errors.append("authors: missing landing page")
else:
    landing_text = landing.read_text(encoding="utf-8")
    for author in AUTHORS:
        if f'data-author-id="{author["author_id"]}"' not in landing_text:
            errors.append(f'authors: landing missing {author["author_id"]}')
        if f'/library/authors/{author["author_id"]}/' not in landing_text:
            errors.append(f'authors: landing missing link for {author["author_id"]}')

for author in AUTHORS:
    page = DIST / "library" / "authors" / author["author_id"] / "index.html"
    if not page.is_file():
        errors.append(f'authors: missing page for {author["author_id"]}')
        continue
    text = page.read_text(encoding="utf-8")
    if f'data-author-profile="{author["author_id"]}"' not in text:
        errors.append(f'authors: wrong profile marker for {author["author_id"]}')
    if author["profile_url"] not in text:
        errors.append(f'authors: profile URL missing for {author["author_id"]}')
    for publication in author_publications(author, PUBLICATIONS):
        if f'data-author-publication-id="{publication["stable_id"]}"' not in text:
            errors.append(f'authors: {author["author_id"]} missing publication {publication["stable_id"]}')
    for selected in author["selected_work"]:
        if selected["url"] not in text or escape(selected["title"]) not in text:
            errors.append(f'authors: {author["author_id"]} missing selected work {selected["title"]}')
    for additional in author["additional_publications"]:
        if additional["url"] not in text or escape(additional["title"]) not in text:
            errors.append(f'authors: {author["author_id"]} missing additional publication {additional["title"]}')

library = (DIST / "library" / "index.html").read_text(encoding="utf-8")
if 'data-library-authors-shelf' not in library:
    errors.append("authors: Library author shelf missing")
for author in AUTHORS:
    if f'data-library-author-id="{author["author_id"]}"' not in library:
        errors.append(f'authors: Library shelf missing {author["author_id"]}')

sitemap = (DIST / "sitemap.xml").read_text(encoding="utf-8")
for suffix in ["/library/authors/"] + [f'/library/authors/{author["author_id"]}/' for author in AUTHORS]:
    if f'https://www.quietwire.ai{suffix}' not in sitemap:
        errors.append(f'authors: sitemap missing {suffix}')

if errors:
    raise SystemExit("\n".join(errors))
print(f"PASS: {len(AUTHORS)} author spaces validated")
print("PASS: author publications, selected work, Library shelf, and sitemap links validated")
