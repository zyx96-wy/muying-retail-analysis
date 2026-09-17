# -*- coding: utf-8 -*-
"""
母婴零售数据清洗
输入：data/raw/{orders,members,traffic,products,stores,related_orders}.csv
输出：data/processed/{同名}.csv
"""
import pandas as pd
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent
RAW = BASE / "data" / "raw"
OUT = BASE / "data" / "processed"
OUT.mkdir(parents=True, exist_ok=True)


# ============ orders ============

def clean_orders():
    df = pd.read_csv(RAW / "orders.csv", encoding="gbk")
    print(f"orders 原始: {len(df)} 行")

    df["日期"] = pd.to_datetime(df["日期"], errors="coerce")
    df["核销日期"] = pd.to_datetime(df["核销日期"], errors="coerce")
    df["销售额"] = pd.to_numeric(df["销售额"], errors="coerce")

    df = df.dropna(subset=["会员编码", "订单号", "销售额"])
    df = df.drop_duplicates(subset=["订单号", "商品编码"])

    df["年"] = df["日期"].dt.year
    df["月"] = df["日期"].dt.month
    df["日"] = df["日期"].dt.day
    df["星期"] = df["日期"].dt.dayofweek

    print(f"orders 清洗后: {len(df)} 行")
    return df


# ============ members ============

def clean_members():
    df = pd.read_csv(RAW / "members.csv", encoding="gbk")
    print(f"members 原始: {len(df)} 行")

    df = df.drop_duplicates(subset=["会员编码"])
    df = df.dropna(subset=["会员编码"])

    print(f"members 清洗后: {len(df)} 行")
    return df


# ============ traffic ============

def clean_traffic():
    df = pd.read_csv(RAW / "traffic.csv", encoding="gbk")
    print(f"traffic 原始: {len(df)} 行")

    df["访问日期"] = pd.to_datetime(df["访问日期"], errors="coerce")
    df["PV"] = pd.to_numeric(df["PV"], errors="coerce").fillna(0).astype(int)

    df["年"] = df["访问日期"].dt.year
    df["月"] = df["访问日期"].dt.month
    df["星期"] = df["访问日期"].dt.dayofweek

    print(f"traffic 清洗后: {len(df)} 行")
    return df


# ============ products ============

def clean_products():
    df = pd.read_csv(RAW / "products.csv", dtype={"商品编码": str}, encoding="utf-8-sig")
    print(f"products 原始: {len(df)} 行")

    df.columns = ["product_id", "category_l1", "category_l2", "brand"]
    df = df.dropna(subset=["product_id"])
    df = df.drop_duplicates(subset=["product_id"])

    print(f"products 清洗后: {len(df)} 行")
    return df


# ============ stores ============

def clean_stores():
    df = pd.read_csv(RAW / "stores.csv", dtype={"门店编码": str}, encoding="utf-8-sig")
    print(f"stores 原始: {len(df)} 行")

    df.columns = ["store_type", "store_id"]
    df = df.dropna(subset=["store_id"])
    df = df.drop_duplicates(subset=["store_id"])

    print(f"stores 清洗后: {len(df)} 行")
    return df


# ============ related_orders ============

def clean_related_orders():
    df = pd.read_csv(RAW / "related_orders.csv", dtype={
        "会员编码": str, "商品编码": str, "订单号": str, "门店编码": str
    }, encoding="utf-8-sig")
    print(f"related_orders 原始: {len(df)} 行")

    df.columns = ["member_id", "baby_age", "order_date", "product_id",
                  "order_id", "store_id", "amount", "order_type",
                  "campaign_type", "scene"]

    df["order_date"] = pd.to_datetime(df["order_date"], errors="coerce")
    df["amount"] = pd.to_numeric(df["amount"], errors="coerce")

    df = df.dropna(subset=["member_id", "order_id", "amount"])
    df = df.drop_duplicates(subset=["order_id", "product_id"])

    print(f"related_orders 清洗后: {len(df)} 行")
    return df


# ============ 主流程 ============

if __name__ == "__main__":
    print("=" * 50)

    print("Step 1: 清洗 orders")
    orders = clean_orders()

    print("\nStep 2: 清洗 members")
    members = clean_members()

    print("\nStep 3: 清洗 traffic")
    traffic = clean_traffic()

    print("\nStep 4: 清洗 products")
    products = clean_products()

    print("\nStep 5: 清洗 stores")
    stores = clean_stores()

    print("\nStep 6: 清洗 related_orders")
    related = clean_related_orders()

    print("\nStep 7: 导出")
    orders.to_csv(OUT / "orders.csv", index=False, encoding="utf-8-sig")
    members.to_csv(OUT / "members.csv", index=False, encoding="utf-8-sig")
    traffic.to_csv(OUT / "traffic.csv", index=False, encoding="utf-8-sig")
    products.to_csv(OUT / "products.csv", index=False, encoding="utf-8-sig")
    stores.to_csv(OUT / "stores.csv", index=False, encoding="utf-8-sig")
    related.to_csv(OUT / "related_orders.csv", index=False, encoding="utf-8-sig")

    print("\n完成！")
    for f in sorted(OUT.glob("*.csv")):
        print(f"  {f.name}  ({len(pd.read_csv(f))} 行)")