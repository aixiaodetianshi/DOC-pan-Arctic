# read DOC from ArcticGRO water quality

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import mean_squared_error
from scipy.stats import pearsonr
import numpy as np

import matplotlib as mpl

# 设置全局字体为Times New Roman
mpl.rcParams['font.family'] = 'Times New Roman'

# 定义文件路径
input_file = r'D:\UZH\2024\20240122 Nutrient and Organic Carbon references\Arctic\ArcticGRO\insitu_DOC\matchup_insitu_LSTM_remotesensing_Kolyma_DOC.xlsx'

# 读取合并后的数据
df = pd.read_excel(input_file)

# 计算均方根误差 (RMSE)
rmse = np.sqrt(mean_squared_error(df['DOC'], df['DOC_2']))

# 计算相关系数 (r)
correlation, _ = pearsonr(df['DOC'], df['DOC_2'])

# 绘制散点图
plt.figure(figsize=(10, 6))
sns.scatterplot(x='DOC', y='DOC_2', data=df)

# 添加回归线
sns.regplot(x='DOC', y='DOC_2', data=df, scatter=False, color='red')

# 添加RMSE和相关系数到图表中
plt.text(0.05, 0.95, f'RMSE: {rmse:.2f}', fontsize=12, verticalalignment='top', transform=plt.gca().transAxes)
plt.text(0.05, 0.90, f'R: {correlation:.2f}', fontsize=12, verticalalignment='top', transform=plt.gca().transAxes)

# 设置图表标题和标签
plt.title('Remote Sensing DOC vs. In-situ DOC in Kolyma')
plt.xlabel('Remote Sensing DOC/(mg/L)')
plt.ylabel('In-situ DOC/(mg/L)')

# 显示图表
plt.grid(True)
plt.show()