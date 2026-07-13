-- Run this file from the 05-sql-business-analysis folder after placing
-- the Kaggle CSV files in ./raw.
--
-- Example:
--   psql -d olist_business_analysis
--   \i schema/01_create_schema.sql
--   \i schema/02_load_csvs.sql

SET client_encoding = 'UTF8';

\copy customers FROM 'raw/olist_customers_dataset.csv' WITH (FORMAT CSV, HEADER true, ENCODING 'UTF8');
\copy geolocation FROM 'raw/olist_geolocation_dataset.csv' WITH (FORMAT CSV, HEADER true, ENCODING 'UTF8');
\copy sellers FROM 'raw/olist_sellers_dataset.csv' WITH (FORMAT CSV, HEADER true, ENCODING 'UTF8');
\copy products FROM 'raw/olist_products_dataset.csv' WITH (FORMAT CSV, HEADER true, ENCODING 'UTF8');
\copy product_category_translation FROM 'raw/product_category_name_translation.csv' WITH (FORMAT CSV, HEADER true, ENCODING 'UTF8');
\copy orders FROM 'raw/olist_orders_dataset.csv' WITH (FORMAT CSV, HEADER true, ENCODING 'UTF8');
\copy order_items FROM 'raw/olist_order_items_dataset.csv' WITH (FORMAT CSV, HEADER true, ENCODING 'UTF8');
\copy order_payments FROM 'raw/olist_order_payments_dataset.csv' WITH (FORMAT CSV, HEADER true, ENCODING 'UTF8');
\copy order_reviews FROM 'raw/olist_order_reviews_dataset.csv' WITH (FORMAT CSV, HEADER true, ENCODING 'UTF8');

ANALYZE customers;
ANALYZE geolocation;
ANALYZE sellers;
ANALYZE products;
ANALYZE product_category_translation;
ANALYZE orders;
ANALYZE order_items;
ANALYZE order_payments;
ANALYZE order_reviews;
