# 输入文件夹路径： 程序遍历四个文件夹（Landsat5_COMID、Landsat7_COMID、HLSL30_COMID、HLSS30_COMID）中的文件。  # English: Enter the folder path
#
# 查找相同文件名： 检查四个文件夹中共有的文件名。  # English: Find the same file name
#
# 合并数据：  # English: Merge data
#
# 读取相同文件名的所有文件。  # English: Read all files with the same file name
# 将文件中的 date 列数据合并。  # English: Put the file in the
# 使用 pandas 对日期进行排序，并确保数据完整性。  # English: use
# 保存结果： 将排序后的结果保存到目标文件夹 Combined_COMID，文件名保持不变，格式为 .xlsx。  # English: Save the results
#
# 执行结果： 程序执行完毕后，所有合并文件将存储在目标文件夹中。  # English: Execution results

import os
import pandas as pd

# 定义文件夹路径  # English: Define folder path
input_discharge_folder = r'D:\UZH\2024\20240122 Nutrient and Organic Carbon references\discharge\river_discharge\Yukon'
output_folder = r'D:\UZH\2024\20240122 Nutrient and Organic Carbon references\CDOM\temporal_resolution\Combined_COMID\Yukon'
input_cdom_folders = [
    r'D:\UZH\2024\20240122 Nutrient and Organic Carbon references\CDOM\temporal_resolution\Landsat5_COMID',
    r'D:\UZH\2024\20240122 Nutrient and Organic Carbon references\CDOM\temporal_resolution\Landsat7_COMID',
    r'D:\UZH\2024\20240122 Nutrient and Organic Carbon references\CDOM\temporal_resolution\HLSL30_COMID',
    r'D:\UZH\2024\20240122 Nutrient and Organic Carbon references\CDOM\temporal_resolution\HLSS30_COMID'
]

# 创建输出文件夹  # English: Create an output folder
os.makedirs(output_folder, exist_ok=True)

# 获取 discharge 文件夹中的文件名  # English: Get
file_names = [f for f in os.listdir(input_discharge_folder) if f.endswith('.xlsx')]

# 在输出文件夹中创建空文件  # English: Create an empty file in the output folder
for file_name in file_names:
    output_path = os.path.join(output_folder, file_name)
    if not os.path.exists(output_path):
        # 创建空的 Excel 文件  # English: Create an empty
        pd.DataFrame().to_excel(output_path, index=False)

# 处理文件名匹配  # English: Process file name matching
for file_name in file_names:
    combined_data = []

    for folder in input_cdom_folders:
        file_path = os.path.join(folder, file_name)
        if os.path.exists(file_path):
            # 读取 Excel 文件中的 date 列  # English: Read
            df = pd.read_excel(file_path, usecols=['date'])
            combined_data.append(df)

    if combined_data:
        # 合并所有数据并排序  # English: Merge all data and sort
        combined_df = pd.concat(combined_data)
        combined_df['date'] = pd.to_datetime(combined_df['date'], errors='coerce')  # 确保日期格式正确  # English: Make sure the date format is correct
        combined_df = combined_df.dropna(subset=['date'])  # 删除无效日期  # English: Delete invalid date
        combined_df = combined_df.sort_values(by='date').reset_index(drop=True)

        # 保存到输出文件夹  # English: Save to output folder
        output_path = os.path.join(output_folder, file_name)
        combined_df.to_excel(output_path, index=False)

print("文件处理完成，结果保存在:", output_folder)
