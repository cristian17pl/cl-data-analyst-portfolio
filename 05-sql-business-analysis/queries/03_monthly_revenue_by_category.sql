-- Business question:
-- How does monthly revenue trend over time for the largest categories?

WITH category_revenue AS (
    SELECT
        COALESCE(t.product_category_name_english, p.product_category_name, 'unknown') AS product_category,
        SUM(oi.price) AS product_revenue
    FROM order_items AS oi
    JOIN orders AS o
        ON oi.order_id = o.order_id
    LEFT JOIN products AS p
        ON oi.product_id = p.product_id
    LEFT JOIN product_category_translation AS t
        ON p.product_category_name = t.product_category_name
    WHERE o.order_status = 'delivered'
    GROUP BY COALESCE(t.product_category_name_english, p.product_category_name, 'unknown')
),
top_categories AS (
    SELECT product_category
    FROM category_revenue
    ORDER BY product_revenue DESC
    LIMIT 10
)
SELECT
    DATE_TRUNC('month', o.order_purchase_timestamp)::DATE AS order_month,
    COALESCE(t.product_category_name_english, p.product_category_name, 'unknown') AS product_category,
    COUNT(DISTINCT o.order_id) AS orders,
    SUM(oi.price) AS product_revenue,
    SUM(SUM(oi.price)) OVER (
        PARTITION BY COALESCE(t.product_category_name_english, p.product_category_name, 'unknown')
        ORDER BY DATE_TRUNC('month', o.order_purchase_timestamp)::DATE
    ) AS running_product_revenue
FROM orders AS o
JOIN order_items AS oi
    ON o.order_id = oi.order_id
LEFT JOIN products AS p
    ON oi.product_id = p.product_id
LEFT JOIN product_category_translation AS t
    ON p.product_category_name = t.product_category_name
JOIN top_categories AS tc
    ON tc.product_category = COALESCE(t.product_category_name_english, p.product_category_name, 'unknown')
WHERE o.order_status = 'delivered'
GROUP BY
    DATE_TRUNC('month', o.order_purchase_timestamp)::DATE,
    COALESCE(t.product_category_name_english, p.product_category_name, 'unknown')
ORDER BY order_month, product_revenue DESC;
