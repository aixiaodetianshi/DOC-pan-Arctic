import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.dates import DateFormatter

import matplotlib as mpl

# 设置全局字体为Times New Roman
mpl.rcParams['font.family'] = 'Times New Roman'

# 读取Excel文件
file_path = r'D:\UZH\2024\20240122 Nutrient and Organic Carbon references\Arctic\CDOM\CDOM_dataset_list.xlsx'
df = pd.read_excel(file_path)

# 提取所需的列（假设第二列为CDOM，第四列为date）
df['date'] = pd.to_datetime(df['date'])  # 转换为datetime格式
df = df.dropna(subset=['CDOM', 'date'])  # 去掉缺失值

# 创建图表
plt.figure(figsize=(10, 6))
plt.plot(df['date'], df['CDOM'], marker='o', linestyle='-', color='b', label='CDOM')

# 设置图表标题和标签
plt.title('CDOM Variation Over Time', fontsize=14)
plt.xlabel('Date', fontsize=12)
plt.ylabel('CDOM', fontsize=12)

# 美化日期显示格式（每两个月显示一个刻度）
plt.gca().xaxis.set_major_locator(mdates.MonthLocator(interval=3))  # 设置每两个月一个刻度
date_form = DateFormatter("%Y-%m")  # 显示为 年-月
plt.gca().xaxis.set_major_formatter(date_form)
plt.gcf().autofmt_xdate()  # 自动旋转日期标签

# 添加网格和图例
plt.grid(True)
plt.legend()

# 显示图表
plt.tight_layout()
plt.show()
