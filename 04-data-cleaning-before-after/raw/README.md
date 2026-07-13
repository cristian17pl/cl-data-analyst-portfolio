# Raw Data

This folder contains the starting point for the data cleaning project.

## File

- `dirty_retail_orders.csv` - intentionally dirty retail order extract

## Important

Treat this file as immutable source data. Cleaning logic should read from this folder and write outputs to `../cleaned/`.

Known issue types include:

- duplicate rows
- repeated order IDs with conflicting details
- inconsistent date formats
- impossible dates
- missing customer/product fields
- inconsistent country, state, city, category, and status values
- currency symbols and text in numeric fields
- negative or invalid quantities/prices
- mixed boolean values for return flags
