import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
import matplotlib.ticker as mticker

# 设置字体
plt.rcParams["font.family"] = "Arial"

# 文件路径设置
input_file = r"D:\UZH\2024\20240122 Nutrient and Organic Carbon references\3_river_mouth_DOC\DOC_update_20250203\Total_DOC_increase_rate\Annual_increase_rate_DOC_All_Property.csv"
output_dir = r"D:\UZH\2024\20240122 Nutrient and Organic Carbon references\3_river_mouth_DOC\DOC_update_20250203\Total_DOC_increase_rate"
output_bar_fig = os.path.join(output_dir, "mean_increase_rate_5class_Unit_In_histogram.tif")

# 读取数据
df = pd.read_csv(input_file)

# 去除缺失值，仅保留正增长数据
df = df.dropna(subset=['area_km2', 'Annual_Increase_Rate_DOC_Area_Unit'])
df_pos = df[df['Annual_Increase_Rate_DOC_Area_Unit'] > 0].copy()

# 分组
bins = [1, 10, 100, 1000, 100000, np.inf]
labels = ['1–10', '10–100', '100–1000', '1000–100000', '>100000']
df_pos['area_class'] = pd.cut(df_pos['area_km2'], bins=bins, labels=labels, right=False)

# 计算每组的平均增长率
grouped = df_pos.groupby('area_class', observed=True)['Annual_Increase_Rate_DOC_Area_Unit'].mean().reset_index()

# 为直方图设置 X 轴数字标签（1–5）
grouped['group_index'] = range(1, len(grouped) + 1)

# 调色板
colors = ["#ffffcc", "#a1dab4", "#41b6c4", "#2c7fb8", "#253494"]

# 绘图
fig, ax = plt.subplots(figsize=(4/2.54, 2/2.54), dpi=600)  # 大小为 6cm x 4cm

bars = ax.bar(
    grouped['group_index'],
    grouped['Annual_Increase_Rate_DOC_Area_Unit'],
    color=colors,
    width=0.6
)

# 设置坐标轴和标签
ax.set_xticklabels([])  # 隐藏横轴坐标标签（1, 2, 3, 4, 5）
ax.set_ylabel("Mean", fontsize=6)
ax.tick_params(axis='y', labelsize=6)
ax.tick_params(axis='x', labelsize=6)

# 设置 Y 轴为对数坐标轴，并确保标签为 10 的幂次方
ax.set_yscale('log')
# 设置手动刻度
yticks = [1e-5, 1e-7, 1e-9, 1e-11]
yticklabels = [r'$10^{-5}$', r'$10^{-7}$', r'$10^{-9}$', r'$10^{-11}$']

ax.set_yticks(yticks)
ax.set_yticklabels(yticklabels, fontsize=6, fontname='Arial')


# 添加数值标签（竖向显示）
for bar in bars:
    height = bar.get_height()
    ax.annotate(f'{height:.2e}',
                xy=(bar.get_x() + bar.get_width() / 2, 1e-10),
                xytext=(0, 5),
                textcoords="offset points",
                ha='center',
                va='bottom',
                fontsize=5,
                rotation=90)  # ⬅️ 设置竖向显示

# 去除边框顶部和右侧
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

plt.tight_layout()
plt.savefig(output_bar_fig, dpi=600, bbox_inches='tight', format='tiff', transparent=True)
plt.close()