# Practices

One folder per practice, named by its slug (lowercase kebab-case, matching the
`practice:<slug>` id in the frontmatter):

```
practices/
  _staging/                ← drafts under editorial review (status: draft | review)
  <practice-slug>/         ← published practices (status: published | superseded)
    practice.md            ← the recommendation; YAML frontmatter + markdown body
    assets/                ← figures, lookup tables referenced by the document
    notebooks/             ← computational provenance (optional)
```

Start from `templates/practice-template.md`. Frontmatter is validated against
`schemas/practice-frontmatter.schema.json` by CI; run locally with:

```
python scripts/build_manifest.py --check
```

A practice moves from `_staging/<slug>/` to `<slug>/` when review concludes
and its status flips to `published`. Never edit a published practice's
normative content without bumping `version`.
