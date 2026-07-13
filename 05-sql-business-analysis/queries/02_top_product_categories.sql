-- Business question:
-- Which product categories generated the most revenue and unit volume?

SELECT
    COALESCE(t.product_category_name_english, p.product_category_name, 'unknown') AS product_category,
    COUNT(*) AS units_sold,
    COUNT(DISTINCT oi.order_id) AS orders,
    SUM(oi.price) AS product_revenue,
    SUM(oi.freight_value) AS freight_revenue,
    ROUND(AVG(oi.price), 2) AS avg_item_price,
    ROUND(SUM(oi.price) / NULLIF(COUNT(*), 0), 2) AS revenue_per_unit
FROM order_items AS oi
JOIN orders AS o
    ON oi.order_id = o.order_id
LEFT JOIN products AS p
    ON oi.product_id = p.product_id
LEFT JOIN product_category_translation AS t
    ON p.product_category_name = t.product_category_name
WHERE o.order_status = 'delivered'
GROUP BY COALESCE(t.product_category_name_english, p.product_category_name, 'unknown')
ORDER BY product_revenue DESC;
