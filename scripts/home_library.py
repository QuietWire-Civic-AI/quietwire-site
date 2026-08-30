#!/usr/bin/env python3
"""Render the explicitly curated English homepage shelf from validated records."""
from __future__ import annotations

from datetime import date
from html import escape


EXPECTED_ITEM_COUNT = 3
VALID_KINDS = {"edition", "publication"}


def _date_label(value: str) -> str:
    parsed = date.fromisoformat(value)
    return f"{parsed.day} {parsed.strftime('%B')} {parsed.year}"


def resolve_home_library(
    config: dict, editions: list[dict], publications: list[dict]
) -> list[tuple[str, dict]]:
    """Resolve explicit selections against already-validated public records."""
    if not isinstance(config, dict) or set(config) != {"items"}:
        raise ValueError("home_library must contain only an items array")
    items = config["items"]
    if not isinstance(items, list) or len(items) != EXPECTED_ITEM_COUNT:
        raise ValueError(f"home_library.items must contain exactly {EXPECTED_ITEM_COUNT} items")

    edition_by_id = {record["edition_id"]: record for record in editions}
    publication_by_id = {record["stable_id"]: record for record in publications}
    seen_ids: set[str] = set()
    resolved: list[tuple[str, dict]] = []
    for index, item in enumerate(items):
        if not isinstance(item, dict) or set(item) != {"kind", "id"}:
            raise ValueError(f"home_library item {index} must contain only kind and id")
        kind, record_id = item["kind"], item["id"]
        if kind not in VALID_KINDS or not isinstance(record_id, str) or not record_id:
            raise ValueError(f"home_library item {index} has malformed kind or id")
        if record_id in seen_ids:
            raise ValueError(f"home_library item {index} duplicates id {record_id!r}")
        seen_ids.add(record_id)
        records = edition_by_id if kind == "edition" else publication_by_id
        if record_id not in records:
            raise ValueError(f"home_library item {index} does not resolve as a {kind}: {record_id!r}")
        resolved.append((kind, records[record_id]))
    return resolved


def _card(kind: str, record: dict) -> str:
    if kind == "edition":
        record_id = record["edition_id"]
        metadata = f'<span>QuietWire Edition</span> · <time datetime="{record["source_date"]}">{_date_label(record["source_date"])}</time>'
        destination = record["canonical_path"]
        link_text = "Read the Edition"
    else:
        record_id = record["stable_id"]
        metadata = f'<span>{escape(record["venue"])}</span> · <time datetime="{record["published_on"]}">{_date_label(record["published_on"])}</time>'
        destination = record["canonical_url"]
        link_text = f'Read at {escape(record["venue"])}'
    return (
        f'<article class="home-library-card" data-home-library-kind="{kind}" data-home-library-id="{escape(record_id)}">'
        f'<div class="publication-meta">{metadata}</div>'
        f'<h3>{escape(record["title"])}</h3>'
        f'<p>{escape(record.get("summary", ""))}</p>'
        f'<a class="text-link" href="{escape(destination, quote=True)}">{link_text} <span aria-hidden="true">→</span></a>'
        '</article>'
    )


def render_home_library(config: dict, editions: list[dict], publications: list[dict]) -> str:
    selected = resolve_home_library(config, editions, publications)
    cards = "".join(_card(kind, record) for kind, record in selected)
    return (
        '<section class="section home-library-preview" data-home-library-shelf>'
        '<div class="shell section-heading" data-reveal><div>'
        '<p class="section-kicker">From QuietWire</p>'
        '<h2>Writing, field notes, appearances, and ideas we are working through in public.</h2>'
        '</div><a class="text-link" href="/library/">Explore the Library <span>→</span></a></div>'
        f'<div class="shell home-library-grid" data-reveal>{cards}</div>'
        '</section>'
    )
