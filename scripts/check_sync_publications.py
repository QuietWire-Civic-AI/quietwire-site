#!/usr/bin/env python3
"""Self-checks for the bounded publications synchronization command."""
from __future__ import annotations

import json
import tempfile
from pathlib import Path

from publications import ManifestError
from sync_publications import sync_manifest


def manifest(stable_id: str = "example-2026-09-24-item") -> dict:
    return {
        "schema_id": "quietwire.publications-manifest.v1",
        "publications": [
            {
                "stable_id": stable_id,
                "publication_state": "confirmed_public",
                "website_visibility": "listed",
                "title": "Example publication",
                "authors": ["Example Author"],
                "venue": "Example Publisher",
                "published_on": "2026-09-24",
                "artifact_type": "article",
                "summary": "Synthetic fixture used only by the repository self-check.",
                "canonical_url": "https://example.com/publication",
            }
        ],
    }


def write_json(path: Path, document: dict) -> bytes:
    raw = (json.dumps(document, ensure_ascii=False, indent=2) + "\n").encode("utf-8")
    path.write_bytes(raw)
    return raw


def main() -> int:
    with tempfile.TemporaryDirectory() as directory:
        root = Path(directory)
        source = root / "source.json"
        destination = root / "destination.json"
        receipt = root / "receipt.json"

        original = write_json(source, manifest())
        first = sync_manifest(source, destination, receipt)
        assert first["status"] == "updated"
        assert destination.read_bytes() == original
        receipt_first = receipt.read_bytes()

        second = sync_manifest(source, destination, receipt)
        assert second["status"] == "no-op"
        assert second["changed"] is False
        assert receipt.read_bytes() == receipt_first

        changed = write_json(source, manifest("example-2026-09-25-item"))
        third = sync_manifest(source, destination, receipt)
        assert third["status"] == "updated"
        assert destination.read_bytes() == changed

        invalid = manifest()
        invalid["publications"][0]["internal_note"] = "must never cross the boundary"
        write_json(source, invalid)
        before = destination.read_bytes()
        try:
            sync_manifest(source, destination, receipt)
        except ManifestError:
            pass
        else:
            raise AssertionError("unsafe manifest was not refused")
        assert destination.read_bytes() == before

    print("publications sync checks passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
