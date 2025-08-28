# separate the river discharge/ DOC dataset into 6 rivers parts


import os
import shutil

# å®šä¹‰è·¯å¾„
river = "Yukon"
comid_folder = r"D:\UZH\2024\20240122 Nutrient and Organic Carbon references\0_2_6large_rivers_watersheds\6River_Parts_river_reachs\\"+river+"_COMID"
discharge_folder = r"D:\UZH\2024\20240122 Nutrient and Organic Carbon references\3_river_mouth_DOC\DOC_update_20250203\Combination_single_river_sort_date_pre_process_filldate"
destination_folder = r"D:\UZH\2024\20240122 Nutrient and Organic Carbon references\3_river_mouth_DOC\DOC_update_20250203\Combination_single_river_sort_date_pre_process_6_Parts\\"+river

# åˆ›å»ºç›®æ ‡æ–‡ä»¶å¤¹ï¼ˆå¦‚æœä¸å­˜åœ¨ï¼‰
os.makedirs(destination_folder, exist_ok=True)

# è¯»å– COMID æ–‡ä»¶å¤¹ä¸­çš„æ–‡ä»¶åï¼ˆå»æ‰æ‰©å±•åï¼Œå¹¶å­˜å…¥é›†åˆä»¥æé«˜åŒ¹é…æ•ˆç‡ï¼‰
try:
    comid_files = {os.path.splitext(file)[0] for file in os.listdir(comid_folder) if file.endswith('.xlsx')}
    print(f"âœ… è¯»å– COMID æ–‡ä»¶å¤¹å®Œæˆï¼Œå…± {len(comid_files)} ä¸ªæ–‡ä»¶")
except Exception as e:
    print(f"âŒ è¯»å– COMID æ–‡ä»¶å¤¹æ—¶å‘ç”Ÿé”™è¯¯: {e}")
    exit(1)  # ç»ˆæ­¢ç¨‹åº

# è®¡æ•°å™¨
copied_count = 0

# éå† discharge æ–‡ä»¶å¤¹ä¸­çš„ CSV æ–‡ä»¶
try:
    for file_name in os.listdir(discharge_folder):
        if file_name.endswith('.csv'):
            file_base_name = os.path.splitext(file_name)[0]

            # ä»…å¤„ç†åŒ¹é…çš„æ–‡ä»¶
            if file_base_name in comid_files:
                source_path = os.path.join(discharge_folder, file_name)
                destination_path = os.path.join(destination_folder, file_name)

                # å¤åˆ¶æ–‡ä»¶
                shutil.copy2(source_path, destination_path)  # `copy2` ä¿ç•™å…ƒæ•°æ®
                copied_count += 1
                print(f"âœ… å·²å¤åˆ¶: {file_name} â†’ {destination_folder}")

except Exception as e:
    print(f"âŒ å¤„ç† CSV æ–‡ä»¶æ—¶å‘ç”Ÿé”™è¯¯: {e}")
    exit(1)  # ç»ˆæ­¢ç¨‹åº

# æœ€ç»ˆè¾“å‡º
if copied_count == 0:
    print("âš ï¸ æ²¡æœ‰æ‰¾åˆ°åŒ¹é…çš„æ–‡ä»¶ï¼Œæœªè¿›è¡Œå¤åˆ¶ã€‚")
else:
    print(f"ğŸ‰ å¤åˆ¶å®Œæˆï¼Œå…± {copied_count} ä¸ªæ–‡ä»¶å·²æˆåŠŸå¤åˆ¶åˆ° {destination_folder}")
