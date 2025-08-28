# 做出每一年每个大流域的场时间尺度的变化  # English: Make changes in the field time scale of each large basin every year


import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from scipy.stats import linregress

# 文件路径  # English: File path
file_path = r"D:\UZH\2024\20240122 Nutrient and Organic Carbon references\3_river_mouth_DOC\DOC_update_20250203\Total_DOC_monthly\All_month\Total_monthly_DOC_All_Parts_5.csv"
output_path = r"D:\UZH\2024\20240122 Nutrient and Organic Carbon references\3_river_mouth_DOC\DOC_update_20250203\Total_DOC_monthly\All_month\Total_monthly_DOC_All_Parts_5.tif"

# 读取数据  # English: Read data
data = pd.read_csv(file_path)

# 单位转换：Ton 转为 Tg (1 Tg = 10^6 Ton)  # English: Unit conversion
data['Total_DOC'] = data['Total_DOC'] / 1e6
data['Total_DOC_uncertainty'] = data['Total_DOC_uncertainty'] / 1e6

# 日期解析：将 'May-84' 格式转换为 datetime，并提取年份  # English: Date analysis
data['year'] = pd.to_datetime(data['year_month'], errors='coerce').dt.year

# 提取数据  # English: Extract data
years = data['year']
total_doc = data['Total_DOC']
uncertainty = data['Total_DOC_uncertainty']

# 计算平均值和不确定性  # English: Calculate mean and uncertainty
mean_doc = np.mean(total_doc)
mean_uncertainty = np.mean(uncertainty)

# 计算趋势线  # English: Calculate trend lines
slope, intercept, r_value, p_value, std_err = linregress(years, total_doc)
trend_label = f'Trend={slope:.3f} Tg C yr⁻¹'

# 创建图像  # English: Create an image
fig, ax = plt.subplots(figsize=(8.5/2.54, 3.5/2.54))  # 转换为厘米  # English: Convert to centimeters

# 绘制年度不确定性范围 (灰色阴影区域)  # English: Draw the annual uncertainty range
ax.fill_between(years,
                total_doc - uncertainty,
                total_doc + uncertainty,
                color='grey',
                alpha=0.3,
                label='Uncertainty')

# 绘制年度总DOC通量变化曲线  # English: Draw the annual total
# ax.plot(years, total_doc, color='royalblue', linewidth=1, label='Total DOC')
ax.plot(years, total_doc, color='royalblue', linewidth=1)

# 添加趋势线 (回归)  # English: Add a trend line
sns.regplot(x=years, y=total_doc, scatter=False, color='darkblue',
            line_kws={"linestyle": "--", "linewidth": 1}, ax=ax, label=trend_label)

# 绘制平均值水平线及其不确定性范围  # English: Draw the mean horizontal line and its uncertainty range
ax.axhline(mean_doc, color='red', linestyle='-.', linewidth=1, label=f'Mean={mean_doc:.3f} Tg C')

# 图例与标签  # English: Legends and labels
ax.set_xlabel('Year', fontsize=6, fontname='Arial')
ax.set_ylabel('Monthly DOC Flux (Tg C)', fontsize=6, fontname='Arial')
ax.legend(fontsize=6, frameon=False, loc='lower left', bbox_to_anchor=(0.00, -0.05), labelspacing=0.25)
# ax.legend(fontsize=6, frameon=False, loc='upper left', labelspacing=0.25)

# 启用网格  # English: Enable grid
ax.grid(True, linestyle='--', alpha=0.5)

# 设置横轴刻度与标签，并明确标出 1984 和 2018  # English: Set horizontal axis scale and label
ax.set_xticks(range(1984, 2019, 4))  # 每 4 年一个刻度  # English: Every
ax.set_xlim(1983.5, 2018.5)
ax.tick_params(axis='both', which='major', labelsize=6)
for label in (ax.get_xticklabels() + ax.get_yticklabels()):
    label.set_fontname('Arial')

# 调整图像边距以减少空白  # English: Adjust image margins to reduce white space
plt.subplots_adjust(left=0.15, right=0.95, top=0.95, bottom=0.15)

# 高质量输出，600 dpi  # English: High-quality output
plt.savefig(output_path, dpi=600, bbox_inches='tight', pad_inches=0.02)