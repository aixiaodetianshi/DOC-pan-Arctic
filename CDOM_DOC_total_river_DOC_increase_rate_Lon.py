# 绘制 河流 DOC 及其不确定性随纬度变化的趋势。
# 使其以 纬度（Lat） 为横轴，而 DOC 通量及其不确定性 为纵轴，并按纬度排序。

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# 读取数据
file_path = r"D:\UZH\2024\20240122 Nutrient and Organic Carbon references\DOC\DOC_update_20250203\Total_DOC_increase_rate\annual_increase_rate_Total_DOC_for_6Parts_Lon.xlsx"
output_path = r"D:\UZH\2024\20240122 Nutrient and Organic Carbon references\DOC\DOC_update_20250203\Total_DOC_increase_rate\annual_increase_rate_Total_DOC_for_6Parts_Lon.tif"
data = pd.read_excel(file_path)

# 单位转换：Ton 转换为 Tg (1 Tg = 10^6 Ton)
data['Annual_Increase_Rate'] = data['Annual_Increase_Rate'] / 1e6

# 按纬度排序（从低到高）
data = data.sort_values(by='Longitude')

# 提取数据
Lon = data['Longitude']
total_doc = data['Annual_Increase_Rate']

# 分离正值和负值
Lon_positive = Lon[total_doc >= 0]
total_doc_positive = total_doc[total_doc >= 0]

Lon_negative = Lon[total_doc < 0]
total_doc_negative = total_doc[total_doc < 0]

# 创建图像
fig, ax = plt.subplots(figsize=(17/2.54, 3.5/2.54))  # 转换为厘米

# 绘制正值（红色）
ax.plot(Lon_positive, total_doc_positive, color='red', linewidth=0.5, label='Increasing')

# 绘制负值（蓝色）
ax.plot(Lon_negative, total_doc_negative, color='blue', linewidth=0.5, label='Decreasing')

# 图例与标签
ax.set_xlabel('Longitude(°E)', fontsize=6, fontname='Arial')
ax.set_ylabel(r'Increase Rate(Tg C yr$^{-1}$)', fontsize=6, fontname='Arial')
ax.legend(fontsize=6, frameon=False, loc='upper left', labelspacing=0.25)

# 设置 Y 轴最大值为 8
ax.set_ylim(-0.125, 0.175)

# 设置 X 轴范围和刻度间隔
ax.set_xlim(-180, 180)
ax.set_xticks(np.arange(-180, 181, 15))

# 启用网格
ax.grid(True, linestyle='--', alpha=0.5)

# 设置刻度
ax.tick_params(axis='both', which='major', labelsize=6)
for label in (ax.get_xticklabels() + ax.get_yticklabels()):
    label.set_fontname('Arial')

# 调整图像边距以减少空白
plt.subplots_adjust(left=0.15, right=0.95, top=0.95, bottom=0.15)

# 高质量输出，600 dpi
plt.savefig(output_path, dpi=600, bbox_inches='tight', pad_inches=0.02)

# 显示图像
plt.show()