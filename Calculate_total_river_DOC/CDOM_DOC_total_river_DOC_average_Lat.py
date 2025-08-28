import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# 读取数据  # English: Read data
file_path = r"D:\UZH\2024\20240122 Nutrient and Organic Carbon references\3_river_mouth_DOC\DOC_update_20250203\Total_DOC_average\All_Properites.csv"
output_path = r"D:\UZH\2024\20240122 Nutrient and Organic Carbon references\3_river_mouth_DOC\DOC_update_20250203\Total_DOC_average\ARCADE_MERIT_All_catchments_average_DOC_Lat.tif"
data = pd.read_csv(file_path)

# 单位转换：Ton 转换为 Tg (1 Tg = 10^6 Ton)  # English: Unit conversion
data['Average_Total_DOC_1'] = data['Average_Total_DOC_1'] / 1e6
data['Average_Total_DOC_Uncertainty_1'] = data['Average_Total_DOC_Uncertainty_1'] / 1e6

# 按纬度排序（从低到高）  # English: Sort by latitude
data = data.sort_values(by='center_lat')

# 提取数据  # English: Extract data
Lat = data['center_lat']
total_doc = data['Average_Total_DOC_1']
uncertainty = data['Average_Total_DOC_Uncertainty_1']

# 创建图像  # English: Create an image
fig, ax = plt.subplots(figsize=(17.355/2.54, 4/2.54), dpi=600)  # 转换为厘米  # English: Convert to centimeters

# 绘制不确定性范围 (灰色阴影区域)  # English: Draw uncertainty ranges
ax.fill_between(Lat,
                total_doc - uncertainty,
                total_doc + uncertainty,
                color='grey', alpha=0.3,
                label='Uncertainty')

# 绘制总DOC通量变化曲线  # English: Draw total
ax.plot(Lat, total_doc, color='royalblue', linewidth=0.5, label='Total DOC Flux')

# 图例与标签  # English: Legends and labels
ax.set_xlabel('Latitude(°N)', fontsize=6, fontname='Arial')
ax.set_ylabel('Total DOC Flux (Tg C)', fontsize=6, fontname='Arial')
ax.legend(fontsize=6, frameon=False, loc='upper left', labelspacing=0.25)

ax.set_xlim(49, 84)
# 设置 Y 轴范围和刻度间隔  # English: set up
ax.set_xticks(np.arange(49, 85, 1))

# 设置 Y 轴最大值为 8  # English: set up
ax.set_ylim(0, 3)

# 启用网格  # English: Enable grid
ax.grid(True, linestyle='--', alpha=0.5)

# 设置刻度  # English: Set the scale
ax.tick_params(axis='both', which='major', labelsize=6)
for label in (ax.get_xticklabels() + ax.get_yticklabels()):
    label.set_fontname('Arial')

# 保存图像  # English: Save the image
plt.tight_layout()
plt.savefig(output_path, dpi=600, bbox_inches='tight', pad_inches=0.01)
plt.show()