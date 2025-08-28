# 将文件夹D:\UZH\2024\20240122 Nutrient and Organic Carbon references\6large_rivers_watersheds\6River_Parts_watrersheds_merge\Ob  # English: Put the folder
# 内的所有shp文件保留所有原有属性，合并为Ob.shp文件，  # English: All within
# 保存在文件夹D:\UZH\2024\20240122 Nutrient and Organic Carbon references\6large_rivers_watersheds\6River_Parts_watrersheds_merge内。  # English: Save in folder

import geopandas as gpd
import pandas as pd
import os

# Define the input directory and output file path
input_dir = r"D:\UZH\2024\20240122 Nutrient and Organic Carbon references\6large_rivers_watersheds\6River_Parts_watrersheds_merge\Mackenzie"
output_file = r"D:\UZH\2024\20240122 Nutrient and Organic Carbon references\6large_rivers_watersheds\6River_Parts_watrersheds_merge\Mackenzie.shp"

# Initialize an empty GeoDataFrame to store merged shapefiles
merged_gdf = gpd.GeoDataFrame()

# Loop through each shapefile in the specified folder
for file in os.listdir(input_dir):
    if file.endswith('.shp'):
        file_path = os.path.join(input_dir, file)

        # Read the shapefile
        gdf = gpd.read_file(file_path)

        # Append the data to the merged GeoDataFrame
        merged_gdf = gpd.GeoDataFrame(pd.concat([merged_gdf, gdf], ignore_index=True))

# Ensure the merged GeoDataFrame has the same CRS
if not merged_gdf.empty:
    merged_gdf = merged_gdf.set_crs(gdf.crs)

# Save the merged GeoDataFrame to a new shapefile
merged_gdf.to_file(output_file)

print(f"Merged shapefile saved at: {output_file}")
