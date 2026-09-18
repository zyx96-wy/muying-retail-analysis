# 母婴零售用户行为分析

基于 80 万订单、26 万会员、104 万访问记录，完成从数据清洗、数据库建模，到 BI 可视化、RFM 用户分层、流失预测、推荐系统的全流程。

## 看板预览

![Dashboard](docs/screenshots/dashboard.png)

完整看板包含 5 个主题看板：

- **用户与销售总览**：用户画像 + 销售趋势 + RFM + 流失
- **商品与关联**：品类 + 品牌 + 关联规则
- **方案2_复购优惠**：预警人群 + 券种发放
- **方案3_搭配推荐**：强关联组合
- **方案4_活动与绑定**：活动质量 + 时序绑定

## 数据来源

本数据集来自和鲸社区（heywhale.com），搜索"母婴零售数据集清洗版本"。

- **原始数据**：6 个 CSV（会员、订单、流量、商品、门店、连带订单）
- **数据量**：80 万订单、26 万会员、104 万访问
- **数据时间**：2021-01 至 2021-12（有效订单 798,277 条）
- **数据截止日**：2021-12-31

**下载方式：**

1. 打开 heywhale.com
2. 搜索"母婴零售数据集清洗版本"
3. 下载 6 个 CSV
4. 放到 `data/raw/` 目录

## 技术栈

| 层 | 工具 | 说明 |
|----|------|------|
| 数据清洗 | Python + pandas | 数据预处理、缺失值处理、格式标准化 |
| 数据库 | PostgreSQL + Docker | 容器化部署，提供稳定、并发支持 |
| BI 可视化 | Apache Superset | 开源 BI 工具，支持丰富图表和交互式看板 |
| 机器学习 | Scikit-learn | 随机森林流失预测（AUC 0.77） |
| 产品设计 | Figma | 3 个核心页面原型 |

## 核心发现

1. **用户画像**：86.7% 女性，1-3 岁宝宝家长为主
2. **地域**：下沉市场为主，河南占 28.7%
3. **访问高峰**：10 点、15 点、20 点
4. **销售波动**：大促后必跌
5. **RFM**：76% 用户流失（R=1）
6. **商品**：奶粉占 58% 销售额，飞鹤是第一名
7. **关联**：3 段奶粉 × 婴童服饰客单价 4220
8. **渠道**：社区服务店占 58% 销售额
9. **活动**：福利秒杀带来的用户复购率最高（56.55%）
10. **时序绑定**：尿裤 → 零辅食平均间隔 29 天（最短）

### 推荐方案成果

| 方案 | 目标 | 成果 |
|------|------|------|
| 方案 1 | 7 天内智能推荐 | SQL 跑通 |
| 方案 2 | 复购优惠（预警人群） | **44,295 人命中** |
| 方案 3 | 搭配推荐（品类关联） | Top 10 强关联组合 |
| 方案 4 | 活动 + 绑定 | **完成**（2 张图 + 时序绑定表） |

**方案 2 详情**：

- 奶粉预警 13,113 人（距上次购买 172~304 天）
- 尿裤预警 12,473 人（177~302 天）
- 零辅食预警 18,709 人（157~299 天）

**方案 4 详情**：

- 活动质量排名：福利秒杀 > 多人拼团 > 特卖促销 > 自然 > 活动报名
- 时序推荐：买尿裤后 29 天推零辅食（最强绑定）

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
│   ├── rfm.py
│   ├── churn_model.py
│   └── sql/              # 所有分析 SQL
├── docs/
│   ├── analysis_report.md
│   ├── data_dictionary.md
│   ├── PRD.md
│   ├── analysis_modules.md
│   └── figma/            # 原型截图
├── docker-compose.yml
├── superset_config.py
├── .env
└── README.md
```

## 环境要求与快速开始

### 1. Python 环境

建议使用 Anaconda 创建独立环境：

```bash
conda create -n muying python=3.11 -y
conda activate muying
pip install pandas openpyxl psycopg2-binary sqlalchemy scikit-learn
```

### 2. Docker Desktop

1. 下载并安装 Docker Desktop：https://www.docker.com/products/docker-desktop/
2. 安装时勾选 **Use WSL 2**（Windows 用户）
3. 安装完成后重启电脑
4. 打开 Docker Desktop，等待状态变为稳定运行（通常为绿色）

**验证安装：**

```bash
docker --version
docker run hello-world
```

看到 "Hello from Docker!" 信息即表示安装成功。

### 3. 下载数据

从和鲸社区下载 6 个 CSV 文件，放到项目的 `data/raw/` 目录下：

- `members.csv`
- `orders.csv`
- `traffic.csv`
- `products.csv`
- `stores.csv`
- `related_orders.csv`

### 4. 清洗数据

在项目根目录执行：

```bash
python etl/clean.py
```

此步骤会处理原始数据中的缺失值、重复记录、格式不一致等问题，输出到 `data/processed/` 目录。

### 5. 启动数据库和 Superset

在项目根目录执行：

```bash
docker compose up -d
```

这会启动配置好的 PostgreSQL 数据库和 Apache Superset 服务。

### 6. 初始化 Superset

执行以下命令初始化 Superset，创建管理员账户并升级数据库：

```bash
# 创建管理员用户
docker exec -it superset superset fab create-admin \
  --username admin \
  --firstname Admin \
  --lastname User \
  --email admin@example.com \
  --password admin

# 升级数据库结构
docker exec -it superset superset db upgrade

# 初始化角色和权限
docker exec -it superset superset init
```

### 7. 建表并导入数据

将数据库表结构导入 PostgreSQL 并加载清洗后的数据：

```bash
# 导入数据库 Schema（Windows PowerShell）
Get-Content db\schema.sql | docker exec -i postgres-muying psql -U postgres -d muying

# 执行 Python 脚本将数据导入数据库
python db/load_to_pg.py
```

> **注意**：如果使用的是 Linux/macOS 或 Git Bash，请将 `Get-Content` 替换为 `cat`：
>
> ```bash
> cat db/schema.sql | docker exec -i postgres-muying psql -U postgres -d muying
> ```

### 8. 执行 RFM 分析与流失预测

```bash
python analysis/rfm.py
python analysis/churn_model.py
```

### 9. 访问 Superset 看板

1. 在浏览器中打开：`http://localhost:8088`
2. 使用管理员账号登录：
   - **用户名**：`admin`
   - **密码**：`admin`
3. 登录后，导航至 **Dashboards**，打开 5 个主题看板：
   - `1. 用户与销售总览`
   - `2. 商品与关联`
   - `3. 方案2_复购优惠`
   - `4. 方案3_搭配推荐`
   - `5. 方案4_活动与绑定`

**已创建的图表清单：**

**用户与销售总览**

- 性别分布 / 宝宝年龄分布 / 访问时段分布
- 省份分布 / 城市等级分布
- 月度分析 / 营销活动分布 / 订单类型分布
- 门店销售额
- LTV 用户占比 / LTV 金额占比
- 用户复购漏斗 / 月度用户与复购率分布
- 流失风险分布 / 流失归因分析
- RF 分析图 / RFM 热力图

**商品与关联**

- 品类销售分布
- 销售额前 10 的品牌
- 品牌定位矩阵
- 地域价位分析
- 门店类型 × 品类分析
- 一级品类关联热力图
- 跨品类关联分析

**方案2_复购优惠**

- 各品类预警人数（饼图）
- 复购周期差异（柱状图）
- 各券种发放数量（柱状图）

**方案3_搭配推荐**

- Top 10 强关联组合分布
- 推荐品类分布

**方案4_活动与绑定**

- 各活动渠道复购率（柱状图）
- 各活动渠道客单价（柱状图）

## 数据字典

详细的字段说明、数据类型和业务含义请见 `docs/data_dictionary.md`。

## 分析报告

完整的分析过程、方法论、核心发现和业务建议请见 `docs/analysis_report.md`。

## PRD 文档

4 个推荐方案的详细产品设计、AB 实验设计、数据逻辑请见 `docs/PRD.md`。

## License

MIT