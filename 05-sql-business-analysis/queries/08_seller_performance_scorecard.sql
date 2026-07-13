-- Business question:
-- Which sellers perform best across revenue, review quality, and delivery reliability?

WITH ranked_reviews AS (
    SELECT
        order_id,
        review_score,
        ROW_NUMBER() OVER (
            PARTITION BY order_id
            ORDER BY review_answer_timestamp DESC NULLS LAST,
                     review_creation_date DESC NULLS LAST,
                     review_id DESC
        ) AS review_rank
    FROM order_reviews
),
review_by_order AS (
    SELECT order_id, review_score
    FROM ranked_reviews
    WHERE review_rank = 1
),
seller_order AS (
    -- Establish one row per seller and order. This keeps reviews and delivery
    -- outcomes order-weighted while revenue and units remain item-based.
    SELECT
        oi.seller_id,
        o.order_id,
        COUNT(*) AS items_sold,
        SUM(oi.price) AS product_revenue,
        AVG(r.review_score) AS review_score,
        EXTRACT(DAY FROM o.order_delivered_customer_date - o.order_purchase_timestamp) AS delivery_days,
        CASE
            WHEN o.order_delivered_customer_date > o.order_estimated_delivery_date THEN 1
            ELSE 0
        END AS is_late
    FROM order_items AS oi
    JOIN orders AS o
        ON oi.order_id = o.order_id
    LEFT JOIN review_by_order AS r
        ON o.order_id = r.order_id
    WHERE o.order_status = 'delivered'
        AND o.order_delivered_customer_date IS NOT NULL
        AND o.order_estimated_delivery_date IS NOT NULL
    GROUP BY
        oi.seller_id,
        o.order_id,
        o.order_purchase_timestamp,
        o.order_delivered_customer_date,
        o.order_estimated_delivery_date
)
SELECT
    s.seller_id,
    s.seller_state,
    COUNT(*) AS delivered_orders,
    SUM(so.items_sold) AS items_sold,
    SUM(so.product_revenue) AS product_revenue,
    ROUND(AVG(so.review_score), 2) AS avg_review_score,
    ROUND(AVG(so.delivery_days), 2) AS avg_delivery_days,
    ROUND(
        100.0 * AVG(so.is_late),
        2
    ) AS late_delivery_rate_pct
FROM seller_order AS so
JOIN sellers AS s
    ON so.seller_id = s.seller_id
GROUP BY s.seller_id, s.seller_state
HAVING COUNT(*) >= 25
ORDER BY product_revenue DESC
LIMIT 50;
