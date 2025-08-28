import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import matplotlib.cm as cm
from shapely.geometry import Point
import numpy as np
import matplotlib.colors as colors
import os
import matplotlib.ticker as mticker
from cartopy.mpl.gridliner import LONGITUDE_FORMATTER, LATITUDE_FORMATTER

# 设置文件路径  # English: Set file path
file_path = 'D:/UZH/2024/20240122 Nutrient and Organic Carbon references/Arctic_River/matchup_RADR_MERIT_Hydro/2_Correction_for_NextDown0_shp/'

file_name1 = 'riv_pfaf_2_MERIT_Hydro_v07_Basins_v01_bugfix1.shp'
file_name2 = 'riv_pfaf_3_MERIT_Hydro_v07_Basins_v01_bugfix1.shp'
file_name3 = 'riv_pfaf_7_MERIT_Hydro_v07_Basins_v01_bugfix1.shp'
file_name4 = 'riv_pfaf_8_MERIT_Hydro_v07_Basins_v01_bugfix1.shp'

# 读取四个 shapefile 文件  # English: Read four
gdf1 = gpd.read_file(os.path.join(file_path, file_name1))
gdf2 = gpd.read_file(os.path.join(file_path, file_name2))
gdf3 = gpd.read_file(os.path.join(file_path, file_name3))
gdf4 = gpd.read_file(os.path.join(file_path, file_name4))

# 合并四个 GeoDataFrame  # English: Merge four
gdf = gpd.GeoDataFrame(pd.concat([gdf1, gdf2, gdf3, gdf4], ignore_index=True))

# 检查并设置 CRS (确保四个文件的 CRS 一致)  # English: Check and set
if not all([gdf1.crs == gdf2.crs == gdf3.crs == gdf4.crs]):
    print("警告: 某些文件的坐标参考系统 (CRS) 不一致，可能需要手动调整。")
else:
    gdf.set_crs(gdf1.crs, inplace=True)

# 计算以10为底的对数值，并添加为新列  # English: Calculate with
gdf['log_uparea'] = np.log10(gdf['uparea'] + 1)  # 加1避免对数计算中的负无穷大问题  # English: add

# 提取终点的经纬度信息  # English: Extract the latitude and longitude information of the end point
def extract_endpoints(row):
    line = row.geometry
    end_point = line.coords[-1]  # 提取河流终点  # English: Extract the end point of the river
    return Point(end_point)

# 创建包含 COMID, 流域面积, 以及终点坐标的 GeoDataFrame  # English: Create Include
gdf_points = gpd.GeoDataFrame(
    gdf[['COMID', 'log_uparea']],
    geometry=gdf.apply(extract_endpoints, axis=1),
    crs=gdf.crs
)

# 设置字体为 Times New Roman  # English: Set the font to
plt.rcParams['font.family'] = 'serif'
plt.rcParams['font.serif'] = ['Times New Roman']


# 设置极地投影  # English: Set up polar projection
projection = ccrs.NorthPolarStereo()

# 创建绘图窗口  # English: Create a drawing window
fig, ax = plt.subplots(figsize=(10, 10), subplot_kw={'projection': projection})

# 提高底图分辨率，使用更加详细的地理特征  # English: Improve basemap resolution
ax.add_feature(cfeature.LAND.with_scale('50m'), edgecolor='none', zorder=1)
ax.add_feature(cfeature.OCEAN.with_scale('50m'), zorder=0)
ax.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.1)
ax.add_feature(cfeature.BORDERS.with_scale('50m'), linestyle=':', linewidth=0.5)
ax.add_feature(cfeature.RIVERS.with_scale('50m'), linewidth=0.5)

# 颜色映射设置，最大值为 log10(40,000)  # English: Color Map Settings
max_log_area = np.log10(40000 + 1)
norm = colors.Normalize(vmin=0, vmax=max_log_area)
cmap = cm.viridis

# 将 GeoDataFrame 投影到极地投影  # English: Will
gdf.to_crs(projection, inplace=True)
gdf_points.to_crs(projection, inplace=True)

# 绘制流域数据并设置颜色映射  # English: Draw basin data and set color maps
gdf.plot(column='log_uparea', cmap=cmap, norm=norm, linewidth=0.3, edgecolor='none', ax=ax, legend=False, transform=projection)

# 在地图上添加河流入海口位置点（不带黑色边框），设置点的大小  # English: Add river inlet location points on the map
scatter = ax.scatter(
    gdf_points.geometry.x, gdf_points.geometry.y,
    c=gdf_points['log_uparea'], s=5, cmap=cmap, norm=norm,  # 修改点的大小为10  # English: The size of the modified point is
    edgecolor='none', transform=projection, zorder=2
)

# 手动添加颜色条  # English: Add color bars manually
sm = plt.cm.ScalarMappable(cmap=cmap, norm=norm)
sm.set_array([])
cbar = plt.colorbar(sm, ax=ax, fraction=0.046, pad=0.04)
cbar.set_label('Log10 of Upstream Area (km²)', fontsize=12)

# 设置标题  # English: Set the title
# ax.set_title('River Basins and Mouth Locations with Log10 Scaled Areas', fontsize=14)

# 设置经度坐标轴的刻度，每30度一个刻度  # English: Set the scale of the longitude axis
# 由于使用的是极地投影，通常经度刻度不适用，在极地投影中，通常显示纬度网格线  # English: Since polar projection is used
# 这里不再设置经度坐标轴刻度  # English: The longitude axis scale is no longer set here

# 设置纬度坐标轴的刻度，每30度一个刻度  # English: Set the scale of the latitude axis
# 极地投影中显示纬度线，通常会有自动的网格线显示  # English: Display latitude lines in polar projection

# 添加经纬度网格和标签  # English: Add latitude and longitude grids and labels
gl = ax.gridlines(draw_labels=True, color='gray', alpha=0.5, linestyle='--')
gl.xlabels_top = False  # 禁用顶部的经度标签  # English: Disable the longitude tag at the top
gl.ylabels_right = False  # 禁用右侧的纬度标签  # English: Disable the latitude tag on the right
gl.xformatter = LONGITUDE_FORMATTER
gl.yformatter = LATITUDE_FORMATTER
gl.xlabel_style = {'size': 10, 'color': 'black', 'family': 'Times New Roman'}
gl.ylabel_style = {'size': 10, 'color': 'black', 'family': 'Times New Roman'}

# 设置经度和纬度的刻度  # English: Set the scales of longitude and latitude
gl.xlocator = mticker.FixedLocator(np.arange(-180, 181, 30))
gl.ylocator = mticker.FixedLocator(np.arange(60, 91, 10))

ax.set_yticks(np.arange(0, 90, 30))  # 只适用于极地投影下的纬度网格线  # English: Only suitable for latitude grid lines under polar projection
ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda y, _: f'{y:.0f}°'))

# 保存图像为300 DPI的TIFF文件格式  # English: Save the image as
plt.savefig('polar_projection_rivers_with_endpoints_log10_small_points.tif', dpi=300, format='tiff', bbox_inches='tight')

# 显示图像  # English: Show image
plt.show()
