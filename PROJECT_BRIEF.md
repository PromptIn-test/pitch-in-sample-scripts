# Project brief: pitch-in-sample-scripts

> Sample data, written to the Pitch In project-brief template.

## What the project does

A small command-line script, `tidy_csv.py`, that cleans up CSV exports: it trims spaces around every cell and drops blank rows. It is a throwaway repo for testing Pitch In with automation work. It has no users.

## Stack and versions

- Python 3.12 or newer (CI uses 3.12), standard library only.
- Tests use `unittest`. No dependencies.

## Setup and test commands

```
python -m unittest discover -s tests -t .
```

There is nothing to install. Run the script with `python tidy_csv.py examples/contacts.csv`.

## Repo map

- `tidy_csv.py`: the script; `tidy_rows` and `tidy_file` hold the logic, `main` handles the command line
- `tests/test_tidy_csv.py`: tests for each function
- `examples/contacts.csv`: a made-up example export (sample data)
- `.github/workflows/ci.yml`: CI, runs the tests

## Conventions

- Functions are small, pure where possible, with a one-line docstring.
- Names in snake_case; type hints on public functions.
- Command-line usage goes in the module docstring and in `README.md`.
- Tests: one `unittest.TestCase` per function, test names start with the function name.
- Commits: one short imperative line.

## Definition of done

- The test command passes.
- New behaviour has tests; changed behaviour has updated tests.
- `README.md` shows any new command-line flag with one example.
- No new dependencies.
