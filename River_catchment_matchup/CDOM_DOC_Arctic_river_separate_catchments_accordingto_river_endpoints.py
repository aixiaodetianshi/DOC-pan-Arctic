# 目标是以 河流入海口点数据（river_endpoints.shp） 为基准，利用 COMID 将 河流reach数据（reach.shp） 分为 10,582 个流域范围  # English: The goal is to

import geopandas as gpd
import os

# 定义路径  # English: Define paths
endpoints_path = r"D:\UZH\2024\20240122 Nutrient and Organic Carbon references\6large_rivers_watersheds\6River_Parts_river_endpoints\Mackenzie_river_endpoints.shp"
reach_path = r"D:\UZH\2024\20240122 Nutrient and Organic Carbon references\6large_rivers_watersheds\Arctic_river_reachs\Arctic_river_reachs.shp"
output_folder = r"D:\UZH\2024\20240122 Nutrient and Organic Carbon references\6large_rivers_watersheds\6River_Parts_river_reachs\Mackenzie"

# 创建输出文件夹（如果不存在）  # English: Create an output folder
os.makedirs(output_folder, exist_ok=True)

# 加载数据  # English: Loading data
endpoints = gpd.read_file(endpoints_path)
reach = gpd.read_file(reach_path)

# 将 COMID 和 NextDownID 存储为字典  # English: Will
reach_dict = dict(zip(reach["COMID"], reach["NextDownID"]))

# 获取所有入海口的 COMID  # English: Get all seaports
endpoints_comid = endpoints["COMID"].tolist()

# 定义函数：递归查找上游河段  # English: Define functions
def find_upstream_segments(comid, reach_dict, upstream_segments):
    for key, value in reach_dict.items():
        if value == comid and key not in upstream_segments:
            upstream_segments.append(key)
            find_upstream_segments(key, reach_dict, upstream_segments)
    return upstream_segments

# 对每个入海口的 COMID 执行追踪  # English: For each entrance
for comid in endpoints_comid:
    # 找到所有上游河段  # English: Find all upper reaches
    upstream_segments = find_upstream_segments(comid, reach_dict, [comid])

    # 筛选出对应的河段数据  # English: Filter out the corresponding river section data
    selected_reaches = reach[reach["COMID"].isin(upstream_segments)]

    # 将 comid 转换为整数以避免文件名中出现 .0  # English: Will
    comid_int = int(comid)

    # 保存为新的 Shapefile  # English: Save as new
    output_path = os.path.join(output_folder, f"{comid_int}.shp")
    selected_reaches.to_file(output_path)

    print(f"流域 {comid} 已完成，保存为 {output_path}")
