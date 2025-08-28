import pandas as pd
import os

# 输入和输出路径  # English: Input and output paths
input_path = r"D:\UZH\2024\20240122 Nutrient and Organic Carbon references\DOC\DOC_update_20250203\How_much_ice_free_season_contribute_to_annual_DOC_export\Total_DOC_monthly\All_Parts\Total_monthly_DOC_All_Parts.csv"
output_path = r"D:\UZH\2024\20240122 Nutrient and Organic Carbon references\DOC\DOC_update_20250203\How_much_ice_free_season_contribute_to_annual_DOC_export\Total_DOC_monthly\All_Parts\ice_free_contribute_DOC.csv"

# 读取数据  # English: Read data
df = pd.read_csv(input_path)

# 转换日期  # English: Convert date
df['year_month'] = pd.to_datetime(df['year_month'], format='%b-%y')
df['year'] = df['year_month'].dt.year
df['month'] = df['year_month'].dt.month

# 限定年份范围  # English: Limited year range
df = df[(df['year'] >= 1984) & (df['year'] <= 2018)]

# 冰冻期：5-10月  # English: Freezing period
ice_free = df[(df['month'] >= 5) & (df['month'] <= 10)].groupby('year').agg({
    'Total_DOC': 'sum',
    'Total_DOC_uncertainty': 'sum'
}).reset_index().rename(columns={
    'Total_DOC': 'ice_free_Total_DOC',
    'Total_DOC_uncertainty': 'ice_free_Total_DOC_uncertainty'
})

# 全年总值  # English: Total value for the whole year
year_total = df.groupby('year').agg({
    'Total_DOC': 'sum',
    'Total_DOC_uncertainty': 'sum'
}).reset_index().rename(columns={
    'Total_DOC': 'year_Total_DOC',
    'Total_DOC_uncertainty': 'year_Total_DOC_uncertainty'
})

# 合并  # English: merge
result = pd.merge(ice_free, year_total, on='year')

# 计算比例  # English: Calculate the proportion
result['ice_free_Total_DOC_proportion'] = result['ice_free_Total_DOC'] / result['year_Total_DOC']

# 不确定性传播（采用标准误差传播公式）  # English: Uncertainty transmission
# 比例R = A / B；不确定性σ_R = R * sqrt( (σ_A/A)^2 + (σ_B/B)^2 )  # English: Proportion
result['ice_free_uncertainty_propagation'] = result['ice_free_Total_DOC_proportion'] * (
    (result['ice_free_Total_DOC_uncertainty'] / result['ice_free_Total_DOC'])**2 +
    (result['year_Total_DOC_uncertainty'] / result['year_Total_DOC'])**2
)**0.5

# 保存  # English: save
result.to_csv(output_path, index=False)
print(f"结果已保存至: {output_path}")

