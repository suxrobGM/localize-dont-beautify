PY ?= uv run python

.PHONY: all numbers baseline figures pdf check clean

all: numbers figures pdf check

numbers:
	$(PY) scripts/aggregate.py

# Recompute data/gt_baseline.csv from the source photographs (no API calls).
# Only needed when the face set or ground-truth photos change; the CSV is committed.
baseline:
	uv run --extra baseline python scripts/gt_baseline.py

figures:
	$(PY) scripts/make_figures.py
	$(PY) scripts/make_qualitative.py

pdf:
	latexmk -pdf -interaction=nonstopmode main.tex

check:
	$(PY) scripts/check_citations.py
	$(PY) scripts/check_readme.py

clean:
	latexmk -C main.tex
