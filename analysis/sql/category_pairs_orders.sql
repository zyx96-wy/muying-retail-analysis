WITH user_categories AS (
    SELECT DISTINCT
        o.member_id,
        p.category_l1
    FROM orders o
    JOIN products p ON o.product_id = p.product_id::VARCHAR
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
    cat_a AS 品类A,
    cat_b AS 品类B,
    co_buyers AS 共同购买用户数
FROM category_pairs
ORDER BY co_buyers DESC
LIMIT 30;