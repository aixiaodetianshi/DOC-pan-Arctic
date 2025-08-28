# 将不同卫星数据separate为单独的河流  # English: Convert different satellite data

import pandas as pd
import os

# 设置存放转换后CSV文件的文件夹路径  # English: Set storage after conversion
in_folder = r'D:\UZH\2024\20240122 Nutrient and Organic Carbon references\DOC\DOC_update_20250203\Landsat7'
# 输出文件夹路径  # English: Output folder path
output_folder = r'D:\UZH\2024\20240122 Nutrient and Organic Carbon references\DOC\DOC_update_20250203\Landsat7_single_river'

# 如果输出文件夹不存在，则创建  # English: If the output folder does not exist
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# 检查数据是否包含必要的列  # English: Check if the data contains the necessary columns
required_columns = ['date', 'COMID', 'CDOM', 'DOC', 'CDOM_uncertainty', 'DOC_uncertainty']
date_format = '%Y-%m-%d'

# 遍历CSV文件夹中的所有CSV文件  # English: Traversal
for filename in os.listdir(in_folder):
    if filename.endswith(".csv"):
        in_file_path = os.path.join(in_folder, filename)

        print(f'文件 {in_file_path} 正在计算')

        # 读取csv文件  # English: Read
        df = pd.read_csv(in_file_path)

        # 检查是否包含所需列  # English: Check if the required column is included
        if not all(col in df.columns for col in required_columns):
            print(f"输入数据缺少必要的列，请检查文件结构: {filename}")
            continue

        # 将 COMID 转换为整数类型（忽略转换失败的情况）  # English: Will
        df['COMID'] = pd.to_numeric(df['COMID'], errors='coerce').fillna(0).astype(int)

        # 按河流 reach 编号（COMID）进行分组  # English: By river
        grouped = df.groupby('COMID')

        # 遍历每个COMID分组，将数据保存为单独的CSV文件  # English: Iterate through each
        for comid, group_data in grouped:
            output_file = os.path.join(output_folder, f'{comid}.csv')

            # 保存该 COMID 数据到 CSV 文件  # English: Save this
            group_data.to_csv(output_file, index=False, columns=['date', 'CDOM', 'CDOM_uncertainty', 'DOC', 'DOC_uncertainty'])
            print(f'文件 {output_file} 已成功保存。')

print("所有文件已成功生成！")
