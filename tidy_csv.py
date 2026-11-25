"""Tidy a CSV export: trim spaces around every cell and drop blank rows.

Usage:
    python tidy_csv.py [--dedupe] input.csv > tidy.csv

With --dedupe, rows that are exact duplicates after tidying are dropped, keeping the first copy.

Sample data: a small script used to test Pitch In with automation work.
"""

import csv
import sys
from typing import Iterable, List, TextIO


def tidy_rows(rows: Iterable[List[str]], dedupe: bool = False) -> List[List[str]]:
    """Trim spaces around every cell and drop blank rows; with dedupe, also drop repeats of earlier rows."""
    tidy = []
    seen = set()
    for row in rows:
        cells = [cell.strip() for cell in row]
        if not any(cells):
            continue
        if dedupe:
            key = tuple(cells)
            if key in seen:
                continue
            seen.add(key)
        tidy.append(cells)
    return tidy


def tidy_file(source: TextIO, target: TextIO, dedupe: bool = False) -> int:
    """Read CSV from source, write the tidy CSV to target, and return how many rows were written."""
    rows = tidy_rows(csv.reader(source), dedupe=dedupe)
    csv.writer(target, lineterminator="\n").writerows(rows)
    return len(rows)


def main(argv: List[str]) -> int:
    args = argv[1:]
    dedupe = "--dedupe" in args
    paths = [arg for arg in args if arg != "--dedupe"]
    if len(paths) != 1:
        print("Usage: python tidy_csv.py [--dedupe] input.csv > tidy.csv", file=sys.stderr)
        return 2
    with open(paths[0], newline="", encoding="utf-8") as source:
        tidy_file(source, sys.stdout, dedupe=dedupe)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
