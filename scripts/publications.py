#!/usr/bin/env python3
"""Validate and render the public-safe publications manifest."""
from __future__ import annotations

import ipaddress
import json
import re
import unicodedata
from datetime import date
from html import escape
from pathlib import Path
from urllib.parse import urlsplit, urlunsplit

SCHEMA_ID = "quietwire.publications-manifest.v1"
ROOT_FIELDS = {"schema_id", "publications"}
RECORD_FIELDS = {
    "stable_id", "publication_state", "website_visibility", "title", "authors", "venue",
    "published_on", "artifact_type", "summary", "canonical_url",
}
REQUIRED_RECORD_FIELDS = RECORD_FIELDS - {"summary"}
ARTIFACT_TYPES = {
    "article": "Article",
    "essay": "Essay",
    "interview": "Interview",
    "podcast": "Podcast",
    "report": "Report",
    "video": "Video",
}
ID_PATTERN = re.compile(r"[a-z0-9]+(?:-[a-z0-9]+)*\Z")
HOST_PATTERN = re.compile(
    r"(?=.{1,253}\Z)(?:[a-z0-9](?:[a-z0-9-]{0,61}[a-z0-9])?\.)+[a-z]{2,63}\Z"
)


class ManifestError(ValueError):
    """The manifest is not safe to publish."""


def _record_error(index: int, message: str) -> ManifestError:
    return ManifestError(f"publication record {index}: {message}")


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


def _canonical_url(value: object, index: int) -> tuple[str, str]:
    url = _plain_text(value, "canonical_url", index, 2048)
    try:
        parts = urlsplit(url)
    except ValueError as exc:
        raise _record_error(index, "canonical_url is malformed") from exc
    if parts.scheme != "https":
        raise _record_error(index, "canonical_url must use https")
    if parts.username is not None or parts.password is not None:
        raise _record_error(index, "canonical_url must not contain credentials")
    if parts.query or parts.fragment:
        raise _record_error(index, "canonical_url must not contain a query or fragment")
    hostname = (parts.hostname or "").lower()
    if not HOST_PATTERN.fullmatch(hostname):
        raise _record_error(index, "canonical_url must use a public DNS hostname")
    try:
        ipaddress.ip_address(hostname)
    except ValueError:
        pass
    else:
        raise _record_error(index, "canonical_url must not use an IP address")
    if hostname in {"quietwire.ai", "www.quietwire.ai"} or hostname.endswith((".internal", ".local")):
        raise _record_error(index, "canonical_url must point to a public external venue")
    try:
        port = parts.port
    except ValueError as exc:
        raise _record_error(index, "canonical_url has an invalid port") from exc
    if port not in (None, 443):
        raise _record_error(index, "canonical_url must not use a non-default port")
    path = parts.path or "/"
    normalized_path = path if path == "/" else path.rstrip("/")
    normalized = urlunsplit(("https", hostname, normalized_path, "", ""))
    return url, normalized


def validate_manifest(document: object) -> list[dict]:
    if not isinstance(document, dict):
        raise ManifestError("manifest root must be an object")
    fields = set(document)
    if fields != ROOT_FIELDS:
        unknown = sorted(fields - ROOT_FIELDS)
        missing = sorted(ROOT_FIELDS - fields)
        raise ManifestError(f"manifest fields do not match contract; unknown={unknown}, missing={missing}")
    if document["schema_id"] != SCHEMA_ID:
        raise ManifestError(f"schema_id must be {SCHEMA_ID!r}")
    records = document["publications"]
    if not isinstance(records, list):
        raise ManifestError("publications must be an array")

    validated: list[dict] = []
    seen_ids: set[str] = set()
    seen_urls: set[str] = set()
    for index, raw in enumerate(records):
        if not isinstance(raw, dict):
            raise _record_error(index, "must be an object")
        fields = set(raw)
        unknown = sorted(fields - RECORD_FIELDS)
        missing = sorted(REQUIRED_RECORD_FIELDS - fields)
        if unknown or missing:
            raise _record_error(index, f"fields do not match contract; unknown={unknown}, missing={missing}")

        stable_id = _plain_text(raw["stable_id"], "stable_id", index, 96)
        if not ID_PATTERN.fullmatch(stable_id):
            raise _record_error(index, "stable_id must be lowercase kebab-case ASCII")
        if stable_id in seen_ids:
            raise _record_error(index, f"duplicate stable_id {stable_id!r}")
        seen_ids.add(stable_id)

        if raw["publication_state"] != "confirmed_public":
            raise _record_error(index, "publication_state must be 'confirmed_public'")
        if raw["website_visibility"] != "listed":
            raise _record_error(index, "website_visibility must be 'listed'")
        title = _plain_text(raw["title"], "title", index, 240)
        venue = _plain_text(raw["venue"], "venue", index, 120)
        artifact_type = raw["artifact_type"]
        if not isinstance(artifact_type, str) or artifact_type not in ARTIFACT_TYPES:
            raise _record_error(index, f"artifact_type must be one of {sorted(ARTIFACT_TYPES)}")

        authors = raw["authors"]
        if not isinstance(authors, list) or not 1 <= len(authors) <= 8:
            raise _record_error(index, "authors must contain between 1 and 8 names")
        authors = [_plain_text(author, f"authors[{author_index}]", index, 120) for author_index, author in enumerate(authors)]
        if len({author.casefold() for author in authors}) != len(authors):
            raise _record_error(index, "authors must not contain duplicate names")

        published_on_text = _plain_text(raw["published_on"], "published_on", index, 10)
        try:
            published_on = date.fromisoformat(published_on_text)
        except ValueError as exc:
            raise _record_error(index, "published_on must be a real ISO 8601 date (YYYY-MM-DD)") from exc
        if published_on.isoformat() != published_on_text:
            raise _record_error(index, "published_on must use YYYY-MM-DD")

        canonical_url, normalized_url = _canonical_url(raw["canonical_url"], index)
        if normalized_url in seen_urls:
            raise _record_error(index, f"duplicate canonical_url {canonical_url!r}")
        seen_urls.add(normalized_url)

        record = {
            "stable_id": stable_id,
            "publication_state": "confirmed_public",
            "website_visibility": "listed",
            "title": title,
            "authors": authors,
            "venue": venue,
            "published_on": published_on_text,
            "artifact_type": artifact_type,
            "canonical_url": canonical_url,
        }
        if "summary" in raw:
            record["summary"] = _plain_text(raw["summary"], "summary", index, 500)
        validated.append(record)

    return sorted(validated, key=lambda item: (item["published_on"], item["stable_id"]), reverse=True)


def load_manifest(path: Path) -> list[dict]:
    try:
        document = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        raise ManifestError(f"cannot read publications manifest {path}: {exc}") from exc
    return validate_manifest(document)


def render_publications(records: list[dict]) -> str:
    cards = []
    for record in records:
        published = date.fromisoformat(record["published_on"])
        authors = escape(", ".join(record["authors"]))
        summary = ""
        if record.get("summary"):
            summary = f'<p class="publication-summary">{escape(record["summary"])}</p>'
        cards.append(
            f'<article class="publication-card" data-publication-id="{escape(record["stable_id"])}">'
            f'<div class="publication-meta"><span>{escape(ARTIFACT_TYPES[record["artifact_type"]])}</span>'
            f'<time datetime="{record["published_on"]}">{published.day} {published.strftime("%B")} {published.year}</time></div>'
            f'<h2>{escape(record["title"])}</h2>'
            f'<p class="publication-byline">By {authors} · {escape(record["venue"])}</p>'
            f'{summary}'
            f'<a class="text-link" href="{escape(record["canonical_url"], quote=True)}">Read at {escape(record["venue"])} <span aria-hidden="true">↗</span></a>'
            f'</article>'
        )
    listing = "".join(cards) if cards else '<p class="publication-empty">No confirmed public records are available.</p>'
    return (
        '<section class="page-hero compact-hero section-dark"><div class="shell page-hero-grid">'
        '<div data-reveal><p class="eyebrow"><span></span> Writing &amp; Media</p>'
        '<h1>Publications</h1><p class="hero-lede">Confirmed public writing and media from QuietWire and its people.</p></div>'
        '<div class="hero-aside" data-reveal><p>This index carries public metadata and canonical links. Full third-party works remain with their original venues.</p></div>'
        '</div></section>'
        f'<section class="section section-cream"><div class="shell publication-list" data-reveal>{listing}</div></section>'
    )
