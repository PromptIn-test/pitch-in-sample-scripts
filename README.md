# pitch-in-sample-scripts

> **Sample data.** A small Python script used to test Pitch In with automation work. The example CSV is made up, and nothing here is maintained.

`tidy_csv.py` cleans up a CSV export: it trims spaces around every cell and drops blank rows.

```
python tidy_csv.py examples/contacts.csv > tidy.csv
```

Add `--dedupe` to also drop rows that are exact duplicates after tidying (the first copy is kept; the header row counts like any other row):

```
python tidy_csv.py --dedupe examples/contacts.csv > tidy.csv
```

Tests: `python -m unittest discover -s tests -t .` (standard library only). `PROJECT_BRIEF.md` is what coding agents read first.
