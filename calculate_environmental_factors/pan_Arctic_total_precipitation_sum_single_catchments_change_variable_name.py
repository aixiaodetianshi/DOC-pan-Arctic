
import os
import pandas as pd

# 输入和输出路径  # English: Input and output paths
input_folder = r'D:\UZH\2025\NPP\pan_Arctic_total_precipitation_sum'
output_folder = os.path.join(input_folder, 'batch1')

# 创建输出目录  # English: Create an output directory
os.makedirs(output_folder, exist_ok=True)

# 遍历文件夹中的所有 CSV 文件  # English: Iterate through all the folders
for filename in os.listdir(input_folder):
    if filename.lower().endswith('.csv'):
        filepath = os.path.join(input_folder, filename)
        print(f'Processing file: {filename}')

        # 读取 CSV 文件  # English: Read
        df = pd.read_csv(filepath)

        # 修改列名（只修改 temperature_2m）  # English: Modify the column name
        df.rename(columns={'temperature_2m': 'total_precipitation_sum'}, inplace=True)

        # 保存到输出文件夹，文件名保持不变  # English: Save to output folder
        output_path = os.path.join(output_folder, filename)
        df.to_csv(output_path, index=False)
