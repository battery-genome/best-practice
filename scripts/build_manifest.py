#!/usr/bin/env python3
"""Validate guidance frontmatter and build the platform manifest.

Scans each content type's documents (including _staging/), validates YAML
frontmatter against the type's JSON Schema, and writes
exports/guidance-manifest.json — the artifact the battery-genome platform
consumes (same pattern as five-star-battery-data's learning manifest).

Content types:
    practices/**/practice.md   ← schemas/practice-frontmatter.schema.json
    methods/**/method.md       ← schemas/method-frontmatter.schema.json

Usage:
    python scripts/build_manifest.py            # validate + write manifest
    python scripts/build_manifest.py --check    # validate only (CI gate)

Exit code is non-zero on any validation failure.
"""
from __future__ import annotations

import argparse
import datetime
import json
import sys
from dataclasses import dataclass
from pathlib import Path

import jsonschema
import yaml

REPO_ROOT = Path(__file__).resolve().parent.parent
MANIFEST_PATH = REPO_ROOT / "exports" / "guidance-manifest.json"
MANIFEST_SCHEMA_VERSION = "battery-genome-guidance/v1alpha1"

# Statuses allowed outside _staging/ (i.e. for published documents).
PUBLISHED_STATUSES = {"published", "superseded", "archived"}


@dataclass(frozen=True)
class ContentType:
    key: str          # manifest key, e.g. "practices"
    id_prefix: str    # frontmatter id prefix, e.g. "practice"
    directory: str    # top-level folder
    filename: str     # document filename
    schema: str       # schema filename in schemas/
    template: str     # template filename in templates/


CONTENT_TYPES = [
    ContentType(
        key="practices",
        id_prefix="practice",
        directory="practices",
        filename="practice.md",
        schema="practice-frontmatter.schema.json",
        template="practice-template.md",
    ),
    ContentType(
        key="methods",
        id_prefix="method",
        directory="methods",
        filename="method.md",
        schema="method-frontmatter.schema.json",
        template="method-template.md",
    ),
]


def split_frontmatter(text: str, path: Path) -> tuple[dict, str]:
    """Return (frontmatter dict, body) from a guidance document."""
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
    """YAML parses bare dates into date objects; the schemas expect ISO strings."""
    if isinstance(value, (datetime.date, datetime.datetime)):
        return value.isoformat()
    if isinstance(value, dict):
        return {k: _stringify_dates(v) for k, v in value.items()}
    if isinstance(value, list):
        return [_stringify_dates(v) for v in value]
    return value


def validate_file(
    path: Path,
    content_type: ContentType,
    validator: jsonschema.Validator,
    errors: list[str],
    is_template: bool = False,
) -> dict | None:
    """Validate one document; append errors, return frontmatter if valid."""
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

    if is_template:
        return frontmatter

    # Slug in id must match the containing folder.
    slug = frontmatter["id"].split(":", 1)[1]
    if path.parent.name != slug:
        errors.append(
            f"{path}: id slug '{slug}' does not match folder name '{path.parent.name}'"
        )
        return None

    # Published documents do not belong in _staging, and vice versa.
    in_staging = "_staging" in path.parts
    status = frontmatter["status"]
    if in_staging and status in PUBLISHED_STATUSES:
        errors.append(f"{path}: status '{status}' not allowed in _staging/")
    if not in_staging and status in ("draft", "review"):
        errors.append(f"{path}: status '{status}' must live in {content_type.directory}/_staging/")

    return frontmatter


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="validate only, do not write manifest")
    args = parser.parse_args()

    errors: list[str] = []
    seen_ids: dict[str, Path] = {}
    entries_by_type: dict[str, list[dict]] = {ct.key: [] for ct in CONTENT_TYPES}
    file_count = 0

    for content_type in CONTENT_TYPES:
        schema_path = REPO_ROOT / "schemas" / content_type.schema
        validator = jsonschema.Draft202012Validator(
            json.loads(schema_path.read_text(encoding="utf-8")),
            format_checker=jsonschema.FormatChecker(),
        )

        content_dir = REPO_ROOT / content_type.directory
        for path in sorted(content_dir.glob(f"**/{content_type.filename}")):
            file_count += 1
            frontmatter = validate_file(path, content_type, validator, errors)
            if frontmatter is None:
                continue
            doc_id = frontmatter["id"]
            if doc_id in seen_ids:
                errors.append(f"{path}: duplicate id '{doc_id}' (also in {seen_ids[doc_id]})")
                continue
            seen_ids[doc_id] = path
            entries_by_type[content_type.key].append(
                {
                    **frontmatter,
                    "path": path.relative_to(REPO_ROOT).as_posix(),
                    "staging": "_staging" in path.parts,
                }
            )

        # Keep each template honest: it must validate against its schema too.
        template_path = REPO_ROOT / "templates" / content_type.template
        validate_file(template_path, content_type, validator, errors, is_template=True)

    # Cross-reference checks against the full id set.
    known = set(seen_ids)
    for entries in entries_by_type.values():
        for entry in entries:
            for field in ("superseded_by", "related_practices"):
                targets = entry.get(field)
                if not targets:
                    continue
                for target in targets if isinstance(targets, list) else [targets]:
                    if target not in known:
                        errors.append(f"{entry['path']}: {field} '{target}' does not exist")

    if errors:
        print(f"FAILED: {len(errors)} error(s) across {file_count} document(s)\n")
        for err in errors:
            print(f"  - {err}")
        return 1

    counts = ", ".join(f"{len(v)} {k}" for k, v in entries_by_type.items())
    print(f"OK: {counts} validated (+ templates)")

    if not args.check:
        manifest = {"schema_version": MANIFEST_SCHEMA_VERSION}
        staging: list[dict] = []
        for key, entries in entries_by_type.items():
            manifest[key] = [e for e in entries if not e["staging"]]
            staging.extend(e for e in entries if e["staging"])
        manifest["staging"] = staging
        MANIFEST_PATH.parent.mkdir(parents=True, exist_ok=True)
        MANIFEST_PATH.write_text(
            json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
        )
        print(f"Wrote {MANIFEST_PATH.relative_to(REPO_ROOT).as_posix()}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
