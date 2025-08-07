# 绘制 河流 DOC 增长率


import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# 读取数据
file_path = r"D:\UZH\2024\20240122 Nutrient and Organic Carbon references\3_river_mouth_DOC\DOC_update_20250203\Total_DOC_increase_rate\Annual_increase_rate_DOC_All_Property.csv"
output_path = r"D:\UZH\2024\20240122 Nutrient and Organic Carbon references\3_river_mouth_DOC\DOC_update_20250203\Total_DOC_increase_rate\annual_increase_rate_Total_DOC_Lat.tif"
data = pd.read_csv(file_path)

# 单位转换：Ton 转换为 Tg (1 Tg = 10^6 Ton)
data['Annual_Increase_Rate_1'] = data['Annual_Increase_Rate_1'] / 1e6

# 按纬度排序（从低到高）
data = data.sort_values(by='center_lat')

# 提取数据
Lat = data['center_lat']
total_doc = data['Annual_Increase_Rate_1']

# 分离正值和负值
Lat_positive = Lat[total_doc >= 0]
total_doc_positive = total_doc[total_doc >= 0]

Lat_negative = Lat[total_doc < 0]
total_doc_negative = total_doc[total_doc < 0]

# 创建图像
fig, ax = plt.subplots(figsize=(18.5/2.54, 3.5/2.54))  # 宽高比调整

# ax.plot(Lat, total_doc, color='red', linewidth=0.5, label='Increasing')
# 绘制总DOC通量变化曲线

# 绘制正值（红色）
ax.plot(Lat_positive, total_doc_positive,  color='red', linewidth=0.5, label='Increasing')

# 绘制负值（蓝色）
ax.plot(Lat_negative, total_doc_negative,  color='blue', linewidth=0.5, label='Decreasing')

# 设置坐标轴
ax.set_xlabel('Latitude (°N)', fontsize=6, fontname='Arial')
ax.set_ylabel(r'Increase Rate(Tg C yr$^{-1})$', fontsize=6, fontname='Arial')

ax.set_xticks(np.arange(49, 85, 1))
ax.set_xlim(49, 83.5)

ax.set_yticks(np.arange(-0.035, 0.0125, 0.005))
ax.set_ylim(-0.031, 0.0125)

# 添加图例
ax.legend(fontsize=6, frameon=False, loc='upper right', labelspacing=0.25)

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