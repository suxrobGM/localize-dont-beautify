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
import sys
from pathlib import Path

MARKER = re.compile(r"<!--\s*(\w+)\s*-->\s*([0-9][0-9,.]*)")
NEWCOMMAND = re.compile(r"\\newcommand\{\\(\w+)\}\{([^}]*)\}")


def main() -> None:
    root = Path(__file__).resolve().parent.parent
    numbers = dict(NEWCOMMAND.findall((root / "tables" / "numbers.tex").read_text(encoding="utf-8")))
    readme = (root / "README.md").read_text(encoding="utf-8")

    tagged = MARKER.findall(readme)
    print(f"tagged numbers in README.md: {len(tagged)}")

    unknown: list[str] = []
    stale: list[tuple[str, str, str]] = []
    for macro, quoted in tagged:
        if macro not in numbers:
            unknown.append(macro)
        elif quoted.replace(",", "") != numbers[macro].replace("{,}", "").replace(",", ""):
            stale.append((macro, quoted, numbers[macro]))

    if unknown:
        print("\nTagged with a macro that numbers.tex does not define:")
        for macro in unknown:
            print("  -", macro)
    if stale:
        print("\nStale (README value vs. generated value):")
        for macro, quoted, actual in stale:
            print(f"  - {macro}: README says {quoted}, numbers.tex says {actual}")
    if unknown or stale:
        sys.exit(1)

    print("All good: every tagged README number matches numbers.tex.")


if __name__ == "__main__":
    main()
