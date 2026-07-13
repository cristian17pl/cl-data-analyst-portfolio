# Data Cleaning: Before & After

**Status: Complete**

## Quick Look

- [Case-study PDF](reports/data-cleaning-before-after-case-study.pdf)
- [Executed notebook](notebooks/clean_retail_orders.ipynb)
- [Reusable cleaning pipeline](scripts/clean_retail_orders.py)
- [Full audited output](cleaned/retail_orders_clean.csv)
- [Publishable records](cleaned/retail_orders_publishable.csv)
- [Manual-review queue](cleaned/retail_orders_review.csv)

## Project Summary

This case study turns a deliberately messy retail-order extract into a reproducible, auditable data product. The pipeline resolves conflicting business keys, normalizes mixed date and numeric formats, standardizes business labels, calculates sales fields, and separates safe-to-publish records from records that require review.

The final design keeps problematic rows visible instead of silently deleting them. Every clean record retains its source, quality status, and issue text so downstream users can trace the decision.

## Results

| Control | Result |
|---|---:|
| Raw rows | 63 |
| Clean business-key rows | 61 |
| Conflicting/repeated rows resolved | 2 |
| Publishable records | 50 |
| Review records retained | 11 |
| Publishable rate | 81.97% |
| Publishable net sales | $4,003.70 |

## Data Source

- Source: `raw/dirty_retail_orders.csv`
- Type: synthetic operational retail-order export
- Purpose: demonstrate realistic cleaning controls without exposing private data
- Grain after cleaning: one row per `order_id`

## Pipeline

1. Profile the source and preserve the raw extract.
2. Normalize whitespace, text casing, dates, currency, percentages, quantities, and booleans.
3. Standardize country, state, city, category, payment, and shipping labels.
4. Resolve repeated order IDs with an explicit source-priority rule: manual adjustments outrank monthly exports.
5. Calculate gross sales, discount amount, and net sales from cleaned fields.
6. Apply field-level quality checks and assign `valid` or `review` status.
7. Write the audited clean layer, publishable subset, review queue, and quality summaries.
8. Run automated validation tests for parser behavior, row contracts, priority rules, and review retention.

## Reproduce

From the repository root:

```powershell
python 04-data-cleaning-before-after/scripts/clean_retail_orders.py
python -m unittest discover -s 04-data-cleaning-before-after/tests -v
```

The notebook uses the same reusable pipeline as the command-line workflow. Its saved outputs show the source profile, transformation results, review queue, before/after examples, validations, and generated files.

## Output Contract

- `retail_orders_clean.csv`: one row per order ID, including audit columns and both quality statuses.
- `retail_orders_publishable.csv`: only records that satisfy the publication rules.
- `retail_orders_review.csv`: retained exceptions requiring a business or source-system decision.
- `data_quality_summary.csv`: headline row counts, rates, and publishable revenue.
- `data_quality_issues.csv`: frequency of each quality issue for remediation prioritization.

## Repository Structure

```text
04-data-cleaning-before-after/
|-- README.md
|-- raw/
|   |-- README.md
|   `-- dirty_retail_orders.csv
|-- notebooks/
|   `-- clean_retail_orders.ipynb
|-- scripts/
|   |-- __init__.py
|   `-- clean_retail_orders.py
|-- tests/
|   `-- test_clean_retail_orders.py
|-- cleaned/
|   |-- data_quality_issues.csv
|   |-- data_quality_summary.csv
|   |-- retail_orders_clean.csv
|   |-- retail_orders_publishable.csv
|   `-- retail_orders_review.csv
|-- docs/
|   |-- cleaning-log.md
|   `-- dirty-data-profile.md
|-- reports/
|   `-- data-cleaning-before-after-case-study.pdf
|-- tools/
|   `-- build_cleaning_case_study_pdf.py
`-- requirements.txt
```

---

This project is part of the [Data Analyst Portfolio](../README.md).
