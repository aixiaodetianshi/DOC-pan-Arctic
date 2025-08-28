# 将HLSS30数据经过系统校准之后与HLSL30合并，  # English: Will
# 合并在一起之后，用于验证校准Landsat7卫星数据  # English: After the merge

import pandas as pd
import os

def Combine_HLSL30_HLSS30(folder, hlsl30_file, l7_file, DOC_dif, output_filename):
    # 读取两个文件  # English: Read two files
    df_hlsl30 = pd.read_csv(os.path.join(folder, hlsl30_file), parse_dates=['date'])
    df_l7 = pd.read_csv(os.path.join(folder, l7_file), parse_dates=['date'])

    # 应用系统差，校正 Landsat 7 的 DOC  # English: Poor application system
    df_l7['DOC'] = df_l7['DOC'] + DOC_dif

    # 只保留两个必要列  # English: Only two necessary columns are retained
    df_hlsl30 = df_hlsl30[['date', 'DOC']]
    df_l7 = df_l7[['date', 'DOC']]

    # 前后拼接数据  # English: Splicing data before and after
    df_combined = pd.concat([df_hlsl30, df_l7], ignore_index=True)

    # 按日期排序  # English: Sort by date
    df_combined = df_combined.sort_values(by='date').reset_index(drop=True)

    # 保存合并后的数据  # English: Save merged data
    output_path = os.path.join(folder, output_filename)
    df_combined.to_csv(output_path, index=False)
    print(f"合并完成，输出文件保存至：{output_path}")

    return df_combined


# ===== 1. 设置基础路径与文件名 =====  # English: Set the basic path and file name
base_dir = r'D:\UZH\2024\20240122 Nutrient and Organic Carbon references\1_Linear_Regression_DOC_CDOM\4_Cross_Validate_Landsat_5_Landsat7_HLSL30_HLSS30_DOC\Cross_validate_dataset'
hls30_file = 'Cross_validate_Combine_HLSL30_HLSS30_Yukon_DOC.csv'
l7_file = 'Cross_validate_Landsat7_Yukon_DOC.csv'
output_filename = 'Cross_validate_HLS30_L7_Yukon_DOC.csv'
DOC_dif = -1.36138232
df_merged = Combine_HLSL30_HLSS30(base_dir, hls30_file, l7_file, DOC_dif, output_filename)