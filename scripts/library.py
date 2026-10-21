#!/usr/bin/env python3
"""Render the visitor-facing Library packaging layer from validated records."""
from __future__ import annotations

from datetime import date
from html import escape


MAX_EDITION_SHELF = 3
MAX_PUBLICATION_SHELF = 3
AUTHORS_SHELF_MARKER = "<!-- quietwire-authors-shelf -->"
MEDIA_SHELF_MARKER = "<!-- quietwire-media-shelf -->"


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
    collaborative_article = next((record for record in publications if record["title"] == "Narrative Integrity Risk: The Next Frontier in Financial Stability"), None)
    if collaborative_article is None:
        raise ValueError("Library requires the verified collaborative Lawfare article")
    collaborative_card = _publication_card(collaborative_article).replace("data-library-publication-id", "data-library-collaboration-id", 1)
    return (
        '<section class="page-hero compact-hero section-dark"><div class="shell page-hero-grid">'
        '<div data-reveal><p class="eyebrow"><span></span> QuietWire Library</p>'
        '<h1>Library</h1>'
        '<p class="hero-lede">Ideas, research, and perspectives from people exploring how AI, cybersecurity, and governance affect the organizations and communities around us.</p></div>'
        '<div class="hero-aside" data-reveal><p>Explore original thinking, shared research, and public conversations from '
        'the people behind and around QuietWire.</p></div>'
        '</div></section>'
        '<section class="section section-mist companion-demo" id="companion-example" data-companion-demo>'
        '<div class="shell companion-demo-grid">'
        '<div class="companion-demo-copy"><p class="section-kicker">An interactive example</p><h2>What should the next person know?</h2>'
        '<p class="large-copy">See how a companion could help make sense of a project handoff: what the records support, what is still uncertain, and what needs a human decision.</p>'
        '<p>This is a guided illustration using fictional information, <strong>not a live AI system</strong>. It runs entirely in your browser and sends no information to QuietWire.</p></div>'
        '<div class="companion-demo-panel"><p class="demo-small">Fictional scenario · Harbour Community Services</p>'
        '<p>A project lead is leaving during a proposed expansion of an AI-assisted help desk. What can their successor safely rely on?</p>'
        '<div class="companion-demo-choices" role="group" aria-label="Choose a question about the fictional project">'
        '<button type="button" data-demo-choice="handoff">What do the records tell us?</button>'
        '<button type="button" data-demo-choice="challenge">Someone says expansion is approved</button>'
        '<button type="button" data-demo-choice="next">What should happen next?</button></div>'
        '<div class="companion-demo-response" data-demo-response aria-live="polite"><p class="demo-placeholder">Choose a question to explore the fictional record.</p></div>'
        '<p class="demo-small demo-end">No login, data collection, or model connection. A live companion demonstration would require separate technical review.</p>'
        '</div></div></section>'
        '<script src="/assets/companion-demo.js" defer></script>'
        '<section class="section section-cream"><div class="shell library-shelf" data-reveal>'
        '<div class="section-heading"><div><p class="section-kicker">Writing &amp; media</p>'
        '<h2>Recent Publications</h2></div><a class="text-link" href="/publications/">All Publications →</a></div>'
        f'<div class="library-grid">{publication_cards}</div></div></section>'
        '<section class="section section-cream library-collaborative"><div class="shell library-shelf" data-reveal>'
        '<div class="section-heading"><div><p class="section-kicker">Featured collaborative writing</p><h2>Different perspectives, one question.</h2>'
        '<p>Chris Beall, Chris Blask, and Jen Rosiere Reynolds examine how narrative manipulation can create financial risk.</p></div></div>'
        f'<div class="library-grid library-featured-writing">{collaborative_card}</div></div></section>'
        f'{AUTHORS_SHELF_MARKER}'
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
        f'{MEDIA_SHELF_MARKER}'
    )
