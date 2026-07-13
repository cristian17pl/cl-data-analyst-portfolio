"""Load local Olist CSVs into DuckDB and export every business-query result.

The portfolio SQL targets PostgreSQL. DuckDB is used as a lightweight local
execution harness because the selected analytical syntax is compatible across
both engines. Raw CSVs remain git-ignored; exported result tables are committed.
"""

from __future__ import annotations

import argparse
from pathlib import Path

import duckdb
import pandas as pd


TABLE_FILES = {
    "customers": "olist_customers_dataset.csv",
    "geolocation": "olist_geolocation_dataset.csv",
    "sellers": "olist_sellers_dataset.csv",
    "products": "olist_products_dataset.csv",
    "product_category_translation": "product_category_name_translation.csv",
    "orders": "olist_orders_dataset.csv",
    "order_items": "olist_order_items_dataset.csv",
    "order_payments": "olist_order_payments_dataset.csv",
    "order_reviews": "olist_order_reviews_dataset.csv",
}


def load_tables(connection: duckdb.DuckDBPyConnection, raw_dir: Path) -> None:
    missing = [name for name in TABLE_FILES.values() if not (raw_dir / name).exists()]
    if missing:
        raise FileNotFoundError("Missing Olist source files: " + ", ".join(missing))

    for table, filename in TABLE_FILES.items():
        path = (raw_dir / filename).as_posix().replace("'", "''")
        connection.execute(
            f"CREATE OR REPLACE TABLE {table} AS "
            f"SELECT * FROM read_csv_auto('{path}', header=true, sample_size=-1)"
        )


def validate(
    connection: duckdb.DuckDBPyConnection, result_dir: Path
) -> None:
    expected_counts = {
        "customers": 99441,
        "geolocation": 1000163,
        "order_items": 112650,
        "order_payments": 103886,
        "order_reviews": 99224,
        "orders": 99441,
        "products": 32951,
        "sellers": 3095,
        "product_category_translation": 71,
    }
    row_results = []
    for table, expected in expected_counts.items():
        actual = connection.execute(f"SELECT COUNT(*) FROM {table}").fetchone()[0]
        row_results.append(
            {"check_type": "row_count", "check_name": table, "actual": actual, "expected": expected, "status": "pass" if actual == expected else "fail"}
        )
        if actual != expected:
            raise ValueError(f"{table}: expected {expected:,} rows, found {actual:,}")

    checks = {
        "orders_without_customer": "SELECT COUNT(*) FROM orders o LEFT JOIN customers c USING (customer_id) WHERE c.customer_id IS NULL",
        "items_without_order": "SELECT COUNT(*) FROM order_items oi LEFT JOIN orders o USING (order_id) WHERE o.order_id IS NULL",
        "items_without_product": "SELECT COUNT(*) FROM order_items oi LEFT JOIN products p USING (product_id) WHERE p.product_id IS NULL",
        "items_without_seller": "SELECT COUNT(*) FROM order_items oi LEFT JOIN sellers s USING (seller_id) WHERE s.seller_id IS NULL",
        "payments_without_order": "SELECT COUNT(*) FROM order_payments op LEFT JOIN orders o USING (order_id) WHERE o.order_id IS NULL",
        "reviews_without_order": "SELECT COUNT(*) FROM order_reviews r LEFT JOIN orders o USING (order_id) WHERE o.order_id IS NULL",
    }
    orphan_results = {name: connection.execute(sql).fetchone()[0] for name, sql in checks.items()}
    for name, count in orphan_results.items():
        row_results.append(
            {"check_type": "orphan_count", "check_name": name, "actual": count, "expected": 0, "status": "pass" if count == 0 else "fail"}
        )
    repeated_reviews = connection.execute(
        "SELECT COUNT(*) FROM (SELECT order_id FROM order_reviews GROUP BY order_id HAVING COUNT(*) > 1)"
    ).fetchone()[0]
    row_results.append(
        {"check_type": "diagnostic", "check_name": "orders_with_multiple_review_rows", "actual": repeated_reviews, "expected": None, "status": "informational"}
    )
    result_dir.mkdir(parents=True, exist_ok=True)
    pd.DataFrame(row_results).to_csv(result_dir / "00_load_validation.csv", index=False)

    failures = {name: count for name, count in orphan_results.items() if count}
    if failures:
        raise ValueError(f"Referential validation failed: {failures}")


def run_queries(connection: duckdb.DuckDBPyConnection, query_dir: Path, result_dir: Path) -> None:
    result_dir.mkdir(parents=True, exist_ok=True)
    for query_path in sorted(query_dir.glob("*.sql")):
        result = connection.execute(query_path.read_text(encoding="utf-8")).fetchdf()
        output_path = result_dir / f"{query_path.stem}.csv"
        result.to_csv(output_path, index=False)
        print(f"{query_path.name}: {len(result):,} rows -> {output_path.name}")


def main() -> None:
    project_dir = Path(__file__).resolve().parents[1]
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--raw-dir", type=Path, default=project_dir / "raw")
    parser.add_argument("--result-dir", type=Path, default=project_dir / "results")
    args = parser.parse_args()

    connection = duckdb.connect()
    load_tables(connection, args.raw_dir)
    validate(connection, args.result_dir)
    run_queries(connection, project_dir / "queries", args.result_dir)


if __name__ == "__main__":
    main()
