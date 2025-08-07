# 合并 Total_DOC 和 Total_DOC_uncertainty
# 采用 groupby('year', as_index=False).agg(...) 方法，同时计算 Total_DOC 和 Total_DOC_uncertainty 的年度累积值。
# 确保 date 列转换为 datetime
# df['date'] = pd.to_datetime(df['date'])，以便正确提取年份。
# groupby 时不再使用 reset_index()
# 直接在 groupby 方法中使用 as_index=False，保证 year 仍然是一个列，而不是索引。
# 这样就能确保每个文件正确计算并输出年度 Total_DOC 和 Total_DOC_uncertainty 的总量。

import pandas as pd
import os

# 文件夹路径
river = "Yukon"
input_folder_path = r"D:\UZH\2024\20240122 Nutrient and Organic Carbon references\3_river_mouth_DOC\DOC_update_20250203\Total_DOC_monthly\\" + river
output_folder_path = r"D:\UZH\2024\20240122 Nutrient and Organic Carbon references\3_river_mouth_DOC\DOC_update_20250203\Total_DOC_annual\\" + river

# 确保输出文件夹存在
if not os.path.exists(output_folder_path):
    os.makedirs(output_folder_path)

# 处理每个DOC文件
for file_name in os.listdir(input_folder_path):
    if file_name.endswith('.csv'):
        # 文件路径
        input_file_path = os.path.join(input_folder_path, file_name)

        # 读取数据
        df = pd.read_csv(input_file_path)
        df.columns = ['year_month', 'Total_DOC', 'Total_DOC_uncertainty']  # 确保列名一致
        df['year_month'] = pd.to_datetime(df['year_month'])  # 将日期列转换为 datetime 格式
        df['year'] = df['year_month'].dt.year  # 提取年份列

        # 按年份计算累计DOC总量和不确定性总量
        annual_DOC_totals = df.groupby('year', as_index=False).agg(
            {'Total_DOC': 'sum', 'Total_DOC_uncertainty': 'sum'}
        )

        # 保存年度DOC总量到新文件
        output_file_path = os.path.join(output_folder_path, file_name)
        annual_DOC_totals.to_csv(output_file_path, index=False)

print("年度DOC总量计算完成，结果保存在 'Total_DOC_annual' 文件夹中。")
