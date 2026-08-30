#!/usr/bin/env python3
"""Validate and render QuietWire's public-safe media and appearances layer."""
from __future__ import annotations

import ipaddress
import json
import re
import unicodedata
from datetime import date
from html import escape
from pathlib import Path
from urllib.parse import urlsplit, urlunsplit

SCHEMA_ID = "quietwire.media-appearances-manifest.v1"
ROOT_FIELDS = {"schema_id", "series", "items"}
SERIES_FIELDS = {
    "series_id", "publication_state", "website_visibility", "title", "publisher", "summary",
    "canonical_path", "source_url", "role_label", "lineage_note",
}
SERIES_REQUIRED = SERIES_FIELDS - {"lineage_note"}
ITEM_FIELDS = {
    "stable_id", "publication_state", "website_visibility", "kind", "title", "event_date", "venue",
    "participants", "canonical_url", "series_id", "episode_number", "summary", "canonical_path",
    "media_url", "transcript_url",
}
ITEM_REQUIRED = {
    "stable_id", "publication_state", "website_visibility", "kind", "title", "event_date", "venue",
    "participants", "canonical_url",
}
KINDS = {
    "episode": "Episode",
    "appearance": "Appearance",
    "public_testimony": "Public Testimony",
    "panel": "Panel",
    "conference_session": "Conference Session",
}
ID_PATTERN = re.compile(r"[a-z0-9]+(?:-[a-z0-9]+)*\Z")
PATH_PATTERN = re.compile(r"/library/media/[a-z0-9]+(?:-[a-z0-9]+)*/\Z")
HOST_PATTERN = re.compile(r"(?=.{1,253}\Z)(?:[a-z0-9](?:[a-z0-9-]{0,61}[a-z0-9])?\.)+[a-z]{2,63}\Z")


class ManifestError(ValueError):
    """The media manifest is not safe to publish."""


def _error(scope: str, index: int, message: str) -> ManifestError:
    return ManifestError(f"{scope} record {index}: {message}")


def _plain(value: object, field: str, scope: str, index: int, maximum: int) -> str:
    if not isinstance(value, str) or not value:
        raise _error(scope, index, f"{field} must be a non-empty string")
    if value != value.strip():
        raise _error(scope, index, f"{field} must not have leading or trailing whitespace")
    if value != unicodedata.normalize("NFC", value):
        raise _error(scope, index, f"{field} must use NFC Unicode normalization")
    if len(value) > maximum:
        raise _error(scope, index, f"{field} exceeds {maximum} characters")
    if any(unicodedata.category(character) == "Cc" for character in value):
        raise _error(scope, index, f"{field} contains a control character")
    if "<" in value or ">" in value:
        raise _error(scope, index, f"{field} must be plain text")
    return value


def _id(value: object, field: str, scope: str, index: int, maximum: int = 120) -> str:
    text = _plain(value, field, scope, index, maximum)
    if not ID_PATTERN.fullmatch(text):
        raise _error(scope, index, f"{field} must be lowercase kebab-case ASCII")
    return text


def _path(value: object, field: str, scope: str, index: int) -> str:
    text = _plain(value, field, scope, index, 180)
    if not PATH_PATTERN.fullmatch(text):
        raise _error(scope, index, f"{field} must be a /library/media/<slug>/ path")
    return text


def _public_url(value: object, field: str, scope: str, index: int) -> tuple[str, str]:
    url = _plain(value, field, scope, index, 2048)
    try:
        parts = urlsplit(url)
    except ValueError as exc:
        raise _error(scope, index, f"{field} is malformed") from exc
    if parts.scheme != "https":
        raise _error(scope, index, f"{field} must use https")
    if parts.username is not None or parts.password is not None:
        raise _error(scope, index, f"{field} must not contain credentials")
    if parts.fragment:
        raise _error(scope, index, f"{field} must not contain a fragment")
    hostname = (parts.hostname or "").lower()
    if not HOST_PATTERN.fullmatch(hostname):
        raise _error(scope, index, f"{field} must use a public DNS hostname")
    try:
        ipaddress.ip_address(hostname)
    except ValueError:
        pass
    else:
        raise _error(scope, index, f"{field} must not use an IP address")
    if hostname in {"quietwire.ai", "www.quietwire.ai"} or hostname.endswith((".internal", ".local")):
        raise _error(scope, index, f"{field} must identify an external public source")
    try:
        port = parts.port
    except ValueError as exc:
        raise _error(scope, index, f"{field} has an invalid port") from exc
    if port not in (None, 443):
        raise _error(scope, index, f"{field} must not use a non-default port")
    path = parts.path or "/"
    normalized_path = path if path == "/" else path.rstrip("/")
    normalized = urlunsplit(("https", hostname, normalized_path, parts.query, ""))
    return url, normalized


def _iso_date(value: object, scope: str, index: int) -> str:
    text = _plain(value, "event_date", scope, index, 10)
    try:
        parsed = date.fromisoformat(text)
    except ValueError as exc:
        raise _error(scope, index, "event_date must be a real ISO date") from exc
    if parsed.isoformat() != text:
        raise _error(scope, index, "event_date must use YYYY-MM-DD")
    return text


def validate_manifest(document: object) -> tuple[list[dict], list[dict]]:
    if not isinstance(document, dict) or set(document) != ROOT_FIELDS:
        raise ManifestError("manifest root fields must be exactly schema_id, series, items")
    if document["schema_id"] != SCHEMA_ID:
        raise ManifestError(f"schema_id must be {SCHEMA_ID!r}")
    if not isinstance(document["series"], list) or not isinstance(document["items"], list):
        raise ManifestError("series and items must be arrays")

    series: list[dict] = []
    series_ids: set[str] = set()
    paths: set[str] = set()
    urls: set[str] = set()
    for index, raw in enumerate(document["series"]):
        if not isinstance(raw, dict):
            raise _error("series", index, "must be an object")
        unknown = sorted(set(raw) - SERIES_FIELDS)
        missing = sorted(SERIES_REQUIRED - set(raw))
        if unknown or missing:
            raise _error("series", index, f"fields do not match contract; unknown={unknown}, missing={missing}")
        series_id = _id(raw["series_id"], "series_id", "series", index, 96)
        if series_id in series_ids:
            raise _error("series", index, f"duplicate series_id {series_id!r}")
        series_ids.add(series_id)
        if raw["publication_state"] != "confirmed_public" or raw["website_visibility"] != "listed":
            raise _error("series", index, "only confirmed_public + listed series are accepted")
        canonical_path = _path(raw["canonical_path"], "canonical_path", "series", index)
        if canonical_path in paths:
            raise _error("series", index, f"duplicate canonical_path {canonical_path!r}")
        paths.add(canonical_path)
        source_url, normalized = _public_url(raw["source_url"], "source_url", "series", index)
        if normalized in urls:
            raise _error("series", index, f"duplicate source_url {source_url!r}")
        urls.add(normalized)
        record = {
            "series_id": series_id,
            "publication_state": "confirmed_public",
            "website_visibility": "listed",
            "title": _plain(raw["title"], "title", "series", index, 240),
            "publisher": _plain(raw["publisher"], "publisher", "series", index, 120),
            "summary": _plain(raw["summary"], "summary", "series", index, 700),
            "canonical_path": canonical_path,
            "source_url": source_url,
            "role_label": _plain(raw["role_label"], "role_label", "series", index, 180),
        }
        if "lineage_note" in raw:
            record["lineage_note"] = _plain(raw["lineage_note"], "lineage_note", "series", index, 1200)
        series.append(record)

    items: list[dict] = []
    item_ids: set[str] = set()
    episode_numbers: set[tuple[str, int]] = set()
    for index, raw in enumerate(document["items"]):
        if not isinstance(raw, dict):
            raise _error("item", index, "must be an object")
        unknown = sorted(set(raw) - ITEM_FIELDS)
        missing = sorted(ITEM_REQUIRED - set(raw))
        if unknown or missing:
            raise _error("item", index, f"fields do not match contract; unknown={unknown}, missing={missing}")
        stable_id = _id(raw["stable_id"], "stable_id", "item", index)
        if stable_id in item_ids:
            raise _error("item", index, f"duplicate stable_id {stable_id!r}")
        item_ids.add(stable_id)
        if raw["publication_state"] != "confirmed_public" or raw["website_visibility"] != "listed":
            raise _error("item", index, "only confirmed_public + listed items are accepted")
        kind = raw["kind"]
        if not isinstance(kind, str) or kind not in KINDS:
            raise _error("item", index, f"kind must be one of {sorted(KINDS)}")
        canonical_url, normalized = _public_url(raw["canonical_url"], "canonical_url", "item", index)
        if normalized in urls:
            raise _error("item", index, f"duplicate canonical_url {canonical_url!r}")
        urls.add(normalized)
        participants = raw["participants"]
        if not isinstance(participants, list) or not 1 <= len(participants) <= 12:
            raise _error("item", index, "participants must contain between 1 and 12 names")
        participants = [_plain(name, f"participants[{position}]", "item", index, 120) for position, name in enumerate(participants)]
        if len({name.casefold() for name in participants}) != len(participants):
            raise _error("item", index, "participants must not contain duplicates")
        record = {
            "stable_id": stable_id,
            "publication_state": "confirmed_public",
            "website_visibility": "listed",
            "kind": kind,
            "title": _plain(raw["title"], "title", "item", index, 260),
            "event_date": _iso_date(raw["event_date"], "item", index),
            "venue": _plain(raw["venue"], "venue", "item", index, 160),
            "participants": participants,
            "canonical_url": canonical_url,
        }
        if "series_id" in raw:
            series_id = _id(raw["series_id"], "series_id", "item", index, 96)
            if series_id not in series_ids:
                raise _error("item", index, f"unknown series_id {series_id!r}")
            record["series_id"] = series_id
        if kind == "episode" and "series_id" not in record:
            raise _error("item", index, "episode requires series_id")
        if kind != "episode" and "series_id" in record:
            raise _error("item", index, "non-episode item must not carry series_id in v1")
        if "episode_number" in raw:
            number = raw["episode_number"]
            if not isinstance(number, int) or isinstance(number, bool) or number < 1:
                raise _error("item", index, "episode_number must be a positive integer")
            if "series_id" not in record:
                raise _error("item", index, "episode_number requires series_id")
            key = (record["series_id"], number)
            if key in episode_numbers:
                raise _error("item", index, f"duplicate episode_number {number} in {record['series_id']}")
            episode_numbers.add(key)
            record["episode_number"] = number
        if "summary" in raw:
            record["summary"] = _plain(raw["summary"], "summary", "item", index, 700)
        if "canonical_path" in raw:
            canonical_path = _path(raw["canonical_path"], "canonical_path", "item", index)
            if canonical_path in paths:
                raise _error("item", index, f"duplicate canonical_path {canonical_path!r}")
            paths.add(canonical_path)
            record["canonical_path"] = canonical_path
        if kind != "episode" and "canonical_path" not in record:
            raise _error("item", index, "standalone public media item requires canonical_path")
        if kind == "episode" and "canonical_path" in record:
            raise _error("item", index, "episode routes are grouped under series in v1")
        for field in ("media_url", "transcript_url"):
            if field in raw:
                value, _ = _public_url(raw[field], field, "item", index)
                record[field] = value
        items.append(record)

    return series, sorted(items, key=lambda item: (item["event_date"], item["stable_id"]), reverse=True)


def load_manifest(path: Path) -> tuple[list[dict], list[dict]]:
    try:
        document = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        raise ManifestError(f"cannot read media manifest {path}: {exc}") from exc
    return validate_manifest(document)


def _date_label(value: str) -> str:
    parsed = date.fromisoformat(value)
    return f"{parsed.day} {parsed.strftime('%B')} {parsed.year}"


def _kind_label(kind: str) -> str:
    return KINDS[kind]


def _series_map(series: list[dict]) -> dict[str, dict]:
    return {record["series_id"]: record for record in series}


def _item_map(items: list[dict]) -> dict[str, dict]:
    return {record["stable_id"]: record for record in items}


def render_library_shelf(config: dict, series: list[dict], items: list[dict]) -> str:
    series_by_id = _series_map(series)
    items_by_id = _item_map(items)
    cards: list[str] = []
    shelf = config.get("library_shelf")
    if not isinstance(shelf, list) or len(shelf) != 3:
        raise ManifestError("media website config requires exactly three explicit library_shelf selections")
    seen: set[tuple[str, str]] = set()
    for position, selection in enumerate(shelf):
        if not isinstance(selection, dict) or set(selection) != {"kind", "id"}:
            raise ManifestError(f"library_shelf selection {position} must contain only kind and id")
        key = (selection["kind"], selection["id"])
        if key in seen:
            raise ManifestError(f"duplicate library_shelf selection {key}")
        seen.add(key)
        if selection["kind"] == "series":
            record = series_by_id.get(selection["id"])
            if record is None:
                raise ManifestError(f"library_shelf references unknown series {selection['id']!r}")
            cards.append(
                f'<article class="work-card" data-library-media-series-id="{escape(record["series_id"])}">'
                f'<span class="card-link">Series · {escape(record["publisher"])}</span>'
                f'<h3>{escape(record["title"])}</h3><p>{escape(record["summary"])}</p>'
                f'<a class="text-link" href="{escape(record["canonical_path"], quote=True)}">Explore the series <span aria-hidden="true">→</span></a>'
                '</article>'
            )
        elif selection["kind"] == "item":
            record = items_by_id.get(selection["id"])
            if record is None or "canonical_path" not in record:
                raise ManifestError(f"library_shelf references unknown/non-routable item {selection['id']!r}")
            cards.append(
                f'<article class="work-card" data-library-media-item-id="{escape(record["stable_id"])}">'
                f'<span class="card-link">{escape(_kind_label(record["kind"]))} · {_date_label(record["event_date"])}</span>'
                f'<h3>{escape(record["title"])}</h3><p>{escape(record.get("summary", record["venue"]))}</p>'
                f'<a class="text-link" href="{escape(record["canonical_path"], quote=True)}">View the record <span aria-hidden="true">→</span></a>'
                '</article>'
            )
        else:
            raise ManifestError(f"library_shelf selection {position} kind must be series or item")
    return (
        '<section class="section section-dark" data-library-media-shelf><div class="shell library-shelf" data-reveal>'
        '<div class="section-heading"><div><p class="section-kicker">Watch &amp; Listen</p>'
        '<h2>Conversations in public</h2></div><a class="text-link" href="/library/media/">All media →</a></div>'
        f'<div class="three-grid">{"".join(cards)}</div></div></section>'
    )


def render_media_landing(series: list[dict], items: list[dict]) -> str:
    series_cards = "".join(
        '<article class="pattern-card" data-media-series-id="{}"><span>Series · {}</span><h2>{}</h2><p>{}</p>'
        '<a class="text-link" href="{}">Explore the series <span aria-hidden="true">→</span></a></article>'.format(
            escape(record["series_id"]), escape(record["publisher"]), escape(record["title"]),
            escape(record["summary"]), escape(record["canonical_path"], quote=True)
        ) for record in series
    )
    standalone = [record for record in items if "canonical_path" in record]
    standalone_cards = "".join(
        f'<article class="library-card" data-media-item-id="{escape(record["stable_id"])}">'
        f'<div class="publication-meta"><span>{escape(_kind_label(record["kind"]))}</span>'
        f'<time datetime="{record["event_date"]}">{_date_label(record["event_date"])}</time></div>'
        f'<h3>{escape(record["title"])}</h3><p>{escape(record["venue"])}</p>'
        f'<a class="text-link" href="{escape(record["canonical_path"], quote=True)}">View the record <span aria-hidden="true">→</span></a></article>'
        for record in standalone
    )
    return (
        '<section class="page-hero compact-hero section-dark"><div class="shell page-hero-grid">'
        '<div data-reveal><p class="eyebrow"><span></span> QuietWire Library</p><h1>Watch &amp; Listen</h1>'
        '<p class="hero-lede">Conversations, testimony, panels, and recurring appearances — indexed without taking custody away from their original public venues.</p></div>'
        '<div class="hero-aside" data-reveal><p>QuietWire keeps the catalog and provenance. External publishers keep their canonical recordings. No autoplay, no third-party player embeds.</p></div>'
        '</div></section>'
        '<section class="section section-cream"><div class="shell"><div class="section-heading" data-reveal>'
        '<div><p class="section-kicker">Recurring work</p><h2>Series</h2></div></div>'
        f'<div class="pattern-grid" data-reveal>{series_cards}</div></div></section>'
        '<section class="section section-soft"><div class="shell library-shelf" data-reveal>'
        '<div class="section-heading"><div><p class="section-kicker">Selected records</p><h2>Appearances</h2></div></div>'
        f'<div class="library-grid">{standalone_cards}</div></div></section>'
    )


def render_series(record: dict, items: list[dict]) -> str:
    episodes = [item for item in items if item.get("series_id") == record["series_id"]]
    episodes.sort(key=lambda item: (item.get("episode_number", 10**9), item["event_date"], item["stable_id"]))
    lineage = ""
    if record.get("lineage_note"):
        lineage = (
            '<section class="section section-cream"><div class="shell origin-grid" data-reveal>'
            '<div><p class="section-kicker">About the name</p><h2>A longer line</h2></div>'
            f'<div><p class="large-copy">{escape(record["lineage_note"])}</p>'
            '<p>Publication dates for the Techstrong series remain 2025 dates; the recollection is preserved as lineage, not as a backdated media artifact.</p></div>'
            '</div></section>'
        )
    cards: list[str] = []
    for item in episodes:
        number = f'Episode {item["episode_number"]}' if item.get("episode_number") else _kind_label(item["kind"])
        participants = ", ".join(item["participants"])
        cards.append(
            f'<article class="publication-card" data-media-episode-id="{escape(item["stable_id"])}">'
            f'<div class="publication-meta"><span>{escape(number)}</span><time datetime="{item["event_date"]}">{_date_label(item["event_date"])}</time></div>'
            f'<h2>{escape(item["title"])}</h2><p class="publication-byline">{escape(participants)} · {escape(item["venue"])}</p>'
            f'<a class="text-link" href="{escape(item["canonical_url"], quote=True)}">Watch at {escape(record["publisher"])} <span aria-hidden="true">↗</span></a>'
            '</article>'
        )
    return (
        '<section class="page-hero compact-hero section-dark"><div class="shell page-hero-grid">'
        f'<div data-reveal><p class="eyebrow"><span></span> Series · {escape(record["publisher"])}</p><h1>{escape(record["title"])}</h1>'
        f'<p class="hero-lede">{escape(record["summary"])}</p></div>'
        f'<div class="hero-aside" data-reveal><p>{escape(record["role_label"])}</p>'
        f'<p><a class="text-link" href="{escape(record["source_url"], quote=True)}">Series at source <span aria-hidden="true">↗</span></a></p></div>'
        '</div></section>'
        f'{lineage}'
        '<section class="section section-soft"><div class="shell"><div class="section-heading" data-reveal>'
        f'<div><p class="section-kicker">Source-linked records</p><h2>{len(episodes)} indexed episodes</h2></div>'
        '<a class="text-link" href="/library/media/">Watch &amp; Listen →</a></div>'
        f'<div class="publication-list" data-reveal>{"".join(cards)}</div></div></section>'
    )


def render_item(record: dict) -> str:
    participants = ", ".join(record["participants"])
    actions = [f'<a class="button button-dark" href="{escape(record.get("media_url", record["canonical_url"]), quote=True)}">Watch at source ↗</a>']
    if record.get("transcript_url"):
        actions.append(f'<a class="text-link" href="{escape(record["transcript_url"], quote=True)}">Read the official transcript <span aria-hidden="true">↗</span></a>')
    source_name = record["venue"].split(" · ", 1)[0]
    transcript_value = "Official transcript linked" if record.get("transcript_url") else "No transcript asserted"
    return (
        '<section class="page-hero compact-hero section-dark"><div class="shell page-hero-grid">'
        f'<div data-reveal><p class="eyebrow"><span></span> {escape(_kind_label(record["kind"]))}</p><h1>{escape(record["title"])}</h1>'
        f'<p class="hero-lede">{escape(record.get("summary", record["venue"]))}</p></div>'
        f'<div class="hero-aside" data-reveal><p>{_date_label(record["event_date"])}<br>{escape(record["venue"])}</p>'
        f'<p>{escape(participants)}</p></div></div></section>'
        '<section class="section section-cream"><div class="shell prose" data-reveal>'
        '<p class="section-kicker">Source record</p><h2>Witness the origin</h2>'
        '<p>QuietWire catalogs this appearance and its public provenance. The external venue remains the canonical source for the recording or event record.</p>'
        f'<div class="button-row">{"".join(actions)}</div>'
        '<div class="truth-grid">'
        f'<article><span>Canonical source</span><p>{escape(source_name)}</p></article>'
        '<article><span>Custody</span><p>External recording; QuietWire catalog record.</p></article>'
        f'<article><span>Transcript</span><p>{escape(transcript_value)}</p></article>'
        '</div>'
        f'<p><a class="text-link" href="{escape(record["canonical_url"], quote=True)}">Open source record <span aria-hidden="true">↗</span></a></p>'
        '<p><a class="text-link" href="/library/media/">Back to Watch &amp; Listen →</a></p>'
        '</div></section>'
    )
