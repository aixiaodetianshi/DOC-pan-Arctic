import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# 读取数据
file_path = r"D:\UZH\2024\20240122 Nutrient and Organic Carbon references\3_river_mouth_DOC\DOC_update_20250203\Total_DOC_average\All_Properites.csv"
output_path = r"D:\UZH\2024\20240122 Nutrient and Organic Carbon references\3_river_mouth_DOC\DOC_update_20250203\Total_DOC_average\ARCADE_MERIT_All_catchments_average_DOC_Lat.tif"
data = pd.read_csv(file_path)

# 单位转换 Ton -> Tg
data['Average_Total_DOC'] = data['Average_Total_DOC'] / 1e6
data['Average_Total_DOC_Uncertainty'] = data['Average_Total_DOC_Uncertainty'] / 1e6

# 按纬度排序
data = data.sort_values(by='center_lat')

# 提取数据
Lat = data['center_lat']
DOC = data['Average_Total_DOC'].copy()
Unc = data['Average_Total_DOC_Uncertainty'].copy()

# 替换 DOC <= 0 为 1e-13
DOC[DOC <= 0] = 1e-13

# 图像设置
fig, ax = plt.subplots(figsize=(19/2.54, 3.5/2.54))

# 绘制不确定性竖线（模拟误差棒）
for lat, doc, unc in zip(Lat, DOC, Unc):
    lower = max(1e-13, doc - unc)
    upper = doc + unc
    ax.plot([lat, lat], [lower, upper], color='grey', linewidth=0.5, alpha=0.5)

# 绘制 DOC 通量本体竖线（柱状）
for lat, doc in zip(Lat, DOC):
    ax.plot([lat, lat], [1e-13, doc], color='royalblue', linewidth=0.5)

# 坐标轴设置
ax.set_xlabel('Latitude(°N)', fontsize=6, fontname='Arial')
ax.set_ylabel('Total DOC Flux (Tg C)', fontsize=6, fontname='Arial')

# 对数 Y 轴
ax.set_yscale('log')
yticks = [1e-13, 1e-11, 1e-9, 1e-7, 1e-5, 1e-3, 1e-1, 1e1]
yticklabels = ['0', '10$^{-11}$', '10$^{-9}$', '10$^{-7}$', '10$^{-5}$', '10$^{-3}$', '10$^{-1}$', '10$^{1}$']
ax.set_yticks(yticks)
ax.set_yticklabels(yticklabels)

# X 轴范围与网格
ax.set_xlim(49, 84)
ax.set_xticks(np.arange(49, 85, 1))
ax.set_ylim(1e-13, 10)
ax.grid(True, linestyle='--', alpha=0.5)

# 字体和边距设置
ax.tick_params(axis='both', labelsize=6)
for label in (ax.get_xticklabels() + ax.get_yticklabels()):
    label.set_fontname('Arial')
plt.subplots_adjust(left=0.15, right=0.95, top=0.95, bottom=0.15)

# 保存与显示
plt.savefig(output_path, dpi=600, bbox_inches='tight', pad_inches=0.02)
plt.show()