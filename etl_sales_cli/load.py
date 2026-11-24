"""Load raw sales data and normalize column names and text values.

This stage only standardizes the structure of the data: column names and
surrounding whitespace. Type conversion (dates, prices) and business rules
(category mapping, duplicates, outliers) happen in later stages.
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd


def normalize_column_name(name: str) -> str:
    """Turn a raw header such as ' Order ID ' into 'order_id'."""
    return name.strip().lower().replace(" ", "_")


def load_raw_sales(path: Path) -> pd.DataFrame:
    """Read a raw sales CSV and return it with normalized columns and text.

    Every column is read as text (``dtype=str``) so no value is changed before
    it is cleaned explicitly. Missing values stay as missing (NaN).
    """
    df = pd.read_csv(path, encoding="utf-8", dtype=str)

    df.columns = [normalize_column_name(column_name) for column_name in df.columns]

    for column_name in df.columns:
        if pd.api.types.is_string_dtype(df[column_name]):
            df[column_name] = df[column_name].str.strip()

    return df
