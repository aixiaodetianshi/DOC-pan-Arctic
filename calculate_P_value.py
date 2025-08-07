import numpy as np
import matplotlib.pyplot as plt
from scipy import stats

# 生成两组示例数据
x = np.random.rand(50)
y = 2 * x + np.random.normal(0, 0.1, 50)  # y是x的线性关系加上一些噪音

# 计算Pearson相关系数和P-value
corr, p_value = stats.pearsonr(x, y)

# 打印相关系数和P-value
print(f"Pearson相关系数: {corr}")
print(f"P-value: {p_value}")

# 绘制散点图
plt.scatter(x, y)
plt.title(f'Scatter plot with Pearson r={corr:.2f}, p-value={p_value:.2e}')
plt.xlabel('X')
plt.ylabel('Y')
plt.show()
