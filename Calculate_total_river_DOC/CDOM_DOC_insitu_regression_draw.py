
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib as mpl
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, mean_absolute_error
from scipy.stats import linregress
import numpy as np

# 设置全局字体为 Times New Roman  # English: Set the global font to
mpl.rcParams['font.family'] = 'Times New Roman'

# 文件路径  # English: File path
input_file = r'D:\UZH\2024\20240122 Nutrient and Organic Carbon references\Arctic\ArcticGRO\CDOM_DOC_in_situ\ArcticGRO_DOC_CDOM_insitu_Ob.xlsx'
output_image_path = r'D:\UZH\2024\20240122 Nutrient and Organic Carbon references\Arctic\ArcticGRO\CDOM_DOC_in_situ\Ob.tif'

# 读取合并数据  # English: Read merged data
merged_data = pd.read_excel(input_file)

# 提取 DOC 和 CDOM 数据  # English: extract
X = merged_data[['DOC']].values.reshape(-1, 1)
y = merged_data['CDOM'].values

# 线性回归模型  # English: Linear regression model
regressor = LinearRegression()
regressor.fit(X, y)

# 获取回归系数和截距  # English: Get regression coefficients and intercepts
a = regressor.coef_[0]
b = regressor.intercept_

# 打印线性回归方程  # English: Print linear regression equations
print(f"Linear Regression Equation: CDOM = {a:.4f} * DOC + {b:.4f}")

# 预测值  # English: Predicted value
y_pred = regressor.predict(X)

# 计算评价指标  # English: Calculate evaluation indicators
rmse = mean_squared_error(y, y_pred, squared=False)  # RMSE
mae = mean_absolute_error(y, y_pred)                 # MAE
bias = np.mean(y_pred - y)                           # Bias
r2 = regressor.score(X, y)                           # R²

# 使用 scipy 计算 P-value  # English: use
slope, intercept, r_value, p_value, std_err = linregress(merged_data['DOC'], merged_data['CDOM'])

# 打印评价指标  # English: Print evaluation indicators
print(f"RMSE: {rmse:.4f}")
print(f"MAE: {mae:.4f}")
print(f"Bias: {bias:.4f}")
print(f"R²: {r2:.4f}")
print(f"P-value: {p_value:.4e}")

# 创建图形，设置大小为 15.24 cm x 15.24 cm  # English: Create a graph
fig, ax1 = plt.subplots(figsize=(15.24 / 2.54, 15.24 / 2.54))  # 将厘米转换为英寸  # English: Convert centimeters to inches

# 绘制散点图和线性回归拟合线  # English: Draw scatter plots and linear regression fit lines
ax1.scatter(merged_data['DOC'], merged_data['CDOM'], alpha=0.7, label='in situ')
ax1.plot(X, y_pred, color='red', linewidth=2, label=f'Fit: CDOM = {a:.4f} * DOC + {b:.4f}')
ax1.set_title('Ob', fontsize=14)
ax1.set_xlabel('DOC (mg/L)', fontsize=14)
ax1.set_ylabel('CDOM (m⁻¹)', fontsize=14)
ax1.grid(True)
ax1.legend()

# 设置 x 和 y 轴范围，确保所有数据点显示并留出边距  # English: set up
x_min, x_max = merged_data['DOC'].min(), merged_data['DOC'].max()
y_min, y_max = merged_data['CDOM'].min(), merged_data['CDOM'].max()
ax1.set_xlim([x_min - 0.1 * (x_max - x_min), x_max + 0.1 * (x_max - x_min)])
ax1.set_ylim([y_min - 0.1 * (y_max - y_min), y_max + 0.1 * (y_max - y_min)])

# 在图像左上角显示评价指标  # English: Display evaluation metrics in the upper left corner of the image
textstr = (f'RMSE: {rmse:.4f}\n'
           f'MAE: {mae:.4f}\n'
           f'Bias: {bias:.4f}\n'
           f'R²: {r2:.4f}\n'
           f'P-value: {p_value:.4f}')
ax1.text(0.05, 0.95, textstr, transform=ax1.transAxes, fontsize=10,
         verticalalignment='top', horizontalalignment='left')

# 保存图像，确保内容完整显示  # English: Save the image
plt.tight_layout()  # 自动调整布局  # English: Automatically adjust layout
fig.savefig(output_image_path, format='tif', dpi=600, bbox_inches='tight')

plt.show()  # 显示图形  # English: Show graphics
