#!/usr/bin/env python3
"""Validate and render reusable QuietWire Library author spaces."""
from __future__ import annotations

import json
import re
from datetime import date
from html import escape
from pathlib import Path
from urllib.parse import urlsplit

SCHEMA_ID = "quietwire.authors-manifest.v1"
ID_PATTERN = re.compile(r"[a-z0-9]+(?:-[a-z0-9]+)*\Z")
ROOT_FIELDS = {"schema_id", "authors"}
AUTHOR_FIELDS = {
    "author_id", "name", "affiliation", "summary", "profile_url",
    "selected_work", "additional_publications",
}
WORK_FIELDS = {"kind", "title", "venue", "summary", "url"}
PUBLICATION_FIELDS = {"title", "venue", "published_on", "summary", "url"}


class AuthorsError(ValueError):
    pass


def _text(value: object, field: str, maximum: int) -> str:
    if not isinstance(value, str) or not value.strip() or value != value.strip():
        raise AuthorsError(f"{field} must be a non-empty trimmed string")
    if len(value) > maximum or any(ch in value for ch in "<>\x00"):
        raise AuthorsError(f"{field} is not safe plain text")
    return value


def _url(value: object, field: str, allow_relative: bool = True) -> str:
    url = _text(value, field, 2048)
    if allow_relative and url.startswith("/"):
        if url.startswith("//") or "?" in url or "#" in url:
            raise AuthorsError(f"{field} relative URL is not canonical")
        return url
    parts = urlsplit(url)
    if parts.scheme != "https" or not parts.hostname or parts.username or parts.password:
        raise AuthorsError(f"{field} must be an https public URL")
    if parts.query or parts.fragment:
        raise AuthorsError(f"{field} must not contain query or fragment")
    return url


def validate_manifest(document: object) -> list[dict]:
    if not isinstance(document, dict) or set(document) != ROOT_FIELDS:
        raise AuthorsError("author manifest root does not match contract")
    if document["schema_id"] != SCHEMA_ID:
        raise AuthorsError(f"schema_id must be {SCHEMA_ID!r}")
    raw_authors = document["authors"]
    if not isinstance(raw_authors, list) or not raw_authors:
        raise AuthorsError("authors must be a non-empty array")

    authors: list[dict] = []
    seen_ids: set[str] = set()
    seen_names: set[str] = set()
    for index, raw in enumerate(raw_authors):
        if not isinstance(raw, dict):
            raise AuthorsError(f"author {index} must be an object")
        unknown = set(raw) - AUTHOR_FIELDS
        required = {"author_id", "name", "affiliation", "summary", "profile_url", "selected_work"}
        missing = required - set(raw)
        if unknown or missing:
            raise AuthorsError(f"author {index} fields mismatch; unknown={sorted(unknown)}, missing={sorted(missing)}")
        author_id = _text(raw["author_id"], f"author {index} author_id", 80)
        if not ID_PATTERN.fullmatch(author_id) or author_id in seen_ids:
            raise AuthorsError(f"author {index} has invalid or duplicate author_id")
        name = _text(raw["name"], f"author {index} name", 120)
        if name.casefold() in seen_names:
            raise AuthorsError(f"author {index} has duplicate name")
        seen_ids.add(author_id); seen_names.add(name.casefold())

        selected_work = raw["selected_work"]
        if not isinstance(selected_work, list):
            raise AuthorsError(f"author {index} selected_work must be an array")
        validated_work = []
        for work_index, work in enumerate(selected_work):
            if not isinstance(work, dict) or set(work) != WORK_FIELDS:
                raise AuthorsError(f"author {index} selected_work {work_index} fields mismatch")
            validated_work.append({
                "kind": _text(work["kind"], "kind", 80),
                "title": _text(work["title"], "title", 240),
                "venue": _text(work["venue"], "venue", 160),
                "summary": _text(work["summary"], "summary", 500),
                "url": _url(work["url"], "url"),
            })

        additional = raw.get("additional_publications", [])
        if not isinstance(additional, list):
            raise AuthorsError(f"author {index} additional_publications must be an array")
        validated_additional = []
        for pub_index, pub in enumerate(additional):
            if not isinstance(pub, dict) or set(pub) != PUBLICATION_FIELDS:
                raise AuthorsError(f"author {index} additional_publications {pub_index} fields mismatch")
            published = _text(pub["published_on"], "published_on", 10)
            try:
                date.fromisoformat(published)
            except ValueError as exc:
                raise AuthorsError(f"author {index} additional publication date invalid") from exc
            validated_additional.append({
                "title": _text(pub["title"], "title", 240),
                "venue": _text(pub["venue"], "venue", 160),
                "published_on": published,
                "summary": _text(pub["summary"], "summary", 500),
                "url": _url(pub["url"], "url", allow_relative=False),
            })

        authors.append({
            "author_id": author_id,
            "name": name,
            "affiliation": _text(raw["affiliation"], f"author {index} affiliation", 160),
            "summary": _text(raw["summary"], f"author {index} summary", 700),
            "profile_url": _url(raw["profile_url"], f"author {index} profile_url", allow_relative=False),
            "selected_work": validated_work,
            "additional_publications": validated_additional,
        })
    return authors


def load_manifest(path: Path) -> list[dict]:
    try:
        return validate_manifest(json.loads(path.read_text(encoding="utf-8")))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        raise AuthorsError(f"cannot read author manifest {path}: {exc}") from exc


def _date_label(value: str) -> str:
    parsed = date.fromisoformat(value)
    return f"{parsed.day} {parsed.strftime('%B')} {parsed.year}"


def _publication_card(record: dict) -> str:
    return (
        f'<article class="library-card" data-author-publication-id="{escape(record["stable_id"])}">'
        f'<div class="publication-meta"><span>{escape(record["artifact_type"].title())}</span>'
        f'<time datetime="{record["published_on"]}">{_date_label(record["published_on"])}</time></div>'
        f'<h3>{escape(record["title"])}</h3>'
        f'<p>{escape(record["venue"])} · {escape(", ".join(record["authors"]))}</p>'
        f'<a class="text-link" href="{escape(record["canonical_url"], quote=True)}">Read at {escape(record["venue"])} '
        '<span aria-hidden="true">↗</span></a></article>'
    )


def _additional_card(record: dict) -> str:
    return (
        '<article class="library-card" data-author-additional-publication>'
        f'<div class="publication-meta"><span>Article</span><time datetime="{record["published_on"]}">{_date_label(record["published_on"])}</time></div>'
        f'<h3>{escape(record["title"])}</h3><p>{escape(record["venue"])}</p>'
        f'<p>{escape(record["summary"])}</p>'
        f'<a class="text-link" href="{escape(record["url"], quote=True)}">Read at {escape(record["venue"])} <span aria-hidden="true">↗</span></a>'
        '</article>'
    )


def _work_card(record: dict) -> str:
    arrow = "→" if record["url"].startswith("/") else "↗"
    return (
        '<article class="work-card" data-author-selected-work>'
        f'<span class="card-link">{escape(record["kind"])} · {escape(record["venue"])}</span>'
        f'<h3>{escape(record["title"])}</h3><p>{escape(record["summary"])}</p>'
        f'<a class="text-link" href="{escape(record["url"], quote=True)}">Explore <span aria-hidden="true">{arrow}</span></a>'
        '</article>'
    )


def author_publications(author: dict, publications: list[dict]) -> list[dict]:
    return [record for record in publications if author["name"] in record["authors"]]


def render_authors_landing(authors: list[dict], publications: list[dict]) -> str:
    cards = []
    for author in authors:
        count = (
            len(author_publications(author, publications))
            + len(author["additional_publications"])
            + len(author["selected_work"])
        )
        cards.append(
            f'<article class="library-card" data-author-id="{escape(author["author_id"])}">'
            f'<div class="publication-meta"><span>Author</span><span>{count} indexed public item{"s" if count != 1 else ""}</span></div>'
            f'<h2>{escape(author["name"])}</h2><p>{escape(author["affiliation"])}</p>'
            f'<p>{escape(author["summary"])}</p>'
            f'<a class="text-link" href="/library/authors/{escape(author["author_id"], quote=True)}/">Explore {escape(author["name"])} <span aria-hidden="true">→</span></a>'
            '</article>'
        )
    return (
        '<section class="page-hero compact-hero section-dark"><div class="shell page-hero-grid">'
        '<div data-reveal><p class="eyebrow"><span></span> QuietWire Library</p><h1>Authors</h1>'
        '<p class="hero-lede">Writing, conversations, field notes, and public work gathered by person without flattening their original venues.</p></div>'
        '<div class="hero-aside" data-reveal><p>Author spaces are durable collection pages. Publications stay linked to their canonical source; media and field work can sit beside them without being mislabeled as articles.</p></div>'
        '</div></section>'
        f'<section class="section section-cream"><div class="shell library-grid" data-reveal>{"".join(cards)}</div></section>'
    )


def render_author(author: dict, publications: list[dict]) -> str:
    writing = author_publications(author, publications)
    publication_cards = "".join(_publication_card(record) for record in writing)
    publication_cards += "".join(_additional_card(record) for record in author["additional_publications"])
    if not publication_cards:
        publication_cards = '<p>No publication records are indexed yet.</p>'
    work_cards = "".join(_work_card(record) for record in author["selected_work"])
    work_section = ""
    if work_cards:
        work_section = (
            '<section class="section section-dark"><div class="shell library-shelf" data-reveal>'
            '<div class="section-heading"><div><p class="section-kicker">Beyond the bibliography</p><h2>Selected public work</h2></div></div>'
            f'<div class="three-grid">{work_cards}</div></div></section>'
        )
    return (
        f'<section class="page-hero compact-hero section-dark" data-author-profile="{escape(author["author_id"])}"><div class="shell page-hero-grid">'
        f'<div data-reveal><p class="eyebrow"><span></span> QuietWire Author</p><h1>{escape(author["name"])}</h1>'
        f'<p class="hero-lede">{escape(author["summary"])}</p></div>'
        f'<div class="hero-aside" data-reveal><p>{escape(author["affiliation"])}</p>'
        f'<p><a class="text-link" href="{escape(author["profile_url"], quote=True)}">Public profile <span aria-hidden="true">↗</span></a></p>'
        '<p><a class="text-link" href="/library/authors/">All authors <span aria-hidden="true">→</span></a></p></div>'
        '</div></section>'
        '<section class="section section-cream"><div class="shell library-shelf" data-reveal>'
        '<div class="section-heading"><div><p class="section-kicker">Writing</p><h2>Publications</h2></div><a class="text-link" href="/publications/">All Publications →</a></div>'
        f'<div class="library-grid">{publication_cards}</div></div></section>'
        f'{work_section}'
    )
