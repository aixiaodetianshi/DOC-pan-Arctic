# read DOC from ArcticGRO water quality

import pandas as pd

# 定义文件路径  # English: Define file path
file1 = r'D:\UZH\2024\20240122 Nutrient and Organic Carbon references\Arctic\ArcticGRO\insitu_DOC\SPP_Ob_remotesensing_Landsat_DOC_filled.xlsx'
file2 = r'D:\UZH\2024\20240122 Nutrient and Organic Carbon references\Arctic\ArcticGRO\insitu_DOC\ArcticGRO_Ob_Discharge_DOC_insitu.xlsx'

# 读取第一个文件的RIVER, date, DOC数据  # English: Read the first file
df1 = pd.read_excel(file1, usecols=['Date', 'DOC'])

# 读取第二个文件的River, Date, DOC数据  # English: Read the second file
df2 = pd.read_excel(file2, usecols=['Date', 'DOC'])

# 重命名df2的列名，以便于后续匹配  # English: Rename
df2.rename(columns={'Date': 'Date', 'DOC': 'DOC_2'}, inplace=True)

# 确保日期格式一致  # English: Ensure that date formats are consistent
df1['Date'] = pd.to_datetime(df1['Date']).dt.date
df2['Date'] = pd.to_datetime(df2['Date']).dt.date

# 合并数据，基于RIVER和date进行匹配  # English: Merge data
merged_df = pd.merge(df1, df2, on=['Date'])

# 将合并后的数据写入新的Excel文件  # English: Write the merged data to a new one
output_file = r'D:\UZH\2024\20240122 Nutrient and Organic Carbon references\Arctic\ArcticGRO\insitu_DOC\matchup_insitu_LSTM_remotesensing_Ob_DOC.xlsx'
merged_df.to_excel(output_file, index=False)

print(f"匹配后的数据已成功保存到 {output_file} 中。")


