-- Post-load validation checks. Every orphan count should be zero.

SELECT 'customers' AS table_name, COUNT(*) AS row_count FROM customers
UNION ALL SELECT 'orders', COUNT(*) FROM orders
UNION ALL SELECT 'order_items', COUNT(*) FROM order_items
UNION ALL SELECT 'order_payments', COUNT(*) FROM order_payments
UNION ALL SELECT 'order_reviews', COUNT(*) FROM order_reviews
UNION ALL SELECT 'products', COUNT(*) FROM products
UNION ALL SELECT 'sellers', COUNT(*) FROM sellers
UNION ALL SELECT 'geolocation', COUNT(*) FROM geolocation
UNION ALL SELECT 'product_category_translation', COUNT(*) FROM product_category_translation
ORDER BY table_name;

SELECT 'orders_without_customer' AS validation, COUNT(*) AS orphan_rows
FROM orders AS o LEFT JOIN customers AS c ON o.customer_id = c.customer_id
WHERE c.customer_id IS NULL
UNION ALL
SELECT 'items_without_order', COUNT(*)
FROM order_items AS oi LEFT JOIN orders AS o ON oi.order_id = o.order_id
WHERE o.order_id IS NULL
UNION ALL
SELECT 'items_without_product', COUNT(*)
FROM order_items AS oi LEFT JOIN products AS p ON oi.product_id = p.product_id
WHERE p.product_id IS NULL
UNION ALL
SELECT 'items_without_seller', COUNT(*)
FROM order_items AS oi LEFT JOIN sellers AS s ON oi.seller_id = s.seller_id
WHERE s.seller_id IS NULL
UNION ALL
SELECT 'payments_without_order', COUNT(*)
FROM order_payments AS op LEFT JOIN orders AS o ON op.order_id = o.order_id
WHERE o.order_id IS NULL
UNION ALL
SELECT 'reviews_without_order', COUNT(*)
FROM order_reviews AS r LEFT JOIN orders AS o ON r.order_id = o.order_id
WHERE o.order_id IS NULL;

-- Diagnostic: multiple reviews per order are valid source behavior and explain
-- why review analyses first aggregate to one row per order.
SELECT COUNT(*) AS orders_with_multiple_review_rows
FROM (
    SELECT order_id
    FROM order_reviews
    GROUP BY order_id
    HAVING COUNT(*) > 1
) AS repeated_reviews;
