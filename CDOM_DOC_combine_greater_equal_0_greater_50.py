# combine the Landsat 5/7, HLSL30 (Landsat 8/9) and HLSS30 (Sentinel-2) datasets
# each river endpoints has one file

import pandas as pd
import os

# 设置输入和输出文件夹路径
in_folder_greater_50 = r'D:\UZH\2024\20240122 Nutrient and Organic Carbon references\DOC\DOC_greater_50\Combination_sort_date'
in_folder_greater_equal_0 = r'D:\UZH\2024\20240122 Nutrient and Organic Carbon references\DOC\DOC_greater_equal_0\Combination_sort_date'
output_folder = r'D:\UZH\2024\20240122 Nutrient and Organic Carbon references\DOC\combination_sort_date'

# 创建输出文件夹（如果不存在）
os.makedirs(output_folder, exist_ok=True)

# 遍历两个输入文件夹中所有的文件名
all_filenames = set(os.listdir(in_folder_greater_50)) | set(os.listdir(in_folder_greater_equal_0))

for filename in all_filenames:
    # 初始化空DataFrame
    combined_df = pd.DataFrame()

    # 读取第一个文件夹中的数据
    in_file_greater_50 = os.path.join(in_folder_greater_50, filename)
    if os.path.isfile(in_file_greater_50):
        df_greater_50 = pd.read_excel(in_file_greater_50)
        combined_df = pd.concat([combined_df, df_greater_50], ignore_index=True)
    else:
        print(f'文件 {filename} 不在文件夹 {in_folder_greater_50} 中')

    # 读取第二个文件夹中的数据
    in_file_greater_equal_0 = os.path.join(in_folder_greater_equal_0, filename)
    if os.path.isfile(in_file_greater_equal_0):
        df_greater_equal_0 = pd.read_excel(in_file_greater_equal_0)
        combined_df = pd.concat([combined_df, df_greater_equal_0], ignore_index=True)
    else:
        print(f'文件 {filename} 不在文件夹 {in_folder_greater_equal_0} 中')

    # 如果DataFrame不为空，按时间排序并保存
    if not combined_df.empty:
        if 'date' in combined_df.columns:
            combined_df['date'] = pd.to_datetime(combined_df['date'], errors='coerce')
            combined_df = combined_df.sort_values(by='date').reset_index(drop=True)
        else:
            print(f"文件 {filename} 缺少 'date' 列，跳过排序。")

        # 输出文件路径
        out_file_path = os.path.join(output_folder, filename)
        combined_df.to_excel(out_file_path, index=False)
        print(f"文件已创建: {out_file_path}")
    else:
        print(f"文件 {filename} 数据为空，未生成输出。")

print("所有文件已成功处理！")
