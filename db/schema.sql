DROP TABLE IF EXISTS orders CASCADE;
DROP TABLE IF EXISTS members CASCADE;
DROP TABLE IF EXISTS traffic CASCADE;

CREATE TABLE members (
    customer_type VARCHAR(8),
    province VARCHAR(32),
    city VARCHAR(32),
    city_level VARCHAR(16),
    member_id VARCHAR(32) PRIMARY KEY,
    gender VARCHAR(4)
);

CREATE TABLE orders (
    member_id VARCHAR(32),
    baby_age VARCHAR(16),
    order_date DATE,
    product_id VARCHAR(64),
    order_id VARCHAR(64),
    store_id VARCHAR(16),
    amount NUMERIC(10, 2),
    order_type VARCHAR(16),
    campaign_type VARCHAR(16),
    scene VARCHAR(16),
    verify_date DATE,
    year INT,
    month INT,
    day INT,
    weekday INT
);

CREATE TABLE traffic (
    member_id VARCHAR(32),
    visit_date DATE,
    visit_hour INT,
    scene_id VARCHAR(16),
    pv INT,
    year INT,
    month INT,
    weekday INT
);

CREATE INDEX idx_orders_member ON orders(member_id);
CREATE INDEX idx_orders_date ON orders(order_date);
CREATE INDEX idx_traffic_member ON traffic(member_id);