import pandas as pd
import os

# 河流名称列表
rivers = ["Ob", "Yenisey", "Lena", "Kolyma", "Yukon", "Mackenzie"]

# 构建所有输入文件路径
base_path = r"D:\UZH\2024\20240122 Nutrient and Organic Carbon references\3_river_mouth_DOC\DOC_update_20250203\Total_DOC_monthly"
input_filenames = [
    os.path.join(base_path, f"{river}_month", f"Total_monthly_DOC_{river}_Parts.csv")
    for river in rivers
]

# 创建空的 DataFrame 列表以存储各河流数据
df_list = []

for file in input_filenames:
    df = pd.read_csv(file, usecols=['year_month', 'Total_DOC', 'Total_DOC_uncertainty'])
    df['year_month'] = pd.to_datetime(df['year_month'], format='%Y-%m')  # 确保格式正确
    df_list.append(df)

# 合并所有数据
combined_df = pd.concat(df_list)

# 按 year_month 分组并求和（合计每个月的 Total_DOC 和 Total_DOC_uncertainty）
summary_df = combined_df.groupby('year_month', as_index=False).sum()

# 输出路径
output_filename = os.path.join(base_path, r"All_month\Total_monthly_DOC_All_Parts.csv")
os.makedirs(os.path.dirname(output_filename), exist_ok=True)

# 保存为CSV
summary_df.to_csv(output_filename, index=False)

print(f"Combined monthly total DOC data saved to: {output_filename}")