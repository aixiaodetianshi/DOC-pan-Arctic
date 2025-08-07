# sort the date
# each river endpoints has one file

import pandas as pd
import os

# 输入文件夹路径
input_folder = r'D:\UZH\2024\20240122 Nutrient and Organic Carbon references\3_river_mouth_DOC\DOC_update_20250203\Combination_single_river'
output_folder = r'D:\UZH\2024\20240122 Nutrient and Organic Carbon references\3_river_mouth_DOC\DOC_update_20250203\Combination_single_river_sort_date'

# 确保输出文件夹存在
os.makedirs(output_folder, exist_ok=True)

# 遍历文件夹中的所有文件
for filename in os.listdir(input_folder):
    in_file_path = os.path.join(input_folder, filename)
    out_file_path = os.path.join(output_folder, filename)

    print(f'文件 {in_file_path} 正在准备')

    # **检查文件是否为空**
    if os.stat(in_file_path).st_size == 0:  # 文件大小为0字节
        print(f"文件 {filename} 是空的，创建空文件。")
        open(out_file_path, 'w').close()  # 直接创建一个同名的空文件
        continue  # 跳过该文件，继续处理下一个

    try:
        # 读取 CSV 文件
        df_DOC = pd.read_csv(in_file_path)

        # 如果 DataFrame 为空，创建空文件
        if df_DOC.empty:
            print(f"文件 {filename} 没有数据记录，创建空文件。")
            open(out_file_path, 'w').close()
            continue  # 跳过该文件，继续处理下一个

        # 确保 'date' 列为日期格式
        df_DOC['date'] = pd.to_datetime(df_DOC['date'], errors='coerce')

        # 按照 'date' 列进行排序
        df_sort_date = df_DOC.sort_values(by='date').reset_index(drop=True)

        # 保存排序后的文件
        df_sort_date.to_csv(out_file_path, index=False)
        print(f"文件已创建: {out_file_path}")

    except pd.errors.EmptyDataError:
        print(f"文件 {filename} 解析失败（可能是空的），创建空文件。")
        open(out_file_path, 'w').close()  # 直接创建一个同名的空文件
        continue  # 跳过该文件

print("所有文件已成功生成！")
