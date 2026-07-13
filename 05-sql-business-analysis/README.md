# SQL Business Analysis - Olist E-Commerce

**Status: Complete**

## Quick Look

- [SQL case-study PDF](reports/olist-sql-business-analysis.pdf)
- [Business findings](docs/findings-summary.md)
- [Entity-relationship diagram](docs/erd.md)
- [Query result extracts](results/)
- [PostgreSQL schema](schema/01_create_schema.sql)

## Project Summary

This project answers ten commercial and operational questions against Olist's public Brazilian e-commerce dataset. The analysis covers revenue, geography, category mix, customer value, delivery performance, payments, reviews, seller quality, retention, and basket pairs.

The work emphasizes fact-grain discipline: item revenue, order delivery, payments, and reviews are not joined indiscriminately. Review and seller analyses establish an order-level layer first so duplicated source reviews and multi-item orders do not overstate outcomes.

## Headline Findings

- **R$15.42M** delivered-order revenue including freight; São Paulo contributes **37.4%**.
- The top five states contribute **73.2%** of delivered revenue.
- Late orders average **2.57 stars**, versus **4.29** for on-time/early orders.
- Credit cards represent **78.46%** of delivered payment value.
- Repeat customers produce only **5.6%** of revenue, but their average lifetime value is almost twice that of one-time customers.

## Data Source

- Dataset: [Brazilian E-Commerce Public Dataset by Olist](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce)
- Scope: approximately 100,000 anonymized marketplace orders from 2016-2018
- Tables: customers, orders, items, payments, reviews, products, sellers, category translation, and geolocation
- Raw CSVs: downloaded locally and intentionally excluded from version control

## Business Questions

1. Which states generate the most revenue?
2. Which categories drive revenue and unit volume?
3. How does category revenue change over time?
4. Which customers have the highest lifetime value?
5. Where is delivery performance weakest?
6. How does payment-method and installment behavior differ?
7. How are delivery outcomes associated with review scores?
8. Which sellers balance revenue, reviews, and delivery reliability?
9. How much revenue comes from repeat customers?
10. Which categories are most frequently purchased together?

## Reproduce

### PostgreSQL

After placing the source CSVs in `raw/`:

```sql
\i schema/01_create_schema.sql
\i schema/02_load_csvs.sql
\i schema/03_validate_load.sql
```

Run each file in `queries/` to answer the corresponding business question.

### Lightweight local execution

The query suite is also executable through DuckDB without a database server:

```powershell
python 05-sql-business-analysis/tools/run_sql_analysis.py
```

The runner validates expected row counts and foreign-key coverage, executes all ten SQL files, and refreshes the committed CSVs in `results/`.

## Technical Highlights

- CTEs and window functions for reusable analytical layers and running revenue.
- Filtered aggregates for late-delivery rates.
- Separate fact paths for item revenue and payment value.
- Review aggregation to order grain before experience analysis.
- Seller-order bridge to keep reviews and delivery outcomes order-weighted.
- Stable customer identity through `customer_unique_id`.
- Self-join at the distinct order-category grain for basket pairs.

## Repository Structure

```text
05-sql-business-analysis/
|-- README.md
|-- raw/                         # local source CSVs; git-ignored
|-- schema/
|   |-- 01_create_schema.sql
|   |-- 02_load_csvs.sql
|   `-- 03_validate_load.sql
|-- queries/                     # ten business-question SQL files
|-- results/                     # validated query result extracts
|-- docs/
|   |-- erd.md
|   `-- findings-summary.md
|-- reports/
|   `-- olist-sql-business-analysis.pdf
|-- tools/
|   |-- run_sql_analysis.py
|   `-- build_sql_case_study_pdf.py
`-- requirements.txt
```

---

This project is part of the [Data Analyst Portfolio](../README.md).
