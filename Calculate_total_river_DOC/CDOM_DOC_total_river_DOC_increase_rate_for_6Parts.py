# è®¡ç®—æ€è·¯
# è¯»å–æ‰€æœ‰æ²³æµçš„ Total_DOC æ•°æ®
#
# è®¡ç®—æ¯ä¸ªæµåŸŸåˆ†åŒºå†…çš„å¢é•¿ç‡
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


import pandas as pd
import numpy as np
from scipy.stats import linregress

# è¾“å…¥æ–‡ä»¶è·¯å¾„
input_file = r"D:\UZH\2024\20240122 Nutrient and Organic Carbon references\DOC\DOC_update_20250203\Total_DOC_average\Total_DOC_annual_All_Parts.csv"

# è¯»å– CSV æ–‡ä»¶
df = pd.read_csv(input_file)

# æ£€æŸ¥æ˜¯å¦åŒ…å«æ‰€éœ€åˆ—
if {'year', 'Total_DOC_Annual'}.issubset(df.columns):
    # é€‰æ‹© 1984-2018 å¹´çš„æ•°æ®
    df_filtered = df[(df['year'] >= 1984) & (df['year'] <= 2018)].dropna()

    if len(df_filtered) >= 5:  # è‡³å°‘5ä¸ªæ•°æ®ç‚¹æ‰èƒ½è¿›è¡Œçº¿æ€§å›å½’
        years = df_filtered['year'].values
        doc_values = df_filtered['Total_DOC_Annual'].values

        # è¿›è¡Œæœ€å°äºŒä¹˜æ³•çº¿æ€§æ‹Ÿåˆ
        slope, intercept, r_value, p_value, std_err = linregress(years, doc_values)

        # åœ¨å±å¹•ä¸Šè¾“å‡ºç»“æœ
        print(f"ğŸ“Š **Ob æ²³æµ Total_DOC å¹´å¢é•¿ç‡åˆ†æç»“æœ** ğŸ“Š")
        print(f"å¹´å¢é•¿ç‡ (Annual Increase Rate): {slope:.6f} Tg C/yrÂ²")
        print(f"æˆªè· (Intercept): {intercept:.6f}")
        print(f"ç›¸å…³ç³»æ•° (R å€¼): {r_value:.6f}")
        print(f"P å€¼ (P-Value): {p_value:.6f}")
        print(f"æ ‡å‡†è¯¯å·® (Std Err): {std_err:.6f}")

    else:
        print("âŒ æ•°æ®ç‚¹ä¸è¶³ï¼Œæ— æ³•è¿›è¡Œçº¿æ€§å›å½’åˆ†æ")
else:
    print("âŒ è¯»å–å¤±è´¥ï¼šæ–‡ä»¶ç¼ºå°‘å¿…è¦çš„åˆ— 'year' æˆ– 'Total_DOC_Annual'")

