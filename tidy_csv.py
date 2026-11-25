"""Tidy a CSV export: trim spaces around every cell and drop blank rows.

Usage:
    python tidy_csv.py input.csv > tidy.csv

Sample data: a small script used to test Pitch In with automation work.
"""

import csv
import sys
from typing import Iterable, List, TextIO


def tidy_rows(rows: Iterable[List[str]]) -> List[List[str]]:
    """Trim spaces around every cell and drop rows whose cells are all empty."""
    tidy = []
    for row in rows:
        cells = [cell.strip() for cell in row]
        if any(cells):
            tidy.append(cells)
    return tidy


def tidy_file(source: TextIO, target: TextIO) -> int:
    """Read CSV from source, write the tidy CSV to target, and return how many rows were written."""
    rows = tidy_rows(csv.reader(source))
    csv.writer(target, lineterminator="\n").writerows(rows)
    return len(rows)


def main(argv: List[str]) -> int:
    if len(argv) != 2:
        print("Usage: python tidy_csv.py input.csv > tidy.csv", file=sys.stderr)
        return 2
    with open(argv[1], newline="", encoding="utf-8") as source:
        tidy_file(source, sys.stdout)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
