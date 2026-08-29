#!/usr/bin/env python3
"""Contract and generated-output checks for the publications vertical slice."""
from __future__ import annotations

import copy
import json
import sys
import unittest
from pathlib import Path

from publications import ManifestError, load_manifest, render_publications, validate_manifest

ROOT = Path(__file__).resolve().parents[1]


def valid_record(**changes) -> dict:
    record = {
        "stable_id": "example-2026-01-02",
        "publication_state": "confirmed_public",
        "website_visibility": "listed",
        "title": "A public example",
        "authors": ["Example Author"],
        "venue": "Example Journal",
        "published_on": "2026-01-02",
        "artifact_type": "article",
        "summary": "A short public summary.",
        "canonical_url": "https://example.org/public-example",
    }
    record.update(changes)
    return record


def manifest(*records: dict) -> dict:
    return {"schema_id": "quietwire.publications-manifest.v1", "publications": list(records)}


class PublicationsContractTests(unittest.TestCase):
    def assert_rejected(self, document: object) -> None:
        with self.assertRaises(ManifestError):
            validate_manifest(document)

    def test_rejects_malformed_record(self) -> None:
        for changes in (
            {"published_on": "2026-02-30"},
            {"artifact_type": ["article"]},
            {"canonical_url": "https://[not-an-address/article"},
            {"title": "<script>not plain text</script>"},
        ):
            with self.subTest(changes=changes):
                self.assert_rejected(manifest(valid_record(**changes)))

    def test_rejects_duplicate_stable_ids(self) -> None:
        first = valid_record()
        second = valid_record(canonical_url="https://example.net/another")
        self.assert_rejected(manifest(first, second))

    def test_rejects_duplicate_canonical_url_aliases(self) -> None:
        first = valid_record()
        second = valid_record(
            stable_id="example-2026-01-03",
            canonical_url="https://EXAMPLE.org:443/public-example/",
        )
        self.assert_rejected(manifest(first, second))

    def test_rejects_candidate_and_private_states(self) -> None:
        for state in ("candidate", "private", "draft", "confirmed"):
            with self.subTest(state=state):
                self.assert_rejected(manifest(valid_record(publication_state=state)))

    def test_requires_explicit_listed_website_visibility(self) -> None:
        missing = valid_record()
        del missing["website_visibility"]
        self.assert_rejected(manifest(missing))
        self.assert_rejected(manifest(valid_record(website_visibility="unlisted")))

    def test_rejects_body_and_private_note_fields(self) -> None:
        for field in ("body", "article_body", "private_notes", "internal_source"):
            with self.subTest(field=field):
                record = valid_record()
                record[field] = "PRIVATE SENTINEL"
                self.assert_rejected(manifest(record))

    def test_rejects_non_external_or_unsafe_urls(self) -> None:
        for url in (
            "http://example.org/article",
            "https://user:secret@example.org/article",
            "https://www.quietwire.ai/article",
            "https://drafts.internal/article",
            "https://127.0.0.1/article",
            "https://example.org/article?private=1",
        ):
            with self.subTest(url=url):
                self.assert_rejected(manifest(valid_record(canonical_url=url)))

    def test_renderer_is_newest_first_and_metadata_only(self) -> None:
        older = valid_record()
        newer = valid_record(
            stable_id="example-2026-03-04",
            title="Newer public example",
            published_on="2026-03-04",
            canonical_url="https://example.net/newer",
        )
        records = validate_manifest(manifest(older, newer))
        output = render_publications(records)
        self.assertLess(output.index("Newer public example"), output.index("A public example"))
        for value in ("Example Author", "Example Journal", "Article", "4 March 2026"):
            self.assertIn(value, output)
        self.assertNotIn("PRIVATE SENTINEL", output)

    def test_input_is_not_mutated(self) -> None:
        document = manifest(valid_record())
        original = copy.deepcopy(document)
        validate_manifest(document)
        self.assertEqual(document, original)


suite = unittest.defaultTestLoader.loadTestsFromTestCase(PublicationsContractTests)
result = unittest.TextTestRunner(verbosity=1).run(suite)
if not result.wasSuccessful():
    raise SystemExit(1)

config = json.loads((ROOT / "site.config.json").read_text(encoding="utf-8"))
collection = config["publications_collection"]
manifest_path = ROOT / collection["manifest"]
records = load_manifest(manifest_path)
errors: list[str] = []
if ".dev." not in manifest_path.name:
    errors.append("publications: first-slice input must remain visibly identified as a development fixture")
if len(records) != 1:
    errors.append(f"publications: development fixture must contain exactly one record, found {len(records)}")
output_path = ROOT / "dist" / collection["output"]
if not output_path.is_file():
    errors.append(f"publications: missing generated route {output_path}")
else:
    output = output_path.read_text(encoding="utf-8")
    for record in records:
        for value in (record["stable_id"], record["title"], *record["authors"], record["venue"], record["canonical_url"]):
            if value not in output:
                errors.append(f"publications: generated output is missing validated value {value!r}")
    for prohibited in ("article_body", "private_notes", "internal_source", "PRIVATE SENTINEL"):
        if prohibited in output:
            errors.append(f"publications: prohibited material reached generated output: {prohibited}")
    if output.count('class="publication-card"') != len(records):
        errors.append("publications: generated card count does not match validated record count")

sitemap = (ROOT / "dist/sitemap.xml").read_text(encoding="utf-8")
expected_url = config["base_url"] + "/publications/"
if expected_url not in sitemap:
    errors.append(f"publications: sitemap is missing {expected_url}")
for locale in config["locales"]:
    if locale["id"] == collection["locale"]:
        continue
    localized_route = f"/{locale['url_prefix'].strip('/')}/publications/"
    if (ROOT / "dist" / locale["url_prefix"] / "publications").exists() or localized_route in sitemap:
        errors.append(f"publications: unreviewed localized route was generated: {localized_route}")

if errors:
    print("\n".join(errors), file=sys.stderr)
    raise SystemExit(1)
print("PASS: publications v1 contract requires confirmed_public plus explicit listed website visibility")
print("PASS: publications v1 contract rejects malformed, duplicate, candidate, private, unlisted, and body-bearing records")
print("PASS: one public development fixture renders metadata-only at /publications/, newest first")
print("PASS: publications remains an explicit English-source route without fabricated translations")
