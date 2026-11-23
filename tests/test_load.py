import pandas as pd

from etl_sales_cli.load import load_raw_sales, normalize_column_name


def test_normalize_column_name_handles_spaces_and_case():
    assert normalize_column_name(" Order ID ") == "order_id"
    assert normalize_column_name("ORDER_DATE") == "order_date"
    assert normalize_column_name("Unit Price") == "unit_price"


def test_load_raw_sales_normalizes_headers_and_text(tmp_path):
    raw = tmp_path / "raw.csv"
    raw.write_text(
        " Order ID ,ORDER_DATE,City,Quantity\n"
        "ORD-1,2024-01-05,  lima ,3\n"
        "ORD-2,05/01/2024,LIMA,\n",
        encoding="utf-8",
    )

    df = load_raw_sales(raw)

    assert list(df.columns) == ["order_id", "order_date", "city", "quantity"]
    assert df.loc[0, "city"] == "lima"
    assert df.loc[1, "city"] == "LIMA"


def test_load_raw_sales_keeps_missing_values_and_reads_text(tmp_path):
    raw = tmp_path / "raw.csv"
    raw.write_text("order_id,quantity\nORD-1,\nORD-2,7\n", encoding="utf-8")

    df = load_raw_sales(raw)

    assert pd.isna(df.loc[0, "quantity"])
    assert df.loc[1, "quantity"] == "7"
