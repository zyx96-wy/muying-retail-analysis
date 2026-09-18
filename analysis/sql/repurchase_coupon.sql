WITH max_date AS (
    SELECT MAX(order_date)::date AS today FROM orders
),
user_categories AS (
    SELECT
        o.member_id,
        p.category_l1,
        MAX(o.order_date)::date AS last_date
    FROM orders o
    JOIN products p ON o.product_id = p.product_id::VARCHAR
    GROUP BY o.member_id, p.category_l1
),
scored AS (
    SELECT
        uc.member_id,
        uc.category_l1 AS 品类,
        uc.last_date AS 上次购买日期,
        (md.today - uc.last_date) AS 距今天数,
        CASE
            WHEN uc.category_l1 = '奶粉'   AND (md.today - uc.last_date) >= 30 THEN '满200减20'
            WHEN uc.category_l1 = '尿裤'   AND (md.today - uc.last_date) >= 45 THEN '满100减10'
            WHEN uc.category_l1 = '零辅食' AND (md.today - uc.last_date) >= 60 THEN '满50减5'
        END AS 推荐优惠
    FROM user_categories uc
    CROSS JOIN max_date md
)
SELECT *
FROM scored
WHERE 推荐优惠 IS NOT NULL
ORDER BY 距今天数 DESC
LIMIT 10000;