# 用于读取 D:\UZH\2024\20240122 Nutrient and Organic Carbon references\DOC\DOC_update_20250203\Combination_single_river_interpolate\Ob
# 文件夹中的 CSV 文件，计算 Total_DOC 和 Total_DOC_uncertainty，
# 并将结果保存到 D:\UZH\2024\20240122 Nutrient and Organic Carbon references\DOC\DOC_update_20250203\Total_DOC\Ob 文件夹。
# 文件格式修改：原代码处理的是 .xlsx 文件，现在改为处理 .csv 文件。
# 列选择修改：只读取 date, DOC, DOC_uncertainty, discharge 4列数据。
# 计算逻辑修改：添加 Total_DOC 和 Total_DOC_uncertainty 计算公式。
# 输出格式修改：保存为 CSV 文件，仅包含 date, Total_DOC, Total_DOC_uncertainty 3列数据。

# 代码解析
# 路径设置：
#
# input_folder_path：源数据文件夹（Combination_single_river_interpolate\Ob）。
# output_folder_path：计算结果存放文件夹（Total_DOC\Ob）。
# 使用 os.makedirs(output_folder_path, exist_ok=True) 确保输出文件夹存在。
# 遍历 CSV 文件：
#
# 使用 os.listdir(input_folder_path) 遍历所有文件。
# 仅处理 .csv 文件（if file_name.endswith('.csv')）。
# 读取和处理数据：
#
# 仅读取 date, DOC, DOC_uncertainty, discharge 这 4 列。
# 将 date 转换为 datetime 格式（确保日期格式正确）。
# 计算 DOC 通量和不确定性：
#
# Total_DOC = DOC * discharge * 86400 / 1_000_000（单位 T）。
# Total_DOC_uncertainty = DOC_uncertainty * discharge * 86400 / 1_000_000（单位 T）。
# 保存结果：
#
# 仅保留 date, Total_DOC, Total_DOC_uncertainty 3列。
# 以相同文件名存入 Total_DOC\Ob 文件夹（.csv 格式）。

import pandas as pd
import os

# 输入文件夹路径（源数据）
river = "Yukon"
input_folder_path = r"D:\UZH\2024\20240122 Nutrient and Organic Carbon references\3_river_mouth_DOC\DOC_update_20250203\Combination_single_river_sort_date_pre_process_filldate_combine_discharge\\" + river

# 输出文件夹路径（计算后数据）
output_folder_path = r"D:\UZH\2024\20240122 Nutrient and Organic Carbon references\3_river_mouth_DOC\DOC_update_20250203\Total_DOC\\" + river

# 确保输出文件夹存在
os.makedirs(output_folder_path, exist_ok=True)

# 遍历所有CSV文件
for file_name in os.listdir(input_folder_path):
    if file_name.endswith('.csv'):  # 只处理CSV文件
        # 构造完整的文件路径
        input_file_path = os.path.join(input_folder_path, file_name)
        output_file_path = os.path.join(output_folder_path, file_name)

        # 读取CSV文件，仅保留需要的列
        df = pd.read_csv(input_file_path, usecols=['date', 'DOC', 'DOC_uncertainty', 'discharge'])

        # 确保 'date' 列是 datetime 格式
        df['date'] = pd.to_datetime(df['date'], errors='coerce')

        # 过滤掉无法解析的日期
        df = df.dropna(subset=['date'])

        # 只保留 5 月 1 日至 10 月 31 日的数据
        # 只保留 1 月 1 日至 12 月 31 日的数据
        df = df[(df['date'].dt.month >= 5) & (df['date'].dt.month <= 10)]

        # 仅计算1984年到2018年之间的数据
        df = df[(df['date'].dt.year >= 1984) & (df['date'].dt.year <= 2018)]

        # 计算 Total_DOC 和 Total_DOC_uncertainty（单位：T）
        df['Total_DOC'] = df['DOC'] * df['discharge'] * 86400 / 1_000_000
        df['Total_DOC_uncertainty'] = df['DOC_uncertainty'] * df['discharge'] * 86400 / 1_000_000

        # 选择需要保存的列
        result_df = df[['date', 'Total_DOC', 'Total_DOC_uncertainty']]

        # 保存计算结果为 CSV 文件
        result_df.to_csv(output_file_path, index=False)
        print(f"Processed: {file_name}")

print("Processing complete. Filtered Total DOC files saved in folder.")
