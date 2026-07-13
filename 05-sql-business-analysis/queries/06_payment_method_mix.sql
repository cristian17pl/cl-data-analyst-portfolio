-- Business question:
-- Which payment methods are most common, and how do installment patterns differ?

SELECT
    op.payment_type,
    COUNT(*) AS payment_records,
    COUNT(DISTINCT op.order_id) AS orders,
    SUM(op.payment_value) AS payment_value,
    ROUND(100.0 * SUM(op.payment_value) / SUM(SUM(op.payment_value)) OVER (), 2) AS payment_value_share_pct,
    ROUND(AVG(op.payment_installments), 2) AS avg_installments,
    ROUND(AVG(op.payment_value), 2) AS avg_payment_value
FROM order_payments AS op
JOIN orders AS o
    ON op.order_id = o.order_id
WHERE o.order_status = 'delivered'
GROUP BY op.payment_type
ORDER BY payment_value DESC;
