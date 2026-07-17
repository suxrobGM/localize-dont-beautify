"""Compare refs.bib against what the compiled paper cites and renders.

Run after touching refs.bib or any \\cite. Needs a compiled main.aux/main.bbl
(run `make pdf` first). All three counts should match; dead or missing keys are
listed by name.
"""

import re
from pathlib import Path

root = Path(__file__).resolve().parent.parent
bib = set(re.findall(r"^@\w+\{([^,\s]+)", (root / "refs.bib").read_text(encoding="utf-8"), re.M))
aux = set()
for group in re.findall(r"\\citation\{([^}]+)\}", (root / "main.aux").read_text(encoding="utf-8")):
    aux.update(key.strip() for key in group.split(","))
bbl = set(re.findall(r"\\bibitem\{([^}]+)\}", (root / "main.bbl").read_text(encoding="utf-8")))

print(f"refs.bib entries: {len(bib)}")
print(f"cited in text:    {len(aux)}")
print(f"rendered in PDF:  {len(bbl)}")

dead = sorted(bib - aux)
missing = sorted(aux - bib)
unrendered = sorted(aux - bbl)
if dead:
    print("\nIn refs.bib but never cited:")
    for key in dead:
        print("  -", key)
if missing:
    print("\nCited but missing from refs.bib:")
    for key in missing:
        print("  -", key)
if unrendered:
    print("\nCited but not rendered (rerun latexmk?):")
    for key in unrendered:
        print("  -", key)
if not (dead or missing or unrendered):
    print("\nAll good: every entry is cited and every citation renders.")
