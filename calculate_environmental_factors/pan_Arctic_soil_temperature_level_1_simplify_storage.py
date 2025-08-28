# pan_Arctic_soil_temperature_level_1数据存储简化处理  # English: Simplified data storage processing
# 
# 对每个流域只存储 date 和 soil_temperature_level_1 两列；  # English: Only store for each basin
# 
# 将温度从开尔文（K）转换为摄氏度（°C）；  # English: Turn the temperature from Kelvin

import os
import pandas as pd

# 输入输出路径  # English: Input and output path
input_folder = r'D:\special_deal'
output_folder = r'D:\UZH\2025\NPP\pan_Arctic_total_precipitation_sum'

# 创建输出文件夹（如不存在）  # English: Create an output folder
os.makedirs(output_folder, exist_ok=True)

# 遍历输入文件夹内所有 CSV 文件  # English: Traverse all input folders
for filename in os.listdir(input_folder):
    if filename.lower().endswith('.csv'):
        filepath = os.path.join(input_folder, filename)
        print(f'Processing file: {filename}')

        # 读取文件，保留列名  # English: Read the file
        df = pd.read_csv(filepath)

        # 只保留 date 和 soil_temperature_level_1 两列  # English: Only retain
        if 'date' in df.columns and 'total_precipitation_sum' in df.columns:
            df = df[['date', 'total_precipitation_sum']].copy()

            # 温度单位转换：K → °C  # English: Temperature unit conversion
            # df['temperature_2m'] = df['temperature_2m'] - 273.15
            # 
            df['total_precipitation_sum'] = df['total_precipitation_sum']

            # 保存到输出目录  # English: Save to output directory
            output_path = os.path.join(output_folder, filename)
            df.to_csv(output_path, index=False)
        else:
            print(f"Skipped file (missing columns): {filename}")