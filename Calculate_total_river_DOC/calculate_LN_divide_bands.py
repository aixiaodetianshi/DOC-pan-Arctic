import os
import pandas as pd
import numpy as np

# 定义文件夹路径  # English: Define folder path
input_folder = r'D:\UZH\2024\20240122 Nutrient and Organic Carbon references\Arctic\ArcticGRO\CDOM_DOC_in_situ\May_October_CDOM_DOC'
output_folder = r'D:\UZH\2024\20240122 Nutrient and Organic Carbon references\Arctic\ArcticGRO\CDOM_DOC_in_situ\May_October_CDOM_DOC\remote_sensing_10points_bands_Ln_divide'

# 如果输出文件夹不存在，则创建它  # English: If the output folder does not exist
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# 遍历输入文件夹中的所有文件  # English: Iterate through all files in the input folder
for filename in os.listdir(input_folder):
    if filename.startswith("SPP") and filename.endswith(".xlsx"):  # 只处理符合条件的文件  # English: Process only files that meet the criteria
        # 构造输入文件的完整路径  # English: Construct the full path to the input file
        input_file_path = os.path.join(input_folder, filename)

        # 读取Excel文件  # English: Read
        df = pd.read_excel(input_file_path)

        # 确保文件中有至少4列，防止文件格式不符合预期  # English: Make sure there is at least one file
        if df.shape[1] >= 4:
            # 修改第二列、第三列和第四列的列名  # English: Modify the second column
            df.columns.values[1] = 'blue'
            df.columns.values[2] = 'green'
            df.columns.values[3] = 'red'

            # 检查是否有第五列，如果有则修改为 'NIR'  # English: Check if there is a fifth column
            if df.shape[1] > 4:
                df.columns.values[4] = 'NIR'

            # 剔除包含负数的行（只考虑blue, green, red, NIR列）  # English: Exclude rows containing negative numbers
            if 'NIR' in df.columns:
                df_filtered = df[(df['blue'] > 0) & (df['green'] > 0) & (df['red'] > 0) & (df['NIR'] > 0)]
            else:
                df_filtered = df[(df['blue'] > 0) & (df['green'] > 0) & (df['red'] > 0)]

            # 按照日期列升序排序  # English: Sort by ascending order by date column
            df_filtered = df_filtered.sort_values(by='date')

            # 添加新列，计算自然对数和比值  # English: Add a new column
            df_filtered['ln(blue)'] = np.log(df_filtered['blue'])
            df_filtered['ln(green)'] = np.log(df_filtered['green'])
            df_filtered['ln(red)'] = np.log(df_filtered['red'])

            if 'NIR' in df_filtered.columns:
                df_filtered['ln(NIR)'] = np.log(df_filtered['NIR'])
                df_filtered['blue/NIR'] = df_filtered['blue'] / df_filtered['NIR']
                df_filtered['green/NIR'] = df_filtered['green'] / df_filtered['NIR']
                df_filtered['ln(green/NIR)'] = np.log(df_filtered['green/NIR'])
            else:
                df_filtered['ln(NIR)'] = np.nan
                df_filtered['blue/NIR'] = np.nan
                df_filtered['green/NIR'] = np.nan
                df_filtered['ln(green/NIR)'] = np.nan

            df_filtered['green/red'] = df_filtered['green'] / df_filtered['red']

            # 构造输出文件的完整路径  # English: Construct the full path to the output file
            output_file_path = os.path.join(output_folder, filename)

            # 将修改后的数据保存到新的Excel文件中  # English: Save the modified data to a new one
            df_filtered.to_excel(output_file_path, index=False)

            print(f'文件 {filename} 已成功处理并保存为 {output_file_path}')

print("所有符合条件的文件都已成功处理！")