# 母婴零售数据字典

## 数据来源
- orders.csv：线上订单表（82.6 万条）
- members.csv：会员信息表（26.2 万条）
- traffic.csv：会员流量表（104.8 万条）
- products.csv：商品表（10.6 万条）
- stores.csv：门店表（435 条）
- related_orders.csv：连带订单表（15.4 万条）

## 表 1：members（会员信息）
| 字段 | 类型 | 含义 | 示例 |
|------|------|------|------|
| customer_type | str | 客户类型 | LA / SA / KA |
| province | str | 省份 | 湖北省 |
| city | str | 城市 | 武汉市 |
| city_level | str | 城市等级 | 新一线 / 三线 |
| member_id | str | 会员编码（主键） | 1548422274 |
| gender | str | 性别 | 女 |

## 表 2：orders（订单明细）
| 字段 | 类型 | 含义 | 示例 |
|------|------|------|------|
| member_id | str | 会员编码 | 1552781386 |
| baby_age | str | 宝宝年龄段 | 3-6岁 |
| order_date | date | 下单日期 | 2021-10-14 |
| product_id | str | 商品编码 | 138837627502787 |
| order_id | str | 订单号 | 6163421565100007831388376 |
| store_id | str | 门店编码 | a6 |
| amount | float | 销售额 | 281.60 |
| order_type | str | 订单类型 | 线上订单 / 连带订单 |
| campaign_type | str | 营销活动类型 | 特卖促销 |
| scene | str | 场景 | 自然 / 社群 / 短视频 |
| verify_date | date | 核销日期 | 2021-10-15 |
| year | int | 年 | 2021 |
| month | int | 月 | 10 |
| day | int | 日 | 14 |
| weekday | int | 星期（0=周一） | 3 |

## 表 3：traffic（访问行为）
| 字段 | 类型 | 含义 | 示例 |
|------|------|------|------|
| member_id | str | 会员编码 | 1502118228 |
| visit_date | date | 访问日期 | 2021-04-10 |
| visit_hour | int | 访问时段（0-23） | 11 |
| scene_id | str | 微信场景ID | 1047 |
| pv | int | 访问次数 | 6 |
| year | int | 年 | 2021 |
| month | int | 月 | 4 |
| weekday | int | 星期（0=周一） | 5 |


## 表 4：products（商品表）
| 字段 | 类型 | 含义 | 示例 |
|------|------|------|------|
| product_id | str | 商品编码（主键） | 137436824539252 |
| category_l1 | str | 一级品类 | 纺织品 |
| category_l2 | str | 二级品类 | 婴童服饰 |
| brand | str | 品牌 | 基诺浦 |

## 表 5：stores（门店表）
| 字段 | 类型 | 含义 | 示例 |
|------|------|------|------|
| store_type | str | 门店类型 | 社区服务店 |
| store_id | str | 门店编码（主键） | a1 |

## 表 6：related_orders（连带订单表）
| 字段 | 类型 | 含义 | 示例 |
|------|------|------|------|
| member_id | str | 会员编码 | 1540369585 |
| baby_age | str | 宝宝年龄段 | 1-3岁 |
| order_date | date | 下单日期 | 2021-06-08 |
| product_id | str | 商品编码 | 136954427541221 |
| order_id | str | 订单号 | 12130898171785591369544 |
| store_id | str | 门店编码 | a162 |
| amount | float | 销售额 | 3416.39 |
| order_type | str | 订单类型 | 连带订单 |
| campaign_type | str | 营销活动类型 | 特卖促销 |
| scene | str | 场景 | 短视频 |

## 表 7：churn_prediction（流失预测）
| 字段 | 类型 | 含义 | 示例 |
|------|------|------|------|
| member_id | str | 会员编码 | 1545739356 |
| frequency | int | 购买次数 | 4 |
| monetary | float | 消费金额 | 222.04 |
| avg_amount | float | 平均客单价 | 55.51 |
| lifespan_days | int | 生命周期天数 | 30 |
| last_order_date | date | 最后购买日期 | 2021-10-14 |
| is_churn | int | 是否流失（1=是） | 1 |
| churn_prob | float | 流失概率 | 0.87 |
## 数据质量说明
1. **orders**：原始 826,375 行，清洗后 800,759 行（去重 + 去空）
2. **members**：261,959 行，无重复
3. **traffic**：1,048,575 行无缺失
4. **核销日期**：286,979 条为空（线上订单无需核销，正常）
5. **数据时间**：2021 年

## 核心指标口径
| 指标 | 计算 |
|------|------|
| GMV | SUM(amount) |
| 订单数 | COUNT(DISTINCT order_id) |
| 用户数 | COUNT(DISTINCT member_id) |
| 客单价 | GMV / 订单数 |
| 复购率 | 购买≥2次的用户 / 总用户 |
| R 分 | 最近购买时间，5=最近 |
| F 分 | 购买频次，5=最频繁 |
| M 分 | 消费金额，5=最高 |