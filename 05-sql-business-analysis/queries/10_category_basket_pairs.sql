-- Business question:
-- Which product categories are most frequently purchased together?

WITH order_categories AS (
    SELECT DISTINCT
        oi.order_id,
        COALESCE(t.product_category_name_english, p.product_category_name, 'unknown') AS product_category
    FROM order_items AS oi
    JOIN orders AS o
        ON oi.order_id = o.order_id
    LEFT JOIN products AS p
        ON oi.product_id = p.product_id
    LEFT JOIN product_category_translation AS t
        ON p.product_category_name = t.product_category_name
    WHERE o.order_status = 'delivered'
),
category_pairs AS (
    SELECT
        a.product_category AS category_a,
        b.product_category AS category_b,
        COUNT(*) AS shared_orders
    FROM order_categories AS a
    JOIN order_categories AS b
        ON a.order_id = b.order_id
        AND a.product_category < b.product_category
    GROUP BY a.product_category, b.product_category
)
SELECT
    category_a,
    category_b,
    shared_orders
FROM category_pairs
WHERE shared_orders >= 5
ORDER BY shared_orders DESC, category_a, category_b
LIMIT 50;
