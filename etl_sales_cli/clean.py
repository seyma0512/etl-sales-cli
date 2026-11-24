"""Clean and convert the loaded sales table.

Input: a DataFrame returned by ``load_raw_sales`` (all values are text).
Output: a DataFrame with real numeric and date types, duplicates removed and
city names unified. Values that cannot be converted become missing (NaN/NaT)
instead of being invented.
"""

from __future__ import annotations

import pandas as pd

CITY_NAMES = {
    "lima": "Lima",
    "arequipa": "Arequipa",
    "trujillo": "Trujillo",
    "cusco": "Cusco",
}

# Formats found in the raw export, tried in this order.
DATE_FORMATS = ["%Y-%m-%d", "%d/%m/%Y", "%d-%b-%Y"]


def remove_duplicates(df: pd.DataFrame) -> pd.DataFrame:
    """Drop rows that are exact copies of an earlier row."""
    return df.drop_duplicates(keep="first").reset_index(drop=True)


def parse_price(series: pd.Series) -> pd.Series:
    """Convert prices such as 'S/ 1,250.50' into numbers such as 1250.5."""
    cleaned = (
        series.str.replace("S/", "", regex=False)
        .str.replace(",", "", regex=False)
        .str.strip()
    )
    return pd.to_numeric(cleaned, errors="coerce")


def parse_quantity(series: pd.Series) -> pd.Series:
    """Convert quantities to whole numbers, keeping missing values as <NA>."""
    return pd.to_numeric(series, errors="coerce").astype("Int64")


def parse_dates(series: pd.Series) -> pd.Series:
    """Read dates written in any of the DATE_FORMATS.

    Each format is tried on the values that are still missing. A value that
    matches none of the formats stays missing (NaT).
    """
    result = pd.to_datetime(series, format=DATE_FORMATS[0], errors="coerce")
    for date_format in DATE_FORMATS[1:]:
        result = result.fillna(pd.to_datetime(series, format=date_format, errors="coerce"))
    return result


def normalize_city(series: pd.Series) -> pd.Series:
    """Map spelling variants such as 'lima' or 'LIMA' to the canonical name 'Lima'.

    Unknown cities are kept as they are.
    """
    canonical = series.str.lower().map(CITY_NAMES)
    return canonical.fillna(series)


def clean_sales(df: pd.DataFrame) -> pd.DataFrame:
    """Apply every cleaning rule and return the cleaned table.

    ``quantity_missing`` is True for rows whose quantity was empty or could not
    be read as a number, so they can be reviewed later.
    """
    df = remove_duplicates(df)
    df["quantity_missing"] = df["quantity"].isna()
    df["quantity"] = parse_quantity(df["quantity"])
    df["unit_price"] = parse_price(df["unit_price"])
    df["order_date"] = parse_dates(df["order_date"])
    df["city"] = normalize_city(df["city"])
    return df
