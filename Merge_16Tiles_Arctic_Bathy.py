
import rasterio
from rasterio.merge import merge
import glob
import os

# 设置输入和输出路径
input_folder = r"D:\UZH\World Trade\figure\ibcao_v5_1000m_16_tiled_GeoTiff"  # 16个 TIFF 文件的文件夹
output_file = r"D:\UZH\World Trade\figure\ibcao_v5_1000m_16_tiled_GeoTiff\ibcao_v5_1000m_merged.tif"  # 输出合并文件

# 获取所有 TIF 文件路径
tif_files = glob.glob(os.path.join(input_folder, "*.tif"))

# 读取所有 TIFF 影像
src_files_to_mosaic = []
for tif in tif_files:
    src = rasterio.open(tif)
    src_files_to_mosaic.append(src)

# 进行影像合并
mosaic, out_transform = merge(src_files_to_mosaic)

# 获取合并后影像的元数据
out_meta = src.meta.copy()
out_meta.update({
    "driver": "GTiff",
    "height": mosaic.shape[1],  # 更新新的行数
    "width": mosaic.shape[2],   # 更新新的列数
    "transform": out_transform,  # 更新地理变换参数
    "compress": "LZW",  # 使用 LZW 压缩
    "bigtiff": "YES"    # 允许大文件
})

# 保存合并后的影像
with rasterio.open(output_file, "w", **out_meta) as dest:
    dest.write(mosaic)

print(f"🎉 合并完成！输出文件: {output_file}")