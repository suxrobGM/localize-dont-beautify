"""Compare refs.bib against what the compiled paper cites and renders.

Run after touching refs.bib or any \\cite. Needs a compiled main.aux/main.bbl
(run `make pdf` first). All three counts should match; dead or missing keys are
listed by name.
"""

import re

from config import PAPER_ROOT, read_text, report_issues


def main() -> None:
    bib = set(re.findall(r"^@\w+\{([^,\s]+)", read_text(PAPER_ROOT / "refs.bib"), re.M))
    aux = {
        key.strip()
        for group in re.findall(r"\\citation\{([^}]+)\}", read_text(PAPER_ROOT / "main.aux"))
        for key in group.split(",")
    }
    bbl = set(re.findall(r"\\bibitem\{([^}]+)\}", read_text(PAPER_ROOT / "main.bbl")))

    print(f"refs.bib entries: {len(bib)}")
    print(f"cited in text:    {len(aux)}")
    print(f"rendered in PDF:  {len(bbl)}")

    report_issues(
        {
            "In refs.bib but never cited": sorted(bib - aux),
            "Cited but missing from refs.bib": sorted(aux - bib),
            "Cited but not rendered (rerun latexmk?)": sorted(aux - bbl),
        },
        "All good: every entry is cited and every citation renders.",
    )


if __name__ == "__main__":
    main()
