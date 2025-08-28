import os
import pandas as pd

# å®šä¹‰æ–‡ä»¶å¤¹è·¯å¾„
river = "Yukon"
doc_folder = r"D:\UZH\2024\20240122 Nutrient and Organic Carbon references\3_river_mouth_DOC\DOC_update_20250203\Combination_single_river_sort_date_pre_process_6_Parts\\" + river
discharge_folder = r"D:\UZH\2024\20240122 Nutrient and Organic Carbon references\0_0_river_mouth_discharge\river_discharge\\" + river
output_folder = r"D:\UZH\2024\20240122 Nutrient and Organic Carbon references\3_river_mouth_DOC\DOC_update_20250203\Combination_single_river_sort_date_pre_process_filldate_combine_discharge\\" + river

# åˆ›å»ºç›®æ ‡æ–‡ä»¶å¤¹ï¼ˆå¦‚æœä¸å­˜åœ¨ï¼‰
os.makedirs(output_folder, exist_ok=True)

# è·å– DOC ç›®å½•ä¸‹çš„æ‰€æœ‰ CSV æ–‡ä»¶
doc_files = [f for f in os.listdir(doc_folder) if f.endswith('.csv')]

# å¤„ç†æ¯ä¸ª DOC æ–‡ä»¶
for doc_file in doc_files:
    doc_path = os.path.join(doc_folder, doc_file)
    discharge_path = os.path.join(discharge_folder, doc_file.replace('.csv', '.xlsx'))
    output_path = os.path.join(output_folder, doc_file)

    # æ£€æŸ¥å¯¹åº”çš„ discharge æ–‡ä»¶æ˜¯å¦å­˜åœ¨
    if not os.path.exists(discharge_path):
        print(f"âš ï¸ æœªæ‰¾åˆ°å¯¹åº”çš„ discharge æ–‡ä»¶: {discharge_path}, è·³è¿‡ {doc_file}")
        continue

    # è¯»å– DOC æ•°æ®
    try:
        doc_df = pd.read_csv(doc_path)
    except Exception as e:
        print(f"âŒ è¯»å– DOC æ–‡ä»¶å¤±è´¥: {doc_file}, é”™è¯¯: {e}")
        continue

    # è¯»å– discharge æ•°æ®
    try:
        discharge_df = pd.read_excel(discharge_path)
    except Exception as e:
        print(f"âŒ è¯»å– discharge æ–‡ä»¶å¤±è´¥: {discharge_path}, é”™è¯¯: {e}")
        continue

    # ç¡®ä¿åˆ—åæ­£ç¡®
    expected_doc_columns = ['date', 'CDOM', 'CDOM_uncertainty', 'DOC', 'DOC_uncertainty']
    expected_discharge_columns = ['time', 'discharge']

    if list(doc_df.columns)[:5] != expected_doc_columns:
        print(
            f"âš ï¸ DOC æ–‡ä»¶åˆ—åä¸åŒ¹é…: {doc_file}, æœŸæœ›: {expected_doc_columns}, ä½†è¯»å–åˆ°: {list(doc_df.columns)}ï¼Œè·³è¿‡ã€‚")
        continue

    if list(discharge_df.columns)[:2] != expected_discharge_columns:
        print(
            f"âš ï¸ Discharge æ–‡ä»¶åˆ—åä¸åŒ¹é…: {doc_file}, æœŸæœ›: {expected_discharge_columns}, ä½†è¯»å–åˆ°: {list(discharge_df.columns)}ï¼Œè·³è¿‡ã€‚")
        continue

    # æ ¼å¼åŒ–æ—¥æœŸ
    doc_df['date'] = pd.to_datetime(doc_df['date'])
    discharge_df['time'] = pd.to_datetime(discharge_df['time'])

    # åˆå¹¶æ•°æ®ï¼ˆå·¦è¿æ¥ï¼Œç¡®ä¿æ‰€æœ‰ DOC æ•°æ®ä¿ç•™ï¼‰
    merged_df = pd.merge(doc_df, discharge_df, left_on='date', right_on='time', how='left')

    # åˆ é™¤ time åˆ—ï¼Œä»…ä¿ç•™ discharge
    merged_df.drop(columns=['time'], inplace=True)

    # ä¿å­˜åˆå¹¶åçš„æ–‡ä»¶
    try:
        merged_df.to_csv(output_path, index=False)
        print(f"âœ… åˆå¹¶å®Œæˆ: {output_path}")
    except Exception as e:
        print(f"âŒ ä¿å­˜æ–‡ä»¶å¤±è´¥: {output_path}, é”™è¯¯: {e}")

print("ğŸ‰ æ‰€æœ‰åŒ¹é…çš„ DOC æ–‡ä»¶å·²æˆåŠŸåˆå¹¶å¹¶ä¿å­˜ï¼")

