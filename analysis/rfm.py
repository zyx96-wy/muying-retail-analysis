# -*- coding: utf-8 -*-
"""
RFM 用户分层
输入：data/processed/orders.csv
输出：data/processed/rfm.csv
"""
import pandas as pd
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent
OUT = BASE / "data" / "processed"

# 1. 读订单（用中文列名）
df = pd.read_csv(OUT / "orders.csv", dtype={"会员编码": str, "订单号": str})
df["日期"] = pd.to_datetime(df["日期"], errors="coerce")

# 2. 算 RFM 原始值
rfm = df.groupby("会员编码").agg(
    last_order_date=("日期", "max"),
    frequency=("订单号", "nunique"),
    monetary=("销售额", "sum")
).reset_index()


def r_score(date):
    if pd.isna(date):
        return 1
    if date >= pd.Timestamp("2021-10-01"):
        return 5
    if date >= pd.Timestamp("2021-07-01"):
        return 4
    if date >= pd.Timestamp("2021-04-01"):
        return 3
    if date >= pd.Timestamp("2021-01-01"):
        return 2
    return 1


def f_score(f):
    if f >= 20: return 5
    if f >= 10: return 4
    if f >= 5: return 3
    if f >= 3: return 2
    return 1


def m_score(m):
    if m >= 10000: return 5
    if m >= 5000: return 4
    if m >= 2000: return 3
    if m >= 500: return 2
    return 1


rfm["r_score"] = rfm["last_order_date"].apply(r_score)
rfm["f_score"] = rfm["frequency"].apply(f_score)
rfm["m_score"] = rfm["monetary"].apply(m_score)
rfm["rfm_segment"] = rfm["r_score"].astype(str) + rfm["f_score"].astype(str) + rfm["m_score"].astype(str)

# 4. 输出
rfm.to_csv(OUT / "rfm.csv", index=False, encoding="utf-8-sig")
print(f"RFM: {len(rfm)} 用户")
print(rfm.head(10).to_string())

# 5. 分层统计
print("\nR 分分布:")
print(rfm["r_score"].value_counts().sort_index().to_string())
print("\nF 分分布:")
print(rfm["f_score"].value_counts().sort_index().to_string())
print("\nM 分分布:")
print(rfm["m_score"].value_counts().sort_index().to_string())