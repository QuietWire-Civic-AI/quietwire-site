#!/usr/bin/env python3
"""Deterministically sync an approved public-safe publications manifest into the site.

This command validates the supplied manifest using the same fail-closed contract
as the site build. It updates only the checked-in publication snapshot and a
small hash receipt. It performs no network access and no production activation.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import tempfile
from pathlib import Path

from publications import ManifestError, validate_manifest

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_DESTINATION = ROOT / "data" / "publications.dev.v1.json"
DEFAULT_RECEIPT = ROOT / "data" / "publications-sync-receipt.v1.json"
RECEIPT_SCHEMA = "quietwire.publications-sync-receipt.v1"


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def atomic_write(path: Path, data: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile(dir=path.parent, delete=False) as handle:
        temporary = Path(handle.name)
        handle.write(data)
        handle.flush()
        os.fsync(handle.fileno())
    os.replace(temporary, path)


def validated_source(source: Path) -> tuple[bytes, list[dict]]:
    try:
        raw = source.read_bytes()
        document = json.loads(raw.decode("utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        raise ManifestError(f"cannot read publications sync source {source}: {exc}") from exc
    records = validate_manifest(document)
    return raw, records


def sync_manifest(source: Path, destination: Path, receipt_path: Path) -> dict:
    raw, records = validated_source(source)

    current = destination.read_bytes() if destination.exists() else b""
    changed = current != raw
    if changed:
        atomic_write(destination, raw)

    destination_bytes = destination.read_bytes()
    receipt = {
        "schema_id": RECEIPT_SCHEMA,
        "source_sha256": sha256(raw),
        "destination_sha256": sha256(destination_bytes),
        "record_count": len(records),
        "validation": "passed",
    }
    receipt_bytes = (json.dumps(receipt, ensure_ascii=False, indent=2) + "\n").encode("utf-8")
    current_receipt = receipt_path.read_bytes() if receipt_path.exists() else b""
    receipt_changed = current_receipt != receipt_bytes
    if receipt_changed:
        atomic_write(receipt_path, receipt_bytes)

    return {
        "status": "updated" if changed else "no-op",
        "changed": changed,
        "receipt_changed": receipt_changed,
        **receipt,
    }


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Validate and sync an approved public-safe publications manifest into quietwire-site."
    )
    parser.add_argument("source", type=Path, help="Approved public-safe publications.v1.json")
    parser.add_argument(
        "--destination",
        type=Path,
        default=DEFAULT_DESTINATION,
        help="Site publication snapshot (default: data/publications.dev.v1.json)",
    )
    parser.add_argument(
        "--receipt",
        type=Path,
        default=DEFAULT_RECEIPT,
        help="Deterministic sync receipt (default: data/publications-sync-receipt.v1.json)",
    )
    args = parser.parse_args()

    try:
        result = sync_manifest(args.source, args.destination, args.receipt)
    except ManifestError as exc:
        print(json.dumps({"status": "refused", "error": str(exc)}, ensure_ascii=False))
        return 2

    print(json.dumps(result, ensure_ascii=False, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
