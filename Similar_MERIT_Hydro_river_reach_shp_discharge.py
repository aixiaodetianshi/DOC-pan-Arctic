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


# Step 1: 读取 RADR_v1.0.0.nc 文件中的 reach ID
file_path = 'D:/UZH/2024/20240122 Nutrient and Organic Carbon references/discharge/RADR_v1.0.0.nc'
# 使用xarray打开NetCDF文件
dataset = xr.open_dataset(file_path)
# 提取 'reach' 数据，并将其转换为 NumPy 数组
reach_ids_radr = dataset['reach'].values
# 强制将两者都转换为整数
reach_ids_radr = reach_ids_radr.astype(int)

print("RADR_v1.0.0")
print(reach_ids_radr[:10])


# Step 2: 读取 RiverATLAS_v10 数据集
riveratlas_file_path = 'D:/UZH/2024/20240122 Nutrient and Organic Carbon references/MERIT-BASINS/pfaf_level_01/riv_pfaf_9_MERIT_Hydro_v07_Basins_v01_bugfix1.shp'
river_atlas = gpd.read_file(riveratlas_file_path)
# 强制将两者都转换为整数
river_atlas['COMID'] = river_atlas['COMID'].astype(int)
print("RiverATLAS_v10")
print(river_atlas['COMID'].unique()[:10])


# Step 3: 匹配 Reach ID，并筛选数据
# 假设 RiverATLAS_v10 数据集中的河流编号列名为 'HYRIV_ID'
matching_rows = river_atlas[river_atlas['COMID'].isin(reach_ids_radr)]
print(f"匹配的行数: {matching_rows.shape[0]}")


# Step 4: 将匹配结果保存为 Shapefile 文件
output_shapefile = 'D:/UZH/2024/20240122 Nutrient and Organic Carbon references/Arctic_River/matchup_RADR_MERIT_Hydro/riv_pfaf_9_MERIT_Hydro_v07_Basins_v01_bugfix1.gpkg'
matching_rows.to_file(output_shapefile, driver = 'GPKG')

print(f"匹配的河流属性数据已成功保存到 {output_shapefile}")
