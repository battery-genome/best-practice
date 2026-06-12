# Battery Genome Guidance

A curated collection of community guidance for battery testing, data
management, and reporting — authored and reviewed here, published on the
[Battery Genome](https://github.com/battery-genome) platform.

## Content types

The repository holds distinct guidance genres, separated by the kind of claim
they make:

- **Practices** (`practices/`) — *normative recommendations*: "you should/must
  do X." Reviewed, versioned, citable, scoped to where they apply
  (test kinds, chemistries, cell formats), and supersedable. Example: how to
  publish time-series data in the Battery Data Format.
- **Methods** (`methods/`) — *explanatory How-To guides*, one per measurement
  or analysis method (GITT, ICI, HPPC, …): what the method is, how it works,
  how to run and analyze it. Keyed to the same test-kind vocabulary that
  scopes practices, so the platform can compose a method page with its
  applicable practices automatically.
- **Benchmark definitions** (planned) — *comparison rules*: metrics,
  reference protocols, and admissibility criteria for cross-cell or
  cross-model comparisons. Results are computed downstream; only the
  versioned definitions will live here.

Machine-readable test protocols, datasets, and benchmark results are **not**
authored here — they live in the BattINFO registry. Guidance documents link
to them by IRI.

## Structure

```
practices/
  _staging/            ← drafts under editorial review
  <slug>/practice.md   ← published practices (+ assets/, notebooks/)
methods/
  _staging/            ← drafts under editorial review
  <slug>/method.md     ← published method guides (+ assets/, notebooks/)
schemas/               ← JSON Schemas for each content type's frontmatter
templates/             ← starting points for new documents
scripts/               ← validation + manifest export (build_manifest.py)
exports/               ← compiled manifest consumed by the platform (CI-built)
```

## Authoring

Copy the relevant template (`templates/practice-template.md` or
`templates/method-template.md`) into the matching `_staging/<your-slug>/`
folder, fill in the frontmatter and body, and validate with:

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
