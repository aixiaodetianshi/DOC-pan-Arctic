# 遍历文件夹 D:\UZH\2025\NPP\pan_Arctic_soil_temperature_level_2_multi_catchments 中所有 .csv 文件；  # English: Traverse folders
# 
# 每隔 903 行提取一个流域（catchment）的数据；  # English: Every other
# 
# 对每个流域提取 date 和 soil_temperature_level_2 两列；  # English: Extract each basin
# 
# 将温度从开尔文（K）转换为摄氏度（°C）；  # English: Turn the temperature from Kelvin
# 
# 使用该流域的 gid 作为文件名；  # English: Using this basin
# 
# 将结果保存为 .csv 文件到 D:\UZH\2025\NPP\pan_Arctic_soil_temperature_level_2_multi_catchments\catchments 目录下。  # English: Save the result as

import os
import pandas as pd

# 输入输出路径  # English: Input and output path
input_folder = r'D:\UZH\2025\NPP\pan_Arctic_soil_temperature_level_1\batch'
output_folder = r'D:\UZH\2025\NPP\pan_Arctic_soil_temperature_level_1'

# 创建输出文件夹（如不存在）  # English: Create an output folder
os.makedirs(output_folder, exist_ok=True)

# 每个 catchment 的记录数（固定为903行）  # English: Each
records_per_catchment = 903

# 遍历输入文件夹内所有 CSV 文件  # English: Traverse all input folders
for filename in os.listdir(input_folder):
    if filename.lower().endswith('.csv'):
        filepath = os.path.join(input_folder, filename)
        print(f'Processing file: {filename}')

        # 读取文件，保留列名  # English: Read the file
        df = pd.read_csv(filepath)

        # 计算有多少个 catchment 块  # English: Calculate how many
        total_rows = len(df)
        num_catchments = total_rows // records_per_catchment

        for i in range(num_catchments):
            start = i * records_per_catchment
            end = start + records_per_catchment

            sub_df = df.iloc[start:end]

            # 提取 date 和 soil_temperature_level_2 列  # English: extract
            catchment_df = sub_df[['date', 'soil_temperature_level_1']].copy()

            # 转换单位：K -> °C  # English: Convert Units
            catchment_df['soil_temperature_level_1'] = catchment_df['soil_temperature_level_1'] - 273.15

            # 获取 gid 作为文件名  # English: Get
            gid = sub_df['gid'].iloc[0]
            output_filename = f'{gid}_soil_temperature_level_1.csv'
            output_path = os.path.join(output_folder, output_filename)

            # 保存到新文件  # English: Save to a new file
            catchment_df.to_csv(output_path, index=False)