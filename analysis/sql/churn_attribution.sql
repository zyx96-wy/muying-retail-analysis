-- 流失归因分析
-- 对比流失用户和未流失用户的特征
-- 输入：orders 表
-- 输出：流失/未流失用户的平均购买次数、消费金额、生命周期

WITH user_stats AS (
    SELECT
        member_id,
        COUNT(DISTINCT order_id) AS freq,
        SUM(amount) AS monetary,
        MAX(order_date) - MIN(order_date) AS lifespan,
        CASE WHEN MAX(order_date) < '2021-10-01' THEN '流失' ELSE '未流失' END AS status
    FROM orders
    GROUP BY member_id
)
SELECT
    status,
    COUNT(*) AS user_count,
    ROUND(AVG(freq), 2) AS avg_freq,
    ROUND(AVG(monetary), 2) AS avg_monetary,
    ROUND(AVG(lifespan), 1) AS avg_lifespan
FROM user_stats
GROUP BY status;