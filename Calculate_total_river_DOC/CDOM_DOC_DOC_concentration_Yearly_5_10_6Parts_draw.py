# 做出每一年每个大流域的长时间尺度的river discharge变化  # English: Making a long-term scale for each large basin every year
# 5-10月  # English: moon


import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from scipy.stats import linregress

# 文件路径  # English: File path
file_path = r"D:\UZH\2024\20240122 Nutrient and Organic Carbon references\DOC\DOC_update_20250203\DOC_concentration\All_DOC_concentration.csv"
output_path = r"D:\UZH\2024\20240122 Nutrient and Organic Carbon references\DOC\DOC_update_20250203\DOC_concentration\All_DOC_concentration.tif"

# 读取数据  # English: Read data
data = pd.read_csv(file_path)

# 提取数据  # English: Extract data
years = data['year']
DOC = data['DOC']

# 计算平均值和不确定性  # English: Calculate mean and uncertainty
mean_DOC = np.mean(DOC)

# 计算趋势线  # English: Calculate trend lines
slope, intercept, r_value, p_value, std_err = linregress(years, DOC)
trend_label = f'Trend={slope:.3f} mg L⁻¹ yr⁻¹'

# 创建图像  # English: Create an image
fig, ax = plt.subplots(figsize=(8.5/2.54, 3.5/2.54))  # 转换为厘米  # English: Convert to centimeters


# 绘制年度总DOC通量变化曲线  # English: Draw the annual total
ax.plot(years, DOC, color='royalblue', linewidth=1.5, label='DOC concentration')

# 添加趋势线 (回归)  # English: Add a trend line
sns.regplot(x=years, y=DOC, scatter=False, color='darkblue',
            line_kws={"linestyle": "--", "linewidth": 1}, ax=ax, label=trend_label)

# 绘制平均值水平线及其不确定性范围  # English: Draw the mean horizontal line and its uncertainty range
ax.axhline(mean_DOC, color='red', linestyle='-.', linewidth=1, label=f'Average={mean_DOC:.3f} mg L⁻¹')

# 图例与标签  # English: Legends and labels
ax.set_xlabel('Year', fontsize=6, fontname='Arial')
ax.set_ylabel('DOC concentration (mg L$^{-1}$)', fontsize=6, fontname='Arial')
ax.legend(fontsize=6, frameon=False, loc='lower left',  labelspacing=0.25)

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