# 目标是以 河流入海口点数据（river_endpoints.shp） 为基准，利用 COMID 将 河流reach数据（reach.shp） 分为 10,582 个流域范围

# 依据上面的得到的河流入海口的流域内河流reach数据，每条河流入海口对应一个excel文件，
# 文件内有一列是河流reach的识别编号COMID，
# 读取文件夹D:\UZH\2024\20240122 Nutrient and Organic Carbon references\6large_rivers_watersheds\6River_Parts_river_reachs\Ob_COMID内的每条河流excel文件，
# 得到该条河流的COMID数据，读取shp文件D:\UZH\2024\20240122 Nutrient and Organic Carbon references\6large_rivers_watersheds\Arctic_catchments\Ob_catchments.shp
# 内的所对应的COMID流域，将这些流域数据以相同的文件名，shp文件格式，
# 写入文件夹D:\UZH\2024\20240122 Nutrient and Organic Carbon references\6large_rivers_watersheds\6River_Parts_watrersheds\Ob中，

import os
import geopandas as gpd
import pandas as pd

# 定义路径
excel_folder = r"D:\UZH\2024\20240122 Nutrient and Organic Carbon references\6large_rivers_watersheds\6River_Parts_river_reachs\Mackenzie_COMID"
shp_file = r"D:\UZH\2024\20240122 Nutrient and Organic Carbon references\6large_rivers_watersheds\Arctic_catchments\Mackenzie_catchments.shp"
output_folder_shp = r"D:\UZH\2024\20240122 Nutrient and Organic Carbon references\6large_rivers_watersheds\6River_Parts_watrersheds\Mackenzie"
output_folder_excel = r"D:\UZH\2024\20240122 Nutrient and Organic Carbon references\6large_rivers_watersheds\6River_Parts_watrersheds\Mackenzie_COMID"

# 创建输出文件夹（如果不存在）
os.makedirs(output_folder_shp, exist_ok=True)
os.makedirs(output_folder_excel, exist_ok=True)

# 读取流域的 shapefile 数据
catchments_gdf = gpd.read_file(shp_file)

# 检查 shapefile 是否包含 COMID 和 unitarea 列
if "COMID" not in catchments_gdf.columns or "unitarea" not in catchments_gdf.columns:
    raise ValueError("Shapefile does not contain required COMID or unitarea columns.")

# 遍历 Excel 文件夹中的每个文件
for excel_file in os.listdir(excel_folder):
    if excel_file.endswith(".xlsx"):

        # 读取 Excel 文件中的 COMID 数据
        excel_path = os.path.join(excel_folder, excel_file)
        comid_data = pd.read_excel(excel_path)

        if "COMID" not in comid_data.columns:
            print(f"文件 {excel_file} 不包含 COMID 列，跳过处理。")
            continue

        # 获取 COMID 列的值
        comid_list = comid_data["COMID"].tolist()

        # 筛选对应的流域数据
        filtered_gdf = catchments_gdf[catchments_gdf["COMID"].isin(comid_list)]

        # 检查是否有匹配的流域数据
        if filtered_gdf.empty:
            print(f"文件 {excel_file} 中的 COMID 未匹配到任何流域数据。")
            continue

        # 提取 unitarea 数据并添加到 Excel 数据最后一列
        unitarea_map = filtered_gdf.set_index("COMID")["unitarea"].to_dict()
        comid_data["unitarea"] = comid_data["COMID"].map(unitarea_map)

        # 保存更新后的 Excel 文件
        output_excel_path = os.path.join(output_folder_excel, excel_file)
        comid_data.to_excel(output_excel_path, index=False)

        # 保存筛选后的流域数据为新的 shapefile
        output_shp_path = os.path.join(output_folder_shp, os.path.splitext(excel_file)[0] + ".shp")
        filtered_gdf.to_file(output_shp_path)

        print(f"处理完成: {excel_file}，保存为 {output_shp_path} 和 {output_excel_path}")

print("所有文件处理完成！")

