#!/usr/bin/env python3
"""Compare a generated tree with an external directory or SHA256SUMS file."""
from __future__ import annotations
import argparse, hashlib, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]

def actual_files(directory: Path) -> dict[str, str]:
    return {str(path.relative_to(directory)): hashlib.sha256(path.read_bytes()).hexdigest()
            for path in sorted(directory.rglob("*")) if path.is_file()}

def expected_files(path: Path) -> dict[str, str]:
    if path.is_file():
        result = {}
        for line in path.read_text(encoding="utf-8").splitlines():
            if line.strip():
                digest, relative = line.split(None, 1)
                result[relative.removeprefix("./")] = digest
        return result
    public = path / "public"
    return actual_files(public if public.is_dir() else path)

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument("baseline", type=Path, help="baseline directory, baseline root, or SHA256SUMS file")
parser.add_argument("--generated", type=Path, default=ROOT / "dist", help="generated directory (default: dist)")
args = parser.parse_args()
if not args.generated.is_dir():
    print(f"ERROR: generated directory does not exist: {args.generated}", file=sys.stderr); raise SystemExit(2)
if not args.baseline.exists():
    print(f"ERROR: baseline does not exist: {args.baseline}", file=sys.stderr); raise SystemExit(2)
actual, expected = actual_files(args.generated), expected_files(args.baseline)
missing = sorted(set(expected) - set(actual))
extra = sorted(set(actual) - set(expected))
changed = sorted(path for path in set(actual) & set(expected) if actual[path] != expected[path])
print(f"Baseline files: {len(expected)}; generated files: {len(actual)}")
for label, paths in (("Missing", missing), ("Extra", extra), ("Changed", changed)):
    print(f"{label}: {len(paths)}")
    for path in paths: print(f"  {path}")
if missing or extra or changed: raise SystemExit(1)
print(f"PASS: {len(actual)} files match byte-for-byte by SHA-256")
