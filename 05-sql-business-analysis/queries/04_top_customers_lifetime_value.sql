-- Business question:
-- Which customers generated the highest lifetime value?

SELECT
    c.customer_unique_id,
    c.customer_state,
    COUNT(DISTINCT o.order_id) AS delivered_orders,
    MIN(o.order_purchase_timestamp)::DATE AS first_order_date,
    MAX(o.order_purchase_timestamp)::DATE AS last_order_date,
    SUM(oi.price) AS product_revenue,
    SUM(oi.freight_value) AS freight_revenue,
    SUM(oi.price + oi.freight_value) AS lifetime_value,
    ROUND(SUM(oi.price + oi.freight_value) / COUNT(DISTINCT o.order_id), 2) AS avg_order_value
FROM customers AS c
JOIN orders AS o
    ON c.customer_id = o.customer_id
JOIN order_items AS oi
    ON o.order_id = oi.order_id
WHERE o.order_status = 'delivered'
GROUP BY c.customer_unique_id, c.customer_state
ORDER BY lifetime_value DESC
LIMIT 25;
