# 将CDOM转换为DOC  # English: Will
# 同时添加不确定性及其不确定性传递  # English: Add uncertainty and its uncertainty transmission at the same time

import pandas as pd
import numpy as np
import xlsxwriter
import os
import math
import gc  # 引入垃圾回收模块  # English: Introducing garbage collection module

# 设置存放CSV文件的文件夹路径  # English: Set storage
csv_folder = r'D:\UZH\2024\20240122 Nutrient and Organic Carbon references\2_river_mouth_CDOM\CDOM\HLSS30'
# 设置存放转换后csv文件的文件夹路径  # English: Set storage after conversion
DOC_folder = r'D:\UZH\2024\20240122 Nutrient and Organic Carbon references\3_river_mouth_DOC\DOC_update_20250203\HLSS30'

# 如果存储XLSX文件的文件夹不存在，则创建  # English: If stored
if not os.path.exists(DOC_folder):
    os.makedirs(DOC_folder)

CDOM_DOC_uncertainty = 2.0919
# 指定要排序的列顺序  # English: Specify the order of columns to sort
desired_columns = ['date', 'COMID', 'CDOM', 'CDOM_uncertainty', 'DOC', 'DOC_uncertainty']
date_format = '%Y-%m-%d'

# 遍历CSV文件夹中的所有CSV文件  # English: Traversal
for filename in os.listdir(csv_folder):
    if filename.endswith(".csv"):  # 只处理CSV文件  # English: Process only
        csv_file_path = os.path.join(csv_folder, filename)

        print(f'文件 {csv_file_path} 正在计算')

        # 读取CSV文件  # English: Read
        df = pd.read_csv(csv_file_path)

        # 如果 'system:index' 和 '.geo' 列存在，删除它们  # English: if
        df = df.drop(columns=['system:index', '.geo'], errors='ignore')

        # 转换 'date' 列为日期格式（如果存在）  # English: Convert
        if 'date' in df.columns:
            df['date'] = pd.to_datetime(df['date'], errors='coerce').dt.strftime(date_format)

        # 仅计算非空 CDOM 的 DOC 值并添加为新列  # English: Calculate only non-null
        if 'CDOM' in df.columns:
            df = df.dropna(subset=['CDOM'])
            df['DOC'] = 0.60082 * df['CDOM'] + 1.77043
            df['DOC_uncertainty'] = np.sqrt(df['CDOM_uncertainty'] ** 2 + CDOM_DOC_uncertainty ** 2)

            # 保存 CSV  # English: save
            DOC_output_file = os.path.join(DOC_folder, filename.replace('.csv', '_DOC.csv'))
            df.to_csv(DOC_output_file, index=False)

        gc.collect()  # 释放内存  # English: Free memory
        print(f'已保存: {csv_file_path}')

    print("批量处理完成！")
