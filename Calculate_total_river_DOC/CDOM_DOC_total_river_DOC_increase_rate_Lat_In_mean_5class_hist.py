import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
import matplotlib.ticker as mticker

# 设置字体  # English: Set fonts
plt.rcParams["font.family"] = "Arial"

# 文件路径设置  # English: File path settings
input_file = r"D:\UZH\2024\20240122 Nutrient and Organic Carbon references\3_river_mouth_DOC\DOC_update_20250203\Total_DOC_increase_rate\Annual_increase_rate_DOC_All_Property.csv"
output_dir = r"D:\UZH\2024\20240122 Nutrient and Organic Carbon references\3_river_mouth_DOC\DOC_update_20250203\Total_DOC_increase_rate"
output_bar_fig = os.path.join(output_dir, "mean_increase_rate_5class_In_histogram.tif")

# 读取数据  # English: Read data
df = pd.read_csv(input_file)

# 单位转换 Tg C/yr  # English: Unit conversion
df['Annual_Increase_Rate_1'] = df['Annual_Increase_Rate_1'] / 1e6

# 去除缺失值，仅保留正增长数据  # English: Remove missing values
df = df.dropna(subset=['area_km2', 'Annual_Increase_Rate_1'])
df_pos = df[df['Annual_Increase_Rate_1'] > 0].copy()

# 分组  # English: Grouping
bins = [1, 10, 100, 1000, 100000, np.inf]
labels = ['1–10', '10–100', '100–1000', '1000–100000', '>100000']
df_pos['area_class'] = pd.cut(df_pos['area_km2'], bins=bins, labels=labels, right=False)

# 计算每组的平均增长率  # English: Calculate the average growth rate for each group
grouped = df_pos.groupby('area_class', observed=True)['Annual_Increase_Rate_1'].mean().reset_index()

# 为直方图设置 X 轴数字标签（1–5）  # English: Setting for histogram
grouped['group_index'] = range(1, len(grouped) + 1)

# 调色板  # English: Palette
colors = ["#ffffcc", "#a1dab4", "#41b6c4", "#2c7fb8", "#253494"]

# 绘图  # English: Drawing
fig, ax = plt.subplots(figsize=(5/2.54, 2.5/2.54), dpi=600)  # 大小为 6cm x 4cm  # English: Size is

bars = ax.bar(
    grouped['group_index'],
    grouped['Annual_Increase_Rate_1'],
    color=colors,
    width=0.6
)

# 设置坐标轴和标签  # English: Set the axis and label
ax.set_xticklabels([])  # 隐藏横轴坐标标签（1, 2, 3, 4, 5）  # English: Hide horizontal axis coordinate label
ax.set_ylabel("Mean", fontsize=6)
ax.tick_params(axis='y', labelsize=6)
ax.tick_params(axis='x', labelsize=6)

# 设置手动刻度  # English: Setting manual ticks
yticks = [0, 2*1e-5, 4*1e-5]
yticklabels = [r'0', r'2x$10^{-5}$', r'4x$10^{-5}$']

ax.set_yticks(yticks)
ax.set_yticklabels(yticklabels, fontsize=6, fontname='Arial')


# 添加数值标签（竖向显示）  # English: Add a numerical tag
for bar in bars:
    height = bar.get_height()
    ax.annotate(f'{height:.2e}',
                xy=(bar.get_x() + bar.get_width() / 2, 0),
                xytext=(0, 5),
                textcoords="offset points",
                ha='center',
                va='bottom',
                fontsize=5,
                rotation=90)  # ⬅️ 设置竖向显示  # English: Set vertical display

# 去除边框顶部和右侧  # English: Remove the top and right sides of the border
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

plt.tight_layout()
plt.savefig(output_bar_fig, dpi=600, bbox_inches='tight', format='tiff', transparent=True)
plt.close()