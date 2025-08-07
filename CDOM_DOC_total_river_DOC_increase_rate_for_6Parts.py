# 计算思路
# 读取所有河流的 Total_DOC 数据
#
# 计算每个流域分区内的增长率
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


import pandas as pd
import numpy as np
from scipy.stats import linregress

# 输入文件路径
input_file = r"D:\UZH\2024\20240122 Nutrient and Organic Carbon references\DOC\DOC_update_20250203\Total_DOC_average\Total_DOC_annual_All_Parts.csv"

# 读取 CSV 文件
df = pd.read_csv(input_file)

# 检查是否包含所需列
if {'year', 'Total_DOC_Annual'}.issubset(df.columns):
    # 选择 1984-2018 年的数据
    df_filtered = df[(df['year'] >= 1984) & (df['year'] <= 2018)].dropna()

    if len(df_filtered) >= 5:  # 至少5个数据点才能进行线性回归
        years = df_filtered['year'].values
        doc_values = df_filtered['Total_DOC_Annual'].values

        # 进行最小二乘法线性拟合
        slope, intercept, r_value, p_value, std_err = linregress(years, doc_values)

        # 在屏幕上输出结果
        print(f"📊 **Ob 河流 Total_DOC 年增长率分析结果** 📊")
        print(f"年增长率 (Annual Increase Rate): {slope:.6f} Tg C/yr²")
        print(f"截距 (Intercept): {intercept:.6f}")
        print(f"相关系数 (R 值): {r_value:.6f}")
        print(f"P 值 (P-Value): {p_value:.6f}")
        print(f"标准误差 (Std Err): {std_err:.6f}")

    else:
        print("❌ 数据点不足，无法进行线性回归分析")
else:
    print("❌ 读取失败：文件缺少必要的列 'year' 或 'Total_DOC_Annual'")

