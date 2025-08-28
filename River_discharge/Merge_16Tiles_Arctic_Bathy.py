
import rasterio
from rasterio.merge import merge
import glob
import os

# è®¾ç½®è¾“å…¥å’Œè¾“å‡ºè·¯å¾„
input_folder = r"D:\UZH\World Trade\figure\ibcao_v5_1000m_16_tiled_GeoTiff"  # 16ä¸ª TIFF æ–‡ä»¶çš„æ–‡ä»¶å¤¹
output_file = r"D:\UZH\World Trade\figure\ibcao_v5_1000m_16_tiled_GeoTiff\ibcao_v5_1000m_merged.tif"  # è¾“å‡ºåˆå¹¶æ–‡ä»¶

# è·å–æ‰€æœ‰ TIF æ–‡ä»¶è·¯å¾„
tif_files = glob.glob(os.path.join(input_folder, "*.tif"))

# è¯»å–æ‰€æœ‰ TIFF å½±åƒ
src_files_to_mosaic = []
for tif in tif_files:
    src = rasterio.open(tif)
    src_files_to_mosaic.append(src)

# è¿›è¡Œå½±åƒåˆå¹¶
mosaic, out_transform = merge(src_files_to_mosaic)

# è·å–åˆå¹¶åå½±åƒçš„å…ƒæ•°æ®
out_meta = src.meta.copy()
out_meta.update({
    "driver": "GTiff",
    "height": mosaic.shape[1],  # æ›´æ–°æ–°çš„è¡Œæ•°
    "width": mosaic.shape[2],   # æ›´æ–°æ–°çš„åˆ—æ•°
    "transform": out_transform,  # æ›´æ–°åœ°ç†å˜æ¢å‚æ•°
    "compress": "LZW",  # ä½¿ç”¨ LZW å‹ç¼©
    "bigtiff": "YES"    # å…è®¸å¤§æ–‡ä»¶
})

# ä¿å­˜åˆå¹¶åçš„å½±åƒ
with rasterio.open(output_file, "w", **out_meta) as dest:
    dest.write(mosaic)

print(f"ğŸ‰ åˆå¹¶å®Œæˆï¼è¾“å‡ºæ–‡ä»¶: {output_file}")