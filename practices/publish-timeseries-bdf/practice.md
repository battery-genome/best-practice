---
id: practice:publish-timeseries-bdf
title: Publish battery time-series data in the Battery Data Format (BDF)
summary: Time-domain battery test data shared beyond the producing lab should be published as BDF tables — canonical column names, declared units, validated structure — alongside the original vendor files, with dataset-level metadata sidecars.
version: 0.1.0
status: published
superseded_by: null
applies_to:
  test_kinds: [cycling, capacity_check, rate_capability, quasi_ocv, hppc, ici, gitt, dcir, formation, calendar_ageing, rpt]
  chemistries: []
  cell_formats: []
maturity: proposal
authors:
  - name: Simon Clark
    orcid: null
    affiliation: SINTEF
sources:
  - role: primary
    title: Battery Data Format specification and reference implementation
    authors: Battery Data Alliance
    url: https://github.com/battery-data-alliance/battery-data-format
    accessed: 2026-06-12
    note: Canonical column vocabulary, units, validation rules, and metadata sidecar contracts.
  - role: tool
    title: batterydf Python package
    authors: Battery Data Alliance
    url: https://pypi.org/project/batterydf/
    accessed: 2026-06-12
    note: Reference implementation used for conversion and validation in this practice.
created_at: 2026-06-12
updated_at: 2026-06-12
---

# Publish battery time-series data in the Battery Data Format (BDF)

## Scope

Applies to time-domain electrochemical test data — cycling, capacity checks,
rate capability, pulse techniques (HPPC, ICI, GITT, DCIR), formation, calendar
ageing, and reference performance tests — whenever the data is shared beyond
the lab that produced it: in publications, data repositories, project
consortia, or the Battery Genome registry.

It does not apply to frequency-domain data (EIS), images, or post-mortem
characterization, which have their own structures. It also does not replace
cell and test *metadata* records (cell type, test protocol, conditions); it
governs the time-series tables those records point to.

## Recommendation

Data publishers **should** release time-domain test data as BDF tables, and
**must** follow these rules when they do:

1. **Use the canonical columns.** Every BDF table must contain the three
   required quantities, in canonical units:
   - `test_time_second` — seconds from test start
   - `voltage_volt` — cell voltage in V
   - `current_ampere` — current in A
2. **Include the recommended quantities when the instrument records them:**
   `unix_time_second` (absolute time), `cycle_count`, `step_count`, and
   `ambient_temperature_celsius`. Capacity, energy, power, resistance, and
   surface-temperature channels have defined optional columns — map them
   rather than inventing new headers.
3. **One header form per file.** Use either the machine-readable names above
   or the human-readable labels (`Test Time / s`, `Voltage / V`,
   `Current / A`); do not mix forms. Machine-readable names are preferred for
   repository deposits.
4. **Convert, don't retype.** Produce BDF files with the reference
   implementation (`pip install batterydf`) so unit conversion and header
   mapping are reproducible:

   ```python
   import bdf
   bdf.ingest("raw/", out_dir="bdf/", format="parquet")
   ```

   Vendor plugins currently cover Biologic MPT, Neware CSV/NDA, Basytec,
   Digatron, Landt, Novonix, Excel, and MATLAB exports.
5. **Validate before publishing.** `bdf.validate(path, report=True)` must
   report `ok: true` for every published file. Validation checks required
   columns, recognized labels, and time monotonicity.
6. **Keep the originals.** Publish the raw vendor files alongside the BDF
   tables (e.g. `timeseries/raw/` next to `timeseries/`). BDF is the access
   copy; the vendor file is the evidence copy.
7. **Attach dataset metadata.** Include a `contribution.json` sidecar with at
   minimum the dataset DOI and license, and a `battery.json` describing the
   cells under test. Without a license statement the data is not legally
   reusable, however good its structure.
8. **Preserve the sign convention.** Do not re-sign current during
   conversion. Record the source convention (`charge_positive` or
   `discharge_positive`) in the dataset metadata.

Parquet is the preferred encoding for large tables; CSV is acceptable and
more approachable for small datasets.

## Rationale and evidence

Every cycler vendor exports a different table: different column names,
units, time formats, and file encodings. Each consumer of shared data
currently re-implements the same fragile header-guessing logic, and subtle
errors — milliamps read as amps, cycle indices off by one, mixed sign
conventions — survive into published analyses precisely because they are
plausible.

A shared canonical table removes that entire error class once, at the
publisher's side, where the knowledge to do the mapping correctly actually
exists. The BDF column vocabulary is maintained by the Battery Data Alliance,
each quantity carries a resolvable IRI into the BDF ontology, and the
reference implementation makes conversion a one-line operation rather than a
bespoke script. Keeping the vendor originals alongside means the conversion
is auditable and re-runnable as the tooling improves.

## How to apply

- For new datasets: run `bdf.ingest` over the raw export directory, check the
  validation report, and deposit both `timeseries/raw/` (vendor files) and
  the converted BDF tables together with `contribution.json` and
  `battery.json`.
- For instruments without a BDF plugin (e.g. Arbin `.res`, Maccor exports):
  parse with your own tooling, emit the canonical column names and units
  directly, and confirm with `bdf.validate`. Consider contributing the parser
  upstream as a plugin.
- For legacy data being curated: record the original file's hash and path,
  convert, validate, and note the conversion tool and version in the dataset
  provenance.
- In the Battery Genome stack, BDF tables slot directly into dataset
  distributions: the ingest pipeline converts incoming time-series to BDF
  internally, so publishing in BDF means your data round-trips without loss.

## Known limitations and open questions

- Arbin and Maccor formats have no reference parser yet; conversions from
  those instruments depend on third-party tooling and need closer review.
- BDF does not yet prescribe a current sign convention; this practice
  requires declaring it, and will be updated if the specification adopts a
  normative convention.
- Step-level derived quantities (per-step capacity and energy) have defined
  columns, but vendor semantics differ in edge cases (rest steps, partial
  steps); when in doubt, publish the directly measured channels and let
  consumers derive aggregates.
- EIS and other frequency-domain data are out of scope pending a
  corresponding BDF table definition.

## References

- Battery Data Alliance, *Battery Data Format* specification and reference
  implementation. https://github.com/battery-data-alliance/battery-data-format
- `batterydf` on PyPI. https://pypi.org/project/batterydf/
- Battery Genome ingest documentation (BattINFO `docs/ingest-manifest-contract.md`)
  for how BDF tables are referenced from dataset records.
