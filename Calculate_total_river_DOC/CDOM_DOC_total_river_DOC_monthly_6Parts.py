import pandas as pd
import os

# 输入文件夹路径（源数据）  # English: Enter the folder path
river = "Mackenzie"
input_folder_path = r"D:\UZH\2024\20240122 Nutrient and Organic Carbon references\3_river_mouth_DOC\DOC_update_20250203\Total_DOC_monthly\\" + river

# 输出文件夹路径（计算后数据）  # English: Output folder path
output_folder_path = r"D:\UZH\2024\20240122 Nutrient and Organic Carbon references\3_river_mouth_DOC\DOC_update_20250203\Total_DOC_monthly\\" + river + "_month"

# 保存到输出文件夹  # English: Save to output folder
output_file_path = os.path.join(output_folder_path, "Total_monthly_DOC_"+river+"_Parts.csv")

# 创建输出目录（如果不存在）  # English: Create an output directory
os.makedirs(output_folder_path, exist_ok=True)

# 创建空的 DataFrame 用于存储所有数据  # English: Create an empty
all_data = pd.DataFrame()

# 遍历文件夹中的所有CSV文件  # English: Iterate through all the folders
for file_name in os.listdir(input_folder_path):
    if file_name.endswith('.csv'):
        file_path = os.path.join(input_folder_path, file_name)

        # 读取CSV文件  # English: Read
        df = pd.read_csv(file_path, usecols=['year_month', 'Total_DOC', 'Total_DOC_uncertainty'])

        # 确保 year_month 是 datetime 格式（以便后续处理）  # English: make sure
        df['year_month'] = pd.to_datetime(df['year_month'], format='%Y-%m')

        # 仅保留 1984 年 1 月 到 2018 年 12 月的数据  # English: Keep only
        df = df[(df['year_month'].dt.year >= 1984) & (df['year_month'].dt.year <= 2018)]

        # 添加到总数据中  # English: Add to total data
        all_data = pd.concat([all_data, df], ignore_index=True)

# 按年月分组并汇总 Total_DOC 和 Total_DOC_uncertainty  # English: Group and summarize by year and month
monthly_total = all_data.groupby(all_data['year_month'].dt.to_period('M')).agg(
    Total_DOC=('Total_DOC', 'sum'),
    Total_DOC_uncertainty=('Total_DOC_uncertainty', 'sum')
).reset_index()

# 转换 year_month 回字符串格式  # English: Convert
monthly_total['year_month'] = monthly_total['year_month'].astype(str)

monthly_total.to_csv(output_file_path, index=False)

print(f"Monthly total DOC data saved to: {output_file_path}")
