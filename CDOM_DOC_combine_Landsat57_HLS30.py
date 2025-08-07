# combine the Landsat 5/7, HLSL30 (Landsat 8/9) and HLSS30 (Sentinel-2) datasets
# each river endpoints has one file

import pandas as pd
import os

# 设置存放转换后XLSX文件的文件夹路径
in_folder_Landsat5 = r'D:\UZH\2024\20240122 Nutrient and Organic Carbon references\3_river_mouth_DOC\DOC_update_20250203\Landsat5_single_river'
in_folder_Landsat7 = r'D:\UZH\2024\20240122 Nutrient and Organic Carbon references\3_river_mouth_DOC\DOC_update_20250203\Landsat7_single_river'
in_folder_HLSL30 = r'D:\UZH\2024\20240122 Nutrient and Organic Carbon references\3_river_mouth_DOC\DOC_update_20250203\HLSL30_single_river'
in_folder_HLSS30 = r'D:\UZH\2024\20240122 Nutrient and Organic Carbon references\3_river_mouth_DOC\DOC_update_20250203\HLSS30_single_river'
# 输出文件夹路径
output_folder = r'D:\UZH\2024\20240122 Nutrient and Organic Carbon references\3_river_mouth_DOC\DOC_update_20250203\Combination_single_river'

# 遍历文件夹中的所有文件
for filename in os.listdir(output_folder):
    out_file_path = os.path.join(output_folder, filename)
    print(f'文件 {out_file_path} 正在准备')

    # 初始化用于合并的DataFrame列表
    df_Landsat5 = []
    df_Landsat7 = []
    df_HLSL30 = []
    df_HLSS30 = []

    # for Landsat 5
    in_folder_Landsat5_filename = os.path.join(in_folder_Landsat5, filename)
    # 检查文件是否存在
    if os.path.isfile(in_folder_Landsat5_filename):
        # 文件存在，打开并读取数据
        # 读取Excel文件
        df_Landsat5 = pd.read_csv(in_folder_Landsat5_filename)
    else:
        # 文件不存在，打印提示信息
        df_Landsat5 = pd.DataFrame()
        print(f'文件 {filename} 不在文件夹 {in_folder_Landsat5} 中')

    # for Landsat 7
    in_folder_Landsat7_filename = os.path.join(in_folder_Landsat7, filename)
    # 检查文件是否存在
    if os.path.isfile(in_folder_Landsat7_filename):
        # 文件存在，打开并读取数据
        # 读取Excel文件
        df_Landsat7 = pd.read_csv(in_folder_Landsat7_filename)
        #df_Landsat7 = df_Landsat7.drop(columns=['date', 'CDOM', 'DOC'], errors='ignore')
    else:
        # 文件不存在，打印提示信息
        df_Landsat7 = pd.DataFrame()
        print(f'文件 {filename} 不在文件夹 {in_folder_Landsat7} 中')

    # for HLSL30
    in_folder_HLSL30_filename = os.path.join(in_folder_HLSL30, filename)
    # 检查文件是否存在
    if os.path.isfile(in_folder_HLSL30_filename):
        # 文件存在，打开并读取数据
        # 读取Excel文件
        df_HLSL30 = pd.read_csv(in_folder_HLSL30_filename)
        #df_HLSL30 = df_HLSL30.drop(columns=['date', 'CDOM', 'DOC'], errors='ignore')
    else:
        # 文件不存在，打印提示信息
        df_HLSL30 = pd.DataFrame()
        print(f'文件 {filename} 不在文件夹 {in_folder_HLSL30} 中')

    # for HLSS30
    in_folder_HLSS30_filename = os.path.join(in_folder_HLSS30, filename)
    # 检查文件是否存在
    if os.path.isfile(in_folder_HLSS30_filename):
        # 文件存在，打开并读取数据
        # 读取Excel文件
        df_HLSS30 = pd.read_csv(in_folder_HLSS30_filename)
        #df_HLSS30 = df_HLSS30.drop(columns=['date', 'CDOM', 'DOC'], errors='ignore')
    else:
        # 文件不存在，打印提示信息
        df_HLSS30 = pd.DataFrame()
        print(f'文件 {filename} 不在文件夹 {in_folder_HLSS30} 中')

    # 合并所有DataFrame
    print(type(df_Landsat5), type(df_Landsat7), type(df_HLSL30), type(df_HLSS30))
    combined_df = pd.concat([df_Landsat5, df_Landsat7, df_HLSL30, df_HLSS30], ignore_index=True)

    # 将合并后的数据写入输出文件
    combined_df.to_csv(out_file_path, index=False)
    print(f"文件已创建: {out_file_path}")

print("所有文件已成功生成！")