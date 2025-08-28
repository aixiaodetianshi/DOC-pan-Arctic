import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.lines import Line2D

# 文件路径  # English: File path
file_path = r"D:\UZH\2024\20240122 Nutrient and Organic Carbon references\3_river_mouth_DOC\DOC_update_20250203\Total_DOC_average\All_Properites.csv"
output_path = r"D:\UZH\2024\20240122 Nutrient and Organic Carbon references\3_river_mouth_DOC\DOC_update_20250203\Total_DOC_average\ARCADE_MERIT_pan_Arctic_average_DOC_Area_vs_Latitude_log7class_colorbrewer_inside_legend.tif"

# 读取数据并清洗  # English: Read data and clean
df = pd.read_csv(file_path)
df = df.dropna(subset=['area_km2', 'Average_Total_DOC_Area_Unit', 'center_lat'])
df = df[df['Average_Total_DOC_Area_Unit'] > 0]

# 设定流域面积的 5 个分类（对数分级）  # English: Set the basin area
bins = [1, 10, 100, 1000, 100000, np.inf]
labels = [
    "$1 \mathregular{-} 10$ km²", "$10 \mathregular{-} 10^2$ km²", "$10^2 \mathregular{-} 10^3$ km²",
    "$10^3 \mathregular{-} 10^5$ km²", "$>10^5$ km²"]
df['area_class'] = pd.cut(df['area_km2'], bins=bins, labels=range(5), include_lowest=True)

# 使用 ColorBrewer Set1 的 5 个颜色  # English: use
colorbrewer_colors = ["#ffffcc", "#a1dab4", "#41b6c4", "#2c7fb8", "#253494"]
colors = colorbrewer_colors

# 散点大小：按流域面积开方调整  # English: Scatter size
sizes = np.sqrt(df['area_km2']) * 0.1  # 缩放因子可根据实际需要微调  # English: The scaling factor can be fine-tuned according to actual needs

# 创建图形  # English: Create a graph
fig, ax = plt.subplots(figsize=(19/2.54, 5/2.54), dpi=600)
font_kwargs = {'fontsize': 6, 'fontname': 'Arial'}

# 分类绘图  # English: Classification drawing
for i in range(5):
    subset = df[df['area_class'] == i]
    ax.scatter(subset['center_lat'], subset['Average_Total_DOC_Area_Unit'],
               s=sizes[subset.index], color=colors[i], alpha=0.7, edgecolors='none', label=labels[i])

# 对数 Y 轴  # English: Logarithm
ax.set_yscale('log')

# 坐标轴与字体设置  # English: Axis and Font Settings
ax.set_xlabel('Latitude (°N)', **font_kwargs)
ax.set_xlim(49, 84)
# 设置 Y 轴范围和刻度间隔  # English: set up
ax.set_xticks(np.arange(49, 85, 1))
ax.set_ylabel('DOC flux per unit area\n(Tg C km$^{-2}$)', **font_kwargs)
ax.tick_params(labelsize=6)
for label in ax.get_xticklabels() + ax.get_yticklabels():
    label.set_fontname('Arial')

# 构建 legend 元素，限制最小 marker size 防止太小  # English: Build
legend_sizes = [np.mean(sizes[df['area_class'] == i]) for i in range(5)]
min_marker_size = 4  # 最小 marker radius（单位：points）  # English: Minimum

legend_elements = [
    Line2D(
        [0], [0],
        marker='o',
        color='none',
        label=labels[i],
        markerfacecolor=colors[i],
        markeredgewidth=0,
        markersize=max(np.sqrt(legend_sizes[i]), min_marker_size)  # 半径开方后做最小限制  # English: Minimum limit after radius square
    )
    for i in range(5)
]

# 构造伪“标题”图例元素  # English: Construct pseudo
title_element = Line2D(
    [0], [0],
    marker='',
    color='none',
    label='Catchment Area (km²)'
)

# 将标题放在 legend_elements 最前面  # English: Put the title
legend_elements_with_title = [title_element] + legend_elements

# 横向放置图例于下方，手动模拟标题放左边  # English: Place the legend horizontally below
legend = ax.legend(
    handles=legend_elements_with_title,
    prop={'size': 6, 'family': 'Arial'},
    loc='upper center',
    bbox_to_anchor=(0.45, -0.25),
    ncol=8,
    frameon=True,
    facecolor='0.9',  # 10% 灰度背景  # English: Grayscale background
    edgecolor='none',  # 边框透明  # English: Transparent border
    borderpad=0.4,
    labelspacing=0.5,
    handletextpad=0.5,
    columnspacing=0.8
)

# 设置标题样式（即第一个文本元素）  # English: Set the title style
legend.get_texts()[0].set_fontname('Arial')
legend.get_texts()[0].set_fontsize(6)


# 添加网格  # English: Add a grid
ax.grid(True, which='both', linestyle='--', alpha=0.5)

# 保存图像  # English: Save the image
plt.tight_layout()
plt.savefig(output_path, dpi=600 , bbox_inches='tight', pad_inches=0.01)
plt.show()