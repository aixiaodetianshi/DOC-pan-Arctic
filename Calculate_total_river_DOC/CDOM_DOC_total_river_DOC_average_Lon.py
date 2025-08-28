# 绘制 河流 DOC 及其不确定性随纬度变化的趋势。  # English: draw
# 使其以 纬度（Lat） 为横轴，而 DOC 通量及其不确定性 为纵轴，并按纬度排序。  # English: Make it

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# 读取数据  # English: Read data
file_path = r"D:\UZH\2024\20240122 Nutrient and Organic Carbon references\DOC\DOC_update_20250203\Total_DOC_average\average_Total_DOC_river_endpoints_Lon.xlsx"
output_path = r"D:\UZH\2024\20240122 Nutrient and Organic Carbon references\DOC\DOC_update_20250203\Total_DOC_average\average_Total_DOC_river_endpoints_Lon.tif"
data = pd.read_excel(file_path)

# 单位转换：Ton 转换为 Tg (1 Tg = 10^6 Ton)  # English: Unit conversion
data['Average_Total_DOC'] = data['Average_Total_DOC'] / 1e6
data['Average_Total_DOC_Uncertainty'] = data['Average_Total_DOC_Uncertainty'] / 1e6

# 按纬度排序（从低到高）  # English: Sort by latitude
data = data.sort_values(by='Longitude')

# 提取数据  # English: Extract data
Lon = data['Longitude']
total_doc = data['Average_Total_DOC']
uncertainty = data['Average_Total_DOC_Uncertainty']

# 创建图像  # English: Create an image
fig, ax = plt.subplots(figsize=(17/2.54, 3.5/2.54))  # 转换为厘米  # English: Convert to centimeters

# 绘制不确定性范围 (灰色阴影区域)  # English: Draw uncertainty ranges
ax.fill_between(Lon,
                total_doc - uncertainty,
                total_doc + uncertainty,
                color='grey', alpha=0.3,
                label='Uncertainty')

# 绘制总DOC通量变化曲线  # English: Draw total
ax.plot(Lon, total_doc, color='royalblue', linewidth=0.5, label='Total DOC Flux')

# 图例与标签  # English: Legends and labels
ax.set_xlabel('Longitude(°E)', fontsize=6, fontname='Arial')
ax.set_ylabel('Total DOC Flux (Tg C)', fontsize=6, fontname='Arial')
ax.legend(fontsize=6, frameon=False, loc='upper left', labelspacing=0.25)

# 设置 X 轴范围和刻度间隔  # English: set up
ax.set_xlim(-180, 180)
ax.set_xticks(np.arange(-180, 181, 15))

# 设置 Y 轴最大值为 8  # English: set up
ax.set_ylim(0, 8)

# 启用网格  # English: Enable grid
ax.grid(True, linestyle='--', alpha=0.5)

# 设置刻度  # English: Set the scale
ax.tick_params(axis='both', which='major', labelsize=6)
for label in (ax.get_xticklabels() + ax.get_yticklabels()):
    label.set_fontname('Arial')

# 调整图像边距以减少空白  # English: Adjust image margins to reduce white space
plt.subplots_adjust(left=0.15, right=0.95, top=0.95, bottom=0.15)

# 高质量输出，600 dpi  # English: High-quality output
plt.savefig(output_path, dpi=600, bbox_inches='tight', pad_inches=0.02)

# 显示图像  # English: Show image
plt.show()