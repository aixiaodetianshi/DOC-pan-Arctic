# 计算最近距离：  # English: Calculate the nearest distance
# 使用 nearest() 方法计算每个 ARCADE 多边形到 MERIT Hydro 数据集中最近多边形的距离。  # English: use
# 计算空间重叠：  # English: Calculate space overlap
# 使用 geopandas.overlay() 找到所有交集并计算交集面积。  # English: use
# 按照每个 ARCADE 多边形找到重叠面积最大的 MERIT Hydro 多边形。  # English: By each
# 综合匹配：  # English: Comprehensive Match
# 如果一个 ARCADE 多边形有多个重叠候选，则优先选择重叠率最高的；如果没有重叠，则选取最近距离的多边形。  # English: If one
# 添加属性：  # English: Add properties
# 将选定的 COMID 添加为 ARCADE 多边形的新属性。  # English: Will the selected


import geopandas as gpd
from shapely.geometry import shape, box
from shapely.ops import nearest_points

# Define file paths
arcade_path = r"D:\UZH\2024\20240122 Nutrient and Organic Carbon references\Matchup_ARCADE_MERIT_catchments\ARCADE_exclude_Greenland_Catchment.shp"
merit_hydro_path = r"D:\UZH\2024\20240122 Nutrient and Organic Carbon references\Matchup_ARCADE_MERIT_catchments\MERIT_Arctic_catchments.shp"
output_path = r"D:\UZH\2024\20240122 Nutrient and Organic Carbon references\Matchup_ARCADE_MERIT_catchments\Matchup_ARCADE_MERIT_Catchment.shp"

# Load datasets
arcade_gdf = gpd.read_file(arcade_path)
merit_gdf = gpd.read_file(merit_hydro_path)

# Ensure both datasets use the same CRS
if arcade_gdf.crs != merit_gdf.crs:
    merit_gdf = merit_gdf.to_crs(arcade_gdf.crs)

# Ensure geometries are valid
arcade_gdf['geometry'] = arcade_gdf['geometry'].apply(lambda geom: shape(geom) if geom and not geom.is_empty else None)
merit_gdf['geometry'] = merit_gdf['geometry'].apply(lambda geom: shape(geom) if geom and not geom.is_empty else None)

# Remove invalid geometries
arcade_gdf = arcade_gdf[arcade_gdf['geometry'].notnull()]
merit_gdf = merit_gdf[merit_gdf['geometry'].notnull()]

# Build spatial index for MERIT polygons
merit_sindex = merit_gdf.sindex

# Function to find the nearest polygon
def find_nearest_comid(row, merit_gdf, merit_sindex):
    # Ensure the row geometry is valid
    if row.geometry is None or row.geometry.is_empty:
        return None

    # Get the bounds as a shapely box
    bounds_box = box(*row.geometry.bounds)

    # Find possible matches using bounding box
    possible_matches_index = list(merit_sindex.query(bounds_box))
    possible_matches = merit_gdf.iloc[possible_matches_index]

    # Find the nearest geometry
    if not possible_matches.empty:
        nearest_geom = nearest_points(row.geometry, possible_matches.geometry.union_all())[1]
        nearest_polygon = possible_matches[possible_matches.geometry == nearest_geom]
        if not nearest_polygon.empty:
            # Debug: Print nearest_polygon and COMID
            print(f"Nearest polygon found: {nearest_polygon}")
            return nearest_polygon.iloc[0]['COMID'] if 'COMID' in nearest_polygon.columns else None
    return None

# Apply the function to find the nearest COMID for each polygon in ARCADE
arcade_gdf['COMID'] = arcade_gdf.apply(
    lambda row: find_nearest_comid(row, merit_gdf, merit_sindex), axis=1
)

# Debug: Check missing COMID rows
missing_comid_count = arcade_gdf['COMID'].isna().sum()
print(f"Number of polygons with missing COMID: {missing_comid_count}")

# Drop specified columns
columns_to_remove = [
    "soilt_23", "soilt_24", "soilt_25", "soilt_27", "soilt_28", "soilt_29",
    "soilt_11", "soilt_12", "soilt_13", "soilt_14", "soilt_15", "soilt_16",
    "soilt_18", "soilt_1", "soilt_3", "soilt_4", "soilt_5", "soilt_20", "soilt_21"
]
arcade_gdf = arcade_gdf.drop(columns=[col for col in columns_to_remove if col in arcade_gdf.columns])

# Save the updated dataset
arcade_gdf.to_file(output_path)

print(f"Processing completed. Results saved to {output_path}")
