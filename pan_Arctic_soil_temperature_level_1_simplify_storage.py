# pan_Arctic_soil_temperature_level_1数据存储简化处理
#
# 对每个流域只存储 date 和 soil_temperature_level_1 两列；
#
# 将温度从开尔文（K）转换为摄氏度（°C）；

import os
import pandas as pd

# 输入输出路径
input_folder = r'D:\special_deal'
output_folder = r'D:\UZH\2025\NPP\pan_Arctic_total_precipitation_sum'

# 创建输出文件夹（如不存在）
os.makedirs(output_folder, exist_ok=True)

# 遍历输入文件夹内所有 CSV 文件
for filename in os.listdir(input_folder):
    if filename.lower().endswith('.csv'):
        filepath = os.path.join(input_folder, filename)
        print(f'Processing file: {filename}')

        # 读取文件，保留列名
        df = pd.read_csv(filepath)

        # 只保留 date 和 soil_temperature_level_1 两列
        if 'date' in df.columns and 'total_precipitation_sum' in df.columns:
            df = df[['date', 'total_precipitation_sum']].copy()

            # 温度单位转换：K → °C
            # df['temperature_2m'] = df['temperature_2m'] - 273.15
            #
            df['total_precipitation_sum'] = df['total_precipitation_sum']

            # 保存到输出目录
            output_path = os.path.join(output_folder, filename)
            df.to_csv(output_path, index=False)
        else:
            print(f"Skipped file (missing columns): {filename}")