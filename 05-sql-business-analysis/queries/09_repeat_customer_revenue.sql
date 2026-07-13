-- Business question:
-- How much revenue comes from repeat customers versus one-time customers?

WITH customer_order_summary AS (
    SELECT
        c.customer_unique_id,
        COUNT(DISTINCT o.order_id) AS delivered_orders,
        SUM(oi.price + oi.freight_value) AS total_revenue
    FROM customers AS c
    JOIN orders AS o
        ON c.customer_id = o.customer_id
    JOIN order_items AS oi
        ON o.order_id = oi.order_id
    WHERE o.order_status = 'delivered'
    GROUP BY c.customer_unique_id
),
customer_segments AS (
    SELECT
        CASE
            WHEN delivered_orders > 1 THEN 'repeat_customer'
            ELSE 'one_time_customer'
        END AS customer_segment,
        delivered_orders,
        total_revenue
    FROM customer_order_summary
)
SELECT
    customer_segment,
    COUNT(*) AS customers,
    SUM(delivered_orders) AS delivered_orders,
    SUM(total_revenue) AS total_revenue,
    ROUND(100.0 * SUM(total_revenue) / SUM(SUM(total_revenue)) OVER (), 2) AS revenue_share_pct,
    ROUND(AVG(total_revenue), 2) AS avg_customer_lifetime_value
FROM customer_segments
GROUP BY customer_segment
ORDER BY total_revenue DESC;
