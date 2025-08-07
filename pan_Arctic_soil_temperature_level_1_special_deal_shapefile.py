# 从温度数据文件夹中提取已有的 gid 值；
#
# 加载 .shp 文件；
#
# 筛选出 不在已有温度数据中的流域；
#
# 输出筛选结果为新的 Shapefile。

# 输入输出路径
import geopandas as gpd
import os

# 路径设置
shapefile_path = r"D:\UZH\2024\20240122 Nutrient and Organic Carbon references\Arctic\ARCADE_catchments\ARCADE_v1_36_1km\ARCADE_v1_36_1km_River_Catchment_simplify.shp"
temp_data_folder = r"D:\UZH\2025\NPP\pan_Arctic_total_precipitation_sum"
output_path = r"D:\UZH\2025\NPP\special_deal_shapefile\pan_Arctic_total_precipitation_sum_special_shapefile.shp"

# 1. 加载流域 shapefile
gdf = gpd.read_file(shapefile_path)

# 2. 获取已存在温度文件的 gid 列表
existing_gids = set()

for filename in os.listdir(temp_data_folder):
    if filename.endswith(".csv"):
        gid_str = filename.split('_')[0]
        try:
            gid = int(gid_str)
            existing_gids.add(gid)
        except ValueError:
            print(f"跳过无法识别 gid 的文件: {filename}")

print(f"识别到已有温度数据的流域数量: {len(existing_gids)}")

# 3. 筛选不在已有 GID 中的流域
gdf['gid'] = gdf['gid'].astype(int)
gdf_filtered = gdf[~gdf['gid'].isin(existing_gids)]

# 4. 保存结果
os.makedirs(os.path.dirname(output_path), exist_ok=True)
gdf_filtered.to_file(output_path)

print(f"保留未匹配温度数据的流域数量: {len(gdf_filtered)}")
print(f"结果保存至: {output_path}")