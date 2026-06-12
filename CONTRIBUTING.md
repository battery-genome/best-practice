# Contributing guidance

This repository holds two content types with a shared editorial pipeline:

- **Practices** (`practices/`, normative) — recommendations with conformance
  weight. Frontmatter: `schemas/practice-frontmatter.schema.json`.
- **Methods** (`methods/`, explanatory) — How-To guides for measurement and
  analysis methods. Frontmatter: `schemas/method-frontmatter.schema.json`.

If your document says "you should/must do X", it is a practice. If it
explains what a method is and how to run it, it is a method guide. Split
mixed documents: the explanation becomes a method, the normative criteria
become one or more practices linked by the shared `test_kinds` vocabulary.

## Lifecycle

```
local draft  →  <type>/_staging/<slug>/  →  <type>/<slug>/  →  platform
                (status: draft | review)     (status: published)
```

1. **Draft.** Copy the matching template (`templates/practice-template.md` or
   `templates/method-template.md`) to `<type>/_staging/<slug>/<type-file>.md`
   (`practice.md` or `method.md`). Choose a short, descriptive, lowercase
   kebab-case slug; set the id to `practice:<slug>` or `method:<slug>`. Fill
   in the frontmatter and all body sections.
2. **Validate.** `python scripts/build_manifest.py --check` (install
   `scripts/requirements.txt` first). CI runs the same check on every PR.
3. **Review.** Open a PR. Set `status: review` when ready for editorial
   review. For practices, reviewers check the recommendation against its
   cited evidence — every normative claim must trace to the rationale
   section. For methods, reviewers check technical correctness and clarity.
4. **Publish.** On approval, move the folder from `_staging/` to
   `<type>/<slug>/`, set `status: published`, and set `updated_at`.
   The platform picks the document up from the next manifest export.

## Sources and attribution

Provenance is structural, not optional: both frontmatter schemas require a
`sources` list with at least one entry, and CI rejects documents without one.
Each source declares a `role`:

- `primary` — the work the content is built on
- `background` — context, history, further reading
- `adapted` — text, figures, or tables adapted from the source; **requires**
  the source `license` and a `note` saying exactly what was adapted. Only
  adapt material whose license permits it (e.g. CC-BY), and keep the
  adaptation note specific enough that a reader can locate the original.
- `data` — a dataset the document draws on
- `tool` — software the document depends on

Give a `doi` or `url` for every source, and an `accessed` date for web
sources. Original synthesis by the listed authors needs no `adapted` entry —
but every factual claim should still trace to a `primary` or `background`
source. The platform renders the sources block as the document's attribution
panel, so what you write here is the public credit.

## Rules

- **Methods are tool-generic.** A method guide describes the measurement
  ("apply a current pulse and record the relaxation"), not an instrument
  walkthrough ("click Schedule in EC-Lab"). Instrument- or software-specific
  how-tos belong with the tool's own documentation or in the Academy, not
  here.
- **Versioning.** Any change to a practice's normative content bumps
  `version` (semver: patch for clarifications, minor for new guidance, major
  for changed recommendations). Methods version more loosely: bump minor for
  substantive additions. Editorial typo fixes don't require a bump.
- **Superseding (practices).** Never delete a published practice. Set
  `status: superseded` and point `superseded_by` at its replacement, so
  existing references and conformance claims stay resolvable. Methods that
  become obsolete are set to `status: archived`.
- **Scope honestly.** `applies_to` (practices) and `test_kinds` (methods)
  drive where the platform surfaces the document. An empty practice scope
  array means "applies to all" — only use it when that is actually true.
- **Evidence in the repo.** Figures and tables go in `assets/`; the
  notebooks or scripts that produced them go in `notebooks/`. Documents must
  stand on static exports — nothing downstream executes notebooks.
- **One document per PR** where possible; keep diffs reviewable.
- **Attribution.** Authors listed in the frontmatter are the citable authors
  under the repository's CC-BY-4.0 license. Add reviewers to the PR, not the
  author list, unless they contributed content.
