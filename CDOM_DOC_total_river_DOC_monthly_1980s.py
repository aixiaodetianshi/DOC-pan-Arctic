# 做出每一年每个大流域的场时间尺度的变化

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import seaborn as sns
import numpy as np
from scipy.stats import linregress

# 文件路径
file_path = r"D:\UZH\2024\20240122 Nutrient and Organic Carbon references\3_river_mouth_DOC\DOC_update_20250203\Total_DOC_monthly\All_month\Total_monthly_DOC_All_Parts.csv"
output_path = r"D:\UZH\2024\20240122 Nutrient and Organic Carbon references\3_river_mouth_DOC\DOC_update_20250203\Total_DOC_monthly\All_month\Total_monthly_DOC_All_Parts_1980s.tif"

# ColorBrewer Set2颜色映射（5-10月）
month_colors = {
    5: '#66c2a5',   # 浅绿
    6: '#fc8d62',   # 橙
    7: '#8da0cb',   # 蓝紫
    8: '#e78ac3',   # 粉红
    9: '#a6d854',   # 黄绿
    10: '#ffd92f'   # 亮黄
}

# 读取数据
data = pd.read_csv(file_path)

# 单位转换（Ton → Tg）
data['Total_DOC'] = data['Total_DOC'] / 1e6
data['Total_DOC_uncertainty'] = data['Total_DOC_uncertainty'] / 1e6

# 转换 year_month 为 datetime
data['date'] = pd.to_datetime(data['year_month'], errors='coerce')
data['year'] = data['date'].dt.year
data['month'] = data['date'].dt.month

# 筛选 1980-1989年 5-10月 数据
data_filtered = data[(data['year'] >= 1980) & (data['year'] <= 1989) & (data['month'].isin(range(5, 11)))]

# 计算趋势线（按datetime转为ordinal）
valid_data = data_filtered.dropna(subset=['Total_DOC', 'date'])
x_ordinals = valid_data['date'].map(pd.Timestamp.toordinal)
slope, intercept, r_value, p_value, std_err = linregress(x_ordinals, valid_data['Total_DOC'])
trend_line = intercept + slope * x_ordinals
trend_label = f'Trend={slope * 365.25:.3f} Tg C yr⁻¹'  # 转换为每年单位

# 平均值和不确定性
mean_doc = valid_data['Total_DOC'].mean()
mean_uncertainty = valid_data['Total_DOC_uncertainty'].mean()

# 创建图像
fig, ax = plt.subplots(figsize=(8.5/2.54, 3.5/2.54))  # cm → inch

# 绘制不同月份的点（带误差线）
for month in range(5, 11):
    month_data = data_filtered[data_filtered['month'] == month]
    ax.errorbar(month_data['date'], month_data['Total_DOC'],
                yerr=month_data['Total_DOC_uncertainty'],
                fmt='o', markersize=2,
                color=month_colors[month],
                label=f'{month}M',
                capsize=1, elinewidth=0.5, alpha=0.9)

# 绘制趋势线
ax.plot(valid_data['date'], trend_line, '--', color='black', linewidth=1.2, label=trend_label)

# 平均值线和不确定性区间
ax.axhline(mean_doc, color='red', linestyle='-.', linewidth=1, label=f'Mean={mean_doc:.3f} Tg C')
ax.fill_between(valid_data['date'],
                mean_doc - mean_uncertainty,
                mean_doc + mean_uncertainty,
                color='red', alpha=0.15)

# 设置坐标轴和标签
ax.set_xlabel('Year-Month', fontsize=6, fontname='Arial')
ax.set_ylabel('Monthly DOC Flux (Tg C)', fontsize=6, fontname='Arial')
ax.set_xlim(pd.to_datetime('1980-01'), pd.to_datetime('1989-12'))
ax.xaxis.set_major_locator(mdates.YearLocator(1))
ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))

# 获取所有图例句柄和标签
handles, labels = ax.get_legend_handles_labels()

# 假设前两个是 trend 和 average，后6个是月份
trend_handles = handles[:2]
trend_labels = labels[:2]
month_handles = handles[2:]
# month_labels = labels[2:]
month_labels = ['May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct']

# 添加 trend + average 图例在下方第一行
legend1 = ax.legend(
    trend_handles,
    trend_labels,
    loc='upper center',
    bbox_to_anchor=(0.5, 1.06),  # 第一行位置
    ncol=2,
    frameon=False,
    fontsize=6,
    handletextpad=0.5,
    columnspacing=1.0
)

# 添加月份图例，显示在图左侧，竖直排列（每个月一行）
legend2 = ax.legend(
    month_handles,
    month_labels,
    loc='center left',            # 图左边垂直居中
    bbox_to_anchor=(-0.025, 0.5),  # 调整更靠左位置，可根据实际图形微调
    ncol=1,                       # 一列 = 竖直显示
    frameon=False,
    fontsize=6,
    handletextpad=0.1,
    handlelength=1.0,    # 控制图标长度（默认 2.0）
    labelspacing=0.4
)

# 添加第一个图例后必须手动添加回去，否则会被第二个覆盖
ax.add_artist(legend1)


# 坐标轴字体
ax.tick_params(axis='both', which='major', labelsize=6)
for label in (ax.get_xticklabels() + ax.get_yticklabels()):
    label.set_fontname('Arial')

# 网格与边距
ax.grid(True, linestyle='--', alpha=0.5)
plt.subplots_adjust(left=0.15, right=0.97, top=0.95, bottom=0.2)

# 保存图像
plt.savefig(output_path, dpi=600, bbox_inches='tight', pad_inches=0.01)
plt.close()
