#!/usr/bin/env python3
"""Contract and generated-output checks for QuietWire Editions v2."""
from __future__ import annotations

import copy
import hashlib
import tempfile
import json
import sys
import unittest
from pathlib import Path
from html.parser import HTMLParser

from editions import EditionsError, attach_covers, load_manifest, render_edition_cover, validate_body_html, validate_manifest

ROOT = Path(__file__).resolve().parents[1]


def valid_record(**changes) -> dict:
    record = {
        "edition_id": "example-edition",
        "release_state": "approved",
        "website_visibility": "listed",
        "title": "A first-party example",
        "slug": "example-edition",
        "authors": ["Example Author"],
        "source_date": "2026-08-30",
        "artifact_type": "article",
        "summary": "A short public summary.",
        "canonical_path": "/editions/example-edition/",
        "body_file": "exports/editions/example-edition.html",
    }
    record.update(changes)
    return record


def manifest(*records: dict) -> dict:
    return {"schema_id": "quietwire.editions-manifest.v1", "editions": list(records)}


class EditionsContractTests(unittest.TestCase):
    def assert_rejected(self, document: object) -> None:
        with self.assertRaises(EditionsError):
            validate_manifest(document)

    def test_requires_explicit_approval_and_listing(self) -> None:
        for changes in (
            {"release_state": "draft"},
            {"release_state": "candidate"},
            {"website_visibility": "unlisted"},
        ):
            with self.subTest(changes=changes):
                self.assert_rejected(manifest(valid_record(**changes)))
        missing = valid_record()
        del missing["website_visibility"]
        self.assert_rejected(manifest(missing))

    def test_rejects_unknown_private_or_body_fields(self) -> None:
        for field in ("private_notes", "internal_source", "body", "article_body", "credentials"):
            with self.subTest(field=field):
                record = valid_record()
                record[field] = "PRIVATE SENTINEL"
                self.assert_rejected(manifest(record))

    def test_rejects_bad_route_body_and_date_contracts(self) -> None:
        for changes in (
            {"canonical_path": "/editions/other/"},
            {"body_file": "exports/editions/other.html"},
            {"source_date": "2026-02-30"},
            {"slug": "Bad Slug"},
        ):
            with self.subTest(changes=changes):
                self.assert_rejected(manifest(valid_record(**changes)))

    def test_rejects_duplicate_ids_slugs_and_paths(self) -> None:
        first = valid_record()
        second = valid_record(
            edition_id="another-edition",
            slug="another-edition",
            canonical_path="/editions/another-edition/",
            body_file="exports/editions/another-edition.html",
        )
        for duplicate in (
            {**second, "edition_id": first["edition_id"]},
            {**second, "slug": first["slug"], "canonical_path": first["canonical_path"], "body_file": first["body_file"]},
            {**second, "canonical_path": first["canonical_path"]},
        ):
            with self.subTest(duplicate=duplicate):
                self.assert_rejected(manifest(first, duplicate))

    def test_body_html_is_fail_closed(self) -> None:
        validate_body_html("<p>A safe body with <strong>emphasis</strong>.</p>")
        for body in (
            "<script>alert(1)</script>",
            '<p onclick="alert(1)">bad</p>',
            "<img src=x>",
            '<a href="javascript:alert(1)">bad</a>',
            "<!-- private note --><p>body</p>",
        ):
            with self.subTest(body=body):
                with self.assertRaises(EditionsError):
                    validate_body_html(body)

    def test_covers_are_local_explicit_and_hash_pinned(self) -> None:
        records = validate_manifest(manifest(valid_record()))
        with tempfile.TemporaryDirectory() as directory:
            assets = Path(directory)
            (assets / "editions").mkdir()
            image = assets / "editions" / "example-edition.webp"
            fixture = b"RIFF" + bytes((4, 0, 0, 0)) + b"WEBP"
            image.write_bytes(fixture)
            share_path = assets / "editions" / "example-edition-share.jpg"
            # Minimal synthetic baseline SOF0 header: 8 bit, 630x1200.
            # This is a header-validator fixture, not a decodable image.
            share_fixture = bytes.fromhex("ffd8 ffc0 000b 08 0276 04b0 01 011100 ffd9")
            share_path.write_bytes(share_fixture)
            metadata = {"alt": 'A "quoted" willow', "caption": "An illustration", "sha256": hashlib.sha256(fixture).hexdigest(), "share_sha256": hashlib.sha256(share_fixture).hexdigest()}
            self.assertEqual(render_edition_cover(records[0]), "")
            for invalid in (
                {"unlisted": metadata},
                {"../example-edition": metadata},
                {"example-edition": {**metadata, "src": "https://example.org/image"}},
                {"example-edition": {**metadata, "alt": "<script>"}},
                {"example-edition": {**metadata, "sha256": "0" * 64}},
                {"example-edition": {**metadata, "share_sha256": "0" * 64}},
                {"example-edition": {**metadata, "share_src": "https://example.org/image.jpg"}},
            ):
                with self.subTest(invalid=invalid), self.assertRaises(EditionsError):
                    attach_covers(records, invalid, assets)
            self.assertEqual(render_edition_cover(records[0]), "")
            attach_covers(records, {"example-edition": metadata}, assets)
            rendered = render_edition_cover(records[0])
            self.assertIn('src="/assets/editions/example-edition.webp"', rendered)
            self.assertIn('alt="A &quot;quoted&quot; willow"', rendered)
            self.assertEqual(records[0]["cover"]["share_src"], "/assets/editions/example-edition-share.jpg")
            share_path.unlink()
            with self.assertRaises(EditionsError):
                attach_covers(records, {"example-edition": metadata}, assets)
            bad_share = share_fixture.replace(bytes.fromhex("0276"), bytes.fromhex("0275"))
            share_path.write_bytes(bad_share)
            with self.assertRaises(EditionsError):
                attach_covers(records, {"example-edition": {**metadata, "share_sha256": hashlib.sha256(bad_share).hexdigest()}}, assets)
            share_path.write_bytes(share_fixture)
            image.unlink()
            with self.assertRaises(EditionsError):
                attach_covers(records, {"example-edition": metadata}, assets)

    def test_input_is_not_mutated(self) -> None:
        document = manifest(valid_record())
        original = copy.deepcopy(document)
        validate_manifest(document)
        self.assertEqual(document, original)


suite = unittest.defaultTestLoader.loadTestsFromTestCase(EditionsContractTests)
result = unittest.TextTestRunner(verbosity=1).run(suite)
if not result.wasSuccessful():
    raise SystemExit(1)

config = json.loads((ROOT / "site.config.json").read_text(encoding="utf-8"))
collection = json.loads((ROOT / "data" / "editions-site.v1.json").read_text(encoding="utf-8"))
manifest_path = ROOT / collection["manifest"]
records = load_manifest(manifest_path)
attach_covers(records, collection.get("covers", {}), ROOT / "src" / "assets")
errors: list[str] = []


class SocialMeta(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.values = {}
        self.in_head = False

    def handle_starttag(self, tag, attrs):
        if tag == "head":
            self.in_head = True
        if tag == "meta" and self.in_head:
            a = dict(attrs)
            key = a.get("property") or a.get("name")
            if key:
                self.values.setdefault(key, []).append(a.get("content"))

    def handle_endtag(self, tag):
        if tag == "head":
            self.in_head = False


def check_social(text, expected, label):
    parser = SocialMeta()
    parser.feed(text)
    for key, value in expected.items():
        if parser.values.get(key) != [value]:
            errors.append(f"editions: {label} missing or duplicate {key}: {parser.values.get(key)}")
    for key in ("og:image:type", "og:image:width", "og:image:height", "og:image:alt", "twitter:image:alt"):
        if key not in expected and key in parser.values:
            errors.append(f"editions: {label} unexpected {key}")


default_share = config["base_url"] + "/assets/quietwire-og.png"
check_social((ROOT / "dist" / "index.html").read_text(encoding="utf-8"), {
    "og:type": "website", "og:image": default_share, "twitter:image": default_share,
}, "home")

landing = ROOT / "dist" / collection["output"]
if not landing.is_file():
    errors.append(f"editions: missing landing route {landing}")

sitemap = (ROOT / "dist" / "sitemap.xml").read_text(encoding="utf-8")
expected_landing_url = config["base_url"] + "/editions/"
if expected_landing_url not in sitemap:
    errors.append(f"editions: sitemap is missing {expected_landing_url}")

if landing.is_file():
    landing_text = landing.read_text(encoding="utf-8")
    if "/publications/" not in landing_text:
        errors.append("editions: landing page must link back to Publications")
    for record in records:
        if record["edition_id"] not in landing_text or record["title"] not in landing_text:
            errors.append(f"editions: landing page is missing {record['edition_id']}")

for record in records:
    rel = Path(record["canonical_path"].lstrip("/")) / "index.html"
    output = ROOT / "dist" / rel
    if not output.is_file():
        errors.append(f"editions: missing generated Edition route {output}")
        continue
    text = output.read_text(encoding="utf-8")
    canonical = config["base_url"] + record["canonical_path"]
    for value in (record["title"], *record["authors"], record["summary"], canonical):
        if value not in text:
            errors.append(f"editions: generated output is missing validated value {value!r}")
    if record["body_html"].rstrip() not in text:
        errors.append(f"editions: generated output is missing validated body for {record['edition_id']}")
    expected_share = {"og:type": "website", "og:image": default_share, "twitter:image": default_share}
    if "cover" in record:
        cover = record["cover"]
        share_url = config["base_url"] + cover["share_src"]
        expected_share = {
            "og:type": "article", "og:image": share_url, "twitter:image": share_url,
            "og:image:type": "image/jpeg", "og:image:width": "1200", "og:image:height": "630",
            "og:image:alt": cover["alt"], "twitter:image:alt": cover["alt"],
        }
        rel_share = cover["share_src"].lstrip("/")
        original_share = ROOT / "src" / rel_share
        copied_share = ROOT / "dist" / rel_share
        if not copied_share.is_file() or original_share.read_bytes() != copied_share.read_bytes():
            errors.append(f"editions: missing or changed social image for {record['edition_id']}")
        rendered_cover = render_edition_cover(record)
        rel_cover = record["cover"]["src"].lstrip("/")
        original = ROOT / "src" / rel_cover
        copied = ROOT / "dist" / rel_cover
        if rendered_cover not in text or not copied.is_file() or original.read_bytes() != copied.read_bytes():
            errors.append(f"editions: missing or changed cover for {record['edition_id']}")
    check_social(text, expected_share, record["edition_id"])
    if canonical not in sitemap:
        errors.append(f"editions: sitemap is missing {canonical}")
    if "private_notes" in text or "internal_source" in text or "PRIVATE SENTINEL" in text:
        errors.append(f"editions: prohibited private material reached {output}")

for locale in config["locales"]:
    if locale["id"] == collection["locale"]:
        continue
    prefix = locale["url_prefix"].strip("/")
    localized_route = f"/{prefix}/editions/"
    if (ROOT / "dist" / prefix / "editions").exists() or localized_route in sitemap:
        errors.append(f"editions: unreviewed localized route was generated: {localized_route}")

if errors:
    print("\n".join(errors), file=sys.stderr)
    raise SystemExit(1)

print("PASS: Editions v2 requires explicit approved release state plus listed website visibility")
print("PASS: Editions v2 rejects private fields, malformed routes, duplicates, and executable body markup")
print(f"PASS: {len(records)} first-party Edition record(s) render at canonical QuietWire routes")
print("PASS: Editions remains an explicit English-source surface without fabricated translations")

print("PASS: illustrated Editions advertise one verified article-specific JPEG in Open Graph and Twitter metadata; other pages retain fallback")
