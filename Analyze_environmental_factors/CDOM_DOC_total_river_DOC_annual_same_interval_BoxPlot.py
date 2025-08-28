import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# 设置全局字体为 Times New Roman  # English: Set the global font to
plt.rcParams['font.family'] = 'Times New Roman'

# 读取CSV文件  # English: Read
file_path = r"D:\UZH\2024\20240122 Nutrient and Organic Carbon references\DOC\average_Total_DOC\average_Total_DOC.csv"
data = pd.read_csv(file_path)

# 确保列名正确  # English: Make sure the column name is correct
data.columns = ['COMID', 'Average_DOC_Total']

# 去除缺失值  # English: Remove missing values
data = data.dropna()

# 根据最大值和最小值，等间距分为15组  # English: According to maximum and minimum values
min_value = data['Average_DOC_Total'].min()
max_value = data['Average_DOC_Total'].max()
bins = np.linspace(min_value, max_value, 16)  # 生成16个点，共15个区间  # English: generate

# 将数据分为15个组  # English: Divide the data into
data['Group'] = pd.cut(data['Average_DOC_Total'], bins=bins, labels=False, include_lowest=True)

# 计算每组的河流数量  # English: Calculate the number of rivers per group
group_counts = data['Group'].value_counts().sort_index()

# 生成每组范围的标签（整数格式）  # English: Generate labels for each set of ranges
group_labels = [f"{int(bins[i])} - {int(bins[i+1])}" for i in range(len(bins)-1)]  # 显示整数  # English: Show integers

# 确保group_counts的长度与group_labels一致，若缺少组则填充0  # English: make sure
group_counts = group_counts.reindex(range(15), fill_value=0)  # 为每个组填充0  # English: Fill for each group

# 绘制柱状图  # English: Draw a bar chart
plt.figure(figsize=(18, 8))  # 调整图像尺寸，确保每个标签清晰可见  # English: Adjust image size
plt.bar(group_labels, group_counts, color='lightcoral', edgecolor='black', width=0.4)  # 缩小柱宽度  # English: Reduce column width

# 美化图表  # English: Beautify the chart
plt.title('Number of Rivers in Each Equal Interval Average DOC Total Group', fontsize=20, fontweight='bold')
plt.xlabel('Groups (Ranges of Average DOC Total)', fontsize=16)
plt.ylabel('Number of Rivers', fontsize=16)
plt.xticks(rotation=45, fontsize=12)
plt.yticks(fontsize=12)

# 设置横轴坐标为整数  # English: Set the horizontal axis coordinates to integers
plt.xticks(ticks=np.arange(len(group_labels)), labels=group_labels)

# 添加网格线  # English: Add grid lines
plt.grid(axis='y', linestyle='--', alpha=0.7)

# 增加标签注释  # English: Add tag comments
for i, count in enumerate(group_counts):
    plt.text(i, count + 0.5, str(count), ha='center', fontsize=10)

# 调整布局以防止标签重叠  # English: Adjust the layout to prevent label overlapping
plt.tight_layout()

# 保存图表为.tif文件，300dpi  # English: Save the chart as
output_path = r"D:\UZH\2024\20240122 Nutrient and Organic Carbon references\DOC\average_Total_DOC\Equal_Interval_Average_DOC_Total_Group_Counts_15.tif"
plt.savefig(output_path, dpi=300, format='tiff')

# 显示图表  # English: Show charts
plt.show()
