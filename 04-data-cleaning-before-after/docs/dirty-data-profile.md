# Dirty Data Profile

Source file: `../raw/dirty_retail_orders.csv`

## Purpose

This is the immutable "before" dataset for the cleaning case study. It mimics an operational retail-order export assembled from monthly extracts and manual adjustments.

## Known Data Quality Issues

| Issue type | Examples in raw file | Implemented control |
|---|---|---|
| Repeated/conflicting business key | `ORD-1035` appears more than once with different note text | Keep one order-level record using deterministic source priority |
| Manual adjustment conflict | `ORD-1002` appears in an export and in `manual_adjustment.csv` | Manual adjustment outranks monthly export |
| Date format inconsistency | `2025-01-03`, `01/05/2025`, `2025/01/07`, `02-03-2025` | Parse recognized formats into ISO `yyyy-mm-dd` |
| Invalid or ambiguous date | `2025-02-30` and ambiguous day/month values | Retain blank canonical date and route the row to review |
| Missing values | blank email, quantity, price, SKU, customer ID, or delivery date | Apply field-specific validation; do not use blanket imputation |
| Messy geography | `USA`, `U.S.`, `United States`, `HN`, `México`; `Cortes` vs `Cortés`; `FM` | Map aliases to canonical location labels |
| Category inconsistency | `Home & Kitchen`, `home/kitchen`, `Home and Kitchen`, `home` | Map raw values to canonical categories |
| Numeric formatting | `$18.50`, `USD 45.00`, `1,299.00`, `10 %`, `5%` | Strip presentation text and cast to typed numeric fields |
| Invalid numeric values | quantity `two`, quantity `-1`, price `-15.00`, negative discount | Preserve the record in the review queue with issue codes |
| Status inconsistency | `Paid`, `paid`, `PAID`; `Cash on Delivery` variants | Normalize casing and known values |
| Boolean inconsistency | `N`, `No`, `false`, `0`, `Y` | Convert recognized tokens to nullable booleans |
| Invalid email | `luis.medina[at]example.com` | Flag invalid contact data without blocking unrelated fields |

## Clean-Layer Contract

The audited clean output keeps the business fields plus calculated and control columns:

- canonical identifiers, dates, customer, location, product, payment, and shipping fields;
- typed `quantity`, `unit_price`, and `discount_rate`;
- calculated `gross_sales`, `discount_amount`, and `net_sales`;
- `record_quality_status` and `quality_issues`;
- retained source metadata for traceability.

The pipeline writes three record-level products:

1. `retail_orders_clean.csv`: all resolved business-key records.
2. `retail_orders_publishable.csv`: records that pass publication rules.
3. `retail_orders_review.csv`: retained exceptions requiring a business decision.

## Decisions

- Invalid dates and invalid numeric values are never guessed.
- Missing prices are not imputed from SKU averages because the sample does not establish a reliable price-history rule.
- Guest orders remain eligible for revenue when their required transaction fields are valid.
- Repeated order IDs are resolved by explicit source priority rather than input order.
- Exception records stay in the audited output and review queue; they are not silently discarded.
