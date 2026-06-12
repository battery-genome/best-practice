# Contributing a best practice

## Lifecycle

```
local draft  →  practices/_staging/<slug>/  →  practices/<slug>/  →  platform
                (status: draft | review)       (status: published)
```

1. **Draft.** Copy `templates/practice-template.md` to
   `practices/_staging/<slug>/practice.md`. Choose a short, descriptive,
   lowercase kebab-case slug; set `id: practice:<slug>`. Fill in the
   frontmatter and all body sections.
2. **Validate.** `python scripts/build_manifest.py --check` (install
   `scripts/requirements.txt` first). CI runs the same check on every PR.
3. **Review.** Open a PR. Set `status: review` when ready for editorial
   review. Reviewers check the recommendation against its cited evidence —
   every normative claim must trace to the rationale section.
4. **Publish.** On approval, move the folder from `_staging/` to
   `practices/<slug>/`, set `status: published`, and set `updated_at`.
   The platform picks the practice up from the next manifest export.

## Rules

- **Versioning.** Any change to normative content bumps `version`
  (semver: patch for clarifications, minor for new guidance, major for
  changed recommendations). Editorial typo fixes don't require a bump.
- **Superseding.** Never delete a published practice. Set
  `status: superseded` and point `superseded_by` at its replacement, so
  existing references and conformance claims stay resolvable.
- **Scope honestly.** `applies_to` drives where the platform surfaces the
  practice. An empty array means "applies to all" — only use it when that is
  actually true.
- **Evidence in the repo.** Figures and tables go in `assets/`; the
  notebooks or scripts that produced them go in `notebooks/`. The document
  must stand on static exports — nothing downstream executes notebooks.
- **One practice per PR** where possible; keep diffs reviewable.
- **Attribution.** Authors listed in the frontmatter are the citable authors
  under the repository's CC-BY-4.0 license. Add reviewers to the PR, not the
  author list, unless they contributed content.
