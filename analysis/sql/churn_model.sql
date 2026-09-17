-- 流失预测模型特征提取
-- 输入：orders
-- 输出：每个用户的特征 + 是否流失标签

WITH user_features AS (
    SELECT
        member_id,
        MAX(order_date) AS last_order_date,
        COUNT(DISTINCT order_id) AS frequency,
        SUM(amount) AS monetary,
        AVG(amount) AS avg_amount,
        MAX(order_date) - MIN(order_date) AS lifespan_days
    FROM orders
    GROUP BY member_id
)
SELECT
    member_id,
    frequency,
    monetary,
    avg_amount,
    lifespan_days,
    CASE
        WHEN last_order_date >= '2021-10-01' THEN 0
        ELSE 1
    END AS is_churn
FROM user_features;