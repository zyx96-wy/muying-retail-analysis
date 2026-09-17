# -*- coding: utf-8 -*-
"""
母婴零售数据清洗
输入：data/raw/{orders,members,traffic}.csv
输出：data/processed/{orders,members,traffic}.csv
"""
import pandas as pd
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent
RAW = BASE / "data" / "raw"
OUT = BASE / "data" / "processed"
OUT.mkdir(parents=True, exist_ok=True)


def clean_orders():
    df = pd.read_csv(RAW / "orders.csv")
    print(f"orders 原始: {len(df)} 行")

    # 日期转 datetime
    df["日期"] = pd.to_datetime(df["日期"], errors="coerce")
    df["核销日期"] = pd.to_datetime(df["核销日期"], errors="coerce")

    # 销售额转数字
    df["销售额"] = pd.to_numeric(df["销售额"], errors="coerce")

    # 去空
    df = df.dropna(subset=["会员编码", "订单号", "销售额"])

    # 去重（同一订单同一商品算一条）
    df = df.drop_duplicates(subset=["订单号", "商品编码"])

    # 派生字段
    df["年"] = df["日期"].dt.year
    df["月"] = df["日期"].dt.month
    df["日"] = df["日期"].dt.day
    df["星期"] = df["日期"].dt.dayofweek  # 0=周一

    print(f"orders 清洗后: {len(df)} 行")
    return df


def clean_members():
    df = pd.read_csv(RAW / "members.csv")
    print(f"members 原始: {len(df)} 行")

    # 会员编码去重
    df = df.drop_duplicates(subset=["会员编码"])

    # 去空
    df = df.dropna(subset=["会员编码"])

    print(f"members 清洗后: {len(df)} 行")
    return df


def clean_traffic():
    df = pd.read_csv(RAW / "traffic.csv")
    print(f"traffic 原始: {len(df)} 行")

    # 日期转 datetime
    df["访问日期"] = pd.to_datetime(df["访问日期"], errors="coerce")

    # PV 转 int
    df["PV"] = pd.to_numeric(df["PV"], errors="coerce").fillna(0).astype(int)

    # 派生字段
    df["年"] = df["访问日期"].dt.year
    df["月"] = df["访问日期"].dt.month
    df["星期"] = df["访问日期"].dt.dayofweek

    print(f"traffic 清洗后: {len(df)} 行")
    return df


if __name__ == "__main__":
    print("=" * 50)

    print("Step 1: 清洗 orders")
    orders = clean_orders()

    print("\nStep 2: 清洗 members")
    members = clean_members()

    print("\nStep 3: 清洗 traffic")
    traffic = clean_traffic()

    print("\nStep 4: 导出")
    orders.to_csv(OUT / "orders.csv", index=False, encoding="utf-8-sig")
    members.to_csv(OUT / "members.csv", index=False, encoding="utf-8-sig")
    traffic.to_csv(OUT / "traffic.csv", index=False, encoding="utf-8-sig")

    print("\n完成！")
    for f in sorted(OUT.glob("*.csv")):
        print(f"  {f.name}  ({len(pd.read_csv(f))} 行)")