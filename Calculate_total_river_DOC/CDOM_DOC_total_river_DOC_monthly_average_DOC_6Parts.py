# 实现每个大流域1984-2018年月度总DOC通量变化  # English: Implement every major river basin

import os
import pandas as pd

# 定义文件夹路径  # English: Define folder path
input_folder = r"D:\UZH\2024\20240122 Nutrient and Organic Carbon references\DOC\DOC_update_20250203\Total_DOC_monthly\six_rivers_parts"
output_folder = r"D:\UZH\2024\20240122 Nutrient and Organic Carbon references\DOC\DOC_update_20250203\Total_DOC_monthly"
output_file = os.path.join(output_folder, "Total_monthly_DOC_All_Parts.csv")

# 初始化用于存储汇总结果的 DataFrame  # English: Initialize the summary results
monthly_total = None

# 遍历文件夹内所有 CSV 文件  # English: Traverse all in the folder
for file_name in os.listdir(input_folder):
    if file_name.endswith(".csv"):
        file_path = os.path.join(input_folder, file_name)

        # 读取 CSV 文件  # English: Read
        df = pd.read_csv(file_path)

        # 确保列名一致并且包含所需列  # English: Make sure the column names are consistent and contain the required columns
        if 'year_month' in df.columns and 'Total_DOC' in df.columns and 'Total_DOC_uncertainty' in df.columns:

            # 按 year_month 汇总 Total_DOC 和 Total_DOC_uncertainty  # English: according to
            grouped = df.groupby('year_month')[['Total_DOC', 'Total_DOC_uncertainty']].sum().reset_index()

            # 检查 year_month 是否为 1984年5月至2018年10月，且每年5-10月6条记录  # English: examine
            grouped['year_month'] = pd.to_datetime(grouped['year_month'], format='%Y-%m')
            grouped = grouped[(grouped['year_month'].dt.month >= 5) & (grouped['year_month'].dt.month <= 10)]
            grouped['year_month'] = grouped['year_month'].dt.strftime('%Y-%m')

            # 如果 monthly_total 是空的，则初始化  # English: if
            if monthly_total is None:
                monthly_total = grouped
            else:
                # 按 year_month 合并并累加 Total_DOC 和 Total_DOC_uncertainty  # English: according to
                monthly_total = pd.merge(monthly_total, grouped, on='year_month', how='outer', suffixes=('', '_dup'))
                monthly_total['Total_DOC'] = monthly_total['Total_DOC'].fillna(0) + monthly_total[
                    'Total_DOC_dup'].fillna(0)
                monthly_total['Total_DOC_uncertainty'] = monthly_total['Total_DOC_uncertainty'].fillna(0) + \
                                                         monthly_total['Total_DOC_uncertainty_dup'].fillna(0)

                # 删除重复列  # English: Delete duplicate columns
                monthly_total = monthly_total[['year_month', 'Total_DOC', 'Total_DOC_uncertainty']]

# 按 year_month 排序  # English: according to
monthly_total.sort_values(by='year_month', inplace=True)

# 保存为 CSV 文件  # English: Save as
monthly_total.to_csv(output_file, index=False)

print(f"结果已保存到 {output_file}")
