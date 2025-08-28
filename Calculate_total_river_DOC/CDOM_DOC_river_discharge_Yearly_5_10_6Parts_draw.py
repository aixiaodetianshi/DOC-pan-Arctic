# 做出每一年每个大流域的长时间尺度的river discharge变化  # English: Making a long-term scale for each large basin every year
# 5-10月  # English: moon


import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from scipy.stats import linregress

# 文件路径  # English: File path
file_path = r"D:\UZH\2024\20240122 Nutrient and Organic Carbon references\discharge\river_discharge\Yearly_Proportion_5_10\Total_discharge_Yearly_All_Parts.xlsx"
output_path = r"D:\UZH\2024\20240122 Nutrient and Organic Carbon references\discharge\river_discharge\Yearly_Proportion_5_10\Total_discharge_Yearly_5_10_All_Parts.tif"

# 读取数据  # English: Read data
data = pd.read_excel(file_path)

# 单位转换：May-Oct_Discharge 转为 km3 (1 km3 = 10^9 m3)  # English: Unit conversion
data['May-Oct_Discharge'] = data['May-Oct_Discharge'] / 1e9

# 提取数据  # English: Extract data
years = data['year']
total_discharge = data['May-Oct_Discharge']

# 计算平均值和不确定性  # English: Calculate mean and uncertainty
mean_discharge = np.mean(total_discharge)

# 计算趋势线  # English: Calculate trend lines
slope, intercept, r_value, p_value, std_err = linregress(years, total_discharge)
trend_label = f'Trend={slope:.3f} km³ yr⁻¹'

# 创建图像  # English: Create an image
fig, ax = plt.subplots(figsize=(8.5/2.54, 3.5/2.54))  # 转换为厘米  # English: Convert to centimeters


# 绘制年度总DOC通量变化曲线  # English: Draw the annual total
ax.plot(years, total_discharge, color='royalblue', linewidth=1.5, label='Discharge')

# 添加趋势线 (回归)  # English: Add a trend line
sns.regplot(x=years, y=total_discharge, scatter=False, color='darkblue',
            line_kws={"linestyle": "--", "linewidth": 1}, ax=ax, label=trend_label)

# 绘制平均值水平线及其不确定性范围  # English: Draw the mean horizontal line and its uncertainty range
ax.axhline(mean_discharge, color='red', linestyle='-.', linewidth=1, label=f'Average={mean_discharge:.3f} km³')

# 图例与标签  # English: Legends and labels
ax.set_xlabel('Year', fontsize=6, fontname='Arial')
ax.set_ylabel('Discharge May-Oct.(km³)', fontsize=6, fontname='Arial')
ax.legend(fontsize=6, frameon=False, loc='upper left',  labelspacing=0.25)

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