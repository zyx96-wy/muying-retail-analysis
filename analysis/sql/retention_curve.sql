-- 留存曲线：月度 30 天复购率
-- 输入：orders
-- 输出：各首购月份的 30 天复购率

WITH first_order AS (
    SELECT
        member_id,
        MIN(order_date) AS first_date,
        EXTRACT(MONTH FROM MIN(order_date)) AS first_month
    FROM orders
    GROUP BY member_id
),
user_repeat AS (
    SELECT
        f.member_id,
        f.first_month,
        CASE WHEN COUNT(DISTINCT o.order_id) >= 2 THEN 1 ELSE 0 END AS is_repeat
    FROM first_order f
    LEFT JOIN orders o
        ON f.member_id = o.member_id
        AND o.order_date <= f.first_date + INTERVAL '30 days'
    GROUP BY f.member_id, f.first_month
)
SELECT
    first_month AS 首购月份,
    COUNT(*) AS 总用户,
    SUM(is_repeat) AS 复购用户,
    ROUND(SUM(is_repeat) * 100.0 / COUNT(*), 1) AS 复购率_30天
FROM user_repeat
GROUP BY first_month
ORDER BY first_month;