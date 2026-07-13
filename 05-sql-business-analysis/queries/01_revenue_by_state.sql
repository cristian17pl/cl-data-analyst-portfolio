-- Business question:
-- Which customer states generated the most completed-order revenue?

SELECT
    c.customer_state,
    COUNT(DISTINCT o.order_id) AS delivered_orders,
    COUNT(DISTINCT c.customer_unique_id) AS unique_customers,
    SUM(oi.price) AS product_revenue,
    SUM(oi.freight_value) AS freight_revenue,
    SUM(oi.price + oi.freight_value) AS total_revenue,
    ROUND(SUM(oi.price + oi.freight_value) / COUNT(DISTINCT o.order_id), 2) AS avg_order_value
FROM orders AS o
JOIN customers AS c
    ON o.customer_id = c.customer_id
JOIN order_items AS oi
    ON o.order_id = oi.order_id
WHERE o.order_status = 'delivered'
GROUP BY c.customer_state
ORDER BY total_revenue DESC;
