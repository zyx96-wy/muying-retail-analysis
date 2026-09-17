-- 跨品类关联分析
-- 输入：related_orders + products
-- 输出：品类A、品类B、共购次数、平均客单价

SELECT
    p1.category_l2 AS 品类A,
    p2.category_l2 AS 品类B,
    COUNT(DISTINCT o1.order_id) AS 共购次数,
    SUM(o1.amount) AS 品类A销售额,
    SUM(o2.amount) AS 品类B销售额,
    ROUND(AVG(o1.amount + o2.amount), 2) AS 平均客单价
FROM related_orders o1
JOIN related_orders o2 ON o1.order_id = o2.order_id AND o1.product_id < o2.product_id
JOIN products p1 ON o1.product_id = p1.product_id::VARCHAR
JOIN products p2 ON o2.product_id = p2.product_id::VARCHAR
WHERE p1.category_l2 < p2.category_l2
  AND p1.category_l2 IS NOT NULL
  AND p2.category_l2 IS NOT NULL
GROUP BY p1.category_l2, p2.category_l2
HAVING COUNT(DISTINCT o1.order_id) > 50
ORDER BY 共购次数 DESC
LIMIT 30;