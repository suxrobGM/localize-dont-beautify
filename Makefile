PY ?= uv run python

.PHONY: all numbers figures pdf clean

all: numbers figures pdf

numbers:
	$(PY) scripts/aggregate.py

figures:
	$(PY) scripts/make_figures.py
	$(PY) scripts/make_qualitative.py

pdf:
	latexmk -pdf -interaction=nonstopmode main.tex

clean:
	latexmk -C main.tex
