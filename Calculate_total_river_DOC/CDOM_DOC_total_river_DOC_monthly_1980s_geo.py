import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np
from scipy.stats import linregress

# 文件路径  # English: File path
file_path = r"D:\UZH\2024\20240122 Nutrient and Organic Carbon references\3_river_mouth_DOC\DOC_update_20250203\Total_DOC_monthly\All_month\Total_monthly_DOC_All_Parts.csv"
output_path = r"D:\UZH\2024\20240122 Nutrient and Organic Carbon references\3_river_mouth_DOC\DOC_update_20250203\Total_DOC_monthly\All_month\Total_monthly_DOC_All_Parts_1980s_geo.tif"

# 统一颜色（表示一个季节区间）  # English: Unified color
season_color = '#1b9e77'
# 每个月的形状  # English: The shape of each month
month_shapes = {
    5: 'o',  # 圆  # English: round
    6: '^',  # 三角  # English: Triangle
    7: 's',  # 方形  # English: Square
    8: 'D',  # 菱形  # English: diamond
    9: 'v',  # 倒三角  # English: Inverted triangle
    10: 'h'  # 六边形  # English: hexagon
}

# 读取数据  # English: Read data
data = pd.read_csv(file_path)

# 单位转换（Ton → Tg）  # English: Unit conversion
data['Total_DOC'] = data['Total_DOC'] / 1e6
data['Total_DOC_uncertainty'] = data['Total_DOC_uncertainty'] / 1e6

# 转换 year_month 为 datetime  # English: Convert
data['date'] = pd.to_datetime(data['year_month'], errors='coerce')
data['year'] = data['date'].dt.year
data['month'] = data['date'].dt.month

# 筛选 1980-1989年 5-10月 数据  # English: filter
data_filtered = data[(data['year'] >= 1980) & (data['year'] <= 1989) & (data['month'].isin(range(5, 11)))]

# 计算趋势线  # English: Calculate trend lines
valid_data = data_filtered.dropna(subset=['Total_DOC', 'date'])
x_ordinals = valid_data['date'].map(pd.Timestamp.toordinal)
slope, intercept, r_value, p_value, std_err = linregress(x_ordinals, valid_data['Total_DOC'])
trend_line = intercept + slope * x_ordinals
trend_label = f'Trend={slope * 365.25:.3f} Tg C yr⁻¹'

# 平均值和不确定性  # English: Average and uncertainty
mean_doc = valid_data['Total_DOC'].mean()
mean_uncertainty = valid_data['Total_DOC_uncertainty'].mean()

# 创建图像  # English: Create an image
fig, ax = plt.subplots(figsize=(8.5/2.54, 3.5/2.54))  # cm → inch

# 绘制不同月份的点（同色不同形状）  # English: Draw points for different months
for month in range(5, 11):
    month_data = data_filtered[data_filtered['month'] == month]
    ax.errorbar(month_data['date'], month_data['Total_DOC'],
                yerr=month_data['Total_DOC_uncertainty'],
                fmt=month_shapes[month], markersize=2,
                color=season_color, ecolor=season_color,
                label=f'{month}M',
                capsize=1, elinewidth=0.5, alpha=0.9)

# 绘制趋势线  # English: Draw a trend line
ax.plot(valid_data['date'], trend_line, '--', color='black', linewidth=1.2, label=trend_label)

# 平均值线和不确定性区间  # English: Average line and uncertainty interval
ax.axhline(mean_doc, color='red', linestyle='-.', linewidth=1, label=f'Mean={mean_doc:.3f} Tg C')
ax.fill_between(valid_data['date'],
                mean_doc - mean_uncertainty,
                mean_doc + mean_uncertainty,
                color='red', alpha=0.15)

# 坐标轴设置  # English: Axis settings
ax.set_xlabel('Year-Month', fontsize=6, fontname='Arial')
ax.set_ylabel('Monthly DOC Flux (Tg C)', fontsize=6, fontname='Arial')
ax.set_xlim(pd.to_datetime('1980-01'), pd.to_datetime('1989-12'))
ax.xaxis.set_major_locator(mdates.YearLocator(1))
ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))

# 图例  # English: legend
handles, labels = ax.get_legend_handles_labels()
trend_handles = handles[:2]
trend_labels = labels[:2]
month_handles = handles[2:]
month_labels = ['May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct']

legend1 = ax.legend(
    trend_handles,
    trend_labels,
    loc='upper center',
    bbox_to_anchor=(0.5, 1.06),
    ncol=2,
    frameon=False,
    fontsize=6,
    handletextpad=0.5,
    columnspacing=1.0
)

legend2 = ax.legend(
    month_handles,
    month_labels,
    loc='center left',
    bbox_to_anchor=(-0.025, 0.5),
    ncol=1,
    frameon=False,
    fontsize=6,
    handletextpad=0.1,
    handlelength=1.0,
    labelspacing=0.4
)

ax.add_artist(legend1)

# 坐标轴字体  # English: Axis Font
ax.tick_params(axis='both', which='major', labelsize=6)
for label in (ax.get_xticklabels() + ax.get_yticklabels()):
    label.set_fontname('Arial')

ax.grid(True, linestyle='--', alpha=0.5)
plt.subplots_adjust(left=0.15, right=0.97, top=0.95, bottom=0.2)

# 保存  # English: save
plt.savefig(output_path, dpi=600, bbox_inches='tight', pad_inches=0.01)
plt.close()
