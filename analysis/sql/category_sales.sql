-- 品类销售分析
-- 输入：orders + products
-- 输出：各一级品类的销售额、订单数

SELECT
    p.category_l1 AS 一级品类,
    SUM(o.amount) AS 销售额,
    COUNT(DISTINCT o.order_id) AS 订单数
FROM orders o
JOIN products p ON o.product_id = p.product_id::VARCHAR
GROUP BY p.category_l1
ORDER BY 销售额 DESC
LIMIT 10;