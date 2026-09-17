**格式有问题。** 主要是 Markdown 代码块没闭合、列表缩进乱。

## 一、问题清单

| 位置 | 问题 |
|------|------|
| `## 项目结构` | 代码块没闭合（缺 ` ``` `） |
| `## 环境要求` | `2. Docker Desktop` 标题没换行 |
| `## 快速开始` | 各步骤标题没换行 |
| `8. Superset 使用说明` | 层级乱了 |
| `9.数据字典`、`10.分析报告` | 缺空格 |

## 二、完整修正版

```markdown
# 母婴零售用户行为分析

基于 82 万订单、26 万会员、162 万访问记录，完成从数据清洗、数据库建模，到 BI 可视化与 RFM 用户分层的全流程。

## 看板预览

![Dashboard](docs/screenshots/dashboard.png)

完整看板包含 11 张图：省份分布、城市等级、门店销售、性别、宝宝年龄段、访问时段、月度分析、营销活动、订单类型、RF 分析、RFM 热力图。

## 数据来源

本数据集来自和鲸社区（heywhale.com），搜索"母婴零售数据集清洗版本"。

- 原始数据：3 个 CSV（会员、订单、流量）
- 数据量：82 万订单、26 万会员、162 万访问
- 数据时间：2021 年

**下载方式：**
1. 打开 heywhale.com
2. 搜索"母婴零售数据集清洗版本"
3. 下载 3 个 CSV
4. 放到 `data/raw/` 目录

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

```
muying-retail-analysis/
├── data/
│   ├── raw/              # 原始 CSV（需自行下载）
│   └── processed/        # 清洗后
├── etl/
│   └── clean.py
├── db/
│   ├── schema.sql
│   └── load_to_pg.py
├── analysis/
│   └── rfm.py
├── docs/
│   ├── analysis_report.md
│   └── data_dictionary.md
├── docker-compose.yml
├── superset_config.py
├── .env
└── README.md
```

## 环境要求

### 1. Python 环境

- 安装 Anaconda（anaconda.com）
- 建环境：

```bash
conda create -n muying python=3.11 -y
conda activate muying
pip install pandas openpyxl psycopg2-binary sqlalchemy
```

### 2. Docker Desktop

- 下载：https://www.docker.com/products/docker-desktop/
- 安装时勾选 **Use WSL 2**
- 装完重启电脑
- 打开 Docker Desktop，等鲸鱼图标稳定（绿色）

**验证：**

```bash
docker --version
docker run hello-world
```

看到 "Hello from Docker!" 就成功。

## 快速开始

### 1. 下载数据

从和鲸社区下载 3 个 CSV，放到 `data/raw/`：
- members.csv
- orders.csv
- traffic.csv

### 2. 清洗数据

```bash
python etl/clean.py
```

输出到 `data/processed/`。

### 3. 启动数据库和 Superset

```bash
docker compose up -d
```

### 4. 初始化 Superset

```bash
docker exec -it superset superset fab create-admin --username admin --firstname Admin --lastname User --email admin@example.com --password admin
docker exec -it superset superset db upgrade
docker exec -it superset superset init
```

### 5. 建表并导入

```bash
Get-Content db\schema.sql | docker exec -i postgres-muying psql -U postgres -d muying
python db/load_to_pg.py
```

### 6. 跑 RFM 分析

```bash
python analysis/rfm.py
```

### 7. 访问 Superset

浏览器打开 `http://localhost:8088`

账号：`admin` / `admin`

### 8. Superset 使用说明

登录后：
1. **Datasets** → 已有 3 个数据集（members、orders、traffic）
2. **Charts** → 已有 11 张图
3. **Dashboards** → 打开 `母婴零售用户分析`，看完整看板

**图表清单：**
- 订单类型分布
- 营销活动分布
- 访问时段分布
- 省份分布
- 城市等级分布
- 宝宝年龄段分布
- 性别分布
- 月度GMV与增长率
- 门店销售 Top 10
- RF 用户分层
- RFM 热力图

## 数据字典

见 `docs/data_dictionary.md`。

## 分析报告

见 `docs/analysis_report.md`。

## License

MIT
```
