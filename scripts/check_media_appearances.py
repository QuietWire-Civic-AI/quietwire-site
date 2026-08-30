#!/usr/bin/env python3
"""Focused checks for the English-only Watch & Listen media slice."""
from __future__ import annotations

import json
import re
from html.parser import HTMLParser
from pathlib import Path

from media_appearances import load_manifest

ROOT = Path(__file__).resolve().parents[1]
DIST = ROOT / "dist"
CONFIG = json.loads((ROOT / "data" / "media-site.v1.json").read_text(encoding="utf-8"))
SERIES, ITEMS = load_manifest(ROOT / CONFIG["manifest"])
errors: list[str] = []


class MediaParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.h1 = 0
        self.iframes = 0
        self.external_scripts: list[str] = []
        self.series_ids: list[str] = []
        self.item_ids: list[str] = []
        self.episode_ids: list[str] = []
        self.library_series_ids: list[str] = []
        self.library_item_ids: list[str] = []
        self.links: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        values = dict(attrs)
        if tag == "h1":
            self.h1 += 1
        if tag == "iframe":
            self.iframes += 1
        if tag == "script" and values.get("src", "").startswith(("http://", "https://")):
            self.external_scripts.append(values["src"] or "")
        if tag == "a" and values.get("href"):
            self.links.append(values["href"] or "")
        for field, target in (
            ("data-media-series-id", self.series_ids),
            ("data-media-item-id", self.item_ids),
            ("data-media-episode-id", self.episode_ids),
            ("data-library-media-series-id", self.library_series_ids),
            ("data-library-media-item-id", self.library_item_ids),
        ):
            if field in values:
                target.append(values[field] or "")


def parse(path: Path) -> MediaParser:
    parser = MediaParser()
    if not path.is_file():
        errors.append(f"media: missing generated route {path.relative_to(DIST) if path.is_relative_to(DIST) else path}")
        return parser
    parser.feed(path.read_text(encoding="utf-8"))
    if parser.h1 != 1:
        errors.append(f"media: expected exactly one H1 in {path}, found {parser.h1}")
    if parser.iframes:
        errors.append(f"media: third-party iframe/embed introduced in {path}")
    if parser.external_scripts:
        errors.append(f"media: external script introduced in {path}: {parser.external_scripts}")
    return parser


landing = parse(DIST / CONFIG["output"])
expected_series = [record["series_id"] for record in SERIES]
if landing.series_ids != expected_series:
    errors.append(f"media: landing series order mismatch; expected {expected_series}, got {landing.series_ids}")
standalone = [record for record in ITEMS if "canonical_path" in record]
expected_standalone = [record["stable_id"] for record in standalone]
if landing.item_ids != expected_standalone:
    errors.append("media: landing standalone appearance set/order does not match validated manifest")

for record in SERIES:
    route = DIST / record["canonical_path"].lstrip("/") / "index.html"
    parser = parse(route)
    expected = [
        item["stable_id"] for item in sorted(
            (value for value in ITEMS if value.get("series_id") == record["series_id"]),
            key=lambda item: (item.get("episode_number", 10**9), item["event_date"], item["stable_id"]),
        )
    ]
    if parser.episode_ids != expected:
        errors.append(f"media: series {record['series_id']} rendered episode set/order mismatch")
    if record["source_url"] not in parser.links:
        errors.append(f"media: series {record['series_id']} is missing its publisher source link")

inevitability = next(record for record in SERIES if record["series_id"] == "the-inevitability-curve")
inevitability_items = [item for item in ITEMS if item.get("series_id") == inevitability["series_id"]]
if len(inevitability_items) != 20 or {item.get("episode_number") for item in inevitability_items} != set(range(1, 21)):
    errors.append("media: The Inevitability Curve must contain exactly episodes 1 through 20")

for record in standalone:
    route = DIST / record["canonical_path"].lstrip("/") / "index.html"
    parser = parse(route)
    if record["canonical_url"] not in parser.links:
        errors.append(f"media: standalone item {record['stable_id']} missing canonical source link")
    if record.get("media_url") and record["media_url"] not in parser.links:
        errors.append(f"media: standalone item {record['stable_id']} missing media source link")
    if record.get("transcript_url") and record["transcript_url"] not in parser.links:
        errors.append(f"media: standalone item {record['stable_id']} missing transcript link")

library_parser = parse(DIST / "library" / "index.html")
expected_shelf_series = [entry["id"] for entry in CONFIG["library_shelf"] if entry["kind"] == "series"]
expected_shelf_items = [entry["id"] for entry in CONFIG["library_shelf"] if entry["kind"] == "item"]
if library_parser.library_series_ids != expected_shelf_series or library_parser.library_item_ids != expected_shelf_items:
    errors.append("media: Library Watch & Listen shelf does not match explicit media-site curation")
if "/library/media/" not in library_parser.links:
    errors.append("media: Library shelf is missing the Watch & Listen collection link")
if "<!-- quietwire-media-shelf -->" in (DIST / "library" / "index.html").read_text(encoding="utf-8"):
    errors.append("media: Library media marker survived the post-build injection")

sitemap = (DIST / "sitemap.xml").read_text(encoding="utf-8")
expected_urls = ["https://www.quietwire.ai/library/media/"]
expected_urls.extend("https://www.quietwire.ai" + record["canonical_path"] for record in SERIES)
expected_urls.extend("https://www.quietwire.ai" + record["canonical_path"] for record in standalone)
for url in expected_urls:
    if f"<loc>{url}</loc>" not in sitemap:
        errors.append(f"media: sitemap missing {url}")

for prefix in ("ar", "es", "fr"):
    if (DIST / prefix / "library" / "media").exists() or f"/{prefix}/library/media/" in sitemap:
        errors.append(f"media: localized media route generated for {prefix}")

builder_source = (ROOT / "scripts" / "build_media.py").read_text(encoding="utf-8")
for research_name in ("media-appearances.index.v0.json", "media-appearances.techstrong-backfill-20260830.json"):
    if research_name in builder_source:
        errors.append(f"media: public builder must not consume research file {research_name}")
if re.search(r"\b(fetch|XMLHttpRequest|WebSocket|EventSource)\b|requests\.|urllib\.request|BeautifulSoup", builder_source):
    errors.append("media: build path introduced runtime network/scraping dependency")

if errors:
    raise SystemExit("\n".join(errors))
print("PASS: Media manifest is fail-closed and public-safe")
print("PASS: Watch & Listen landing, two series routes, and standalone appearance routes")
print("PASS: 20/20 Inevitability Curve episodes and explicitly curated Library shelf")
print("PASS: No embeds, external scripts, localized leakage, or research-index runtime dependency")
