# The analysis scripts

Everything in `tables/` and `figures/generated/` is produced by the scripts in
`scripts/`. Don't edit those outputs by hand; they get overwritten on the next
run. Run them with `make numbers` and `make figures`, or directly with
`uv run python scripts/<name>.py`.

The scripts read run data from a local checkout of the experiment repo; the
default path is hardwired in `config.py` and can be overridden with the
`PLASTYVUE_POC` environment variable. They never write to that repo, so the
paper can't corrupt the experiments (or vice versa).

## config.py

Shared paths and naming. Two things worth knowing about:

- `CANONICAL_RUN_PREFIXES` decides which experiment runs count toward the
  paper. Right now that's the registered 2026-07-16 matrix runs plus the
  chained-procedures probe. Older development runs stay on disk but are
  ignored, so re-running an old experiment won't quietly change the paper.
- `MODEL_NAMES` / `PROCEDURE_NAMES` / `CONTROL_NAMES` map config slugs to the
  display names used in tables and figures.

## aggregate.py

Reads every eligible `results.csv`, normalizes the older column names, keeps
rows that succeeded and were actually scored, and dedupes repeated cells (the
row with the most populated metrics wins, latest run breaks ties). Writes:

- `data/canonical_rows.csv` - the deduped row set, with a `run_id` column so
  any number can be traced back to its source run
- `tables/main_results.tex` and `tables/setup_models.tex` - table bodies
- `tables/numbers.tex` - one `\newcommand` per number quoted in the prose

That last file is the reason the paper text contains no hand-typed metrics: the
prose cites macros like `\MedLocComposite`, and rebuilding regenerates them.

## make_figures.py

The three quantitative figures (identity-vs-localization scatter, boxplots,
ground-truth strip plot) as column-width PDFs. `SOURCE_DATE_EPOCH` is pinned so
rebuilding produces byte-identical files and `git status` stays clean.

## make_qualitative.py and figure_stems.py

Builds the before/after image grids from the run outputs. Which faces appear is
controlled by `figure_stems.py`, and each face carries a `verified` flag tied
to the license checklist in `docs/real_face_checklist.md` - a face whose source
hasn't cleared the checklist simply doesn't show up in the figures.

## check_citations.py

Sanity check for the bibliography: compares refs.bib against what the compiled
paper actually cites and renders, and lists any dead entries or missing keys.
Run it after touching refs.bib or any `\cite`; all three counts should match.
