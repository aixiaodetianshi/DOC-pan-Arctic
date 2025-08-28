# è®¡ç®—æ€è·¯
# è¯»å–æ‰€æœ‰æ²³æµçš„ Total_DOC æ•°æ®
#
# æ•°æ®ä½äº "D:\UZH\2024\20240122 Nutrient and Organic Carbon references\DOC\DOC_update_20250203\Total_DOC_annual"
# è¿™ä¸ªç›®å½•ä¸‹æœ‰ 6 ä¸ªå­æ–‡ä»¶å¤¹ï¼Œæ¯ä¸ªå­æ–‡ä»¶å¤¹é‡Œæœ‰å¤šä¸ª .csv æ–‡ä»¶ï¼ˆä»¥æ²³æµç¼–å·å‘½åï¼‰
# æ¯ä¸ª .csv æ–‡ä»¶åŒ…å« 3 åˆ—ï¼šyear, Total_DOC, Total_DOC_uncertainty
# éœ€è¦åˆ†æ 1984-2018 å¹´çš„ Total_DOC å˜åŒ–
# ä½¿ç”¨æœ€å°äºŒä¹˜æ³•çº¿æ€§å›å½’
#
# è®¾ year ä¸º Xï¼ŒTotal_DOC ä¸º Y
# ç”¨ çº¿æ€§å›å½’å…¬å¼ è®¡ç®—æ–œç‡ï¼ˆslopeï¼‰ï¼Œå³ å¹´å¢é•¿ç‡
# ğ‘Œ
# =
# ğ‘
# ğ‘‹
# +
# ğ‘
# Y=aX+b
# å…¶ä¸­ aï¼ˆæ–œç‡ï¼‰å³ä¸ºå¹´å¢é•¿ç‡
# ä¿å­˜ç»“æœ
#
# ç»“æœå­˜æ”¾åœ¨ "D:\UZH\2024\20240122 Nutrient and Organic Carbon references\DOC\DOC_update_20250203\Total_DOC_average"
# è¾“å‡ºæ–‡ä»¶åä¸º "annual_increase_rate_Total_DOC.csv"
# æ–‡ä»¶æ ¼å¼ï¼šCOMID, Annual_Increase_Rate

import os
import pandas as pd
import numpy as np
from scipy.stats import linregress

# å®šä¹‰è¾“å…¥å’Œè¾“å‡ºæ–‡ä»¶å¤¹è·¯å¾„
input_folder = r"D:\UZH\2024\20240122 Nutrient and Organic Carbon references\3_river_mouth_DOC\DOC_update_20250203\Total_DOC_annual"
output_folder = r"D:\UZH\2024\20240122 Nutrient and Organic Carbon references\3_river_mouth_DOC\DOC_update_20250203\Total_DOC_increase_rate"
output_file = os.path.join(output_folder, "annual_increase_rate_Total_DOC.csv")

# ç¡®ä¿è¾“å‡ºæ–‡ä»¶å¤¹å­˜åœ¨
os.makedirs(output_folder, exist_ok=True)

# å­˜å‚¨è®¡ç®—ç»“æœçš„åˆ—è¡¨
results = []

# éå†6ä¸ªå­æ–‡ä»¶å¤¹
for subfolder in os.listdir(input_folder):
    subfolder_path = os.path.join(input_folder, subfolder)

    if os.path.isdir(subfolder_path):  # ä»…å¤„ç†æ–‡ä»¶å¤¹
        for file_name in os.listdir(subfolder_path):
            if file_name.endswith(".csv"):
                file_path = os.path.join(subfolder_path, file_name)

                # è¯»å– CSV æ–‡ä»¶
                df = pd.read_csv(file_path)

                # æ£€æŸ¥æ˜¯å¦å­˜åœ¨æ‰€éœ€åˆ—
                if {'year', 'Total_DOC'}.issubset(df.columns):
                    # é€‰æ‹© 1984-2018 å¹´çš„æ•°æ®
                    df_filtered = df[(df['year'] >= 1984) & (df['year'] <= 2018)].dropna()

                    if len(df_filtered) >= 5:  # è‡³å°‘5ä¸ªæ•°æ®ç‚¹æ‰èƒ½æ‹Ÿåˆ
                        years = df_filtered['year'].values
                        doc_values = df_filtered['Total_DOC'].values

                        # è¿›è¡Œæœ€å°äºŒä¹˜æ³•çº¿æ€§æ‹Ÿåˆ
                        slope, intercept, r_value, p_value, std_err = linregress(years, doc_values)

                        # è·å–æ²³æµç¼–å·ï¼ˆæ–‡ä»¶åå»æ‰æ‰©å±•åï¼‰
                        river_id = os.path.splitext(file_name)[0]

                        # æ·»åŠ åˆ°ç»“æœåˆ—è¡¨
                        results.append({
                            'COMID': river_id,
                            'Annual_Increase_Rate': slope,
                            'Intercept': intercept,
                            'R_Value': r_value,
                            'P_Value': p_value,
                            'Std_Err': std_err
                        })

                else:
                    print(f"âŒ è­¦å‘Š: æ–‡ä»¶ {file_name} ç¼ºå°‘æ‰€éœ€åˆ—ï¼Œå·²è·³è¿‡")

# å°†ç»“æœè½¬æ¢ä¸º DataFrame
results_df = pd.DataFrame(results)

# ä¿å­˜ä¸º CSV æ–‡ä»¶
results_df.to_csv(output_file, index=False)

print(f"âœ… è®¡ç®—å®Œæˆï¼Œç»“æœå·²ä¿å­˜åˆ° {output_file}")
