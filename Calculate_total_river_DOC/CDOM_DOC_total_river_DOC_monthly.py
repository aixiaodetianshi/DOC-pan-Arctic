# 读取数据：从 input_folder_path 目录下的每个 .csv 文件中读取 date, Total_DOC, 和 Total_DOC_uncertainty 列。  # English: Read data
# 日期过滤：确保 date 列转换为 datetime 格式，且仅保留 5 月 1 日到 10 月 31 日的数据。  # English: Date filtering
# 按年月分组：通过 df['date'].dt.to_period('M') 提取年月信息，将数据按年和月进行分组。  # English: Grouped by year and month
# 计算每月总 DOC 通量：使用 groupby 和 agg 方法计算每个月 Total_DOC 和 Total_DOC_uncertainty 的总和。  # English: Calculate monthly totals
# 保存结果：将每个河流（文件）处理后的结果保存到新的文件夹 Total_DOC_monthly\Ob 中，文件名与原文件相同。  # English: Save the results
# 输出文件：  # English: Output file
# 每个文件包含两列：  # English: Each file contains two columns
#
# year_month：表示年月（格式为 YYYY-MM）。  # English: Indicates year and month
# Total_DOC：每月的 DOC 通量总和。  # English: Monthly
# Total_DOC_uncertainty：每月的 DOC 不确定性总和。  # English: Monthly
# 执行后，每条河流的每月总 DOC 通量将存储为 .csv 文件，保存在指定的文件夹中。  # English: After execution

import pandas as pd
import os

# 输入文件夹路径（源数据）  # English: Enter the folder path
river = "Yukon"
input_folder_path = r"D:\UZH\2024\20240122 Nutrient and Organic Carbon references\3_river_mouth_DOC\DOC_update_20250203\Total_DOC\\" + river
# 输出文件夹路径（计算后数据）  # English: Output folder path
output_folder_path = r"D:\UZH\2024\20240122 Nutrient and Organic Carbon references\3_river_mouth_DOC\DOC_update_20250203\Total_DOC_monthly\\" + river

# 确保输出文件夹存在  # English: Make sure the output folder exists
os.makedirs(output_folder_path, exist_ok=True)

# 遍历所有CSV文件  # English: Iterate through all
for file_name in os.listdir(input_folder_path):
    if file_name.endswith('.csv'):  # 只处理CSV文件  # English: Process only
        # 构造完整的文件路径  # English: Construct the complete file path
        input_file_path = os.path.join(input_folder_path, file_name)
        output_file_path = os.path.join(output_folder_path, file_name)

        # 读取CSV文件  # English: Read
        df = pd.read_csv(input_file_path, usecols=['date', 'Total_DOC', 'Total_DOC_uncertainty'])

        # 确保 'date' 列是 datetime 格式  # English: make sure
        df['date'] = pd.to_datetime(df['date'], errors='coerce')

        # 过滤掉无法解析的日期  # English: Filter out unresolved dates
        df = df.dropna(subset=['date'])

        # 仅保留 5 月 1 日至 10 月 31 日的数据  # English: Keep only
        # 仅保留 1 月 1 日至 12 月 31 日的数据  # English: Keep only
        df = df[(df['date'].dt.month >= 5) & (df['date'].dt.month <= 10)]

        # 仅计算1984年到2018年之间的数据  # English: Calculate only
        df = df[(df['date'].dt.year >= 1984) & (df['date'].dt.year <= 2018)]

        # 按年月分组并计算总DOC通量  # English: Group by year and month and calculate total
        df['year_month'] = df['date'].dt.to_period('M')  # 获取年月  # English: Get the year and month
        monthly_total = df.groupby('year_month').agg(
            Total_DOC=('Total_DOC', 'sum'),
            Total_DOC_uncertainty=('Total_DOC_uncertainty', 'sum')
        ).reset_index()

        # 保存计算结果为 CSV 文件  # English: Save the calculation result as
        monthly_total.to_csv(output_file_path, index=False)
        print(f"Processed: {file_name}")

print("Processing complete. Monthly Total DOC files saved in Total_DOC_monthl folder")
