#!/usr/bin/env python3
"""Render the visitor-facing Library packaging layer from validated records."""
from __future__ import annotations

from datetime import date
from html import escape


MAX_EDITION_SHELF = 3
MAX_PUBLICATION_SHELF = 3


def _date_label(value: str) -> str:
    parsed = date.fromisoformat(value)
    return f"{parsed.day} {parsed.strftime('%B')} {parsed.year}"


def _edition_card(record: dict) -> str:
    return (
        f'<article class="library-card" data-library-edition-id="{escape(record["edition_id"])}">'
        f'<div class="publication-meta"><span>QuietWire Edition</span>'
        f'<time datetime="{record["source_date"]}">{_date_label(record["source_date"])}</time></div>'
        f'<h3>{escape(record["title"])}</h3>'
        f'<p>{escape(record["summary"])}</p>'
        f'<a class="text-link" href="{escape(record["canonical_path"], quote=True)}">Read the Edition '
        '<span aria-hidden="true">→</span></a></article>'
    )


def _publication_card(record: dict) -> str:
    return (
        f'<article class="library-card" data-library-publication-id="{escape(record["stable_id"])}">'
        f'<div class="publication-meta"><span>{escape(record["artifact_type"].title())}</span>'
        f'<time datetime="{record["published_on"]}">{_date_label(record["published_on"])}</time></div>'
        f'<h3>{escape(record["title"])}</h3>'
        f'<p>{escape(record["venue"])} · {escape(", ".join(record["authors"]))}</p>'
        f'<a class="text-link" href="{escape(record["canonical_url"], quote=True)}">Read at {escape(record["venue"])} '
        '<span aria-hidden="true">↗</span></a></article>'
    )


def render_library(editions: list[dict], publications: list[dict]) -> str:
    """Render bounded shelves; inputs must already be validated and newest-first."""
    if not editions:
        raise ValueError("Library requires at least one validated Edition")
    featured = editions[0]
    edition_shelf = editions[1:1 + MAX_EDITION_SHELF]
    publication_shelf = publications[:MAX_PUBLICATION_SHELF]
    edition_cards = "".join(_edition_card(record) for record in edition_shelf)
    publication_cards = "".join(_publication_card(record) for record in publication_shelf)
    return (
        '<section class="page-hero compact-hero section-dark"><div class="shell page-hero-grid">'
        '<div data-reveal><p class="eyebrow"><span></span> QuietWire Library</p>'
        '<h1>Library</h1>'
        '<p class="hero-lede">A visitor-facing home for QuietWire writing, media, and first-party publishing.</p></div>'
        '<div class="hero-aside" data-reveal><p>Start with QuietWire Editions, our canonical first-party work, '
        'then explore confirmed writing and media held at its original public venues.</p></div>'
        '</div></section>'
        '<section class="section section-cream"><div class="shell library-feature" data-reveal>'
        '<p class="section-kicker">Featured Edition</p>'
        f'<article class="library-feature-card" data-library-featured-edition="{escape(featured["edition_id"])}">'
        f'<div><div class="publication-meta"><span>QuietWire Edition</span> · '
        f'<time datetime="{featured["source_date"]}">{_date_label(featured["source_date"])}</time></div>'
        f'<h2>{escape(featured["title"])}</h2><p>{escape(featured["summary"])}</p></div>'
        f'<a class="button" href="{escape(featured["canonical_path"], quote=True)}">Read the featured Edition</a>'
        '</article></div></section>'
        '<section class="section section-soft"><div class="shell library-shelf" data-reveal>'
        '<div class="section-heading"><div><p class="section-kicker">First-party originals</p>'
        '<h2>Recent Editions</h2></div><a class="text-link" href="/editions/">All Editions →</a></div>'
        f'<div class="library-grid">{edition_cards}</div></div></section>'
        '<section class="section section-cream"><div class="shell library-shelf" data-reveal>'
        '<div class="section-heading"><div><p class="section-kicker">Writing &amp; media</p>'
        '<h2>Recent Publications</h2></div><a class="text-link" href="/publications/">All Publications →</a></div>'
        f'<div class="library-grid">{publication_cards}</div></div></section>'
    )
