# 读取‪D:\UZH\2024\20240122 Nutrient and Organic Carbon references\river_endpoints_water_surface_info\Kolyma_river_endpoints_WaterInfo.csv文件数据  # English: Read
# 共有变量： system:index； COMID；water_occurrence；.geo 5个，第一行是变量名，  # English: There are common variables
# 现在统计water_occurrence的数值分布情况，将其分为11组，第一组是空值；第二组范围是大于等于0，小于10；  # English: Statistics now
# 第3组范围是大于等于10，小于20；第4组范围是大于等于20，小于30；第5组范围是大于等于30，小于40；  # English: The
# 第6组范围是大于等于40，小于50；第7组范围是大于等于50，小于60；第8组范围是大于等于60，  # English: The
# 小于70；第9组范围是大于等于70，小于80；第10组范围是大于等于80，小于90；第11组范围是大于等于90，小于等于100，  # English: Less than
# 将分组结果输出以相同的文件名输出到  # English: Output the grouping result output to the same file name
# 文件夹D:\UZH\2024\20240122 Nutrient and Organic Carbon references\river_endpoints_water_surface_info\water_group_river_points中，  # English: Folders
# 第一列是分组范围，第二列是每组的数量。  # English: The first column is the grouping range


import pandas as pd
import os

# 定义文件路径  # English: Define file path
input_file = r"D:\UZH\2024\20240122 Nutrient and Organic Carbon references\river_endpoints_water_surface_info\Yukon_river_endpoints_WaterInfo.csv"
output_folder = r"D:\UZH\2024\20240122 Nutrient and Organic Carbon references\river_endpoints_water_surface_info\water_group_river_points"

# 确保输出文件夹存在  # English: Make sure the output folder exists
os.makedirs(output_folder, exist_ok=True)

# 读取CSV文件  # English: Read
try:
    data = pd.read_csv(input_file)
except Exception as e:
    raise ValueError(f"读取文件时出错: {e}")

# 检查是否存在 water_occurrence 列  # English: Check if it exists
if "water_occurrence" not in data.columns:
    raise ValueError("The file does not contain the 'water_occurrence' column.")

# 定义分组范围和标签  # English: Define grouping ranges and labels
bins = [-float('inf'), 0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
labels = ["<=0", "0-10", "10-20", "20-30", "30-40", "40-50", "50-60", "60-70", "70-80", "80-90", "90-100"]

# 统计总记录数  # English: Total records count
total_records = len(data)

# 统计每组（第2组到第11组）的数量  # English: Statistics of each group
# 对 water_occurrence 列进行分组统计  # English: right
data['group'] = pd.cut(data['water_occurrence'], bins=bins, labels=labels, right=True, include_lowest=True)
group_counts = data['group'].value_counts().sort_index()

# 计算第一组（空值）的数量  # English: Calculate the first group
empty_count = total_records - group_counts.sum()

# 合并所有组的统计结果  # English: Combined statistics for all groups
output_data = pd.DataFrame({
    "Group Range": ["Empty (NaN)"] + labels,
    "Count": [empty_count] + group_counts.tolist()
})

# 输出文件路径  # English: Output file path
output_file = os.path.join(output_folder, "Yukon_river_endpoints_WaterInfo_grouped.csv")

# 保存结果到文件  # English: Save the results to file
output_data.to_csv(output_file, index=False)

print(f"分组结果已保存到文件: {output_file}")
