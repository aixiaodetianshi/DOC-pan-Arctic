import os
import pandas as pd

# 定义文件夹路径  # English: Define folder path
folder_path = r'D:\UZH\2024\20240122 Nutrient and Organic Carbon references\Arctic\ArcticGRO\CDOM_DOC_in_situ\May_October_CDOM_DOC\remote_sensing_10points_bands_Ln_divide'

# 遍历文件夹中的每个文件  # English: Iterate through each file in the folder
for filename in os.listdir(folder_path):
    if filename.endswith(".xlsx"):  # 只处理xlsx文件  # English: Process only
        # 构造文件的完整路径  # English: The complete path to the construct file
        file_path = os.path.join(folder_path, filename)

        # 读取Excel文件  # English: Read
        df = pd.read_excel(file_path)

        # 获取数据记录条数（去掉表头的行数）  # English: Get the number of data records
        row_count = len(df)

        # 输出文件名称和记录条数  # English: Output file name and record number
        print(f'文件: {filename}, 数据记录条数: {row_count}')
