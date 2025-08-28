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

# 将数据分为20组（基于Average_DOC_Total），并计算每组的范围  # English: Divide the data into
data['Group'], bins = pd.qcut(data['Average_DOC_Total'], q=20, retbins=True, labels=False)

# 计算每组的河流数量  # English: Calculate the number of rivers per group
group_counts = data['Group'].value_counts().sort_index()

# 生成每组范围的标签  # English: Generate labels for each set of ranges
group_labels = [f"{bins[i]:.2f} - {bins[i+1]:.2f}" for i in range(len(bins)-1)]

# 绘制柱状图  # English: Draw a bar chart
plt.figure(figsize=(14, 7))
plt.bar(group_labels, group_counts, color='skyblue', edgecolor='black')

# 美化图表  # English: Beautify the chart
plt.title('Number of Rivers in Each Average DOC Total Group', fontsize=18)
plt.xlabel('Groups (Ranges of Average DOC Total)', fontsize=14)
plt.ylabel('Number of Rivers', fontsize=14)
plt.xticks(rotation=45, fontsize=10)

# 调整布局以防止标签重叠  # English: Adjust the layout to prevent label overlapping
plt.tight_layout()

# 保存图表为.tif文件，300dpi  # English: Save the chart as
output_path = r"D:\UZH\2024\20240122 Nutrient and Organic Carbon references\DOC\average_Total_DOC\Average_DOC_Total_Group_Counts.tif"
plt.savefig(output_path, dpi=300, format='tiff')

# 显示图表  # English: Show charts
plt.show()
