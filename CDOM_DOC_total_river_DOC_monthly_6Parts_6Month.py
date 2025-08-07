import pandas as pd
import os

# 设置河流名称和输入路径
river = "All"
input_folder_path = rf"D:\UZH\2024\20240122 Nutrient and Organic Carbon references\3_river_mouth_DOC\DOC_update_20250203\Total_DOC_monthly\All_month"
input_file_path = os.path.join(input_folder_path, f"Total_monthly_DOC_{river}_Parts.csv")

# 读取CSV文件，提取需要的列
df = pd.read_csv(input_file_path, usecols=['year_month', 'Total_DOC', 'Total_DOC_uncertainty'])

# 将 year_month 转换为 datetime 格式
# df['year_month'] = pd.to_datetime(df['year_month'], format='%Y-%m')
df['year_month'] = pd.to_datetime(df['year_month'], errors='coerce')

# 只提取每年5月的数据（即月份为5）
df5 = df[df['year_month'].dt.month == 5]
output_filename5 = os.path.join(input_folder_path, f"Total_monthly_DOC_{river}_Parts_5.csv")
df5.to_csv(output_filename5, index=False)

# 只提取每年6月的数据（即月份为6）
df6 = df[df['year_month'].dt.month == 6]
output_filename6 = os.path.join(input_folder_path, f"Total_monthly_DOC_{river}_Parts_6.csv")
df6.to_csv(output_filename6, index=False)

# 只提取每年7月的数据（即月份为7）
df7 = df[df['year_month'].dt.month == 7]
output_filename7 = os.path.join(input_folder_path, f"Total_monthly_DOC_{river}_Parts_7.csv")
df7.to_csv(output_filename7, index=False)

# 只提取每年8月的数据（即月份为8）
df8 = df[df['year_month'].dt.month == 8]
output_filename8 = os.path.join(input_folder_path, f"Total_monthly_DOC_{river}_Parts_8.csv")
df8.to_csv(output_filename8, index=False)

# 只提取每年9月的数据（即月份为5）
df9 = df[df['year_month'].dt.month == 9]
output_filename9 = os.path.join(input_folder_path, f"Total_monthly_DOC_{river}_Parts_9.csv")
df9.to_csv(output_filename9, index=False)

# 只提取每年10月的数据（即月份为6）
df10 = df[df['year_month'].dt.month == 10]
output_filename10 = os.path.join(input_folder_path, f"Total_monthly_DOC_{river}_Parts_10.csv")
df10.to_csv(output_filename10, index=False)