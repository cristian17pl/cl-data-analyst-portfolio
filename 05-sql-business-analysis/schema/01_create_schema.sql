-- PostgreSQL schema for the Olist Brazilian E-Commerce dataset.
-- Grain follows the original CSV files so the analysis stays close to the source.

DROP TABLE IF EXISTS order_reviews;
DROP TABLE IF EXISTS order_payments;
DROP TABLE IF EXISTS order_items;
DROP TABLE IF EXISTS orders;
DROP TABLE IF EXISTS product_category_translation;
DROP TABLE IF EXISTS products;
DROP TABLE IF EXISTS sellers;
DROP TABLE IF EXISTS geolocation;
DROP TABLE IF EXISTS customers;

CREATE TABLE customers (
    customer_id VARCHAR(40) PRIMARY KEY,
    customer_unique_id VARCHAR(40) NOT NULL,
    customer_zip_code_prefix INTEGER,
    customer_city TEXT,
    customer_state CHAR(2)
);

CREATE TABLE geolocation (
    geolocation_zip_code_prefix INTEGER,
    geolocation_lat NUMERIC(10, 6),
    geolocation_lng NUMERIC(10, 6),
    geolocation_city TEXT,
    geolocation_state CHAR(2)
);

CREATE TABLE sellers (
    seller_id VARCHAR(40) PRIMARY KEY,
    seller_zip_code_prefix INTEGER,
    seller_city TEXT,
    seller_state CHAR(2)
);

CREATE TABLE products (
    product_id VARCHAR(40) PRIMARY KEY,
    product_category_name TEXT,
    -- Source CSV uses "lenght"; keep the original header spelling for direct loads.
    product_name_lenght INTEGER,
    product_description_lenght INTEGER,
    product_photos_qty INTEGER,
    product_weight_g INTEGER,
    product_length_cm INTEGER,
    product_height_cm INTEGER,
    product_width_cm INTEGER
);

CREATE TABLE product_category_translation (
    product_category_name TEXT PRIMARY KEY,
    product_category_name_english TEXT
);

CREATE TABLE orders (
    order_id VARCHAR(40) PRIMARY KEY,
    customer_id VARCHAR(40) NOT NULL REFERENCES customers(customer_id),
    order_status TEXT,
    order_purchase_timestamp TIMESTAMP,
    order_approved_at TIMESTAMP,
    order_delivered_carrier_date TIMESTAMP,
    order_delivered_customer_date TIMESTAMP,
    order_estimated_delivery_date TIMESTAMP
);

CREATE TABLE order_items (
    order_id VARCHAR(40) NOT NULL REFERENCES orders(order_id),
    order_item_id INTEGER NOT NULL,
    product_id VARCHAR(40) REFERENCES products(product_id),
    seller_id VARCHAR(40) REFERENCES sellers(seller_id),
    shipping_limit_date TIMESTAMP,
    price NUMERIC(12, 2),
    freight_value NUMERIC(12, 2),
    PRIMARY KEY (order_id, order_item_id)
);

CREATE TABLE order_payments (
    order_id VARCHAR(40) NOT NULL REFERENCES orders(order_id),
    payment_sequential INTEGER NOT NULL,
    payment_type TEXT,
    payment_installments INTEGER,
    payment_value NUMERIC(12, 2),
    PRIMARY KEY (order_id, payment_sequential)
);

CREATE TABLE order_reviews (
    review_id VARCHAR(40),
    order_id VARCHAR(40) REFERENCES orders(order_id),
    review_score INTEGER,
    review_comment_title TEXT,
    review_comment_message TEXT,
    review_creation_date TIMESTAMP,
    review_answer_timestamp TIMESTAMP,
    PRIMARY KEY (review_id, order_id)
);

CREATE INDEX idx_customers_state ON customers(customer_state);
CREATE INDEX idx_customers_unique_id ON customers(customer_unique_id);
CREATE INDEX idx_orders_customer_id ON orders(customer_id);
CREATE INDEX idx_orders_status ON orders(order_status);
CREATE INDEX idx_orders_purchase_month ON orders(DATE_TRUNC('month', order_purchase_timestamp));
CREATE INDEX idx_order_items_product_id ON order_items(product_id);
CREATE INDEX idx_order_items_seller_id ON order_items(seller_id);
CREATE INDEX idx_order_payments_type ON order_payments(payment_type);
CREATE INDEX idx_order_reviews_score ON order_reviews(review_score);
CREATE INDEX idx_products_category ON products(product_category_name);
CREATE INDEX idx_sellers_state ON sellers(seller_state);
