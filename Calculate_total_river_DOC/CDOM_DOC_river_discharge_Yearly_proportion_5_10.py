# 1984-2018年期间每一条河流河流入海口在一年之内5-10月总的河流流量占全年流量的比例  # English: During the year, each river flows into the sea estuary within one year

import pandas as pd
import os

# 输入文件夹路径（源数据）  # English: Enter the folder path
input_folder_path = r"D:\UZH\2024\20240122 Nutrient and Organic Carbon references\discharge\river_discharge\Monthly\Monthly_Mackenzie"

# 输出文件夹路径（计算后数据）  # English: Output folder path
output_folder_path = r"D:\UZH\2024\20240122 Nutrient and Organic Carbon references\discharge\river_discharge\Yearly_Proportion_5_10\Mackenzie"

for file_name in os.listdir(input_folder_path):
    if file_name.endswith('.xlsx'):  # 只处理XLSX文件  # English: Process only
        # 构造完整的文件路径  # English: Construct the complete file path
        input_file_path = os.path.join(input_folder_path, file_name)
        output_file_path = os.path.join(output_folder_path, file_name)

        # 读取文件  # English: Read the file
        df = pd.read_excel(input_file_path, usecols=['year_month', 'Total_discharge'])

        # 确保 'year_month' 列是 datetime 格式  # English: make sure
        df['year_month'] = pd.to_datetime(df['year_month'], format='%Y-%m', errors='coerce')

        # 过滤掉无法解析的日期  # English: Filter out unresolved dates
        df = df.dropna(subset=['year_month'])

        # 提取年份和月份  # English: Extract year and month
        df['year'] = df['year_month'].dt.year
        df['month'] = df['year_month'].dt.month

        # 计算每年 5-10 月的总流量  # English: Calculate annually
        seasonal_discharge = df[df['month'].between(5, 10)].groupby('year')['Total_discharge'].sum().reset_index()
        seasonal_discharge.rename(columns={'Total_discharge': 'May-Oct_Discharge'}, inplace=True)

        # 计算全年总流量  # English: Calculate the total traffic for the whole year
        annual_discharge = df.groupby('year')['Total_discharge'].sum().reset_index()
        annual_discharge.rename(columns={'Total_discharge': 'Annual_Discharge'}, inplace=True)

        # 合并数据  # English: Merge data
        merged_df = pd.merge(annual_discharge, seasonal_discharge, on='year', how='left').fillna(0)

        # 计算 5-10 月流量占全年流量的比例  # English: calculate
        merged_df['Proportion_5_10'] = merged_df['May-Oct_Discharge'] / merged_df['Annual_Discharge']

        # 保存计算结果为 XLSX 文件  # English: Save the calculation result as
        merged_df.to_excel(output_file_path, index=False)
        print(f"Processed: {file_name}")

print("Processing complete. Yearly Proportion 5-10 Discharge files saved in 'Yearly_Proportion_5_10\Ob' folder.")
