import os
import random
import csv
from datetime import date, timedelta

random.seed(20261026)

# 天津各区：基准单价（元/㎡）、基准挂牌天数、库存小区名
DISTRICTS = {
    "和平区": (58000, 65, ["小白楼公寓", "南市大街小区", "华安北里", "新兴里", "南京路公馆"]),
    "河西区": (37000, 55, ["友谊路小区", "梅江康城", "体院北里", "小海地三区", "八里台新村"]),
    "南开区": (33000, 58, ["水上公园里", "王顶堤小区", "天塔街公寓", "学府花园", "万兴街小区"]),
    "河东区": (25000, 72, ["中山门小区", "太阳城公寓", "大王庄新村", "万新村北里", "二号桥小区"]),
    "河北区": (23000, 78, ["中山路小区", "小树林公寓", "王串场新村", "建昌道小区", "金钟河家园"]),
    "红桥区": (21000, 85, ["西站公寓", "邵公庄新村", "西于庄小区", "芥园道家园", "丁字沽三号路"]),
    "西青区": (19000, 70, ["王兰庄小区", "中北镇家园", "李七庄公寓", "精武镇新村", "杨柳青镇区"]),
    "北辰区": (16500, 82, ["双街新苑", "宜兴埠小区", "小淀家园", "北辰花园", "果园新村"]),
    "东丽区": (15500, 76, ["金钟街小区", "新立花园", "华明新家园", "军粮城公寓", "东丽湖璟苑"]),
    "津南区": (14500, 80, ["咸水沽新村", "双港花园", "八里台镇区", "海河教育园公寓", "辛庄家园"]),
    "武清区": (12500, 88, ["杨村花园", "下朱庄新苑", "南湖公寓", "武清开发区小区", "曹子里镇区"]),
    "宝坻区": (9500, 95, ["宝坻新城公寓", "京津新城苑", "潮阳花园", "高家庄镇区", "宝平家园"]),
}

LAYOUTS = [
    ("1室1厅", (35, 55)),
    ("2室1厅", (55, 85)),
    ("2室2厅", (75, 95)),
    ("3室1厅", (85, 110)),
    ("3室2厅", (95, 135)),
    ("4室2厅", (130, 180)),
]

ORIENTATIONS = ["南", "南北", "东南", "西南", "东", "西", "北", "西北"]

FLOOR_TYPES = ["低楼层", "中楼层", "高楼层"]


def pick_layout():
    r = random.random()
    if r < 0.10:
        return LAYOUTS[0]
    if r < 0.38:
        return LAYOUTS[1]
    if r < 0.62:
        return LAYOUTS[2]
    if r < 0.78:
        return LAYOUTS[3]
    if r < 0.95:
        return LAYOUTS[4]
    return LAYOUTS[5]


rows = []
today = date(2026, 10, 26)

for i in range(800):
    district = random.choice(list(DISTRICTS.keys()))
    base_price, base_days, communities = DISTRICTS[district]

    layout, (amin, amax) = pick_layout()
    area = round(random.uniform(amin, amax), 1)

    orientation = random.choices(
        ORIENTATIONS,
        weights=[22, 30, 12, 10, 8, 8, 6, 4],
    )[0]

    floor_type = random.choices(FLOOR_TYPES, weights=[28, 48, 24])[0]
    total_floors = random.choice([6, 11, 18, 26, 33])

    # 单价调整：面积越大单价略低；南北通透/南向溢价；中高楼层溢价
    unit = base_price
    unit *= 1 - (area - 80) * 0.0009          # 面积影响
    if orientation in ("南北", "南"):
        unit *= 1.05
    elif orientation in ("北", "西北"):
        unit *= 0.94
    if floor_type == "中楼层":
        unit *= 1.02
    elif floor_type == "低楼层":
        unit *= 0.97
    unit *= random.uniform(0.90, 1.12)         # 房源个体差异
    unit = int(round(unit, -1))

    total_price = round(unit * area / 10000, 1)  # 万元

    # 挂牌天数：区域基准 × 随机波动；大户型更难卖
    days = int(base_days * random.uniform(0.35, 2.1) * (1 + (area - 80) * 0.002))
    days = max(3, days)

    # 挂牌时间 = 今天往前推 days 天
    list_date = today - timedelta(days=days)

    # 降价：挂得越久越可能降，幅度也越大
    drop_prob = min(0.80, 0.05 + days / 320)
    if random.random() < drop_prob:
        price_dropped = "是"
        drop_pct = round(random.uniform(1.0, 3.0 + days / 90), 1)
        drop_pct = min(drop_pct, 18.0)
    else:
        price_dropped = "否"
        drop_pct = 0.0

    rows.append({
        "房源编号": f"TJ{i + 1:04d}",
        "区域": district,
        "小区": random.choice(communities),
        "户型": layout,
        "面积": area,
        "楼层": f"{floor_type}/共{total_floors}层",
        "朝向": orientation,
        "挂牌总价": total_price,
        "单价": unit,
        "挂牌天数": days,
        "是否降价": price_dropped,
        "降价幅度": drop_pct,
        "挂牌日期": list_date.isoformat(),
    })

# 故意留一点缺失值，模拟真实数据（读取时能学到"数据不干净"这一课）
for idx in random.sample(range(len(rows)), 18):
    rows[idx]["朝向"] = ""
for idx in random.sample(range(len(rows)), 6):
    rows[idx]["面积"] = ""

out_dir = r"D:\自然语言处理\职业规划\项目01_天津二手房"
os.makedirs(out_dir, exist_ok=True)
out_path = os.path.join(out_dir, "天津二手房_2026年10月.csv")
with open(out_path, "w", newline="", encoding="utf-8-sig") as f:
    writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
    writer.writeheader()
    writer.writerows(rows)

print(f"已生成 {len(rows)} 条数据")
print(f"保存到：{out_path}")
