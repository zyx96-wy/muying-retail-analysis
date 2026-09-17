# -*- coding: utf-8 -*-
"""
用户流失预测模型
输入：data/processed/orders.csv
输出：data/processed/churn_prediction.csv
"""
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, roc_auc_score
from pathlib import Path


BASE = Path(__file__).resolve().parent.parent
OUT = BASE / "data" / "processed"

# 1. 读数据
df = pd.read_csv(OUT / "orders.csv", dtype={"会员编码": str, "订单号": str})
df["日期"] = pd.to_datetime(df["日期"], errors="coerce")

# 2. 构造特征
features = df.groupby("会员编码").agg(
    frequency=("订单号", "nunique"),
    monetary=("销售额", "sum"),
    avg_amount=("销售额", "mean"),
    lifespan_days=("日期", lambda x: (x.max() - x.min()).days),
    last_order_date=("日期", "max")
).reset_index()

# 3. 标签：最后购买在 2021-10-01 之前 = 流失
features["is_churn"] = (features["last_order_date"] < "2021-10-01").astype(int)

# 4. 训练
X = features[["frequency", "monetary", "avg_amount", "lifespan_days"]]
y = features["is_churn"]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# 5. 评估
y_pred = model.predict(X_test)
y_prob = model.predict_proba(X_test)[:, 1]

print("分类报告：")
print(classification_report(y_test, y_pred))
print(f"AUC: {roc_auc_score(y_test, y_prob):.4f}")

# 6. 特征重要性
importance = pd.DataFrame({
    "feature": X.columns,
    "importance": model.feature_importances_
}).sort_values("importance", ascending=False)
print("\n特征重要性：")
print(importance.to_string())

# 7. 输出预测结果
features["churn_prob"] = model.predict_proba(X)[:, 1]
features.to_csv(OUT / "churn_prediction.csv", index=False, encoding="utf-8-sig")
print(f"\n已输出 churn_prediction.csv")