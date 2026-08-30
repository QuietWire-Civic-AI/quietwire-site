#!/usr/bin/env python3
"""Validate and render the public-safe QuietWire Editions export."""
from __future__ import annotations

import copy
import json
import re
import unicodedata
from datetime import date
from html import escape
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit

SCHEMA_ID = "quietwire.editions-manifest.v1"
ROOT_FIELDS = {"schema_id", "editions"}
RECORD_FIELDS = {
    "edition_id",
    "release_state",
    "website_visibility",
    "title",
    "slug",
    "authors",
    "source_date",
    "artifact_type",
    "summary",
    "canonical_path",
    "body_file",
}
ARTIFACT_TYPES = {
    "article": "Article",
    "essay": "Essay",
    "report": "Report",
    "transcript": "Transcript",
    "audio": "Audio",
    "video": "Video",
}
ID_PATTERN = re.compile(r"[a-z0-9]+(?:-[a-z0-9]+)*\Z")
ALLOWED_TAGS = {"p", "h2", "h3", "ul", "ol", "li", "blockquote", "strong", "em", "a", "hr"}
VOID_TAGS = {"hr"}


class EditionsError(ValueError):
    """The Editions export is not safe to publish."""


def _record_error(index: int, message: str) -> EditionsError:
    return EditionsError(f"edition record {index}: {message}")


def _plain_text(value: object, field: str, index: int, maximum: int) -> str:
    if not isinstance(value, str) or not value:
        raise _record_error(index, f"{field} must be a non-empty string")
    if value != value.strip():
        raise _record_error(index, f"{field} must not have leading or trailing whitespace")
    if value != unicodedata.normalize("NFC", value):
        raise _record_error(index, f"{field} must use NFC Unicode normalization")
    if len(value) > maximum:
        raise _record_error(index, f"{field} exceeds {maximum} characters")
    if any(unicodedata.category(character) == "Cc" for character in value):
        raise _record_error(index, f"{field} contains a control character")
    if "<" in value or ">" in value:
        raise _record_error(index, f"{field} must be plain text, not markup")
    return value


class _SafeFragmentParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.stack: list[str] = []
        self.seen_content = False

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag not in ALLOWED_TAGS:
            raise EditionsError(f"body HTML uses prohibited tag <{tag}>")
        if tag == "a":
            if len(attrs) != 1 or attrs[0][0] != "href" or not attrs[0][1]:
                raise EditionsError("body HTML links may contain only one href attribute")
            href = attrs[0][1]
            if href.startswith("/"):
                if href.startswith("//"):
                    raise EditionsError("body HTML links must not use protocol-relative URLs")
            else:
                parts = urlsplit(href)
                if parts.scheme != "https" or not parts.netloc or parts.username or parts.password:
                    raise EditionsError("body HTML links must be root-relative or public https URLs")
        elif attrs:
            raise EditionsError(f"body HTML tag <{tag}> must not contain attributes")
        if tag not in VOID_TAGS:
            self.stack.append(tag)

    def handle_startendtag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag not in VOID_TAGS or attrs:
            raise EditionsError(f"unsupported self-closing body HTML tag <{tag}/>")

    def handle_endtag(self, tag: str) -> None:
        if tag in VOID_TAGS:
            raise EditionsError(f"void tag <{tag}> must not have a closing tag")
        if not self.stack or self.stack[-1] != tag:
            raise EditionsError(f"body HTML has mismatched closing tag </{tag}>")
        self.stack.pop()

    def handle_data(self, data: str) -> None:
        if data.strip():
            self.seen_content = True

    def handle_comment(self, data: str) -> None:
        raise EditionsError("body HTML comments are not allowed")

    def handle_decl(self, decl: str) -> None:
        raise EditionsError("body HTML declarations are not allowed")

    def unknown_decl(self, data: str) -> None:
        raise EditionsError("body HTML declarations are not allowed")

    def close(self) -> None:
        super().close()
        if self.stack:
            raise EditionsError(f"body HTML has unclosed tag <{self.stack[-1]}>")
        if not self.seen_content:
            raise EditionsError("body HTML must contain visible text")


def validate_body_html(body: object) -> str:
    if not isinstance(body, str) or not body.strip():
        raise EditionsError("body HTML must be a non-empty string")
    lowered = body.lower()
    for sentinel in ("<script", "javascript:", "onerror=", "onclick=", "<style"):
        if sentinel in lowered:
            raise EditionsError(f"body HTML contains prohibited executable markup: {sentinel}")
    parser = _SafeFragmentParser()
    parser.feed(body)
    parser.close()
    return body


def validate_manifest(document: object) -> list[dict]:
    if not isinstance(document, dict):
        raise EditionsError("manifest root must be an object")
    fields = set(document)
    if fields != ROOT_FIELDS:
        unknown = sorted(fields - ROOT_FIELDS)
        missing = sorted(ROOT_FIELDS - fields)
        raise EditionsError(f"manifest fields do not match contract; unknown={unknown}, missing={missing}")
    if document["schema_id"] != SCHEMA_ID:
        raise EditionsError(f"schema_id must be {SCHEMA_ID!r}")
    records = document["editions"]
    if not isinstance(records, list) or not records:
        raise EditionsError("editions must be a non-empty array")

    validated: list[dict] = []
    seen_ids: set[str] = set()
    seen_slugs: set[str] = set()
    seen_paths: set[str] = set()
    for index, raw in enumerate(records):
        if not isinstance(raw, dict):
            raise _record_error(index, "must be an object")
        fields = set(raw)
        unknown = sorted(fields - RECORD_FIELDS)
        missing = sorted(RECORD_FIELDS - fields)
        if unknown or missing:
            raise _record_error(index, f"fields do not match contract; unknown={unknown}, missing={missing}")

        edition_id = _plain_text(raw["edition_id"], "edition_id", index, 96)
        slug = _plain_text(raw["slug"], "slug", index, 96)
        if not ID_PATTERN.fullmatch(edition_id) or not ID_PATTERN.fullmatch(slug):
            raise _record_error(index, "edition_id and slug must be lowercase kebab-case ASCII")
        if edition_id in seen_ids or slug in seen_slugs:
            raise _record_error(index, "duplicate edition_id or slug")
        seen_ids.add(edition_id)
        seen_slugs.add(slug)

        if raw["release_state"] != "approved":
            raise _record_error(index, "release_state must be 'approved'")
        if raw["website_visibility"] != "listed":
            raise _record_error(index, "website_visibility must be 'listed'")

        title = _plain_text(raw["title"], "title", index, 240)
        summary = _plain_text(raw["summary"], "summary", index, 500)

        authors = raw["authors"]
        if not isinstance(authors, list) or not 1 <= len(authors) <= 8:
            raise _record_error(index, "authors must contain between 1 and 8 names")
        authors = [
            _plain_text(author, f"authors[{author_index}]", index, 120)
            for author_index, author in enumerate(authors)
        ]
        if len({author.casefold() for author in authors}) != len(authors):
            raise _record_error(index, "authors must not contain duplicate names")

        source_date_text = _plain_text(raw["source_date"], "source_date", index, 10)
        try:
            source_date = date.fromisoformat(source_date_text)
        except ValueError as exc:
            raise _record_error(index, "source_date must be a real ISO 8601 date (YYYY-MM-DD)") from exc
        if source_date.isoformat() != source_date_text:
            raise _record_error(index, "source_date must use YYYY-MM-DD")

        artifact_type = raw["artifact_type"]
        if not isinstance(artifact_type, str) or artifact_type not in ARTIFACT_TYPES:
            raise _record_error(index, f"artifact_type must be one of {sorted(ARTIFACT_TYPES)}")

        canonical_path = _plain_text(raw["canonical_path"], "canonical_path", index, 160)
        expected_path = f"/editions/{slug}/"
        if canonical_path != expected_path:
            raise _record_error(index, f"canonical_path must be {expected_path!r}")
        if canonical_path in seen_paths:
            raise _record_error(index, "duplicate canonical_path")
        seen_paths.add(canonical_path)

        body_file = _plain_text(raw["body_file"], "body_file", index, 220)
        expected_body_file = f"exports/editions/{slug}.html"
        if body_file != expected_body_file:
            raise _record_error(index, f"body_file must be {expected_body_file!r}")

        validated.append({
            "edition_id": edition_id,
            "release_state": "approved",
            "website_visibility": "listed",
            "title": title,
            "slug": slug,
            "authors": authors,
            "source_date": source_date_text,
            "artifact_type": artifact_type,
            "summary": summary,
            "canonical_path": canonical_path,
            "body_file": body_file,
        })

    return sorted(validated, key=lambda item: (item["source_date"], item["edition_id"]), reverse=True)


def load_manifest(path: Path) -> list[dict]:
    try:
        document = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        raise EditionsError(f"cannot read Editions manifest {path}: {exc}") from exc
    records = validate_manifest(document)
    root = path.resolve().parents[1]
    hydrated: list[dict] = []
    for record in records:
        body_path = root / record["body_file"]
        try:
            body = body_path.read_text(encoding="utf-8")
        except (OSError, UnicodeError) as exc:
            raise EditionsError(f"cannot read Edition body {body_path}: {exc}") from exc
        item = copy.deepcopy(record)
        item["body_html"] = validate_body_html(body)
        hydrated.append(item)
    return hydrated


def _date_label(value: str) -> str:
    parsed = date.fromisoformat(value)
    return f"{parsed.day} {parsed.strftime('%B')} {parsed.year}"


def render_editions_landing(records: list[dict]) -> str:
    cards = []
    for record in records:
        authors = escape(", ".join(record["authors"]))
        cards.append(
            f'<article class="publication-card" data-edition-id="{escape(record["edition_id"])}">'
            f'<div class="publication-meta"><span>QuietWire Edition</span> · '
            f'<time datetime="{record["source_date"]}">Source artifact: {_date_label(record["source_date"])}</time></div>'
            f'<h2>{escape(record["title"])}</h2>'
            f'<p class="publication-byline">By {authors} · QuietWire Editions</p>'
            f'<p class="publication-summary">{escape(record["summary"])}</p>'
            f'<a class="text-link" href="{escape(record["canonical_path"], quote=True)}">'
            f'Read the Edition <span aria-hidden="true">→</span></a>'
            f'</article>'
        )
    listing = "".join(cards)
    return (
        '<section class="page-hero compact-hero section-dark"><div class="shell page-hero-grid">'
        '<div data-reveal><p class="eyebrow"><span></span> First-party originals</p>'
        '<h1>QuietWire Editions</h1>'
        '<p class="hero-lede">Original essays, field notes, reports, transcripts, and media published under QuietWire’s own custody.</p></div>'
        '<div class="hero-aside" data-reveal><p>QuietWire Editions is our canonical first-party publishing lane. '
        'Writing and appearances whose original home is elsewhere remain indexed in '
        '<a href="/publications/">Publications</a>.</p></div>'
        '</div></section>'
        f'<section class="section section-cream"><div class="shell publication-list" data-reveal>{listing}</div></section>'
    )


def render_edition(record: dict, base_url: str) -> str:
    authors = escape(", ".join(record["authors"]))
    date_label = _date_label(record["source_date"])
    canonical = base_url.rstrip("/") + record["canonical_path"]
    return (
        '<section class="page-hero compact-hero section-dark"><div class="shell page-hero-grid">'
        '<div data-reveal><p class="eyebrow"><span></span> QuietWire Editions</p>'
        f'<h1>{escape(record["title"])}</h1><p class="hero-lede">{escape(record["summary"])}</p></div>'
        f'<div class="hero-aside" data-reveal><p>Canonical first-party Edition by {authors}.<br>'
        f'<time datetime="{record["source_date"]}">Source artifact: {date_label}</time></p>'
        '<p><a class="text-link" href="/editions/">All QuietWire Editions <span aria-hidden="true">←</span></a></p></div>'
        '</div></section>'
        '<section class="section section-cream"><div class="shell">'
        '<article class="detail-grid"><div class="detail-number">QuietWire<br>Edition</div><div>'
        f'<p class="section-kicker">By {authors}</p>'
        f'<div class="large-copy">{record["body_html"].rstrip()}</div>'
        '<hr>'
        f'<p class="microcopy">Canonical first-party Edition at QuietWire. Source artifact dated {date_label}. '
        f'Canonical URL: <a href="{escape(canonical, quote=True)}">{escape(canonical)}</a>.</p>'
        '<p><a class="text-link" href="/publications/">Browse all writing &amp; media '
        '<span aria-hidden="true">→</span></a></p>'
        '</div></article></div></section>'
    )
