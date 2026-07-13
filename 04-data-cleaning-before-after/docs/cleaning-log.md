# Cleaning Log

Generated on: 2026-07-12

## Outputs

- Full cleaned dataset with audit status: `cleaned/retail_orders_clean.csv`
- Publishable valid records: `cleaned/retail_orders_publishable.csv`
- Review queue: `cleaned/retail_orders_review.csv`
- Data-quality KPI summary: `cleaned/data_quality_summary.csv`
- Issue-frequency summary: `cleaned/data_quality_issues.csv`

## Decisions

- Manual adjustment rows outrank monthly export rows when an order ID conflicts.
- Unknown or impossible dates remain blank and are flagged instead of guessed.
- Negative quantities, prices, and discounts are retained in the review queue, not published silently.
- Revenue is calculated from cleaned quantity, unit price, and discount rate.
- Every output row retains source, quality status, and issue text for traceability.
