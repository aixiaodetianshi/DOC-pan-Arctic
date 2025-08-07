import pandas as pd
import matplotlib.pyplot as plt
import matplotlib as mpl
from sklearn.linear_model import LinearRegression
import numpy as np

# 设置全局字体为Times New Roman
mpl.rcParams['font.family'] = 'Times New Roman'

DOC_input_file = 'D:/UZH/2024/20240122 Nutrient and Organic Carbon references/Arctic/ArcticGRO/CDOM_DOC_in_situ/ArcticGRO_Mackenzie_Discharge_DOC_insitu.xlsx'
DOC_data = pd.read_excel(DOC_input_file)
# 提取所需的列：Date, DOC
DOC_data1 = DOC_data[['Date', 'DOC']]

# 确保DOC数据中的日期列为datetime类型
DOC_data1.loc[:, 'Date'] = pd.to_datetime(DOC_data1['Date'], format='%Y-%m-%d', errors='coerce')

# 定义读取CDOM数据文件的函数
def read_cdom_data(file_path, sheet_name):
    # 使用pandas读取Excel文件中的指定工作表
    df = pd.read_excel(file_path, sheet_name=sheet_name, header=None)

    # 假设第一行为日期，第二行为CDOM值
    dates = pd.to_datetime(df.iloc[0].tolist(), format='%Y-%m-%d', errors='coerce')
    cdom_values = df.iloc[1].tolist()

    # 创建一个新的DataFrame，将行数据转换为列数据
    transformed_df = pd.DataFrame({
        'Date': dates,
        'CDOM': pd.to_numeric(cdom_values, errors='coerce')  # 确保CDOM值为数值型
    })

    # 应用转换公式
    transformed_df['CDOM'] = 2.303 * transformed_df['CDOM'] / 0.01

    return transformed_df

# 文件路径和工作表名称
CDOM_file_path = 'D:/UZH/2024/20240122 Nutrient and Organic Carbon references/Arctic/ArcticGRO/CDOM_DOC_in_situ/ArcticGRO_Absorbance_Data.xlsx'
sheet_name = 'Mackenzie'

# 读取文件并打印内容
CDOM_data1 = read_cdom_data(CDOM_file_path, sheet_name)

# 确保CDOM数据中的日期列为datetime类型
CDOM_data1.loc[:, 'Date'] = pd.to_datetime(CDOM_data1['Date'], format='%Y-%m-%d', errors='coerce')

# 合并DOC和CDOM数据，基于日期匹配
merged_data = pd.merge(DOC_data1, CDOM_data1, on='Date', how='inner')

# 删除包含 NaN 的行
merged_data = merged_data.dropna()

# 保存合并数据到新的Excel文件
output_file = 'D:/UZH/2024/20240122 Nutrient and Organic Carbon references/Arctic/ArcticGRO/CDOM_DOC_in_situ/ArcticGRO_DOC_CDOM_insitu_Mackenzie.xlsx'
merged_data.to_excel(output_file, index=False)

# 创建子图
fig, ax1 = plt.subplots(figsize=(10, 10))


# 进行线性回归
X = merged_data[['DOC']].values.reshape(-1, 1)
y = merged_data['CDOM'].values
regressor = LinearRegression()
regressor.fit(X, y)

# 获取回归系数
a = regressor.coef_[0]
b = regressor.intercept_

# 打印回归系数
print(f"Linear Regression Equation: CDOM = {a:.4f} * DOC + {b:.4f}")

# 绘制散点图和线性回归拟合线（子图2）
ax1.scatter(merged_data['DOC'], merged_data['CDOM'], alpha=0.7, label='in situ')
ax1.plot(X, regressor.predict(X), color='red', linewidth=2, label=f'Fit: CDOM = {a:.4f} * DOC {b:.4f}')
ax1.set_title('Mackenzie', fontsize=14)
ax1.set_xlabel('DOC mg/L', fontsize=14)
ax1.set_ylabel('CDOM/m-1', fontsize=14)
ax1.grid(True)
ax1.legend()

# 显示图形
plt.tight_layout()
plt.show()