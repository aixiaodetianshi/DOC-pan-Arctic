import pandas as pd
import matplotlib.pyplot as plt

import matplotlib as mpl

# 设置全局字体为Times New Roman
mpl.rcParams['font.family'] = 'Times New Roman'

# 定义文件路径
file1 = r'D:\UZH\2024\20240122 Nutrient and Organic Carbon references\Arctic\ArcticGRO\insitu_DOC\SPP_Yukon_remotesensing_Landsat_DOC_filled.xlsx'
file2 = r'D:\UZH\2024\20240122 Nutrient and Organic Carbon references\Arctic\ArcticGRO\insitu_DOC\ArcticGRO_Yukon_Discharge_DOC_insitu.xlsx'

# 读取第一个文件的River, Date, DOC数据
df1 = pd.read_excel(file1, usecols=['Date', 'DOC'])

# 读取第二个文件的River, Date, DOC数据
df2 = pd.read_excel(file2, usecols=['River', 'Date', 'DOC'])

# 将日期列转换为日期格式
df1['Date'] = pd.to_datetime(df1['Date'])
df2['Date'] = pd.to_datetime(df2['Date'])

# 剔除 remotesensing DOC 数据集中数值最大的 5%
upper_bound = df1['DOC'].quantile(0.99)
df1_filtered = df1[df1['DOC'] <= upper_bound]

# 以日期为索引
df1_filtered.set_index('Date', inplace=True)
df2.set_index('Date', inplace=True)

# 绘制图像
plt.figure(figsize=(14, 7))

# 绘制第一个数据集（remotesensing DOC），使用蓝色线
plt.plot(df1_filtered.index, df1_filtered['DOC'], 'o', label='Remote sensing DOC', color='#6495ED', markersize=2)

# 绘制第二个数据集（in situ DOC），使用粉色线
plt.plot(df2.index, df2['DOC'], 'o', label='In Situ DOC', color='pink', markersize=6)

# 添加标题和标签，调整字体大小
plt.title('Yukon', fontsize=18)
plt.xlabel('Date', fontsize=16)
plt.ylabel('DOC/(mg/L)', fontsize=16)

# 调整刻度标签的字体大小
plt.xticks(fontsize=14)
plt.yticks(fontsize=14)

# 添加网格线
plt.grid(True)

# 显示图例，调整图例字体大小
plt.legend(fontsize=14)

# 显示图像
plt.show()