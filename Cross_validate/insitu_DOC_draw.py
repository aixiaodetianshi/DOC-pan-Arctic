import pandas as pd
import matplotlib.pyplot as plt
import matplotlib as mpl
import matplotlib.dates as mdates
import math

# 设置全局字体为Times New Roman  # English: Set the global font to
mpl.rcParams['font.family'] = 'Times New Roman'

# 定义文件路径  # English: Define file path
file2 = r'D:\UZH\2024\20240122 Nutrient and Organic Carbon references\Arctic\ArcticGRO\insitu_DOC\ArcticGRO_Yukon_Discharge_DOC_insitu.xlsx'

# 读取第二个文件的River, Date, DOC数据  # English: Read the second file
df2 = pd.read_excel(file2, usecols=['River', 'Date', 'DOC'])

# 将日期列转换为日期格式  # English: Convert date column to date format
df2['Date'] = pd.to_datetime(df2['Date'])

# 以日期为索引  # English: Indexed with date
df2.set_index('Date', inplace=True)

# 按年份分组数据  # English: Group data by year
years = df2.index.year.unique()
n_years = len(years)

# 设置子图的行数和列数  # English: Set the number of rows and columns of the subplot
n_cols = 3  # 每行子图数  # English: Number of sub-pictures per line
n_rows = math.ceil(n_years / n_cols)  # 计算行数  # English: Calculate the number of rows

# 创建大图及其子图  # English: Create large images and their sub-pictures
fig, axs = plt.subplots(n_rows, n_cols, figsize=(14, 5 * n_rows), sharex=True, sharey=True)

# 展平子图数组以方便索引  # English: Flatten sub-graph arrays for easy indexing
axs = axs.flatten()

# 为每一年创建子图  # English: Create sub-pictures for each year
for i, year in enumerate(years):
    # 提取该年的数据  # English: Extract data from that year
    yearly_data = df2[df2.index.year == year]

    # 在子图上绘制数据  # English: Draw data on subgraph
    ax = axs[i]
    ax.plot(yearly_data.index, yearly_data['DOC'], 'o', label='In Situ DOC', color='pink', markersize=6)

    # 设置子图标题  # English: Set sub-image titles
    ax.set_title(f'{year}', fontsize=14)
    ax.set_xlabel('Date', fontsize=12)
    ax.set_ylabel('DOC/(mg/L)', fontsize=12)

    # 设置日期格式  # English: Set date format
    ax.xaxis.set_major_locator(mdates.MonthLocator())  # 每月一个刻度  # English: One tick per month
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%b'))  # 月份格式  # English: Month format

    # 添加网格线  # English: Add grid lines
    ax.grid(True)

    # 添加图例  # English: Add legend
    ax.legend(fontsize=12)

# 关闭未使用的子图  # English: Close unused subgraphs
for j in range(i + 1, len(axs)):
    fig.delaxes(axs[j])

# 自动调整子图布局  # English: Automatically adjust sub-picture layout
plt.tight_layout()

# 保存大图  # English: Save the larger image
plt.savefig('Yukon_all_years.png', bbox_inches='tight')

# 显示图像  # English: Show image
plt.show()
