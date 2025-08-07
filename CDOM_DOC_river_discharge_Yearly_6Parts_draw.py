# 做出每一年每个大流域的长时间尺度的river discharge变化


import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from scipy.stats import linregress

# 文件路径
file_path = r"D:\UZH\2024\20240122 Nutrient and Organic Carbon references\discharge\river_discharge\Yearly_Proportion_5_10\Total_discharge_Yearly_All_Parts.xlsx"
output_path = r"D:\UZH\2024\20240122 Nutrient and Organic Carbon references\discharge\river_discharge\Yearly_Proportion_5_10\Total_discharge_Yearly_All_Parts.tif"

# 读取数据
data = pd.read_excel(file_path)

# 单位转换：Annual_Discharge 转为 km3 (1 km3 = 10^9 m3)
data['Annual_Discharge'] = data['Annual_Discharge'] / 1e9

# 提取数据
years = data['year']
total_discharge = data['Annual_Discharge']

# 计算平均值和不确定性
mean_discharge = np.mean(total_discharge)

# 计算趋势线
slope, intercept, r_value, p_value, std_err = linregress(years, total_discharge)
trend_label = f'Trend={slope:.3f} km³ yr⁻¹'

# 创建图像
fig, ax = plt.subplots(figsize=(8.5/2.54, 3.5/2.54))  # 转换为厘米


# 绘制年度总DOC通量变化曲线
ax.plot(years, total_discharge, color='royalblue', linewidth=1.5, label='Annual discharge')

# 添加趋势线 (回归)
sns.regplot(x=years, y=total_discharge, scatter=False, color='darkblue',
            line_kws={"linestyle": "--", "linewidth": 1}, ax=ax, label=trend_label)

# 绘制平均值水平线及其不确定性范围
ax.axhline(mean_discharge, color='red', linestyle='-.', linewidth=1, label=f'Average={mean_discharge:.3f} km³')

# 图例与标签
ax.set_xlabel('Year', fontsize=6, fontname='Arial')
ax.set_ylabel('Annual discharge (km³)', fontsize=6, fontname='Arial')
ax.legend(fontsize=6, frameon=False, loc='upper left',  labelspacing=0.25)

# 启用网格
ax.grid(True, linestyle='--', alpha=0.5)

# 设置横轴刻度与标签，并明确标出 1984 和 2018
ax.set_xticks(range(1984, 2019, 4))  # 每 4 年一个刻度
ax.set_xlim(1983.5, 2018.5)
ax.tick_params(axis='both', which='major', labelsize=6)
for label in (ax.get_xticklabels() + ax.get_yticklabels()):
    label.set_fontname('Arial')

# 调整图像边距以减少空白
plt.subplots_adjust(left=0.15, right=0.95, top=0.95, bottom=0.15)

# 高质量输出，600 dpi
plt.savefig(output_path, dpi=600, bbox_inches='tight', pad_inches=0.02)