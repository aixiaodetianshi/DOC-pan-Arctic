
import pandas as pd
import os

# 输入文件夹路径  # English: Enter the folder path
MERIT_river_endpoints = r'D:\UZH\2024\20240122 Nutrient and Organic Carbon references\discharge\riv_pfaf_MERIT_Hydro_v07_Basins_v01_endpoints_COMID.xlsx'

MERIT_6_large_parts_river_endpoints = r'D:\UZH\2024\20240122 Nutrient and Organic Carbon references\discharge\Total_6_river_endpoints.xlsx'

# 读取  MERIT_river_endpoints 文件  # English: Read
df_MERIT = pd.read_excel(MERIT_river_endpoints)

# 读取  MERIT_6_large_parts_river_endpoints 文件  # English: Read
df_6_large_parts = pd.read_excel(MERIT_6_large_parts_river_endpoints)

# 提取 COMID 列  # English: extract
comid_MERIT = df_MERIT['COMID']
comid_6_large_parts = df_6_large_parts['COMID']

# 找出 MERIT_river_endpoints 中有但 MERIT_6_large_parts_river_endpoints 中没有的 COMID  # English: Find out
missing_comid = comid_MERIT[~comid_MERIT.isin(comid_6_large_parts)]

# 打印缺少的 COMID 编号  # English: Print missing
print("缺少的 COMID 编号：")
print(missing_comid.values)