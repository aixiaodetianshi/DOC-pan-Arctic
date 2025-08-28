import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.colors as mcolors
import matplotlib.cm as cm
from scipy import stats

# 读取数据  # English: Read data
file_path = r"D:\UZH\2024\20240122 Nutrient and Organic Carbon references\3_river_mouth_DOC\DOC_update_20250203\Total_DOC_average\All_Properites.csv"
output_path = r"D:\UZH\2024\20240122 Nutrient and Organic Carbon references\3_river_mouth_DOC\DOC_update_20250203\Total_DOC_average\ARCADE_MERIT_pan_Arctic_average_DOC_Area_Unit_linear.tif"
df = pd.read_csv(file_path)

# 数据清洗与转换  # English: Data cleaning and conversion
df['area_km2'] = pd.to_numeric(df['area_km2'], errors='coerce')
df['DOC_Area_Unit'] = pd.to_numeric(df['DOC_Area_Unit'], errors='coerce')
df['center_lat'] = pd.to_numeric(df['center_lat'], errors='coerce')
df = df.dropna(subset=['area_km2', 'DOC_Area_Unit', 'center_lat'])

# 纬度分区  # English: Latitude partition
def lat_to_zone(lat):
    if 45 <= lat < 50:
        return 1
    elif 50 <= lat < 55:
        return 2
    elif 55 <= lat < 60:
        return 3
    elif 60 <= lat < 65:
        return 4
    elif 65 <= lat < 70:
        return 5
    elif 70 <= lat < 75:
        return 6
    else:
        return 7

df['LatZone'] = df['center_lat'].apply(lat_to_zone)
df = df.dropna(subset=['LatZone'])

# ====== 拟合部分：log-log 拟合 ======  # English: Fitting part
x = df['area_km2']
y = df['DOC_Area_Unit']

# 颜色映射配置  # English: Color Mapping Configuration
cmap = cm.get_cmap('YlGnBu', 7)
norm = mcolors.BoundaryNorm(boundaries=np.arange(1, 9), ncolors=7)

# 图像设置  # English: Image settings

fig, ax = plt.subplots(figsize=(19/2.54, 5/2.54), dpi=600)

font_kwargs = {'fontsize': 6, 'fontname': 'Arial'}

# 原始点图  # English: Original dot map
sc = ax.scatter(x, y, c=df['LatZone'], cmap=cmap, norm=norm,
                alpha=0.7, edgecolors='none', linewidth=0.3, s=0.2)

# 图例（显示拟合方程）  # English: legend
ax.legend(loc='lower left', fontsize=6, frameon=False)

# 轴标签  # English: Axis Labels
ax.set_xlabel('Catchment area (km$^{2}$)', **font_kwargs)
ax.set_ylabel('DOC flux per unit area\n(Tg C km$^{-2}$)', **font_kwargs)
ax.tick_params(labelsize=6)
for label in (ax.get_xticklabels() + ax.get_yticklabels()):
    label.set_fontname('Arial')

ax.set_xscale('log')
ax.set_xlim(1, 1e7)
ax.set_yscale('log')
ax.grid(True, linestyle='--', alpha=0.5)

# 颜色条  # English: Color bars
cbar = fig.colorbar(sc, ax=ax, shrink=1, pad=0.001, ticks=np.arange(1.5, 8.5, 1))
cbar.set_label('Latitude(°N)', **font_kwargs)
cbar.ax.set_yticklabels(['50', '55', '60', '65', '70', '75', '80'])
cbar.ax.tick_params(labelsize=6)
for label in cbar.ax.get_yticklabels():
    label.set_fontname('Arial')

# 保存图像  # English: Save the image
plt.tight_layout()
plt.savefig(output_path, dpi=600, bbox_inches='tight', pad_inches=0.02)
plt.show()
