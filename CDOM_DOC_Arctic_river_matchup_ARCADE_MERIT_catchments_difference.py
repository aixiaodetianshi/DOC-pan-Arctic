# 使用 geopandas 来比较两个 shapefile，
# 根据属性 gid 找出 ARCADE_exclude_Greenland_Catchment
# 中不在 ARCADE_Ob_Mackenzie 中的 58 个要素，并保存为一个新的 shapefile。


import geopandas as gpd

# 文件路径
catchment_file = r"D:\UZH\2024\20240122 Nutrient and Organic Carbon references\Matchup_ARCADE_MERIT_catchments\ARCADE_exclude_Greenland_Catchment.shp"
ob_mackenzie_file = r"D:\UZH\2024\20240122 Nutrient and Organic Carbon references\Matchup_ARCADE_MERIT_catchments\Yenisey\ARCADE_Ob_Mackenzie.shp"
output_file = r"D:\UZH\2024\20240122 Nutrient and Organic Carbon references\Matchup_ARCADE_MERIT_catchments\difference_Catchment.shp"

# 加载两个 shapefile
catchment_gdf = gpd.read_file(catchment_file)
ob_mackenzie_gdf = gpd.read_file(ob_mackenzie_file)

# 提取不在 ARCADE_Ob_Mackenzie 中的 gid
remaining_gdf = catchment_gdf[~catchment_gdf['gid'].isin(ob_mackenzie_gdf['gid'])]

# 检查结果数量是否正确
print(f"剩余要素数量: {len(remaining_gdf)}")  # 应为 58

# 保存剩余要素为新的 shapefile
remaining_gdf.to_file(output_file, driver="ESRI Shapefile")

print(f"剩余要素已保存到: {output_file}")

