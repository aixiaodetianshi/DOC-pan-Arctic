# 输入文件路径:
#
# input_shp 是原始 shapefile 文件路径。
# comid_folder 是包含文件名等于 COMID 的文件夹路径。
# 提取 COMID 列表:
#
# 从文件夹中提取所有文件名，并将其与 shapefile 的 COMID 属性进行匹配。
# 筛选 GeoDataFrame:
#
# 使用 isin() 方法筛选 shapefile 中 COMID 与文件夹文件名匹配的多边形。
# 确保输出文件夹存在:
#
# 使用 os.makedirs() 创建保存结果文件的文件夹路径。
# 保存为新 shapefile:
#
# 使用 to_file() 方法保存提取后的 shapefile 为 Ob.shp。
# 注意事项
# 确保 COMID 列的数据类型与文件名一致（如需要，将其转换为字符串）。
# 输出文件夹 Ob 需存在或可由程序自动创建。
# 如果 COMID 列的命名有变化，请修改代码中对 COMID 的引用。


import geopandas as gpd
import os

# Define file paths
input_shp = r"D:\UZH\2024\20240122 Nutrient and Organic Carbon references\Matchup_ARCADE_MERIT_catchments\Matchup_ARCADE_MERIT_Catchment.shp"
comid_folder = r"D:\UZH\2024\20240122 Nutrient and Organic Carbon references\6large_rivers_watersheds\6River_Parts_watrersheds\Ob_COMID"
output_shp = r"D:\UZH\2024\20240122 Nutrient and Organic Carbon references\Matchup_ARCADE_MERIT_catchments\Ob\Ob.shp"

# Load the shapefile
input_gdf = gpd.read_file(input_shp)

# List all files in the COMID folder and extract COMID values from filenames
comid_files = os.listdir(comid_folder)
comid_values = [os.path.splitext(filename)[0] for filename in comid_files]  # Extract COMID from filenames

# Filter polygons where COMID matches any value in the COMID list
filtered_gdf = input_gdf[input_gdf['COMID'].astype(str).isin(comid_values)]

# Ensure the output folder exists
os.makedirs(os.path.dirname(output_shp), exist_ok=True)

# Save the filtered GeoDataFrame to a new shapefile
filtered_gdf.to_file(output_shp)

print(f"Filtered shapefile saved to: {output_shp}")
