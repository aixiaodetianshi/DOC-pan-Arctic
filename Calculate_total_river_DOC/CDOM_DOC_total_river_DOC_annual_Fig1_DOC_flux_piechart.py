import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os

# 设置字体  # English: Set fonts
plt.rcParams["font.family"] = "Arial"

# 输出目录和文件名  # English: Output directory and filename
output_dir = r"D:\UZH\2024\20240122 Nutrient and Organic Carbon references\3_river_mouth_DOC\DOC_update_20250203\Total_DOC_average"
output_area_fig = os.path.join(output_dir, "Fig1_DOC_flux_piechart.tif")

# 分组定义  # English: Grouping definition
river_Name = ["Ob",    "Yenisey", "Lena", "Kolyma", "Yukon",   "Mackenzie"]
river_number = [18.74, 0.15,       7.71,   1.79,    4.2,       33.32]

# === 新增：计算百分比 ===  # English: New
total_river = sum(river_number)
river_percent = [num / total_river * 100 for num in river_number]

# 打印计算结果，检查  # English: Print calculation results
for name, num, pct in zip(river_Name, river_number, river_percent):
    print(f"{name}: {num} DOC flux，占比 {pct:.2f}%")

# 调色板  # English: Palette
colors = ["#66c2a5", "#fc8d62", "#8da0cb", "#e78ac3", "#a6d854", "#ffd92f"]

# === 饼状图 ===  # English: Pie bar chart
fig1, ax1 = plt.subplots(figsize=(0.75, 0.75))  #

wedges, texts, autotexts = ax1.pie(
    river_number,
    labels=None,  # 不显示文字，百分比显示在autotexts  # English: No text displayed
    autopct=lambda p: f'{p:.1f}',  # 百分比格式  # English: Percentage format
    colors=colors,
    startangle=-60,
    textprops={"fontsize": 6},
    labeldistance=0.6
)

# 标题  # English: title
ax1.set_title("DOC flux(%)", fontsize=6, pad=-160)

# 统一百分比文字大小  # English: Unified percentage text size
for autotext in autotexts:
    autotext.set_fontsize(6)


# 示例：如果想调整某一个百分比标签位置（例如索引4，Yukon）  # English: Example
idx = 1  # 第5个元素（从0开始计）  # English: The
angle = (wedges[idx].theta2 + wedges[idx].theta1) / 2
x = 1.25 * np.cos(np.radians(angle))
y = 1.1 * np.sin(np.radians(angle))
autotexts[idx].set_position((x, y))
autotexts[idx].set_ha('center')
autotexts[idx].set_va('center')

# 示例：如果想调整某一个百分比标签位置（例如索引4，Yukon）  # English: Example
idx = 3  # 第5个元素（从0开始计）  # English: The
angle = (wedges[idx].theta2 + wedges[idx].theta1) / 2
x = 1.3 * np.cos(np.radians(angle))
y = 1.1 * np.sin(np.radians(angle))
autotexts[idx].set_position((x, y))
autotexts[idx].set_ha('center')
autotexts[idx].set_va('center')

# 示例：如果想调整某一个百分比标签位置（例如索引4，Yukon）  # English: Example
idx = 4  # 第5个元素（从0开始计）  # English: The
angle = (wedges[idx].theta2 + wedges[idx].theta1) / 2
x = 1.3 * np.cos(np.radians(angle))
y = 0.7 * np.sin(np.radians(angle))
autotexts[idx].set_position((x, y))
autotexts[idx].set_ha('center')
autotexts[idx].set_va('center')

# 不显示标签文字，仅显示百分比  # English: No label text displayed
for text in texts:
    text.set_text('')

# 保存图像  # English: Save the image
plt.savefig(output_area_fig, dpi=600, bbox_inches='tight', pad_inches=0.001, format='tiff', transparent=True)
plt.close()