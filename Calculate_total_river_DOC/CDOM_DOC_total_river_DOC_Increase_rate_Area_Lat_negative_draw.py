import warnings
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.lines import Line2D

# 忽略 openpyxl 警告  # English: neglect
warnings.filterwarnings('ignore', category=UserWarning, module='openpyxl')

# 文件路径  # English: File path
file_path = r"D:\UZH\2024\20240122 Nutrient and Organic Carbon references\3_river_mouth_DOC\DOC_update_20250203\Total_DOC_increase_rate\Annual_increase_rate_DOC_All_Property.csv"
output_path = r"D:\UZH\2024\20240122 Nutrient and Organic Carbon references\3_river_mouth_DOC\DOC_update_20250203\Total_DOC_increase_rate\Annual_increase_rate_DOC_De.tif"

# 读取数据  # English: Read data
df = pd.read_csv(file_path)
df['Annual_Increase_Rate_1'] = df['Annual_Increase_Rate_1'] / 1e6  # Tg C/yr
df.dropna(subset=['area_km2', 'Annual_Increase_Rate_1', 'center_lat'], inplace=True)

# 设定流域面积的 5 个分类（对数分级）  # English: Set the basin area
bins = [1, 10, 100, 1000, 100000, np.inf]
labels = [
    "$1 \mathregular{-} 10$ km²", "$10 \mathregular{-} 10^2$ km²", "$10^2 \mathregular{-} 10^3$ km²",
    "$10^3 \mathregular{-} 10^5$ km²", "$>10^5$ km²"]
df['area_class'] = pd.cut(df['area_km2'], bins=bins, labels=range(5), include_lowest=True)

# 使用 ColorBrewer Set1 的 5 个颜色  # English: use
colors = ["#ffffcc", "#a1dab4", "#41b6c4", "#2c7fb8", "#253494"]

# 筛选负增长数据  # English: Screen negative growth data
df_neg = df[df['Annual_Increase_Rate_1'] < 0].copy()

# 图形设置  # English: Graphic settings
fig, ax = plt.subplots(figsize=(19 / 2.54, 5 / 2.54), dpi=600)
font_kwargs = {'fontsize': 6, 'fontname': 'Arial'}

# 绘图：按 area_class 分组  # English: Drawing
for i in range(5):
    subset = df_neg[df_neg['area_class'] == i]
    ax.scatter(
        subset['center_lat'],
        -subset['Annual_Increase_Rate_1'],  # 取负值以显示在 log 正方向  # English: Take a negative value to display in
        s=np.sqrt(subset['area_km2']) * 0.04,
        color=colors[i],
        alpha=0.7,
        edgecolors='none',
        label=labels[i]
    )

# 设置坐标轴  # English: Set the axis
ax.set_xlabel('Latitude (°N)', **font_kwargs)
ax.set_xlim(49, 84)
ax.set_ylabel('Decrease rate (Tg C yr$^{-1}$)', **font_kwargs)
ax.tick_params(labelsize=6)

# 设置 Y 轴为对数坐标轴，显示负增长的绝对值  # English: set up
ax.set_yscale('log')
yticks = [1e-1, 1e-3, 1e-5, 1e-7, 1e-9, 1e-11]
yticklabels = [r'$10^{-1}$', r'$10^{-3}$', r'$10^{-5}$', r'$10^{-7}$', r'$10^{-9}$', r'$10^{-11}$']
ax.set_yticks(yticks)
ax.set_yticklabels(yticklabels, **font_kwargs)

# 字体设置  # English: Font settings
for label in ax.get_xticklabels() + ax.get_yticklabels():
    label.set_fontname('Arial')

# 构建 legend 元素  # English: Build
legend_elements = [
    Line2D([0], [0], marker='o', color='none', label=labels[i],
           markerfacecolor=colors[i], markeredgewidth=0, markersize=i + 3)
    for i in range(5)
]
title_element = Line2D([0], [0], marker='', color='none', label='Catchment area (km²)')
legend_elements_with_title = [title_element] + legend_elements
legend = ax.legend(
    handles=legend_elements_with_title,
    prop={'size': 6, 'family': 'Arial'},
    loc='upper center',
    bbox_to_anchor=(0.45, -0.25),
    ncol=8,
    frameon=True,
    facecolor='0.9',
    edgecolor='none',
    borderpad=0.4,
    labelspacing=0.5,
    handletextpad=0.5,
    columnspacing=0.8
)
legend.get_texts()[0].set_fontname('Arial')
legend.get_texts()[0].set_fontsize(6)

# 添加网格  # English: Add a grid
ax.grid(True, which='both', linestyle='--', alpha=0.5)

# 保存图像  # English: Save the image
plt.tight_layout()
plt.savefig(output_path, dpi=600, bbox_inches='tight', pad_inches=0.1)
plt.show()