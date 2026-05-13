"""
Artifact Integrity Verifier (REQ-OEA-020)
==========================================
Compares SHA-256 hashes of committed result artifacts against
experiments/manifest.json. Reports pass/fail for each entry.

Usage:
    python experiments/verify_manifest.py
"""
from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "experiments" / "manifest.json"


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()


def main() -> int:
    if not MANIFEST.exists():
        print(f"ERROR: manifest not found: {MANIFEST}", file=sys.stderr)
        return 1

    with MANIFEST.open(encoding="utf-8") as f:
        manifest: dict[str, str] = json.load(f)

    # Filter out metadata keys (prefixed with _)
    entries = {k: v for k, v in manifest.items() if not k.startswith("_")}

    passed = 0
    failed = 0
    missing = 0

    for rel_path, expected_hash in sorted(entries.items()):
        full_path = ROOT / rel_path
        if not full_path.exists():
            print(f"  MISSING  {rel_path}")
            missing += 1
            continue
        actual_hash = sha256_file(full_path)
        if actual_hash == expected_hash:
            print(f"  OK       {rel_path}")
            passed += 1
        else:
            print(f"  FAIL     {rel_path}")
            print(f"           expected: {expected_hash}")
            print(f"           actual:   {actual_hash}")
            failed += 1

    total = passed + failed + missing
    print(f"\n{passed}/{total} passed, {failed} failed, {missing} missing")

    if failed > 0 or missing > 0:
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
