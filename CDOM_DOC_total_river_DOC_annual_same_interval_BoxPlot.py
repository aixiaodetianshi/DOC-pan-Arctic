import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# 设置全局字体为 Times New Roman
plt.rcParams['font.family'] = 'Times New Roman'

# 读取CSV文件
file_path = r"D:\UZH\2024\20240122 Nutrient and Organic Carbon references\DOC\average_Total_DOC\average_Total_DOC.csv"
data = pd.read_csv(file_path)

# 确保列名正确
data.columns = ['COMID', 'Average_DOC_Total']

# 去除缺失值
data = data.dropna()

# 根据最大值和最小值，等间距分为15组
min_value = data['Average_DOC_Total'].min()
max_value = data['Average_DOC_Total'].max()
bins = np.linspace(min_value, max_value, 16)  # 生成16个点，共15个区间

# 将数据分为15个组
data['Group'] = pd.cut(data['Average_DOC_Total'], bins=bins, labels=False, include_lowest=True)

# 计算每组的河流数量
group_counts = data['Group'].value_counts().sort_index()

# 生成每组范围的标签（整数格式）
group_labels = [f"{int(bins[i])} - {int(bins[i+1])}" for i in range(len(bins)-1)]  # 显示整数

# 确保group_counts的长度与group_labels一致，若缺少组则填充0
group_counts = group_counts.reindex(range(15), fill_value=0)  # 为每个组填充0

# 绘制柱状图
plt.figure(figsize=(18, 8))  # 调整图像尺寸，确保每个标签清晰可见
plt.bar(group_labels, group_counts, color='lightcoral', edgecolor='black', width=0.4)  # 缩小柱宽度

# 美化图表
plt.title('Number of Rivers in Each Equal Interval Average DOC Total Group', fontsize=20, fontweight='bold')
plt.xlabel('Groups (Ranges of Average DOC Total)', fontsize=16)
plt.ylabel('Number of Rivers', fontsize=16)
plt.xticks(rotation=45, fontsize=12)
plt.yticks(fontsize=12)

# 设置横轴坐标为整数
plt.xticks(ticks=np.arange(len(group_labels)), labels=group_labels)

# 添加网格线
plt.grid(axis='y', linestyle='--', alpha=0.7)

# 增加标签注释
for i, count in enumerate(group_counts):
    plt.text(i, count + 0.5, str(count), ha='center', fontsize=10)

# 调整布局以防止标签重叠
plt.tight_layout()

# 保存图表为.tif文件，300dpi
output_path = r"D:\UZH\2024\20240122 Nutrient and Organic Carbon references\DOC\average_Total_DOC\Equal_Interval_Average_DOC_Total_Group_Counts_15.tif"
plt.savefig(output_path, dpi=300, format='tiff')

# 显示图表
plt.show()
