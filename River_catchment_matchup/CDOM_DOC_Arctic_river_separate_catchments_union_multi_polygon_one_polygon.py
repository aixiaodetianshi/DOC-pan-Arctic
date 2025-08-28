# 功能  # English: Function
#
# 遍历文件夹中的所有 .shp 文件。  # English: Iterate through all the folders
# 读取每个 SHP 文件，并检查是否包含有效的几何数据。  # English: Read each
# 使用 unary_union 将所有 polygon 合并为一个 polygon。  # English: use
# 将合并后的数据保存为新的 SHP 文件到目标文件夹。  # English: Save the merged data as new
# 文件结构  # English: File structure
# 确保输入文件夹中每个 SHP 文件的相关文件（.cpg, .dbf, .prj, .shx）完整且路径正确。  # English: Make sure to enter each folder
#
# 输出  # English: Output
#
# 合并后的 SHP 文件保存在目标文件夹中，文件名与原文件一致。  # English: Merged

import geopandas as gpd
import os
from shapely.ops import unary_union
from shapely.geometry import Polygon

# 输入文件夹路径  # English: Enter the folder path
input_folder = r'D:\UZH\2024\20240122 Nutrient and Organic Carbon references\6large_rivers_watersheds\6River_Parts_watrersheds\Mackenzie'

# 输出文件夹路径  # English: Output folder path
output_folder = r'D:\UZH\2024\20240122 Nutrient and Organic Carbon references\6large_rivers_watersheds\6River_Parts_watrersheds_merge\Mackenzie'

# 如果输出文件夹不存在，则创建  # English: If the output folder does not exist
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# 遍历输入文件夹中的所有文件  # English: Iterate through all files in the input folder
for filename in os.listdir(input_folder):
    if filename.endswith('.shp'):
        input_file_path = os.path.join(input_folder, filename)
        print(f"正在处理文件: {input_file_path}")

        try:
            # 读取 shapefile 文件  # English: Read
            gdf = gpd.read_file(input_file_path)

            # 检查是否有有效的几何数据  # English: Check if there is valid geometric data
            if gdf.empty:
                print(f"文件 {filename} 中没有有效几何数据，跳过处理。")
                continue

            # 合并所有 polygon 为一个单一的 polygon  # English: Merge all
            merged_polygon = unary_union(gdf.geometry)

            # 修复可能存在的孔洞或自交问题  # English: Fix possible holes or self-infection problems
            if isinstance(merged_polygon, Polygon):
                merged_polygon = Polygon(merged_polygon.exterior)  # 仅保留外部边界  # English: Only external boundaries are preserved
            elif merged_polygon.is_empty:
                print(f"文件 {filename} 合并后几何体为空，跳过处理。")
                continue

            # 计算 unitarea 的总和  # English: calculate
            total_unitarea = gdf['unitarea'].sum() if 'unitarea' in gdf.columns else None
            if total_unitarea is None:
                print(f"文件 {filename} 中缺少 'unitarea' 属性，无法计算总和。")

            # 获取 COMID 值为文件名（去掉文件扩展名）  # English: Get
            comid_value = os.path.splitext(filename)[0]

            # 创建一个新的 GeoDataFrame 来存储合并后的数据  # English: Create a new
            merged_gdf = gpd.GeoDataFrame(
                [{'geometry': merged_polygon, 'COMID': comid_value, 'unitarea': total_unitarea}],
                crs=gdf.crs
            )

            # 输出文件路径  # English: Output file path
            output_file_path = os.path.join(output_folder, filename)

            # 保存合并后的 GeoDataFrame  # English: Save the merged
            merged_gdf.to_file(output_file_path)
            print(f"文件已成功保存: {output_file_path}")

        except Exception as e:
            print(f"处理文件 {filename} 时发生错误: {e}")

print("所有文件处理完成！")
