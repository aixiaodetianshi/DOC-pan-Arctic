# 遍历文件夹 D:\UZH\2025\NPP\pan_Arctic_soil_temperature_level_2_multi_catchments 中所有 .csv 文件；
#
# 每隔 903 行提取一个流域（catchment）的数据；
#
# 对每个流域提取 date 和 soil_temperature_level_2 两列；
#
# 将温度从开尔文（K）转换为摄氏度（°C）；
#
# 使用该流域的 gid 作为文件名；
#
# 将结果保存为 .csv 文件到 D:\UZH\2025\NPP\pan_Arctic_soil_temperature_level_2_multi_catchments\catchments 目录下。

import os
import pandas as pd

# 输入输出路径
input_folder = r'D:\UZH\2025\NPP\pan_Arctic_total_precipitation_sum\batch'
output_folder = r'D:\UZH\2025\NPP\pan_Arctic_total_precipitation_sum'

# 创建输出文件夹（如不存在）
os.makedirs(output_folder, exist_ok=True)

# 每个 catchment 的记录数（固定为903行）
records_per_catchment = 903

# 遍历输入文件夹内所有 CSV 文件
for filename in os.listdir(input_folder):
    if filename.lower().endswith('.csv'):
        filepath = os.path.join(input_folder, filename)
        print(f'Processing file: {filename}')

        # 读取文件，保留列名
        df = pd.read_csv(filepath)

        # 计算有多少个 catchment 块
        total_rows = len(df)
        num_catchments = total_rows // records_per_catchment

        for i in range(num_catchments):
            start = i * records_per_catchment
            end = start + records_per_catchment

            sub_df = df.iloc[start:end]

            # 提取 date 和 total_precipitation_sum 列
            catchment_df = sub_df[['date', 'total_precipitation_sum']].copy()

            # 获取 gid 作为文件名
            gid = sub_df['gid'].iloc[0]
            output_filename = f'{gid}_total_precipitation_sum.csv'
            output_path = os.path.join(output_folder, output_filename)

            # 保存到新文件
            catchment_df.to_csv(output_path, index=False)