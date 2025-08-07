
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from scipy.stats import linregress
river = "Mackenzie"
# 读取数据
file_path = r"D:\UZH\2024\20240122 Nutrient and Organic Carbon references\3_river_mouth_DOC\DOC_update_20250203\Total_DOC_monthly\All_month\Total_monthly_DOC_"+river+"_Parts.csv"
output_path = r"D:\UZH\2024\20240122 Nutrient and Organic Carbon references\3_river_mouth_DOC\DOC_update_20250203\Total_DOC_monthly\All_month\Total_monthly_DOC_"+river+"_Parts.tif"
data = pd.read_csv(file_path)

# 单位转换：Ton 转换为 Tg (1 Tg = 10^6 Ton)
data['Total_DOC'] = data['Total_DOC'] / 1e6
data['Total_DOC_uncertainty'] = data['Total_DOC_uncertainty'] / 1e6

# 转换 year_month 为 datetime 类型，并计算年份的小数形式
data['year_month'] = pd.to_datetime(data['year_month'], errors='coerce')
data['year_decimal'] = data['year_month'].dt.year + (data['year_month'].dt.month - 1) / 12

# 提取数据
year_decimal = data['year_decimal']
total_doc = data['Total_DOC']
uncertainty = data['Total_DOC_uncertainty']

# 计算平均值和不确定性
mean_doc = np.mean(total_doc)
mean_uncertainty = np.mean(uncertainty)

# 计算趋势线
slope, intercept, r_value, p_value, std_err = linregress(year_decimal, total_doc)
trend_label = f'Trend={slope:.3f} Tg C yr⁻¹'

# 创建图像
fig, ax = plt.subplots(figsize=(18.5/2.54, 4/2.54))  # 转换为厘米

# 绘制年度不确定性范围 (灰色阴影区域)
ax.fill_between(year_decimal,
                total_doc - uncertainty,
                total_doc + uncertainty,
                color='grey',
                alpha=0.3,
                label='Uncertainty')

# 绘制年度总DOC通量变化曲线
# ax.plot(year_decimal, total_doc, color='royalblue', linewidth=1.5, label='Total DOC')
ax.plot(year_decimal, total_doc, color='royalblue', linewidth=1)

# 添加趋势线 (回归)
sns.regplot(x=year_decimal, y=total_doc, scatter=False, color='darkblue',
            line_kws={"linestyle": "--", "linewidth": 1}, ax=ax, label=trend_label)

# 绘制平均值水平线
ax.axhline(mean_doc, color='red', linestyle='-.', linewidth=1, label=f'Mean={mean_doc:.3f} Tg C')

# 图例与标签
ax.set_xlabel('Year-Month', fontsize=6, fontname='Arial')
ax.set_ylabel('Monthly DOC Flux (Tg C)', fontsize=6, fontname='Arial')
ax.legend(fontsize=6, frameon=False, loc='upper right', labelspacing=0.25)

# 启用网格
ax.grid(True, linestyle='--', alpha=0.5)

# 设置横轴刻度与标签，并明确标出 1984 和 2018
ax.set_xticks(data['year_decimal'][::6])  # 每年一个刻度
ax.set_xticklabels(data['year_month'].dt.strftime('%Y-%m')[::6], rotation=90)
ax.set_xlim(1984, 2019)
ax.tick_params(axis='both', which='major', labelsize=6)
for label in (ax.get_xticklabels() + ax.get_yticklabels()):
    label.set_fontname('Arial')

# 调整图像边距以减少空白
plt.subplots_adjust(left=0.15, right=0.95, top=0.95, bottom=0.25)

# 高质量输出，600 dpi
plt.savefig(output_path, dpi=600, bbox_inches='tight', pad_inches=0.02)

# 显示图像
plt.show()
