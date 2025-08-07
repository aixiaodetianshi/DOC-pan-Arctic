# 读取数据：从 D:\UZH\2024\20240122 Nutrient and Organic Carbon references\discharge\river_discharge\Ob 目录下的每个 .csv 文件中
# 读取 time 和 discharge 列。
# 日期过滤：确保 time 列转换为 datetime 格式，
# 按年月分组：通过 df['date'].dt.to_period('M') 提取年月信息，将数据按年和月进行分组。
# 计算每月总 discharge 通量：使用 groupby 和 agg 方法计算每个月 Total discharge 总和。
# 保存结果：将每个河流（文件）处理后的结果保存到
# 新的文件夹 D:\UZH\2024\20240122 Nutrient and Organic Carbon references\discharge\river_discharge\Monthly_Ob 中，文件名与原文件相同。
# 输出文件：
# 每个文件包含两列：
#
# year_month：表示年月（格式为 YYYY-MM）。
# Total_discharge：每月的 discharge 通量总和。
# 执行后，每条河流的每月总 DOC 通量将存储为 .csv 文件，保存在指定的文件夹中。

import pandas as pd
import os

# 输入文件夹路径（源数据）
input_folder_path = r"D:\UZH\2024\20240122 Nutrient and Organic Carbon references\discharge\river_discharge\Mackenzie"

# 输出文件夹路径（计算后数据）
output_folder_path = r"D:\UZH\2024\20240122 Nutrient and Organic Carbon references\discharge\river_discharge\Monthly\Monthly_Mackenzie"

# 遍历所有xlsx文件
for file_name in os.listdir(input_folder_path):
    if file_name.endswith('.xlsx'):  # 只处理xlsx文件
        # 构造完整的文件路径
        input_file_path = os.path.join(input_folder_path, file_name)
        output_file_path = os.path.join(output_folder_path, file_name)

        # 读取CSV文件
        df = pd.read_excel(input_file_path, usecols=['time', 'discharge'])

        # 确保 'time' 列是 datetime 格式
        df['time'] = pd.to_datetime(df['time'], errors='coerce')

        # 过滤掉无法解析的日期
        df = df.dropna(subset=['time'])

        # 计算每日总流量 (m³/s * 86400s = m³/day)
        df['daily_discharge'] = df['discharge'] * 86400

        # 按年月分组并计算总DOC通量
        df['year_month'] = df['time'].dt.to_period('M')  # 获取年月
        monthly_total = df.groupby('year_month').agg(
            Total_discharge=('daily_discharge', 'sum')
        ).reset_index()

        # 保存计算结果为 CSV 文件
        monthly_total.to_excel(output_file_path, index=False)
        print(f"Processed: {file_name}")

print("Processing complete. Monthly Total DOC files saved in 'Total_DOC_monthly\\Ob' folder.")
