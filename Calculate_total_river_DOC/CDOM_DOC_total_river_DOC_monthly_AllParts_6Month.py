import pandas as pd
import os

# 河流名称列表  # English: List of river names
rivers = ["Ob", "Yenisey", "Lena", "Kolyma", "Yukon", "Mackenzie"]

# 构建所有输入文件路径  # English: Build all input file paths
base_path = r"D:\UZH\2024\20240122 Nutrient and Organic Carbon references\3_river_mouth_DOC\DOC_update_20250203\Total_DOC_monthly"
input_filenames = [
    os.path.join(base_path, f"{river}_month", f"Total_monthly_DOC_{river}_Parts.csv")
    for river in rivers
]

# 创建空的 DataFrame 列表以存储各河流数据  # English: Create an empty
df_list = []

for file in input_filenames:
    df = pd.read_csv(file, usecols=['year_month', 'Total_DOC', 'Total_DOC_uncertainty'])
    df['year_month'] = pd.to_datetime(df['year_month'], format='%Y-%m')  # 确保格式正确  # English: Make sure the format is correct
    df_list.append(df)

# 合并所有数据  # English: Merge all data
combined_df = pd.concat(df_list)

# 按 year_month 分组并求和（合计每个月的 Total_DOC 和 Total_DOC_uncertainty）  # English: according to
summary_df = combined_df.groupby('year_month', as_index=False).sum()

# 输出路径  # English: Output path
output_filename = os.path.join(base_path, r"All_month\Total_monthly_DOC_All_Parts.csv")
os.makedirs(os.path.dirname(output_filename), exist_ok=True)

# 保存为CSV  # English: Save as
summary_df.to_csv(output_filename, index=False)

print(f"Combined monthly total DOC data saved to: {output_filename}")