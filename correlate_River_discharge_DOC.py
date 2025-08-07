import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression

# 文件路径和表名
file_path = r'D:\UZH\2024\20240122 Nutrient and Organic Carbon references\Arctic\ArcticGRO\ArcticGRO_Discharge_DOC.xlsx'
sheet_name = 'Ob'

# 读取Excel文件（跳过前两行: 第一行为变量名，第二行为数据）
data = pd.read_excel(file_path, sheet_name=sheet_name)

# 选择需要的列（Discharge 和 DOC）
discharge = data['Discharge']
doc = data['DOC']

# 同时去除两列中含有缺失值的行
data_cleaned = data[['Discharge', 'DOC']].dropna()

# 提取去除缺失值后的列
discharge_cleaned = data_cleaned['Discharge']
doc_cleaned = data_cleaned['DOC']

# 转换为 numpy 数组用于拟合
X = discharge_cleaned.values.reshape(-1, 1)  # 将 Discharge 作为特征
y = doc_cleaned.values  # 将 DOC 作为目标变量

# 线性回归模型拟合
model = LinearRegression()
model.fit(X, y)

# 获取拟合结果
y_pred = model.predict(X)

# 获取拟合的斜率和截距
slope = model.coef_[0]
intercept = model.intercept_

# 创建散点图
plt.figure(figsize=(6, 6))
plt.scatter(discharge_cleaned, doc_cleaned, color='blue', label='Observed Data', alpha=0.6, edgecolor='black')

# 绘制1:1线
plt.plot([min(discharge_cleaned), max(discharge_cleaned)], [min(discharge_cleaned), max(discharge_cleaned)],
         color='red', linestyle='--', label='1:1 Line')

# 绘制拟合线
plt.plot(discharge_cleaned, y_pred, color='green', label=f'Fit Line (y = {slope:.2f}x + {intercept:.2f})')

# 添加标签和标题
plt.xlabel('Discharge')
plt.ylabel('DOC')
plt.title('Linear Fit of Discharge vs DOC')

# 添加图例
plt.legend()

# 显示网格
plt.grid(True, linestyle='--', linewidth=0.5)

# 调整布局，显示图像
plt.tight_layout()

# 显示图像
plt.show()
