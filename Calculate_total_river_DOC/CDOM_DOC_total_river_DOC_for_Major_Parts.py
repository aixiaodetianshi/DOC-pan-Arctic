# 读取 Kolyma 文件夹内所有 CSV 文件。  # English: Read
# 确保每个文件包含 year 和 Total_DOC 列。  # English: Make sure each file contains
# 按 year 聚合所有河流的 Total_DOC，计算每年的总 DOC 通量。  # English: according to
# 将最终结果保存为 Total_DOC_annual_Kolyma_Parts.csv。  # English: Save the final result as

import os
import pandas as pd

# 定义文件夹路径  # English: Define folder path
river = 'Yukon'
input_folder = r"D:\UZH\2024\20240122 Nutrient and Organic Carbon references\3_river_mouth_DOC\DOC_update_20250203\Total_DOC_annual\\" + river
output_file = r"D:\UZH\2024\20240122 Nutrient and Organic Carbon references\3_river_mouth_DOC\DOC_update_20250203\Total_DOC_average\Total_DOC_annual_"+river+"_Parts.csv"

# 初始化空列表用于存储数据  # English: Initialize an empty list for storing data
total_doc_list = []
total_doc_uncertainty_list = []  # 新增用于存储 uncertainty 数据  # English: Added for storage

# 遍历文件夹内所有 CSV 文件  # English: Traverse all in the folder
for file in os.listdir(input_folder):
    if file.endswith(".csv"):
        file_path = os.path.join(input_folder, file)
        df = pd.read_csv(file_path)

        # 确保数据包含所需的列  # English: Make sure the data contains the required columns
        if set(['year', 'Total_DOC', 'Total_DOC_uncertainty']).issubset(df.columns):
            df['year'] = df['year'].astype(int)  # 确保年份是整数类型  # English: Make sure the year is an integer type
            total_doc_list.append(df[['year', 'Total_DOC']])
            total_doc_uncertainty_list.append(df[['year', 'Total_DOC_uncertainty']])  # 添加 uncertainty 数据  # English: Add to

        else:
            print(f"文件 {file} 缺少所需列，已跳过。")

# 合并所有数据  # English: Merge all data
total_doc_df = pd.concat(total_doc_list, ignore_index=True)
total_doc_uncertainty_df = pd.concat(total_doc_uncertainty_list, ignore_index=True)

# 按年份汇总 DOC 通量和 uncertainty 数据  # English: Summary by year
total_doc_df = total_doc_df.groupby('year', as_index=False).sum()
total_doc_uncertainty_df = total_doc_uncertainty_df.groupby('year', as_index=False).sum()

# 合并 total DOC 和 uncertainty 数据  # English: merge
final_df = pd.merge(total_doc_df, total_doc_uncertainty_df, on='year', how='inner')

# 重命名列  # English: Rename column
final_df.rename(columns={'Total_DOC': 'Total_DOC_Annual', 'Total_DOC_uncertainty': 'Total_DOC_Annual_Uncertainty'},
                inplace=True)

# 保存结果  # English: Save the results
final_df.to_csv(output_file, index=False)

print(f"汇总的 Total_DOC_Annual 和 Total_DOC_Annual_Uncertainty 结果已保存至 {output_file}")