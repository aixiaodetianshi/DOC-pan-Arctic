import pandas as pd
import os
import matplotlib.pyplot as plt

# 文件路径
in_file_path = r'D:\UZH\2024\20240122 Nutrient and Organic Carbon references\DOC\CDOM_DOC_stastics_date_count.xlsx'

# 读取 Excel 文件
df_DOC = pd.read_excel(in_file_path)

# 提取数据
x = df_DOC['COMID']
y = df_DOC['count']

# 绘制散点图
plt.figure(figsize=(10, 6))
plt.scatter(x, y, color='b', alpha=0.6)
plt.xlabel('COMID')
plt.ylabel('Count')
plt.title('Scatter plot of COMID vs Count')
plt.grid(True)
plt.show()