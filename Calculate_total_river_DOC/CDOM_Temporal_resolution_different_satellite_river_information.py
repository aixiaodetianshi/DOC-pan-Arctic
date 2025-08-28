# 包含河流COMID日期数据的Excel文件，并计算以下指标：  # English: Including rivers
#
# 共计天数 (total days): 文件中所有唯一日期的总数。  # English: Total days
# 总年份数 (total year): 从最早年份到最晚年份的跨度。  # English: Total number of years
# 开始年份 (start year): 数据记录的最早年份。  # English: Start year
# 结束年份 (end year): 数据记录的最晚年份。  # English: End year
# 每年平均天数 (average days): 数据记录总天数除以年份跨度。  # English: Average number of days per year

import pandas as pd
import os

# 输入文件夹路径  # English: Enter the folder path
input_folder = r'D:\UZH\2024\20240122 Nutrient and Organic Carbon references\CDOM\temporal_resolution\HLSS30_COMID'
# 输出文件路径  # English: Output file path
output_folder = r'D:\UZH\2024\20240122 Nutrient and Organic Carbon references\CDOM\temporal_resolution\temporal_resolution'
output_file = os.path.join(output_folder, 'HLSS30.xlsx')

# 如果输出文件夹不存在，则创建  # English: If the output folder does not exist
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# 初始化结果列表  # English: Initialization result list
results = []

# 遍历文件夹中的每个文件  # English: Iterate through each file in the folder
for filename in os.listdir(input_folder):
    if filename.endswith('.xlsx'):
        file_path = os.path.join(input_folder, filename)

        # 读取 Excel 文件  # English: Read
        try:
            df = pd.read_excel(file_path)

            # 检查日期列是否存在  # English: Check if the date column exists
            if 'date' not in df.columns:
                print(f"文件 {filename} 缺少 'date' 列，跳过。")
                continue

            # 确保日期列格式正确  # English: Make sure the date column is formatted correctly
            df['date'] = pd.to_datetime(df['date'])

            # 计算所需统计数据  # English: Calculate required statistics
            total_days = df['date'].nunique()
            start_year = df['date'].min().year
            end_year = df['date'].max().year
            total_years = end_year - start_year + 1
            average_days = total_days / total_years if total_years > 0 else 0

            # 提取河流编号（文件名去掉扩展名部分）  # English: Extract river number
            comid = int(os.path.splitext(filename)[0])

            # 添加结果到列表  # English: Add results to list
            results.append({
                'COMID': comid,
                'total_days': total_days,
                'total_years': total_years,
                'start_year': start_year,
                'end_year': end_year,
                'average_days': average_days
            })
        except Exception as e:
            print(f"处理文件 {filename} 时出错: {e}")

# 将结果转换为 DataFrame 并保存到 Excel 文件  # English: Convert the result to
results_df = pd.DataFrame(results,
                          columns=['COMID', 'total_days', 'total_years', 'start_year', 'end_year', 'average_days'])

try:
    results_df.to_excel(output_file, index=False)
    print(f"结果已成功保存到 {output_file}")
except Exception as e:
    print(f"保存结果文件时出错: {e}")
