import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os

# 设置字体
plt.rcParams["font.family"] = "Arial"

# 路径设置
input_file = r"D:\UZH\2024\20240122 Nutrient and Organic Carbon references\3_river_mouth_DOC\DOC_update_20250203\Total_DOC_average\All_Properites.csv"
output_dir = r"D:\UZH\2024\20240122 Nutrient and Organic Carbon references\3_river_mouth_DOC\DOC_update_20250203\Total_DOC_average"
output_area_fig = os.path.join(output_dir, "area_5class_total_DOC_piechart.tif")

# 读取数据
df = pd.read_csv(input_file)

# 分组定义
bins = [1, 10, 100, 1000, 100000, np.inf]
labels = ['1–10', '10–100', '100–1000', '1000–100000', '>100000']
df['area_class'] = pd.cut(df['area_km2'], bins=bins, labels=labels, right=False)

# 统计每组面积总和和 DOC 总和
grouped = df.groupby('area_class', observed=True).agg(
    total_area_km2=('area_km2', 'sum'),
    total_DOC=('Average_Total_DOC', 'sum')
)

# 计算百分比
grouped['Average_Total_DOC_percent'] = grouped['total_DOC'] / grouped['total_DOC'].sum() * 100

# 调色板
colors = ["#ffffcc", "#a1dab4", "#41b6c4", "#2c7fb8", "#253494"]

# === 饼状图：面积百分比 ===
fig1, ax1 = plt.subplots(figsize=(1.18, 1.18))  # 4cm x 4cm ≈ 1.57in x 1.57in
wedges, texts, autotexts = ax1.pie(
    grouped['total_DOC'],
    labels=None,
    autopct=lambda p: f'{p:.1f}%',
    colors=colors,
    startangle=140,
    textprops={"fontsize": 6},
    labeldistance=0.6
)

# 设置标题
ax1.set_title("Total DOC Distribution", fontsize=6, pad=-160)

# 设置统一字体大小
for i in range(len(autotexts)):
    autotexts[i].set_fontsize(6)

# 将第5组的百分比标签移动到饼图外部、紧贴边缘
idx = 4  # 第5组索引
angle = (wedges[idx].theta2 + wedges[idx].theta1) / 2
x = 1.1 * np.cos(np.radians(angle))  # 调整 1.0~1.2 控制贴图边缘
y = 1.1 * np.sin(np.radians(angle))
autotexts[idx].set_position((x, y))
autotexts[idx].set_ha('center')
autotexts[idx].set_va('center')

# 不显示 label，仅显示百分比
for text in texts:
    text.set_text('')

# 保存图像
plt.savefig(output_area_fig, dpi=600, bbox_inches='tight', format='tiff', transparent=True)
plt.close()

