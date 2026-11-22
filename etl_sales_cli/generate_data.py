"""Generate a synthetic, deliberately messy sales CSV for testing the pipeline.

The output contains the kinds of problems found in real data: duplicated rows,
missing values, mixed date formats, numbers stored as text, inconsistent
category spelling, messy headers and a few extreme values (outliers).

Run from the project root:

    python -m etl_sales_cli.generate_data                 # random seed
    python -m etl_sales_cli.generate_data --seed 42       # reproducible run
"""

from __future__ import annotations

import argparse
import csv
import random
from datetime import date, timedelta
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUTPUT = PROJECT_ROOT / "data" / "raw" / "sales_messy.csv"

PRODUCTS = {
    "Laptop": 2800.0,
    "Monitor": 650.0,
    "Keyboard": 90.0,
    "Mouse": 45.0,
    "Headset": 210.0,
    "Webcam": 180.0,
}

# Each city appears with several spellings, as it would in raw exports.
CITY_VARIANTS = {
    "Lima": ["Lima", "lima ", "LIMA", " Lima"],
    "Arequipa": ["Arequipa", "AREQUIPA", "arequipa"],
    "Trujillo": ["Trujillo", "trujillo  ", "Trujillo "],
    "Cusco": ["Cusco", "cusco", "CUSCO"],
}

DATE_FORMATS = [
    "%Y-%m-%d",   # 2024-03-05
    "%d/%m/%Y",   # 05/03/2024
    "%d-%b-%Y",   # 05-Mar-2024
]

HEADER = [" Order ID ", "ORDER_DATE", "City", "Product", "Quantity", "Unit Price"]


def _random_date(rng: random.Random, start: date, days: int) -> date:
    return start + timedelta(days=rng.randrange(days))


def _format_date(rng: random.Random, value: date) -> str:
    fmt = rng.choice(DATE_FORMATS)
    return value.strftime(fmt)


def _format_price(rng: random.Random, value: float) -> str:
    # Mix numeric values with text values such as "S/ 1,250.50".
    if rng.random() < 0.3:
        return f"S/ {value:,.2f}"
    return f"{value:.2f}"


def generate_rows(rows: int, seed: int) -> list[list[str]]:
    """Return the messy data rows (without header) for the given seed."""
    rng = random.Random(seed)
    start = date(2024, 1, 1)
    span_days = 730  # two years of sales

    data: list[list[str]] = []
    for order_number in range(1, rows + 1):
        product = rng.choice(list(PRODUCTS))
        unit_price = PRODUCTS[product] * rng.uniform(0.9, 1.1)

        # About 1% of prices are extreme values, to test outlier detection later.
        if rng.random() < 0.01:
            unit_price *= 20

        quantity: str
        if rng.random() < 0.05:
            quantity = ""  # missing value
        else:
            quantity = str(rng.randint(1, 10))

        city = rng.choice(list(CITY_VARIANTS))
        city_text = rng.choice(CITY_VARIANTS[city])

        order_date = _random_date(rng, start, span_days)

        data.append(
            [
                f"ORD-{order_number:05d}",
                _format_date(rng, order_date),
                city_text,
                product,
                quantity,
                _format_price(rng, unit_price),
            ]
        )

    # Duplicate about 3% of the rows, as happens with repeated exports.
    duplicates = [row[:] for row in rng.sample(data, k=max(1, rows // 33))]
    data.extend(duplicates)
    rng.shuffle(data)
    return data


def write_csv(output: Path, rows: int, seed: int) -> int:
    """Write the messy CSV to ``output`` and return the number of data rows written."""
    data = generate_rows(rows, seed)
    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow(HEADER)
        writer.writerows(data)
    return len(data)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Generate a messy sales CSV for testing.")
    parser.add_argument(
        "--seed",
        type=int,
        default=None,
        help="Random seed. Omit it to get a different file on every run.",
    )
    parser.add_argument("--rows", type=int, default=500, help="Number of unique orders (default: 500).")
    parser.add_argument(
        "--output",
        type=Path,
        default=DEFAULT_OUTPUT,
        help=f"Output CSV path (default: {DEFAULT_OUTPUT}).",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    if args.rows < 1:
        raise SystemExit("--rows must be at least 1")

    # Pick a random seed when none is given, but always print the one used,
    # so any run can be reproduced later with --seed.
    seed = args.seed if args.seed is not None else random.SystemRandom().randrange(10**6)

    written = write_csv(args.output, args.rows, seed)
    print(f"Seed used: {seed}")
    print(f"Rows written: {written}")
    print(f"Output: {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
