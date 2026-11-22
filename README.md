# etl-sales-cli

[Versión en español](README.es.md)

A command-line ETL tool that cleans messy sales data from CSV files, validates it, and exports the result to CSV and Parquet.

> **Status:** early development. The project is being built in stages, following the course *Ingeniería de Datos* (Module 1: Python and data manipulation).

## Goals

- Load a raw CSV with inconsistent formats (dates, numbers, categories, duplicates, nulls).
- Clean and normalize the data with explicit, documented rules.
- Flag statistical outliers using the IQR method, without silently deleting them.
- Export the result to CSV and Parquet.
- Run everything from the terminal, so it can later run on a server without a GUI.

## Planned stages

1. Generate a synthetic messy sales CSV for testing.
2. Load and normalize the data with pandas.
3. Clean and transform (duplicates, nulls, categories, `groupby`, `merge`).
4. Vectorized calculations with NumPy.
5. Descriptive statistics and IQR outlier detection.
6. Exploratory data analysis in a Jupyter notebook.
7. Export to CSV and Parquet.
8. Wrap everything in a reusable CLI.

## Project structure

```
etl-sales-cli/
├── etl_sales_cli/     # package with the pipeline code
├── data/
│   ├── raw/           # input CSV files (not versioned)
│   └── processed/     # cleaned outputs (not versioned)
├── notebooks/         # EDA notebooks
├── tests/             # unit tests
├── requirements.txt
└── README.md
```

## Setup

Requires Python 3.11 or newer.

```powershell
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

## Usage

Not implemented yet. The planned interface is:

```powershell
python -m etl_sales_cli data/raw/sales_messy.csv --output data/processed/sales_clean
```

## License

MIT. See [LICENSE](LICENSE).
