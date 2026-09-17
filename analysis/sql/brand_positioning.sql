-- 品牌定位矩阵
-- 输入：orders + products
-- 输出：各品牌的销售额、客单价、订单数（用于散点图）

SELECT
    p.brand AS 品牌,
    SUM(o.amount) AS 销售额,
    SUM(o.amount) / COUNT(DISTINCT o.order_id) AS 客单价,
    COUNT(DISTINCT o.order_id) AS 订单数
FROM orders o
JOIN products p ON o.product_id = p.product_id::VARCHAR
WHERE p.brand NOT IN ('其他', '其他品牌', '默认品牌', '自采品牌')
GROUP BY p.brand
HAVING SUM(o.amount) > 100000
ORDER BY 销售额 DESC;