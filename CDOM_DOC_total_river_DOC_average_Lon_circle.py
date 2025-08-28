# 绘制 河流 DOC 及其不确定性随纬度变化的趋势。
# 使其以 纬度（Lat） 为横轴，而 DOC 通量及其不确定性 为纵轴，并按纬度排序。

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# 读取数据
file_path = r"D:\UZH\2024\20240122 Nutrient and Organic Carbon references\DOC\DOC_update_20250203\Total_DOC_average\average_Total_DOC_river_endpoints_Lon.xlsx"
output_path = r"D:\UZH\2024\20240122 Nutrient and Organic Carbon references\DOC\DOC_update_20250203\Total_DOC_average\average_Total_DOC_river_endpoints_Lon_circular_adjusted.tif"
data = pd.read_excel(file_path)

# 单位转换：Ton 转换为 Tg (1 Tg = 10^6 Ton)
data['Average_Total_DOC'] = data['Average_Total_DOC'] / 1e6
data['Average_Total_DOC_Uncertainty'] = data['Average_Total_DOC_Uncertainty'] / 1e6

# 按经度排序
data = data.sort_values(by='Longitude')

# 提取数据
Lon = data['Longitude']
total_doc = data['Average_Total_DOC']
uncertainty = data['Average_Total_DOC_Uncertainty']

# 将经度转换为弧度（0°E 对应 0°，360°E 对应 2π）
theta = np.radians(Lon)

# 创建极坐标图
fig, ax = plt.subplots(figsize=(8, 8), subplot_kw={'projection': 'polar'})

# 设置 0°E 在正下方，东经在右，西经在左
ax.set_theta_zero_location("S")  # 让 0°E 位于正下方
ax.set_theta_direction(1)  # 顺时针方向（右侧为东经，左侧为西经）

# 绘制不确定性范围 (灰色阴影区域)
ax.fill_between(theta, total_doc - uncertainty, total_doc + uncertainty, color='grey', alpha=0.3, label='Uncertainty')

# 绘制 DOC 曲线
ax.plot(theta, total_doc, color='royalblue', linewidth=1.5, label='Total DOC')

# 设置角度刻度（间隔30°，去掉360°）
longitude_labels = np.arange(0, 360, 30)  # 生成 0° 到 330°，不包括 360°
ax.set_xticks(np.radians(longitude_labels))  # 角度转换为弧度
ax.set_xticklabels([f"{deg}°E" if deg <= 180 else f"{360-deg}°W" for deg in longitude_labels])  # 东经和西经格式

# 设置径向刻度
ax.set_ylabel('Average Total DOC Flux (Tg C)', fontsize=10)
ax.legend(fontsize=8, loc='upper right')

# 美化网格
ax.grid(True, linestyle='--', alpha=0.5)

# 高质量输出
plt.savefig(output_path, dpi=600, bbox_inches='tight', pad_inches=0.02)

# 显示图像
plt.show()
