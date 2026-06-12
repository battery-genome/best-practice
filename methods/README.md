# Methods

Explanatory How-To guides, one folder per measurement or analysis method,
named by slug (lowercase kebab-case, matching the `method:<slug>` id in the
frontmatter):

```
methods/
  _staging/              ← drafts under editorial review (status: draft | review)
  <method-slug>/         ← published guides (status: published | archived)
    method.md            ← the guide; YAML frontmatter + markdown body
    assets/              ← figures, example data
    notebooks/           ← worked analysis examples (optional)
```

Start from `templates/method-template.md`. Frontmatter is validated against
`schemas/method-frontmatter.schema.json` by CI; run locally with:

```
python scripts/build_manifest.py --check
```

Methods are *explanatory*, not normative — recommendations with conformance
weight belong in `practices/`, linked via the shared `test_kinds` vocabulary.
