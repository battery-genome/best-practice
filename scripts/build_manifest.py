#!/usr/bin/env python3
"""Validate practice frontmatter and build the platform manifest.

Scans practices/**/practice.md (including _staging/), validates each file's
YAML frontmatter against schemas/practice-frontmatter.schema.json, and writes
exports/best-practices-manifest.json — the artifact the battery-genome
platform consumes (same pattern as five-star-battery-data's learning
manifest).

Usage:
    python scripts/build_manifest.py            # validate + write manifest
    python scripts/build_manifest.py --check    # validate only (CI gate)

Exit code is non-zero on any validation failure.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import jsonschema
import yaml

REPO_ROOT = Path(__file__).resolve().parent.parent
SCHEMA_PATH = REPO_ROOT / "schemas" / "practice-frontmatter.schema.json"
PRACTICES_DIR = REPO_ROOT / "practices"
TEMPLATE_PATH = REPO_ROOT / "templates" / "practice-template.md"
MANIFEST_PATH = REPO_ROOT / "exports" / "best-practices-manifest.json"

MANIFEST_SCHEMA_VERSION = "battery-genome-best-practices/v1alpha1"


def split_frontmatter(text: str, path: Path) -> tuple[dict, str]:
    """Return (frontmatter dict, body) from a practice.md file."""
    if not text.startswith("---"):
        raise ValueError(f"{path}: missing YAML frontmatter block")
    try:
        _, fm_text, body = text.split("---", 2)
    except ValueError as exc:
        raise ValueError(f"{path}: malformed frontmatter delimiters") from exc
    frontmatter = yaml.safe_load(fm_text)
    if not isinstance(frontmatter, dict):
        raise ValueError(f"{path}: frontmatter is not a mapping")
    return _stringify_dates(frontmatter), body


def _stringify_dates(value):
    """YAML parses bare dates into date objects; the schema expects ISO strings."""
    import datetime

    if isinstance(value, (datetime.date, datetime.datetime)):
        return value.isoformat()
    if isinstance(value, dict):
        return {k: _stringify_dates(v) for k, v in value.items()}
    if isinstance(value, list):
        return [_stringify_dates(v) for v in value]
    return value


def validate_file(path: Path, validator: jsonschema.Validator, errors: list[str]) -> dict | None:
    """Validate one practice.md; append errors, return frontmatter if valid."""
    try:
        frontmatter, _ = split_frontmatter(path.read_text(encoding="utf-8"), path)
    except ValueError as exc:
        errors.append(str(exc))
        return None

    file_errors = sorted(validator.iter_errors(frontmatter), key=lambda e: list(e.path))
    for err in file_errors:
        location = "/".join(str(p) for p in err.path) or "<root>"
        errors.append(f"{path}: {location}: {err.message}")
    if file_errors:
        return None

    # Slug in id must match the containing folder (skip for the template).
    if path != TEMPLATE_PATH:
        slug = frontmatter["id"].split(":", 1)[1]
        if path.parent.name != slug:
            errors.append(
                f"{path}: id slug '{slug}' does not match folder name '{path.parent.name}'"
            )
            return None

    # Published/superseded practices do not belong in _staging, and vice versa.
    in_staging = "_staging" in path.parts
    status = frontmatter["status"]
    if in_staging and status in ("published", "superseded"):
        errors.append(f"{path}: status '{status}' not allowed in _staging/")
    if not in_staging and path != TEMPLATE_PATH and status in ("draft", "review"):
        errors.append(f"{path}: status '{status}' must live in practices/_staging/")

    return frontmatter


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="validate only, do not write manifest")
    args = parser.parse_args()

    validator = jsonschema.Draft202012Validator(
        json.loads(SCHEMA_PATH.read_text(encoding="utf-8")),
        format_checker=jsonschema.FormatChecker(),
    )

    errors: list[str] = []
    entries: list[dict] = []
    seen_ids: dict[str, Path] = {}

    practice_files = sorted(PRACTICES_DIR.glob("**/practice.md"))
    for path in practice_files:
        frontmatter = validate_file(path, validator, errors)
        if frontmatter is None:
            continue
        pid = frontmatter["id"]
        if pid in seen_ids:
            errors.append(f"{path}: duplicate id '{pid}' (also in {seen_ids[pid]})")
            continue
        seen_ids[pid] = path
        entries.append(
            {
                **frontmatter,
                "path": path.relative_to(REPO_ROOT).as_posix(),
                "staging": "_staging" in path.parts,
            }
        )

    # Keep the template honest: it must validate against the schema too.
    validate_file(TEMPLATE_PATH, validator, errors)

    # superseded_by must point at a known id.
    known = set(seen_ids)
    for entry in entries:
        target = entry.get("superseded_by")
        if target and target not in known:
            errors.append(f"{entry['path']}: superseded_by '{target}' does not exist")

    if errors:
        print(f"FAILED: {len(errors)} error(s) across {len(practice_files)} practice file(s)\n")
        for err in errors:
            print(f"  - {err}")
        return 1

    print(f"OK: {len(entries)} practice(s) validated (+ template)")

    if not args.check:
        manifest = {
            "schema_version": MANIFEST_SCHEMA_VERSION,
            "practices": [e for e in entries if not e["staging"]],
            "staging": [e for e in entries if e["staging"]],
        }
        MANIFEST_PATH.parent.mkdir(parents=True, exist_ok=True)
        MANIFEST_PATH.write_text(
            json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
        )
        print(f"Wrote {MANIFEST_PATH.relative_to(REPO_ROOT).as_posix()}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
