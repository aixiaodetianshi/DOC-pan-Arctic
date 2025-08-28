import os
import pandas as pd
import math

# 输入和输出文件夹路径  # English: Input and output folder paths
input_file_name = r"D:\UZH\2024\20240122 Nutrient and Organic Carbon references\DOC\DOC_greater_equal_0\HLSS30\HLSS30_Mackenzie_CDOM_water_0_13_13_DOC.xlsx"
output_file_name = r"D:\UZH\2024\20240122 Nutrient and Organic Carbon references\DOC\DOC_greater_equal_0\HLSS30_uncertainty\HLSS30_Mackenzie_CDOM_water_0_13_13_DOC.xlsx"

# Landsat 5
# 不确定性数值  # English: Uncertainty value
# CDOM_uncertainty = 0.4252 # Ob
# CDOM_uncertainty = 0.3957 # Yenisey
# CDOM_uncertainty = 2.6405 # Lena
# CDOM_uncertainty = 0.2158 # Kolyma
# CDOM_uncertainty = 1.0778 # Yukon
# CDOM_uncertainty = 0.7068 # Mackenzie

# Landsat 7
# 不确定性数值  # English: Uncertainty value
# CDOM_uncertainty = 1.5433   # Ob
# CDOM_uncertainty = 2.4717 # Yenisey
# CDOM_uncertainty = 4.4340 # Lena
# CDOM_uncertainty = 1.7359 # Kolym
# CDOM_uncertainty = 1.8919 # Yukon
# CDOM_uncertainty = 0.8311 # Mackenzie

# HLSL30
# 不确定性数值  # English: Uncertainty value
# CDOM_uncertainty = 1.0533   # Ob
# CDOM_uncertainty = 2.0994 # Yenisey
# CDOM_uncertainty = 2.6217 # Lena
# CDOM_uncertainty = 2.9893 # Kolyma
# CDOM_uncertainty = 1.7271 # Yukon
# CDOM_uncertainty = 0.7281 # Mackenzie

# HLSS30
# 不确定性数值  # English: Uncertainty value
# CDOM_uncertainty = 1.5917   # Ob
# CDOM_uncertainty = 2.0925 # Yenisey
# CDOM_uncertainty = 2.2230 # Lena
# CDOM_uncertainty = 1.2574 # Kolyma
# CDOM_uncertainty = 2.1446 # Yukon
CDOM_uncertainty = 0.8053 # Mackenzie


CDOM_DOC_uncertainty = 2.0919
DOC_uncertainty = math.sqrt(CDOM_uncertainty * CDOM_uncertainty + CDOM_DOC_uncertainty * CDOM_DOC_uncertainty)

# 遍历输入文件夹中的所有xlsx文件  # English: Iterate through all the input folders
if input_file_name.endswith('.xlsx'):
    # 读取Excel文件  # English: Read
    df = pd.read_excel(input_file_name)

    # 添加不确定性列  # English: Add uncertainty columns
    df['CDOM_uncertainty'] = CDOM_uncertainty
    df['CDOM_DOC_uncertainty'] = CDOM_DOC_uncertainty
    df['DOC_uncertainty'] = DOC_uncertainty

    # 保存到目标文件夹  # English: Save to destination folder
    df.to_excel(output_file_name, index=False)

print("所有文件已处理并保存到目标文件夹。")
