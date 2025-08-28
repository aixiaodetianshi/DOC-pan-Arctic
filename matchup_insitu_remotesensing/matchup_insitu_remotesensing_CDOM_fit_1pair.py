import pandas as pd
import os


river = 'Yukon'
satellite = 'HLSL30'


# Load the data from Excel
input_path = r'D:\UZH\2024\20240122 Nutrient and Organic Carbon references\Arctic\ArcticGRO\CDOM_DOC_in_situ\May_October_CDOM_DOC\matchup_insitu_remotesensing_fit_CDOM_HLSL30_xlsx\SPP_River_' + river + '_surround_' + satellite + '_10Points_insitu_DOC_CDOM.xlsx'
data = pd.read_excel(input_path)

# Extract file name for saving the figure and coefficients later
file_name = os.path.basename(input_path).replace('.xlsx', '')

# 计算CDOM与rs_CDOM的偏差绝对值  # English: calculate
data['abs_diff'] = (data['CDOM'] - data['rs_CDOM']).abs()

# 按insitu_date分组，并找到每组中偏差最小的一行  # English: according to
selected_rows = data.loc[data.groupby('insitu_date')['abs_diff'].idxmin()]

# 去掉偏差绝对值列  # English: Remove the deviation absolute value column
selected_rows.drop(columns=['abs_diff'], inplace=True)

# Save the updated DataFrame to a new Excel file
output_folder  = r'D:\UZH\2024\20240122 Nutrient and Organic Carbon references\Arctic\ArcticGRO\CDOM_DOC_in_situ\May_October_CDOM_DOC\matchup_insitu_remotesensing_fit_CDOM_HLSL30_xlsx\1_1_Pairs'
output_excel_file = os.path.join(output_folder, f"{file_name}.xlsx")
selected_rows.to_excel(output_excel_file, index=False)