import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# 设置全局字体为 Times New Roman  # English: Set the global font to
plt.rcParams['font.family'] = 'Times New Roman'

# 读取CSV文件  # English: Read
file_path = r"D:\UZH\2024\20240122 Nutrient and Organic Carbon references\DOC\DOC_update_20250203\Total_DOC_average\average_Total_DOC.csv"
data = pd.read_csv(file_path)

# 确保列名正确  # English: Make sure the column name is correct
data.columns = ['COMID', 'Average_Total_DOC', 'Average_Total_DOC_Uncertainty']

# 去除缺失值  # English: Remove missing values
data = data.dropna()

# 将数据分为20组（基于Average_DOC_Total），并计算每组的范围  # English: Divide the data into
data['Group'], bins = pd.qcut(data['Average_Total_DOC'], q=20, retbins=True, labels=False)

# 生成每组范围的标签  # English: Generate labels for each set of ranges
group_labels = [f"{bins[i]:.2f} - {bins[i+1]:.2f}" for i in range(len(bins)-1)]

# 为每组生成箱线图  # English: Generate box diagrams for each group
plt.figure(figsize=(14, 7))
sns.boxplot(
    x='Group',
    y='Average_Total_DOC',
    data=data,
    hue=None,  # 明确设置无分组  # English: Clearly set no grouping
    showfliers=False
)

# 美化图表  # English: Beautify the chart
plt.title('Annual Average Total DOC Distribution', fontsize=18)
plt.xlabel('Groups (Ranges of Average Total DOC)', fontsize=14)
plt.ylabel('Average  Total DOC (ton)', fontsize=14)  # 更新单位为ton  # English: The update unit is
plt.xticks(ticks=np.arange(20), labels=group_labels, rotation=45, fontsize=10)

# 调整布局以防止标签重叠  # English: Adjust the layout to prevent label overlapping
plt.tight_layout()

# 保存图表为.tif文件，300dpi  # English: Save the chart as
output_path = r"D:\UZH\2024\20240122 Nutrient and Organic Carbon references\DOC\DOC_update_20250203\Total_DOC_average\Average_Total_DOC_Boxplot.tif"
plt.savefig(output_path, dpi=300, format='tiff')

# 显示图表  # English: Show charts
plt.show()
