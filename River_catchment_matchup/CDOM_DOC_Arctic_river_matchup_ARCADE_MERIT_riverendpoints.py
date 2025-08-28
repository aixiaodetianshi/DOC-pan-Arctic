# 检查流域范围内是否包含河流入海口点。  # English: Check whether river inlet points are included in the basin
# 如果包含，选择该点作为匹配点。  # English: If included
# 如果不包含，选择距离流域边界最近的河流入海口点。  # English: If not included
# 将匹配点的 COMID 添加到多边形属性中。  # English: Will match the point
# 在每次写入 COMID 值时，将其转换为 int。  # English: Every time
# 在最终保存之前，使用 astype({"COMID": "int32"}) 确保 COMID 字段在保存到 shapefile 时为整数类型。  # English: Before final saving


import geopandas as gpd
from shapely.geometry import Point

# 定义文件路径  # English: Define file path
data_folder = r"D:\\UZH\\2024\\20240122 Nutrient and Organic Carbon references\\Matchup_ARCADE_MERIT_catchments\\Mackenzie"
endpoints_file = f"{data_folder}\\Mackenzie_river_endpoints.shp"
polygons_file = f"{data_folder}\\ARCADE_Mackenzie.shp"
output_file = f"{data_folder}\\ARCADE_MERIT_Mackenzie.shp"

# 读取点和多边形数据  # English: Read point and polygon data
endpoints = gpd.read_file(endpoints_file)
polygons = gpd.read_file(polygons_file)

# 检查坐标参考系，确保两者一致  # English: Check the coordinate reference system
if endpoints.crs != polygons.crs:
    endpoints = endpoints.to_crs(polygons.crs)

# 确保 COMID 字段是整数类型  # English: make sure
if "COMID" not in polygons.columns:
    polygons["COMID"] = None

# 为每个多边形匹配最近的点或内部点  # English: Match the nearest point or internal point for each polygon
for idx, polygon in polygons.iterrows():
    # 查找多边形内包含的点  # English: Find points contained in polygons
    points_within = endpoints[endpoints.geometry.within(polygon.geometry)]

    if not points_within.empty:
        # 如果有点在多边形内部，选择第一个点的 COMID  # English: If the point is inside the polygon
        polygons.at[idx, "COMID"] = int(points_within.iloc[0]["COMID"])
    else:
        # 如果没有点在多边形内部，找到距离多边形边界最近的点  # English: If no points are inside the polygon
        distances = endpoints.geometry.distance(polygon.geometry)
        nearest_point_idx = distances.idxmin()
        polygons.at[idx, "COMID"] = int(endpoints.loc[nearest_point_idx, "COMID"])

# 保存匹配后的多边形数据到新的 shapefile，确保 COMID 是整数类型  # English: Save the matching polygon data to the new one
polygons = polygons.astype({"COMID": "int32"})
polygons.to_file(output_file, driver="ESRI Shapefile")

print(f"处理完成，生成的文件已保存到 {output_file}")
