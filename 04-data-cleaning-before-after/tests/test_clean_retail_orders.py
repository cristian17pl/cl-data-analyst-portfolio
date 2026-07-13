from __future__ import annotations

from pathlib import Path
import sys
import unittest

import pandas as pd


PROJECT_DIR = Path(__file__).resolve().parents[1]
if str(PROJECT_DIR) not in sys.path:
    sys.path.insert(0, str(PROJECT_DIR))

from scripts.clean_retail_orders import (  # noqa: E402
    CATEGORY_MAP,
    apply_quality_rules,
    build_clean_orders,
    calculate_order_values,
    clean_discount,
    clean_money,
    clean_quantity,
    load_raw_orders,
    map_value,
    parse_mixed_date,
    run_pipeline,
    standardize_orders,
)


class CleaningFunctionTests(unittest.TestCase):
    def test_mixed_date_parser(self) -> None:
        self.assertEqual(parse_mixed_date("2025/01/07"), pd.Timestamp("2025-01-07"))
        self.assertTrue(pd.isna(parse_mixed_date("2025-02-30")))

    def test_numeric_cleaners(self) -> None:
        self.assertEqual(clean_money("USD 1,299.00"), 1299.0)
        self.assertEqual(clean_quantity("two"), 2.0)
        self.assertEqual(clean_discount("5%"), 0.05)

    def test_category_mapping(self) -> None:
        self.assertEqual(map_value("home/kitchen", CATEGORY_MAP), "Home & Kitchen")

    def test_pipeline_contracts(self) -> None:
        result = run_pipeline(PROJECT_DIR, write_output_files=False)
        clean = result["clean"]
        self.assertEqual(len(result["raw"]), 63)
        self.assertEqual(len(clean), 61)
        self.assertFalse(clean["order_id"].duplicated().any())
        self.assertEqual(len(result["publishable"]), 50)
        self.assertEqual(len(result["review"]), 11)

    def test_manual_adjustment_wins_order_conflict(self) -> None:
        result = run_pipeline(PROJECT_DIR, write_output_files=False)
        selected = result["clean"].loc[result["clean"]["order_id"] == "ORD-1002"].iloc[0]
        self.assertEqual(selected["source_file"], "manual_adjustment.csv")

    def test_review_flags_are_retained(self) -> None:
        raw = load_raw_orders(PROJECT_DIR / "raw" / "dirty_retail_orders.csv")
        staged = apply_quality_rules(calculate_order_values(standardize_orders(raw)))
        clean = build_clean_orders(staged)
        negative_price = clean.loc[clean["order_id"] == "ORD-1048"].iloc[0]
        self.assertEqual(negative_price["record_quality_status"], "review")
        self.assertIn("negative_unit_price", negative_price["quality_issues"])


if __name__ == "__main__":
    unittest.main()
