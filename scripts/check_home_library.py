#!/usr/bin/env python3
"""Focused checks for the explicitly curated English homepage Library shelf."""
from __future__ import annotations

import copy
import json
import re
from html.parser import HTMLParser
from pathlib import Path

from editions import load_manifest as load_editions_manifest
from home_library import resolve_home_library
from publications import load_manifest as load_publications_manifest

ROOT = Path(__file__).resolve().parents[1]
DIST = ROOT / "dist"
config = json.loads((ROOT / "site.config.json").read_text(encoding="utf-8"))
edition_config = json.loads((ROOT / "data/editions-site.v1.json").read_text(encoding="utf-8"))
editions = load_editions_manifest(ROOT / edition_config["manifest"])
publications = load_publications_manifest(ROOT / config["publications_collection"]["manifest"])
home_config = config["home_library"]
errors: list[str] = []
output = ""


class ShelfParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.shelves = 0
        self.items: list[tuple[str, str]] = []
        self.links: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        attrs_dict = dict(attrs)
        if "data-home-library-shelf" in attrs_dict:
            self.shelves += 1
        if "data-home-library-kind" in attrs_dict:
            self.items.append((attrs_dict.get("data-home-library-kind", ""), attrs_dict.get("data-home-library-id", "")))
        if tag == "a" and attrs_dict.get("href"):
            self.links.append(attrs_dict["href"])


def assert_rejected(candidate: dict, label: str) -> None:
    try:
        resolve_home_library(candidate, editions, publications)
    except ValueError:
        return
    errors.append(f"home_library: {label} configuration did not fail closed")


output_path = DIST / "index.html"
if not output_path.is_file():
    errors.append("home_library: missing generated English homepage")
else:
    output = output_path.read_text(encoding="utf-8")
    parser = ShelfParser()
    parser.feed(output)
    expected_items = [(item["kind"], item["id"]) for item in home_config["items"]]
    if parser.shelves != 1:
        errors.append(f"home_library: expected exactly one shelf, found {parser.shelves}")
    if parser.items != expected_items:
        errors.append(f"home_library: rendered selection/order differs from configured items: {parser.items}")
    if len(parser.items) != 3:
        errors.append("home_library: expected exactly three curated items")
    if "/library/" not in parser.links:
        errors.append("home_library: missing Explore the Library link")
    if "/editions/own-the-origin/" not in parser.links:
        errors.append("home_library: Edition card has the wrong destination")
    selected_ids = {item_id for _, item_id in parser.items}
    for record in publications:
        if record["stable_id"] in selected_ids and record["canonical_url"] not in parser.links:
            errors.append(f"home_library: publication {record['stable_id']} does not use its validated canonical URL")
    if "chris-blask-2026-08-19-token-exhaustion-attacks" in output and "https://www.cybrsecmedia.com/the-token-exhaustion-attack/" not in output:
        errors.append("home_library: Token-Exhaustion canonical URL missing")
    if "chris-blask-2026-07-28-model-wasnt-rogue" in output and "https://securityboulevard.com/2026/07/the-model-wasnt-rogue-the-control-plane-was/" not in output:
        errors.append("home_library: Model Wasn't Rogue canonical URL missing")
    if output.count("data-home-library-id=") != 3:
        errors.append("home_library: unconfigured item leaked into shelf")
    if "From QuietWire" not in output or "Explore the Library" not in output:
        errors.append("home_library: required English shelf copy is missing")
    if not (output.index("patterns-preview") < output.index("data-home-library-shelf") < output.index("method-preview")):
        errors.append("home_library: shelf is not between Patterns and Method")

resolved = resolve_home_library(home_config, editions, publications)
if [(kind, record["edition_id"] if kind == "edition" else record["stable_id"]) for kind, record in resolved] != [
    ("edition", "own-the-origin"),
    ("publication", "chris-blask-2026-08-19-token-exhaustion-attacks"),
    ("publication", "chris-blask-2026-07-28-model-wasnt-rogue"),
]:
    errors.append("home_library: selections did not resolve from validated records in configured order")
missing = copy.deepcopy(home_config); missing["items"][0]["id"] = "missing-edition"
assert_rejected(missing, "missing ID")
duplicate = copy.deepcopy(home_config); duplicate["items"][2] = copy.deepcopy(duplicate["items"][1])
assert_rejected(duplicate, "duplicate ID")
wrong_kind = copy.deepcopy(home_config); wrong_kind["items"][0]["kind"] = "publication"
assert_rejected(wrong_kind, "wrong kind")
malformed = {"items": [{"kind": "edition", "id": "own-the-origin", "extra": True}] * 3}
assert_rejected(malformed, "malformed item")

sitemap = (DIST / "sitemap.xml").read_text(encoding="utf-8")
for prefix in ("ar", "es", "fr"):
    path = DIST / prefix / "index.html"
    if not path.is_file():
        errors.append(f"home_library: missing localized homepage {path}")
        continue
    text = path.read_text(encoding="utf-8")
    for phrase in ("From QuietWire", "Explore the Library", "Own the Origin"):
        if phrase in text:
            errors.append(f"home_library: localized {prefix} output contains {phrase!r}")
    source_path = {"ar": "src/content/ar/pages/index.html", "es": "src/content/es/pages/index.html", "fr": "src/content/fr-CA/pages/index.html"}[prefix]
    main_match = re.search(r"<main id=\"main\">(.*?)</main>", text, re.DOTALL)
    if not main_match or main_match.group(1).strip() != (ROOT / source_path).read_text(encoding="utf-8").strip():
        errors.append(f"home_library: localized {prefix} homepage body changed")
    if (DIST / prefix / "library").exists() or f"/{prefix}/library/" in sitemap:
        errors.append(f"home_library: localized Library route leaked for {prefix}")

source = (ROOT / "scripts/home_library.py").read_text(encoding="utf-8")
if re.search(r"\b(fetch|XMLHttpRequest|WebSocket|EventSource)\b|requests\.|urllib\.request|BeautifulSoup|<script", source):
    errors.append("home_library: runtime API, scraping, or executable content introduced")
if any(token in output for token in ("google-analytics.com", "googletagmanager.com", "facebook.net", "doubleclick.net")):
    errors.append("home_library: tracker reference introduced")
if "{{home_library_shelf}}" not in (ROOT / "src/content/en-CA/pages/index.html").read_text(encoding="utf-8"):
    errors.append("home_library: explicit English source marker is missing")

if errors:
    raise SystemExit("\n".join(errors))
print("PASS: one English From QuietWire shelf with exactly three configured items in order")
print("PASS: Edition/Publications resolve only from validated records and derive destinations")
print("PASS: missing, duplicate, wrong-kind, and malformed selections fail closed")
print("PASS: shelf placement, localized no-leakage, unchanged localized bodies, and no Library route")
print("PASS: no newest-N leakage, trackers, external scripts, runtime APIs, scraping, or executable shelf content")
