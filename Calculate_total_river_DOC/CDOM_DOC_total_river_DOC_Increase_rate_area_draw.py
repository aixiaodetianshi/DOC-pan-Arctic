import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.ticker import FuncFormatter
from matplotlib.lines import Line2D

# 文件路径  # English: File path
file_path = r"D:\UZH\2024\20240122 Nutrient and Organic Carbon references\DOC\DOC_update_20250203\Total_DOC_increase_rate\ARCADE_MERIT_pan_Arctic_Increase_rate_DOC_Area_Unit.xlsx"
output_path = r"D:\UZH\2024\20240122 Nutrient and Organic Carbon references\DOC\DOC_update_20250203\Total_DOC_increase_rate\ARCADE_MERIT_pan_Arctic_Increase_rate_DOC_Area_Unit.tif"

# 读取数据  # English: Read data
df = pd.read_excel(file_path)
df['Annual_Increase_Rate'] = df['Annual_Increase_Rate'] / 1e6

# 清洗缺失数据  # English: Clean missing data
df = df.dropna(subset=['area_km2', 'Annual_Increase_Rate', 'center_lat'])

# 图像设置  # English: Image settings
fig, ax = plt.subplots(figsize=(21/2.54, 5/2.54), dpi=600)
font_kwargs = {'fontsize': 6, 'fontname': 'Arial'}

# 绘图  # English: Drawing
sc = ax.scatter(df['area_km2'], df['Annual_Increase_Rate'], c=df['center_lat'],
                cmap='viridis', alpha=0.7, edgecolors='none', linewidth=0.3, s=1)

# 轴标签  # English: Axis Labels
ax.set_xlabel('Catchment area (km$^{2}$)', **font_kwargs)
ax.set_ylabel('Increase rate (Tg C yr$^{-1}$)', **font_kwargs)

# 设置对数X轴  # English: Set logarithm
ax.set_xscale('log')
ax.set_xlim(1, 1e7)

# 字体美化  # English: Font beautification
ax.tick_params(labelsize=6)
for label in (ax.get_xticklabels() + ax.get_yticklabels()):
    label.set_fontname('Arial')

# 网格  # English: Grid
ax.grid(True, linestyle='--', alpha=0.5)

# 添加颜色条  # English: Add color bars
cbar = fig.colorbar(sc, ax=ax, shrink=0.8, pad=0.001)
cbar.set_label('Latitude (°N)', **font_kwargs)
cbar.ax.tick_params(labelsize=6)
for label in cbar.ax.get_yticklabels():
    label.set_fontname('Arial')

# 保存与展示  # English: Save and display
plt.tight_layout()
plt.savefig(output_path, dpi=600, bbox_inches='tight', pad_inches=0.02)
plt.show()

