# Battery Genome Best Practices

A curated collection of best practice recommendations for battery testing,
data management, and reporting — authored and reviewed here, published on the
[Battery Genome](https://github.com/battery-genome) platform.

## What lives here

Each best practice is a reviewed, versioned, citable document: a recommendation
for how to perform, report, or structure battery research data, grounded in
evidence and scoped to where it applies (test kinds, chemistries, cell formats).

Examples of the kind of content this repository is for:

- Test execution guidance (e.g. GITT relaxation stop criteria)
- Data reporting and metadata recommendations
- Protocol design and documentation practices

## Structure

```
practices/
  _staging/            ← drafts under editorial review
  <practice-slug>/     ← published practices, one folder each
    practice.md        ← the recommendation (YAML frontmatter + markdown body)
    assets/            ← figures, lookup tables
    notebooks/         ← computational provenance, where applicable
schemas/               ← JSON Schema for the practice frontmatter
templates/             ← starting point for new practices
scripts/               ← validation + manifest export (build_manifest.py)
exports/               ← compiled manifest consumed by the platform (CI-built)
```

## Authoring

Copy `templates/practice-template.md` into
`practices/_staging/<your-slug>/practice.md`, fill in the frontmatter and
body, and validate with:

```
pip install -r scripts/requirements.txt
python scripts/build_manifest.py --check
```

CI runs the same validation on every push and pull request. See
[CONTRIBUTING.md](CONTRIBUTING.md) for the editorial lifecycle, versioning
rules, and review expectations.

## License

This work is licensed under
[Creative Commons Attribution 4.0 International (CC BY 4.0)](https://creativecommons.org/licenses/by/4.0/).
You are free to share and adapt the material for any purpose, provided you
give appropriate credit to the authors. See [LICENSE](LICENSE) for the full
legal text.
