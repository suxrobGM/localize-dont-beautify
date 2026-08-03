"""Verify the numbers quoted in README.md against tables/numbers.tex.

The paper prose cites macros, so it can never drift; Markdown has no macros, so
a number written into the README goes stale silently when the canonical row set
changes. Tag each one with the macro it mirrors and this script keeps them
honest:

    it contains <!--NumPrimaryFaces-->15 main-analysis faces

The comment renders as nothing on GitHub. Run it with `make check`, or after
`make numbers` reports different totals.
"""

import re

from config import PAPER_ROOT, read_text, report_issues

MARKER = re.compile(r"<!--\s*(\w+)\s*-->\s*([0-9][0-9,.]*)")
NEWCOMMAND = re.compile(r"\\newcommand\{\\(\w+)\}\{([^}]*)\}")


def digits(value: str) -> str:
    """Compare on the bare number: TeX writes thousands as 1{,}000, Markdown as 1,000."""
    return value.replace("{,}", "").replace(",", "")


def main() -> None:
    numbers = dict(NEWCOMMAND.findall(read_text(PAPER_ROOT / "tables" / "numbers.tex")))
    tagged = MARKER.findall(read_text(PAPER_ROOT / "README.md"))
    print(f"tagged numbers in README.md: {len(tagged)}")

    report_issues(
        {
            "Tagged with a macro that numbers.tex does not define": [
                macro for macro, _ in tagged if macro not in numbers
            ],
            "Stale (README value vs. generated value)": [
                f"{macro}: README says {quoted}, numbers.tex says {numbers[macro]}"
                for macro, quoted in tagged
                if macro in numbers and digits(quoted) != digits(numbers[macro])
            ],
        },
        "All good: every tagged README number matches numbers.tex.",
    )


if __name__ == "__main__":
    main()
