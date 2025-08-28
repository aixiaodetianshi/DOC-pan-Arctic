# 将不同卫星数据separate为单独的河流  # English: Convert different satellite data
# 添加系统误差 system diff  # English: Add system error

import pandas as pd
import os
from glob import glob

satellite = "Landsat5"
river = "Yukon"
system_dif = -1.797083559

# 设置存放转换后CSV文件的文件夹路径  # English: Set storage after conversion
in_folder = r'D:\UZH\2024\20240122 Nutrient and Organic Carbon references\3_river_mouth_DOC\DOC_update_20250203\\' + satellite
# 输出文件夹路径  # English: Output folder path
output_folder = r'D:\UZH\2024\20240122 Nutrient and Organic Carbon references\3_river_mouth_DOC\DOC_update_20250203\\' + satellite + '_single_river'

# 查找文件  # English: Find files
files = glob(os.path.join(in_folder, f"{satellite}_{river}_CDOM*_DOC.csv"))

# 如果输出文件夹不存在，则创建  # English: If the output folder does not exist
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# 检查数据是否包含必要的列  # English: Check if the data contains the necessary columns
required_columns = ['date', 'COMID', 'CDOM', 'DOC', 'CDOM_uncertainty', 'DOC_uncertainty']
date_format = '%Y-%m-%d'

# 遍历CSV文件夹中的所有CSV文件  # English: Traversal
for filename in files:
    print(f'文件 {filename} 正在计算')
    df = pd.read_csv(filename)

    # 检查是否包含所需列  # English: Check if the required column is included
    if not all(col in df.columns for col in required_columns):
        print(f"输入数据缺少必要的列，请检查文件结构: {filename}")
        continue

    # 将 COMID 转换为整数类型（忽略转换失败的情况）  # English: Will
    df['COMID'] = pd.to_numeric(df['COMID'], errors='coerce').fillna(0).astype(int)
    df['DOC'] = df['DOC'] + system_dif
    df = df[(df["DOC"] >= 0)].copy()

    # 按河流 reach 编号（COMID）进行分组  # English: By river
    grouped = df.groupby('COMID')

    # 遍历每个COMID分组，将数据保存为单独的CSV文件  # English: Iterate through each
    for comid, group_data in grouped:
        output_file = os.path.join(output_folder, f'{comid}.csv')
        # 保存该 COMID 数据到 CSV 文件  # English: Save this
        group_data.to_csv(output_file, index=False, columns=['date', 'CDOM', 'CDOM_uncertainty', 'DOC', 'DOC_uncertainty'])
        print(f'文件 {output_file} 已成功保存。')

print("所有文件已成功生成！")
