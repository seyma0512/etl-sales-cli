from etl_sales_cli.generate_data import HEADER, generate_rows, write_csv


def test_same_seed_produces_identical_file(tmp_path):
    first = tmp_path / "first.csv"
    second = tmp_path / "second.csv"

    write_csv(first, rows=100, seed=42)
    write_csv(second, rows=100, seed=42)

    assert first.read_bytes() == second.read_bytes()


def test_different_seeds_produce_different_data():
    assert generate_rows(100, seed=1) != generate_rows(100, seed=2)


def test_output_contains_header_and_messy_rows(tmp_path):
    output = tmp_path / "sales.csv"

    written = write_csv(output, rows=200, seed=7)

    lines = output.read_text(encoding="utf-8").splitlines()
    assert lines[0].split(",") == HEADER
    assert len(lines) - 1 == written
    # Duplicates are added on purpose, so there are more rows than unique orders.
    assert written > 200
