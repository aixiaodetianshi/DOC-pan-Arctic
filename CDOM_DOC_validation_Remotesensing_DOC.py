# 现在有两河流DOC时间序列文件，文件都存储在文件夹
# D:\UZH\2024\20240122 Nutrient and Organic Carbon references\DOC\DOC_update_20250203\validation_DOC内，
# 文件ArcticGRO_DOC_insitu_Ob.csv记录了河流Ob溶解有机碳DOC的现场实测数据，
# 文件Remotesensing_DOC_Ob.csv记录了河流Ob溶解有机碳DOC的卫星反演数据。
# 对于文件ArcticGRO_DOC_insitu_Ob.csv，有4列数据，分别为River，Date，Discharge，DOC，意义为：河流名称，日期，流量和溶解有机碳DOC现场观测数据；
# 对于文件Remotesensing_DOC_Ob.csv，有5列，分别为date，CDOM，CDOM_uncertainty， DOC，DOC_uncertainty，意义为：日期，卫星获取的CDOM, CDOM的不确定性，卫星反演得到的DOC，DOC的不确定性。
# 数据文件中均存在数据控缺陷项。
# 以现场实测DOC数据为基础，获取卫星数据与实测数据相同日期的卫星反演DOC数据，
# 将新得到的数据保存在相同数据文件夹内，命名为Validation_Remotesensing_DOC_insitu_Ob.csv，
# 数据中保存3列，分别为date，insitu_DOC, remotesensing_DOC.

# 计算匹配数据的相关系数 (Pearson r)、均方根误差 (RMSE) 和 Bias。
# 绘制散点图并添加回归线、RMSE 和 Pearson 相关系数。

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import mean_squared_error
from scipy.stats import pearsonr
import numpy as np
import matplotlib as mpl

# 设置全局字体为 Times New Roman
mpl.rcParams['font.family'] = 'Times New Roman'

# 指定河流名称
river_name = 'Kolyma'  # 只需修改此处，其他部分会自动调整

# 定义文件路径
folder_path = r'D:\UZH\2024\20240122 Nutrient and Organic Carbon references\DOC\DOC_update_20250203\validation_DOC'
insitu_file = f'{folder_path}\\ArcticGRO_DOC_insitu_{river_name}.csv'
remote_file = f'{folder_path}\\Remotesensing_DOC_{river_name}.csv'
output_file = f'{folder_path}\\Validation_Remotesensing_DOC_insitu_{river_name}.csv'

# 读取数据
df_insitu = pd.read_csv(insitu_file, usecols=['Date', 'DOC'])
df_remote = pd.read_csv(remote_file, usecols=['date', 'DOC'])

# 确保日期格式一致
df_insitu['Date'] = pd.to_datetime(df_insitu['Date'])
df_remote['date'] = pd.to_datetime(df_remote['date'])

# 删除包含 NaT (缺失日期) 的行
df_insitu.dropna(subset=['Date'], inplace=True)
df_remote.dropna(subset=['date'], inplace=True)

# 按日期排序
df_insitu = df_insitu.sort_values('Date')
df_remote = df_remote.sort_values('date')

# 进行日期匹配，允许时间差最大为 3 天
merged_df = pd.merge_asof(df_insitu, df_remote, left_on='Date', right_on='date', direction='nearest', tolerance=pd.Timedelta(days=3))

# 仅保留必要的列
merged_df = merged_df[['Date', 'DOC_x', 'DOC_y']]
merged_df.columns = ['date', 'insitu_DOC', 'remotesensing_DOC']

# 删除包含 NaN 值的行
merged_df.dropna(inplace=True)

# 剔除异常大的遥感 DOC 值
Q1 = merged_df['remotesensing_DOC'].quantile(0.25)
Q3 = merged_df['remotesensing_DOC'].quantile(0.75)
IQR = Q3 - Q1

# 定义异常值阈值（1.5 倍 IQR）
lower_bound = Q1 - 1.5 * IQR
upper_bound = Q3 + 1.5 * IQR

# 仅保留在正常范围内的数据
filtered_df = merged_df[(merged_df['remotesensing_DOC'] >= lower_bound) &
                        (merged_df['remotesensing_DOC'] <= upper_bound)]

# 保存匹配后的数据
filtered_df.to_csv(output_file, index=False)

# 计算 RMSE
rmse = np.sqrt(mean_squared_error(filtered_df['insitu_DOC'], filtered_df['remotesensing_DOC']))

# 计算相关系数 (Pearson r)
correlation, _ = pearsonr(filtered_df['insitu_DOC'], filtered_df['remotesensing_DOC'])

# 计算 Bias
bias = np.mean(filtered_df['remotesensing_DOC'] - filtered_df['insitu_DOC'])

# 绘制散点图
plt.figure(figsize=(10, 6))
sns.scatterplot(x='insitu_DOC', y='remotesensing_DOC', data=filtered_df, alpha=0.7, edgecolor=None)

# 添加回归线
sns.regplot(x='insitu_DOC', y='remotesensing_DOC', data=filtered_df, scatter=False, color='red')

# 确定文本框左上角的相对坐标
text_x, text_y = 0.05, 0.95
text_fontsize = 12

# 添加 RMSE、R 和 Bias 到图表中
plt.text(text_x, text_y, f'RMSE: {rmse:.2f}', fontsize=text_fontsize, verticalalignment='top', transform=plt.gca().transAxes)
plt.text(text_x, text_y - 0.05, f'R: {correlation:.2f}', fontsize=text_fontsize, verticalalignment='top', transform=plt.gca().transAxes)
plt.text(text_x, text_y - 0.10, f'Bias: {bias:.2f}', fontsize=text_fontsize, verticalalignment='top', transform=plt.gca().transAxes)

# 设置图表标题和标签
plt.title(f'Remote Sensing DOC vs. In-situ DOC in {river_name} River')
plt.xlabel('In-situ DOC (mg/L)')
plt.ylabel('Remote Sensing DOC (mg/L)')
plt.grid(True)

# 调整布局，防止重叠
plt.tight_layout()

# 显示图表
plt.show()

