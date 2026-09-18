-- 7 天内智能推荐（方案 1）
-- 输入：orders + products
-- 输出：用户-推荐品类

WITH sample_users AS (
    SELECT DISTINCT member_id FROM orders LIMIT 1000
),
user_categories AS (
    SELECT DISTINCT
        o.member_id,
        p.category_l1
    FROM orders o
    JOIN products p ON o.product_id = p.product_id::VARCHAR
    WHERE o.member_id IN (SELECT member_id FROM sample_users)
),
category_pairs AS (
    SELECT
        p1.category_l1 AS cat_a,
        p2.category_l1 AS cat_b,
        COUNT(DISTINCT o1.member_id) AS co_buyers
    FROM orders o1
    JOIN orders o2 ON o1.member_id = o2.member_id AND o1.order_id != o2.order_id
    JOIN products p1 ON o1.product_id = p1.product_id::VARCHAR
    JOIN products p2 ON o2.product_id = p2.product_id::VARCHAR
    WHERE p1.category_l1 < p2.category_l1
    GROUP BY p1.category_l1, p2.category_l1
    HAVING COUNT(DISTINCT o1.member_id) > 100
)
SELECT
    uc.member_id,
    cp.cat_b AS 推荐品类,
    cp.co_buyers AS 相似用户数
FROM user_categories uc
JOIN category_pairs cp ON uc.category_l1 = cp.cat_a
WHERE cp.cat_b NOT IN (
    SELECT category_l1 FROM user_categories WHERE member_id = uc.member_id
)
ORDER BY uc.member_id, cp.co_buyers DESC
LIMIT 1000;