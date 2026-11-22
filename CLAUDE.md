# CLAUDE.md

Project instructions for Claude Code. Keep this file focused on rules that apply to everyone working on the repo.

## Project

`etl-sales-cli` is a command-line ETL tool that cleans messy sales CSV files, flags outliers with IQR, and exports to CSV and Parquet. It is built in stages; see the roadmap in `README.md`. Do not implement a later stage before the current one is done and reviewed.

## Commands

```powershell
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python -m pytest
```

The CLI entry point is planned as `python -m etl_sales_cli`; it does not exist yet.

## Structure

- `etl_sales_cli/`: package with the pipeline code.
- `data/raw/`: input files. Never modify them.
- `data/processed/`: generated outputs. Safe to delete and regenerate.
- `notebooks/`: exploratory analysis only. Pipeline logic belongs in the package.
- `tests/`: unit tests.

## Code conventions

- Use English for code, identifiers, comments, commit messages and `README.md`.
- Use `snake_case` for functions and variables, and type hints on public functions.
- Public functions get a short docstring that says what they do and why.
- Do not delete outliers. Flag them in an `is_outlier` column and document the rule.
- Every cleaning rule must be explicit and covered by a test.

## Git

- Make small commits with imperative English messages, for example `Add IQR outlier flag`.
- Do not push, create remote repositories or change repository visibility without asking first.
- Do not add dependencies to `requirements.txt` without a reason written in the commit message.
