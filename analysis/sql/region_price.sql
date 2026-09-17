-- 地域 × 价位分析
-- 输入：orders + members
-- 输出：各省份、各价位段的销售额和订单数

SELECT
    m.province AS 省份,
    CASE
        WHEN o.amount < 100 THEN '1_100元以下'
        WHEN o.amount < 300 THEN '2_100-300元'
        WHEN o.amount < 500 THEN '3_300-500元'
        ELSE '4_500元以上'
    END AS 价位段,
    SUM(o.amount) AS 销售额,
    COUNT(DISTINCT o.order_id) AS 订单数
FROM orders o
JOIN members m ON o.member_id = m.member_id
GROUP BY m.province, 价位段
ORDER BY m.province, 价位段;