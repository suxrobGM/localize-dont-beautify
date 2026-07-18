# Localize, Don't Beautify

LaTeX source and analysis artifacts for *"Localize, Don't Beautify: Client-Side
Control of Hosted Image Editors for Cosmetic Surgery Previews"* (IEEE
conference format).

This pilot evaluates whether a landmark-derived, client-side composite can prevent
hosted image editors from changing pixels outside a requested facial region. It
does: preservation is enforced by construction while target-region pixel change is
largely retained. The study does **not** establish clinical plausibility or predict
surgical outcomes; it contains 15 main-analysis faces, one output per cell, and no
surgeon ratings.

## Repository scope

The repository contains the canonical score table, aggregation code, generated
tables/plots, qualitative figures, and paper source:

```text
experiment run records (separate, non-public repository)
        |
        v
scripts/aggregate.py  --> data/canonical_rows.csv
                     --> tables/main_results.tex
                     --> tables/setup_models.tex
                     --> tables/numbers.tex
scripts/make_figures.py     --> figures/generated/*.pdf
scripts/make_qualitative.py --> figures/generated/*.png
```

The committed canonical CSV is sufficient to audit the paper's quantitative
summaries and regenerate quantitative plots. It is not sufficient for end-to-end
reproduction of API generation, masking, alignment, scoring, or qualitative image
selection. `PLASTYVUE_POC` must point to the separate experiment repository to
rebuild from raw run records.

## Building

You need a TeX distribution with `latexmk` and [uv](https://docs.astral.sh/uv/).

```sh
make numbers    # requires the separate experiment repository
make figures    # quantitative plots use the committed CSV; qualitative grids need source images
make pdf        # latexmk -> main.pdf
make check      # verify citation parity
```

Or run `make pdf` with the committed generated artifacts.

## Identifiable source images

The qualitative figures contain publicly accessible before/after photographs of
real people. Public visibility is not proof of permission to republish or transmit
an image to hosted AI services. Exact sources, terms, required attribution, and an
institutional-review determination must be documented before archival submission;
see `docs/real_face_checklist.md`.
