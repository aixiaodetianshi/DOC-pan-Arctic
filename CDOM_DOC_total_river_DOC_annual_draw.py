# 做出每一年每个大流域的场时间尺度的变化

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from scipy.stats import linregress

# 读取数据
river = 'All'
file_path = r"D:\UZH\2024\20240122 Nutrient and Organic Carbon references\3_river_mouth_DOC\DOC_update_20250203\Total_DOC_average\Total_DOC_annual_"+river+"_Parts.csv"
output_path = r"D:\UZH\2024\20240122 Nutrient and Organic Carbon references\3_river_mouth_DOC\DOC_update_20250203\Total_DOC_average\Total_DOC_annual_"+river+"_Parts.tif"
data = pd.read_csv(file_path)

# 单位转换：Ton 转换为 Tg (1 Tg = 10^6 Ton)
data['Total_DOC_Annual'] = data['Total_DOC_Annual'] / 1e6
data['Total_DOC_Annual_Uncertainty'] = data['Total_DOC_Annual_Uncertainty'] / 1e6

# 提取数据
years = data['year']
total_doc = data['Total_DOC_Annual']
uncertainty = data['Total_DOC_Annual_Uncertainty']

# 计算趋势线
slope, intercept, r_value, p_value, std_err = linregress(years, total_doc)
trend_label = f'Trend={slope:.3f} Tg C yr⁻¹'

# 计算平均值和不确定性
mean_doc = np.mean(total_doc)
mean_uncertainty = np.mean(uncertainty)

# 创建图像
fig, ax = plt.subplots(figsize=(8.5/2.54, 3.5/2.54))  # 转换为厘米

# 绘制年度不确定性范围 (灰色阴影区域)
ax.fill_between(years,
                total_doc - uncertainty,
                total_doc + uncertainty,
                color='grey',
                alpha=0.3,
                label= 'Uncertainty')

# 绘制年度总DOC通量变化曲线
# ax.plot(years, total_doc, color='royalblue', linewidth=1.5, label='Total DOC')
ax.plot(years, total_doc, color='royalblue', linewidth=1, label=None)

# 添加趋势线 (回归)
sns.regplot(x=years, y=total_doc, scatter=False, color='darkblue',
            line_kws={"linestyle": "--", "linewidth": 1}, ax=ax, label=trend_label)


# 绘制平均值水平线及其不确定性范围
ax.axhline(mean_doc, color='red', linestyle='-.', linewidth=1, label=f'Mean={mean_doc:.2f} Tg C')
"""
ax.fill_between(years,
                mean_doc - mean_uncertainty,
                mean_doc + mean_uncertainty,
                color='red',
                alpha=0.1)
"""

# 图例与标签
ax.set_xlabel('Year', fontsize=6, fontname='Arial')
ax.set_ylabel('Total DOC Flux (Tg C)', fontsize=6, fontname='Arial')
ax.legend(fontsize=6, frameon=False, loc='lower left', bbox_to_anchor=(0.00, -0.05), labelspacing=0.25)  # 将图例放在左下角减少空白
# ax.legend(fontsize=6, frameon=False, loc='upper left', labelspacing=0.25)  # 将图例放在左下角减少空白

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

# 显示图像
plt.show()
