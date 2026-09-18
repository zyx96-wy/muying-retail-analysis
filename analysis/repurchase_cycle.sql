WITH user_orders AS (
    SELECT
        member_id,
        product_id,
        order_date,
        LAG(order_date) OVER (PARTITION BY member_id, product_id ORDER BY order_date) AS prev_date
    FROM orders
),
intervals AS (
    SELECT
        product_id,
        order_date - prev_date AS days_between
    FROM user_orders
    WHERE prev_date IS NOT NULL
)
SELECT
    p.category_l1 AS 品类,
    COUNT(*) AS 复购次数,
    ROUND(AVG(i.days_between), 1) AS 平均复购周期_天,
    ROUND(PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY i.days_between)::numeric, 1) AS 中位数复购周期_天
FROM intervals i
JOIN products p ON i.product_id = p.product_id::VARCHAR
GROUP BY p.category_l1
ORDER BY 复购次数 DESC;