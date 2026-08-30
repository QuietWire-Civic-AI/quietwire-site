#!/usr/bin/env python3
"""Contract and generated-output checks for QuietWire Editions v2."""
from __future__ import annotations

import copy
import json
import sys
import unittest
from pathlib import Path

from editions import EditionsError, load_manifest, validate_body_html, validate_manifest

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
errors: list[str] = []

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
