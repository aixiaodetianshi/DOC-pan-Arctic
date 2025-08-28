# 从 MERIT Hydro 数据集中提取 river reach 终点位置点经纬度信息  # English: from

import geopandas as gpd
from shapely.geometry import Point

# Step 1: 读取 MERIT Hydro数据集信息  # English: Read
file_name = 'riv_pfaf_2_MERIT_Hydro_v07_Basins_v01_bugfix1.shp'
file_path = 'D:/UZH/2024/20240122 Nutrient and Organic Carbon references/Arctic_River/matchup_RADR_MERIT_Hydro/2_Correction_for_NextDown0_shp/' + file_name
gdf = gpd.read_file(file_path)

# 检查并设置坐标参考系统 (CRS)  # English: Check and set the coordinate reference system
if gdf.crs is None:
    # 如果没有定义 CRS，手动设置。例如：WGS84 (EPSG:4326)  # English: If not defined
    gdf.set_crs(epsg=4326, inplace=True)
else:
    print(f"CRS 已定义: {gdf.crs}")

# 提取终点的经纬度信息  # English: Extract the latitude and longitude information of the end point
def extract_endpoints(row):
    # 获取河流线段的几何形状（Polyline）  # English: Get the geometry of the river segment
    line = row.geometry
    # 提取终点（最后一个点）  # English: Extract the end point
    # end_point = line.coords[-1]
    end_point = line.coords[0]
    # 返回终点的经纬度信息  # English: Return to the end point latitude and longitude information
    return Point(end_point)

# 生成包含终点的 GeoDataFrame  # English: Generate an endpoint containing
gdf_points = gpd.GeoDataFrame(gdf[['COMID']],
                              geometry=gdf.apply(extract_endpoints, axis=1),
                              crs=gdf.crs)

# 显示包含新列的 GeoDataFrame  # English: Show new columns
print(gdf_points.head())
out_file_name = 'riv_pfaf_2_MERIT_Hydro_v07_Basins_v01_endpoints.shp'
out_path = 'D:/UZH/2024/20240122 Nutrient and Organic Carbon references/Arctic_River/matchup_RADR_MERIT_Hydro/3_startpoint_river_reach_shp/' + out_file_name

gdf_points.to_file(out_path)  # 保存为 Shapefile  # English: Save as
print(f"匹配的河流属性数据已成功保存到 {out_path}")