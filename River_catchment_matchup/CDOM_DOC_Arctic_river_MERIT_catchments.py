# 现在有文件夹D:\UZH\2024\20240122 Nutrient and Organic Carbon references\6large_rivers_watersheds\6River_Parts_watrersheds_merge，  # English: There is now a folder
# 文件夹内有子文件夹6个，分别为6个北极区域名字， 每个子文件夹内有很多流域shp文件，每个shp文件有属性shape，COMID，unitarea，  # English: There are subfolders in the folder
# 将这个文件夹内的所有shp文件合并在一个shp文件中，保持原来的属性，  # English: Put all the folder in
# 将合并得到的shp文件保存在文件夹D:\UZH\2024\20240122 Nutrient and Organic Carbon references\6large_rivers_watersheds\6River_Parts_watrersheds_merge内  # English: Will merge the result
# 命名为MERIT_Arctic_catchments.shp  # English: Named

# 以上代码会将指定文件夹内的所有 shapefile 合并为一个 shapefile，并保存到目标路径。请确认以下事项：  # English: The above code will all the folders in the specified folder

import geopandas as gpd
import pandas as pd
import os

# Define the input directory and output file path
input_dir = r"D:\UZH\2024\20240122 Nutrient and Organic Carbon references\6large_rivers_watersheds\6River_Parts_watrersheds_merge"
output_file = os.path.join(input_dir, "MERIT_Arctic_catchments.shp")

# Initialize an empty GeoDataFrame to store merged shapefiles
merged_gdf = gpd.GeoDataFrame()

# Loop through each subfolder
for region_folder in os.listdir(input_dir):
    region_path = os.path.join(input_dir, region_folder)

    # Check if the current path is a directory
    if os.path.isdir(region_path):
        # Loop through each shapefile in the subfolder
        for file in os.listdir(region_path):
            if file.endswith('.shp'):
                file_path = os.path.join(region_path, file)

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
