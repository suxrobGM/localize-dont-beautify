# Real-face figure gate: license/attribution checklist

The `real_*` faces in the experiment data are publicly available before/after photos
(real people, not private patients). Public availability does not by itself grant the
right to republish them in a paper. A real face may appear in a figure only after every
item below is checked for its source and the decision is recorded here.

For each source of `real_*` faces (see the `source` column in the experiment repo's
`data/manifest.csv`):

- [ ] Source identified (URL / dataset name / publisher).
- [ ] License or terms of use located and read.
- [ ] Terms explicitly permit reproduction in an academic publication (not just research use).
- [ ] Required attribution wording recorded below and added to the figure caption or ethics section.
- [ ] No additional restrictions (non-commercial only is acceptable for a paper; "no redistribution" is not).

Until all boxes are checked for a face's source, that face stays out of the figures
(`consent_verified = False` in `scripts/figure_stems.py`) and the paper ships with
synthetic faces only.

## Decisions

| Source | License/terms | Publication OK? | Attribution required | Date checked |
|--------|---------------|-----------------|----------------------|--------------|
| (pending) | | | | |
