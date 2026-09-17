# -*- coding: utf-8 -*-
"""
把 CSV 导入 PostgreSQL
ID 类字段强制当字符串
"""
import pandas as pd
from sqlalchemy import create_engine
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent
OUT = BASE / "data" / "processed"

DB_URL = "postgresql://postgres:postgres@localhost:5432/muying"
engine = create_engine(DB_URL)

# ============ members ============
df = pd.read_csv(OUT / "members.csv", dtype={"会员编码": str})
df.columns = ["customer_type", "province", "city", "city_level", "member_id", "gender"]
df.to_sql("members", engine, if_exists="append", index=False)
print(f"members: {len(df)} 行")

# ============ orders ============
df = pd.read_csv(OUT / "orders.csv", dtype={
    "会员编码": str,
    "商品编码": str,
    "订单号": str,
    "门店编码": str,
})
df.columns = ["member_id", "baby_age", "order_date", "product_id", "order_id",
              "store_id", "amount", "order_type", "campaign_type", "scene",
              "verify_date", "year", "month", "day", "weekday"]
df.to_sql("orders", engine, if_exists="append", index=False)
print(f"orders: {len(df)} 行")

# ============ traffic ============
df = pd.read_csv(OUT / "traffic.csv", dtype={"会员编码": str, "微信场景ID": str})
df.columns = ["member_id", "visit_date", "visit_hour", "scene_id", "pv",
              "year", "month", "weekday"]
df.to_sql("traffic", engine, if_exists="append", index=False)
print(f"traffic: {len(df)} 行")

print("导入完成")