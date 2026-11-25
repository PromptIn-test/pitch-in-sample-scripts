# pitch-in-sample-scripts

> **Sample data.** A small Python script used to test Pitch In with automation work. The example CSV is made up, and nothing here is maintained.

`tidy_csv.py` cleans up a CSV export: it trims spaces around every cell and drops blank rows.

```
python tidy_csv.py examples/contacts.csv > tidy.csv
```

Tests: `python -m unittest discover -s tests -t .` (standard library only). `PROJECT_BRIEF.md` is what coding agents read first.
