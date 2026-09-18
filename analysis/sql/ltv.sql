-- 用户 LTV 分层
-- 输入：orders
-- 输出：LTV 分层用户数

WITH user_stats AS (
    SELECT
        member_id,
        COUNT(DISTINCT order_id) AS frequency,
        SUM(amount) AS monetary,
        AVG(amount) AS avg_amount,
        MAX(order_date) - MIN(order_date) AS lifespan_days
    FROM orders
    GROUP BY member_id
),
ltv_calc AS (
    SELECT
        member_id,
        avg_amount * frequency * (lifespan_days / 30.0) AS ltv
    FROM user_stats
)
SELECT
    CASE
        WHEN ltv < 500 THEN '1_低价值'
        WHEN ltv < 2000 THEN '2_中价值'
        WHEN ltv < 5000 THEN '3_高价值'
        ELSE '4_超高价值'
    END AS ltv_level,
    COUNT(*) AS user_count,
    ROUND(AVG(ltv), 2) AS avg_ltv
FROM ltv_calc
GROUP BY ltv_level
ORDER BY ltv_level;