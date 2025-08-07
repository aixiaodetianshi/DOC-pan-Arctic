import pandas as pd
import os

# 文件夹路径
input_folder_path = r"D:\UZH\2024\20240122 Nutrient and Organic Carbon references\discharge\river_discharge"
output_folder_path = r"D:\UZH\2024\20240122 Nutrient and Organic Carbon references\discharge\Annual_river_discharge"

# 确保输出文件夹存在
if not os.path.exists(output_folder_path):
    os.makedirs(output_folder_path)

# 处理每个DOC文件
for file_name in os.listdir(input_folder_path):
    if file_name.endswith('.xlsx'):
        # 文件路径
        input_file_path = os.path.join(input_folder_path, file_name)

        # 读取数据
        df = pd.read_excel(input_file_path)
        df.columns = ['time', 'discharge']  # 确保列名一致
        df['time'] = pd.to_datetime(df['time'])  # 将日期列转换为datetime格式
        df['year'] = df['time'].dt.year  # 添加年份列

        # 按年份计算累计DOC总量
        annual_DOC_totals = df.groupby('year')['discharge'].sum().reset_index()
        annual_DOC_totals.columns = ['year', 'annual_discharge']  # 重命名列

        # 保存年度DOC总量到新文件
        output_file_path = os.path.join(output_folder_path, file_name)
        annual_DOC_totals.to_excel(output_file_path, index=False)

print("年度discharge总量计算完成，结果保存在 'Annual_discharge' 文件夹中。")
