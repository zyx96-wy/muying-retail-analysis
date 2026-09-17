-- AARRR 漏斗分析
-- 输入：orders
-- 输出：总用户、复购用户、忠诚用户、高频用户

WITH user_orders AS (
    SELECT
        member_id,
        COUNT(DISTINCT order_id) AS order_count
    FROM orders
    GROUP BY member_id
)
SELECT '1_总用户' AS level, COUNT(*) AS user_count FROM user_orders
UNION ALL
SELECT '2_复购用户', SUM(CASE WHEN order_count >= 2 THEN 1 ELSE 0 END) FROM user_orders
UNION ALL
SELECT '3_忠诚用户', SUM(CASE WHEN order_count >= 5 THEN 1 ELSE 0 END) FROM user_orders
UNION ALL
SELECT '4_高频用户', SUM(CASE WHEN order_count >= 10 THEN 1 ELSE 0 END) FROM user_orders
ORDER BY level;