-- Business question:
-- How are review scores related to delivery speed and late deliveries?

WITH ranked_reviews AS (
    -- The source can contain more than one review row for an order.
    -- Rank latest feedback first so every order contributes one integer score.
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
reviewed_orders AS (
    SELECT
        o.order_id,
        r.review_score,
        EXTRACT(DAY FROM o.order_delivered_customer_date - o.order_purchase_timestamp) AS delivery_days,
        CASE
            WHEN o.order_delivered_customer_date > o.order_estimated_delivery_date THEN 'late'
            ELSE 'on_time_or_early'
        END AS delivery_status
    FROM orders AS o
    JOIN review_by_order AS r
        ON o.order_id = r.order_id
    WHERE o.order_status = 'delivered'
        AND o.order_delivered_customer_date IS NOT NULL
        AND o.order_estimated_delivery_date IS NOT NULL
)
SELECT
    delivery_status,
    review_score,
    COUNT(*) AS reviewed_orders,
    ROUND(AVG(delivery_days), 2) AS avg_delivery_days,
    ROUND(100.0 * COUNT(*) / SUM(COUNT(*)) OVER (PARTITION BY delivery_status), 2) AS score_mix_pct
FROM reviewed_orders
GROUP BY delivery_status, review_score
ORDER BY delivery_status, review_score DESC;
