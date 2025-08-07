# 目标是以 河流入海口点数据（river_endpoints.shp） 为基准，利用 COMID 将 河流reach数据（reach.shp） 分为 10,582 个流域范围

# 保存所有属性列：使用 gdf.to_excel 方法保存整个 GeoDataFrame 到 Excel 文件，而不仅限于 COMID 列。
# 检查数据有效性：增加检查，确保文件包含数据后再保存。
# 使用 openpyxl 引擎：to_excel 的引擎指定为 openpyxl，确保与 Excel 文件兼容。
# 输出结构：
# 每个 .shp 文件对应一个 .xlsx 文件，文件名与 .shp 文件相同，但扩展名改为 .xlsx。
# Excel 文件包含原始 shp 文件的所有属性列。

import os
import geopandas as gpd
import pandas as pd

# 定义输入和输出路径
input_folder = r"D:\UZH\2024\20240122 Nutrient and Organic Carbon references\6large_rivers_watersheds\6River_Parts_river_reachs\Mackenzie"
output_folder = r"D:\UZH\2024\20240122 Nutrient and Organic Carbon references\6large_rivers_watersheds\6River_Parts_river_reachs\Mackenzie_COMID"

# 创建输出文件夹（如果不存在）
os.makedirs(output_folder, exist_ok=True)

# 遍历输入文件夹中的所有 .shp 文件
for file_name in os.listdir(input_folder):
    if file_name.endswith(".shp"):

        # 构建完整文件路径
        shp_path = os.path.join(input_folder, file_name)

        # 加载 shapefile 数据
        gdf = gpd.read_file(shp_path)

        # 检查是否包含数据
        if not gdf.empty:

            # 输出 Excel 文件路径
            excel_file_name = os.path.splitext(file_name)[0] + ".xlsx"
            output_path = os.path.join(output_folder, excel_file_name)

            # 保存所有属性到 Excel 文件
            gdf.to_excel(output_path, index=False, engine='openpyxl')

            print(f"处理完成: {file_name}，保存为 {output_path}")
        else:
            print(f"文件 {file_name} 不包含任何数据，跳过处理。")