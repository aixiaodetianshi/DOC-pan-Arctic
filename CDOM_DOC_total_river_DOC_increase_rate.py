# 计算思路
# 读取所有河流的 Total_DOC 数据
#
# 数据位于 "D:\UZH\2024\20240122 Nutrient and Organic Carbon references\DOC\DOC_update_20250203\Total_DOC_annual"
# 这个目录下有 6 个子文件夹，每个子文件夹里有多个 .csv 文件（以河流编号命名）
# 每个 .csv 文件包含 3 列：year, Total_DOC, Total_DOC_uncertainty
# 需要分析 1984-2018 年的 Total_DOC 变化
# 使用最小二乘法线性回归
#
# 设 year 为 X，Total_DOC 为 Y
# 用 线性回归公式 计算斜率（slope），即 年增长率
# 𝑌
# =
# 𝑎
# 𝑋
# +
# 𝑏
# Y=aX+b
# 其中 a（斜率）即为年增长率
# 保存结果
#
# 结果存放在 "D:\UZH\2024\20240122 Nutrient and Organic Carbon references\DOC\DOC_update_20250203\Total_DOC_average"
# 输出文件名为 "annual_increase_rate_Total_DOC.csv"
# 文件格式：COMID, Annual_Increase_Rate

import os
import pandas as pd
import numpy as np
from scipy.stats import linregress

# 定义输入和输出文件夹路径
input_folder = r"D:\UZH\2024\20240122 Nutrient and Organic Carbon references\3_river_mouth_DOC\DOC_update_20250203\Total_DOC_annual"
output_folder = r"D:\UZH\2024\20240122 Nutrient and Organic Carbon references\3_river_mouth_DOC\DOC_update_20250203\Total_DOC_increase_rate"
output_file = os.path.join(output_folder, "annual_increase_rate_Total_DOC.csv")

# 确保输出文件夹存在
os.makedirs(output_folder, exist_ok=True)

# 存储计算结果的列表
results = []

# 遍历6个子文件夹
for subfolder in os.listdir(input_folder):
    subfolder_path = os.path.join(input_folder, subfolder)

    if os.path.isdir(subfolder_path):  # 仅处理文件夹
        for file_name in os.listdir(subfolder_path):
            if file_name.endswith(".csv"):
                file_path = os.path.join(subfolder_path, file_name)

                # 读取 CSV 文件
                df = pd.read_csv(file_path)

                # 检查是否存在所需列
                if {'year', 'Total_DOC'}.issubset(df.columns):
                    # 选择 1984-2018 年的数据
                    df_filtered = df[(df['year'] >= 1984) & (df['year'] <= 2018)].dropna()

                    if len(df_filtered) >= 5:  # 至少5个数据点才能拟合
                        years = df_filtered['year'].values
                        doc_values = df_filtered['Total_DOC'].values

                        # 进行最小二乘法线性拟合
                        slope, intercept, r_value, p_value, std_err = linregress(years, doc_values)

                        # 获取河流编号（文件名去掉扩展名）
                        river_id = os.path.splitext(file_name)[0]

                        # 添加到结果列表
                        results.append({
                            'COMID': river_id,
                            'Annual_Increase_Rate': slope,
                            'Intercept': intercept,
                            'R_Value': r_value,
                            'P_Value': p_value,
                            'Std_Err': std_err
                        })

                else:
                    print(f"❌ 警告: 文件 {file_name} 缺少所需列，已跳过")

# 将结果转换为 DataFrame
results_df = pd.DataFrame(results)

# 保存为 CSV 文件
results_df.to_csv(output_file, index=False)

print(f"✅ 计算完成，结果已保存到 {output_file}")
