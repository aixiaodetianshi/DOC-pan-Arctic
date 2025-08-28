import pandas as pd
import matplotlib.pyplot as plt
import matplotlib as mpl
from sklearn.linear_model import LinearRegression
import numpy as np

# 设置全局字体为Times New Roman  # English: Set the global font to
mpl.rcParams['font.family'] = 'Times New Roman'

DOC_CDOM_input_file = 'D:/UZH/2024/20240122 Nutrient and Organic Carbon references/Arctic/ArcticGRO/CDOM_DOC_in_situ/ArcticGRO_DOC_CDOM_insitu_total.xlsx'
DOC_CDOM = pd.read_excel(DOC_CDOM_input_file)
# 提取所需的列：Date, DOC  # English: Extract the required columns
DOC_CDOM1 = DOC_CDOM[['Date', 'DOC', 'CDOM']]
# 确保DOC数据中的日期列为datetime类型  # English: make sure
DOC_CDOM1.loc[:, 'Date'] = pd.to_datetime(DOC_CDOM1['Date'], format='%Y-%m-%d', errors='coerce')

# 创建子图  # English: Create a subgraph
fig, ax1 = plt.subplots(figsize=(10, 10))


# 进行线性回归  # English: Perform linear regression
X = DOC_CDOM1[['DOC']].values.reshape(-1, 1)
y = DOC_CDOM1['CDOM'].values
regressor = LinearRegression()
regressor.fit(X, y)

# 获取回归系数  # English: Get the regression coefficient
a = regressor.coef_[0]
b = regressor.intercept_

# 打印回归系数  # English: Print regression coefficients
print(f"Linear Regression Equation: CDOM = {a:.4f} * DOC + {b:.4f}")

# 绘制散点图和线性回归拟合线（子图2）  # English: Draw scatter plots and linear regression fit lines
ax1.scatter(DOC_CDOM1['DOC'], DOC_CDOM1['CDOM'], alpha=0.7, label='in situ')
ax1.plot(X, regressor.predict(X), color='red', linewidth=2, label=f'Fit: CDOM = {a:.4f} * DOC {b:.4f}')
ax1.set_title('Total universal river', fontsize=14)
ax1.set_xlabel('DOC mg/L', fontsize=14)
ax1.set_ylabel('CDOM/m-1', fontsize=14)
ax1.grid(True)
ax1.legend()

# 显示图形  # English: Show graphics
plt.tight_layout()
plt.show()
