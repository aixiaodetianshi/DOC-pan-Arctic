import pandas as pd
import os

input_folder = r'D:\UZH\2024\20240122 Nutrient and Organic Carbon references\Linear_Regression_DOC_CDOM\2_Enhance_Number_In_situ_Samples_CDOM\3_Enhanced_In_situ_CDOM'
output_folder = input_folder

for file in os.listdir(input_folder):
    if file.endswith('.xlsx'):
        try:
            xlsx_path = os.path.join(input_folder, file)
            csv_path = os.path.join(output_folder, file.replace('.xlsx', '.csv'))

            df = pd.read_excel(xlsx_path)
            df = df.dropna(how='all')
            df.columns = [col.strip() for col in df.columns]

            if 'Date' not in df.columns or 'CDOM' not in df.columns:
                print(f"❌ Missing 'Date' or 'CDOM' column in {file}")
                continue

            if pd.api.types.is_numeric_dtype(df['Date']):
                df['Date'] = pd.to_datetime('1899-12-30') + pd.to_timedelta(df['Date'], unit='D')
            else:
                df['Date'] = pd.to_datetime(df['Date'], errors='coerce')

            df = df.dropna(subset=['Date', 'CDOM'])

            # 格式化日期为字符串（不加引号，不加零宽空格）
            df['Date'] = df['Date'].dt.strftime('%Y-%m-%d %H:%M:%S')

            # 保存为无 BOM 的 UTF-8 编码
            df.to_csv(csv_path, index=False, encoding='utf-8')

            print(f"✔ Saved cleaned CSV (no BOM): {csv_path}")

        except Exception as e:
            print(f"❌ Error processing {file}: {e}")
