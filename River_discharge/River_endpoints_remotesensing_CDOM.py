import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.dates import DateFormatter

import matplotlib as mpl

# 设置全局字体为Times New Roman  # English: Set the global font to
mpl.rcParams['font.family'] = 'Times New Roman'

# 读取Excel文件  # English: Read
file_path = r'D:\UZH\2024\20240122 Nutrient and Organic Carbon references\Arctic\CDOM\CDOM_dataset_list.xlsx'
df = pd.read_excel(file_path)

# 提取所需的列（假设第二列为CDOM，第四列为date）  # English: Extract the required columns
df['date'] = pd.to_datetime(df['date'])  # 转换为datetime格式  # English: Convert to
df = df.dropna(subset=['CDOM', 'date'])  # 去掉缺失值  # English: Remove missing values

# 创建图表  # English: Create a chart
plt.figure(figsize=(10, 6))
plt.plot(df['date'], df['CDOM'], marker='o', linestyle='-', color='b', label='CDOM')

# 设置图表标题和标签  # English: Set chart titles and labels
plt.title('CDOM Variation Over Time', fontsize=14)
plt.xlabel('Date', fontsize=12)
plt.ylabel('CDOM', fontsize=12)

# 美化日期显示格式（每两个月显示一个刻度）  # English: Beautify date display format
plt.gca().xaxis.set_major_locator(mdates.MonthLocator(interval=3))  # 设置每两个月一个刻度  # English: Set a scale every two months
date_form = DateFormatter("%Y-%m")  # 显示为 年-月  # English: Show as
plt.gca().xaxis.set_major_formatter(date_form)
plt.gcf().autofmt_xdate()  # 自动旋转日期标签  # English: Automatically rotate date tags

# 添加网格和图例  # English: Add grid and legend
plt.grid(True)
plt.legend()

# 显示图表  # English: Show charts
plt.tight_layout()
plt.show()
