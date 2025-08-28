
# LOESS å¹³æ»‘
#
# é‡‡ç”¨ å±€éƒ¨å›å½’å¹³æ»‘ï¼ˆLOWESSï¼‰ï¼Œå¯¹ DOC æ•°æ®è¿›è¡Œéå‚æ•°å›å½’ã€‚
# å‚æ•° frac=0.05 æ§åˆ¶å¹³æ»‘ç¨‹åº¦ï¼Œå¯è°ƒèŠ‚ä½¿æ•°æ® æ—¢å¹³æ»‘åˆä¿ç•™è¶‹åŠ¿ã€‚
# è¿­ä»£ 3 æ¬¡ (it=3) ä»¥å¢å¼ºç¨³å®šæ€§ã€‚
# æ—¶é—´è¿ç»­æ€§
#
# è¯»å–æ–‡ä»¶ä¸­çš„ date åˆ—ï¼Œç¡®ä¿æ—¶é—´æ•°æ® å®Œæ•´æ— ç¼ºå¤±ã€‚
# ç¡®ä¿æ•°æ®æŒ‰æ—¥æœŸ å‡åºæ’åˆ— è¿›è¡Œå¹³æ»‘ã€‚
# é€‚ç”¨æ€§
#
# é€‚ç”¨äº é•¿æœŸç¯å¢ƒæ•°æ®ï¼Œé¿å…ç§»åŠ¨å¹³å‡æ³•å¯èƒ½å¯¼è‡´çš„æ•°æ®å¤±çœŸã€‚
# å¯ç”¨äº å‡å°‘çªå‘æ€§å¼‚å¸¸æ³¢åŠ¨ï¼Œä½†ä»ä¿ç•™ DOC çš„çœŸå®é•¿æœŸå˜åŒ–è¶‹åŠ¿ã€‚


import pandas as pd
import os
from statsmodels.nonparametric.smoothers_lowess import lowess

# æ–‡ä»¶å¤¹è·¯å¾„
input_folder = r"D:\UZH\2024\20240122 Nutrient and Organic Carbon references\DOC\DOC_update_20250203\Combination_single_river_sort_date_pre_process_filldate"
output_folder = r"D:\UZH\2024\20240122 Nutrient and Organic Carbon references\DOC\DOC_update_20250203\Combination_single_river_sort_date_pre_process_smooth"
os.makedirs(output_folder, exist_ok=True)

frac = 0.05  # LOESS å¹³æ»‘å‚æ•°
num_cols = ['CDOM', 'CDOM_uncertainty', 'DOC', 'DOC_uncertainty']

for filename in os.listdir(input_folder):
    if not filename.endswith(".csv"):
        continue

    input_file = os.path.join(input_folder, filename)
    output_file = os.path.join(output_folder, filename)

    try:
        # è¯»å–æ•°æ®
        df = pd.read_csv(input_file, dtype=str)

        # è§£ææ—¥æœŸ
        df['date'] = pd.to_datetime(df['date'], errors='coerce')

        # æ‰¾å‡ºæ— æ³•è§£æçš„æ—¥æœŸ
        invalid_dates = df[df['date'].isna()]
        if not invalid_dates.empty:
            print(f"âš ï¸ æ–‡ä»¶ {filename} å­˜åœ¨æ— æ³•è§£æçš„æ—¥æœŸï¼Œè·³è¿‡ä»¥ä¸‹è¡Œï¼š")
            print(invalid_dates.head())

        # åˆ é™¤æ— æ•ˆæ—¥æœŸ
        df = df.dropna(subset=['date']).sort_values(by='date')

        # ç¡®ä¿æ—¥æœŸè½¬æ¢æˆåŠŸ
        if df.empty:
            print(f"âŒ æ–‡ä»¶ {filename} æ²¡æœ‰æœ‰æ•ˆçš„æ—¥æœŸæ•°æ®ï¼Œè·³è¿‡")
            continue

        # ç¡®ä¿æ•°å€¼åˆ—ä¸º float ç±»å‹
        df[num_cols] = df[num_cols].apply(pd.to_numeric, errors='coerce')

        # è½¬æ¢æ—¥æœŸä¸º Unix æ—¶é—´æˆ³
        date_numeric = df['date'].astype('int64') // 10**9

        # å¯¹æ¯ä¸ªå˜é‡è¿›è¡Œ LOESS å¹³æ»‘
        for col in num_cols:
            valid_data = df[col].dropna()
            if len(valid_data) > 5:
                smoothed_values = lowess(valid_data, date_numeric[valid_data.index], frac=frac, it=3, return_sorted=False)
                df.loc[valid_data.index, col] = smoothed_values

        # çº¿æ€§æ’å€¼å¡«å……
        df[num_cols] = df[num_cols].interpolate(method='linear', limit_direction='both')

        # ä¿å­˜ç»“æœ
        df.to_csv(output_file, index=False)
        print(f"âœ… å¹³æ»‘å®Œæˆ: {filename} -> {output_file}")

    except Exception as e:
        print(f"âŒ å¤„ç†æ–‡ä»¶ {filename} æ—¶æŠ¥é”™: {e}")

print("ğŸ‰ æ‰€æœ‰æ–‡ä»¶å¤„ç†å®Œæˆï¼")
