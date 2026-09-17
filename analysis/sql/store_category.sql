-- 门店类型 × 品类分析
-- 输入：orders + stores + products
-- 输出：各门店类型、各品类的销售额

SELECT
    s.store_type AS 门店类型,
    p.category_l1 AS 品类,
    SUM(o.amount) AS 销售额
FROM orders o
JOIN stores s ON o.store_id = s.store_id
JOIN products p ON o.product_id = p.product_id::VARCHAR
GROUP BY s.store_type, p.category_l1
ORDER BY s.store_type, 销售额 DESC;