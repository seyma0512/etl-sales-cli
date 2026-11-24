import pandas as pd

from etl_sales_cli.clean import (
    clean_sales,
    normalize_city,
    parse_dates,
    parse_price,
    parse_quantity,
    remove_duplicates,
)


def test_remove_duplicates_drops_exact_copies():
    df = pd.DataFrame({"order_id": ["A", "A", "B"], "city": ["Lima", "Lima", "Cusco"]})

    result = remove_duplicates(df)

    assert len(result) == 2


def test_parse_price_removes_currency_and_thousands_separator():
    prices = pd.Series(["S/ 1,250.50", "43.55", None])

    result = parse_price(prices)

    assert result.iloc[0] == 1250.5
    assert result.iloc[1] == 43.55
    assert pd.isna(result.iloc[2])


def test_parse_quantity_keeps_missing_values_as_missing():
    quantities = pd.Series(["4", None, "7"])

    result = parse_quantity(quantities)

    assert result.dtype == "Int64"
    assert result.iloc[0] == 4
    assert pd.isna(result.iloc[1])


def test_parse_dates_reads_every_supported_format():
    dates = pd.Series(["2025-03-10", "27/05/2024", "15-May-2024", "no es fecha"])

    result = parse_dates(dates)

    assert result.iloc[0] == pd.Timestamp("2025-03-10")
    assert result.iloc[1] == pd.Timestamp("2024-05-27")
    assert result.iloc[2] == pd.Timestamp("2024-05-15")
    assert pd.isna(result.iloc[3])


def test_normalize_city_unifies_spellings():
    cities = pd.Series(["lima", "LIMA", "Lima", "Cusco", "cusco"])

    result = normalize_city(cities)

    assert result.tolist() == ["Lima", "Lima", "Lima", "Cusco", "Cusco"]


def test_clean_sales_removes_duplicates_and_flags_missing_quantity():
    df = pd.DataFrame(
        {
            "order_id": ["ORD-1", "ORD-1", "ORD-2"],
            "order_date": ["2024-01-05", "2024-01-05", "05/01/2024"],
            "city": ["lima", "lima", "LIMA"],
            "product": ["Mouse", "Mouse", "Monitor"],
            "quantity": ["3", "3", None],
            "unit_price": ["S/ 45.00", "S/ 45.00", "650.00"],
        }
    )

    result = clean_sales(df)

    assert len(result) == 2
    assert result["quantity_missing"].tolist() == [False, True]
    assert result["city"].tolist() == ["Lima", "Lima"]
    assert result["unit_price"].tolist() == [45.0, 650.0]
    assert result.loc[0, "order_date"] == pd.Timestamp("2024-01-05")
    assert pd.isna(result.loc[1, "quantity"])
