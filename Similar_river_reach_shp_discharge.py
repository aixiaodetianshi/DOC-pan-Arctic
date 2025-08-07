# 从 RADR_v1.0.0.nc 数据集里面读取 river reach ID
# 从 RiverATLAS_v10 数据集里面读取 HYRIV_ID（river reach ID）
# 发现相同的HYRIV_ID，并将文件保存为shape文件

# 实现步骤
# 1. 读取 RADR_v1.0.0.nc 文件中的 reach ID。
# 2. 读取 RiverATLAS_v10 数据集并提取 HYRIV_ID。
# 3. 匹配 Reach ID 并筛选数据。
# 4. 保存匹配结果为 Shapefile 文件。

import xarray as xr
import pandas as pd
import geopandas as gpd


def swap_second_third_digit(num):
    # 将整数转换为8位字符串
    num_str = f"{num:08d}"
    # 交换第二位和第三位
    swapped_str = num_str[0] + num_str[2] + num_str[1] + num_str[3:]
    # 将结果转换回整数
    return int(swapped_str)


# Step 1: 读取 RADR_v1.0.0.nc 文件中的 reach ID
file_path = 'D:/UZH/2024/20240122 Nutrient and Organic Carbon references/discharge/RADR_v1.0.0.nc'
# 使用xarray打开NetCDF文件
dataset = xr.open_dataset(file_path)
# 提取 'reach' 数据，并将其转换为 NumPy 数组
reach_ids_radr = dataset['reach'].values
# 强制将两者都转换为整数
reach_ids_radr = reach_ids_radr.astype(int)
# 对每个ID进行位数交换
reach_ids_radr = [swap_second_third_digit(id) for id in reach_ids_radr]
print("RADR_v1.0.0")
print(reach_ids_radr[:10])


# Step 2: 读取 RiverATLAS_v10 数据集
riveratlas_file_path = 'D:/UZH/2024/20240122 Nutrient and Organic Carbon references/Arctic_River/River_all_attributes/RiverATLAS_v10_si.shp'
river_atlas = gpd.read_file(riveratlas_file_path)
# 强制将两者都转换为整数
river_atlas['HYRIV_ID'] = river_atlas['HYRIV_ID'].astype(int)
print("RiverATLAS_v10")
print(river_atlas['HYRIV_ID'].unique()[:10])


# Step 3: 匹配 Reach ID，并筛选数据
# 假设 RiverATLAS_v10 数据集中的河流编号列名为 'HYRIV_ID'
matching_rows = river_atlas[river_atlas['HYRIV_ID'].isin(reach_ids_radr)]
print(f"匹配的行数: {matching_rows.shape[0]}")


# Step 4: 将匹配结果保存为 Shapefile 文件
output_shapefile = 'D:/UZH/2024/20240122 Nutrient and Organic Carbon references/Arctic_River/matchup_RADR_RiverATLAS/RiverATLAS_v10_si.gpkg'
matching_rows.to_file(output_shapefile, driver = 'GPKG')

print(f"匹配的河流属性数据已成功保存到 {output_shapefile}")
