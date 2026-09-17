# 母婴零售用户行为分析

基于 82 万条订单、26 万会员、162 万条访问记录，完成从数据清洗、数据库建模，到 BI 可视化与 RFM 用户分层的全流程。

## 项目背景

母婴零售是高频、刚需、复购型业务。本项目旨在回答：
1. 谁在买？（用户画像）
2. 买什么？（商品/年龄段）
3. 什么时候买？（时间分布）
4. 怎么留住他们？（RFM 分层）

## 技术栈

| 层 | 工具 |
|----|------|
| 数据清洗 | Python + pandas |
| 数据库 | PostgreSQL + Docker |
| BI 可视化 | Apache Superset |

## 核心发现

1. **用户画像**：86.7% 女性，1-3 岁宝宝家长为主
2. **地域**：下沉市场为主，河南占 28.7%
3. **访问高峰**：10 点、15 点、20 点
4. **销售波动**：大促后必跌
5. **RFM**：76% 用户流失（R=1）

## 项目结构
muying-retail-analysis/
├── .env                      # Superset 密钥（不传）
├── .gitignore
├── docker-compose.yml
├── README.md
├── superset_config.py
├── analysis/
│   ├── rfm.py
│   └── charts/               # 空
├── data/
│   ├── raw/                  # 原始 CSV
│   │   ├── members.csv
│   │   ├── orders.csv
│   │   └── traffic.csv
│   └── processed/            # 清洗后
│       ├── members.csv
│       ├── orders.csv
│       ├── rfm.csv
│       └── traffic.csv
├── db/
│   ├── load_to_pg.py
│   └── schema.sql
├── docs/
│   ├── analysis_report.md
│   └── data_dictionary.md
└── etl/
    └── clean.py

text

## 快速开始

```bash
# 1. 启动数据库和 Superset
docker compose up -d

# 2. 清洗数据
python etl/clean.py

# 3. 建表并导入
Get-Content db\schema.sql | docker exec -i postgres-muying psql -U postgres -d muying
python db/load_to_pg.py

# 4. 访问 Superset
# http://localhost:8088  admin/admin
数据模型
members：26.2 万会员

orders：80 万订单

traffic：162 万访问记录