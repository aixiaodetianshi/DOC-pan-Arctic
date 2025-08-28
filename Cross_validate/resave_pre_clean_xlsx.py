
import pandas as pd
import os

input_folder = r'D:\UZH\2024\20240122 Nutrient and Organic Carbon references\Linear_Regression_DOC_CDOM\2_Enhance_Number_In_situ_Samples_CDOM\2_In_situ_CDOM'
output_folder = r'D:\UZH\2024\20240122 Nutrient and Organic Carbon references\Linear_Regression_DOC_CDOM\2_Enhance_Number_In_situ_Samples_CDOM'

for file in os.listdir(input_folder):
    if file.endswith('.xlsx'):
        xlsx_path = os.path.join(input_folder, file)
        out_path = os.path.join(output_folder, file)

        # 读取第一个sheet  # English: Read the first one
        df = pd.read_excel(xlsx_path)
        print(df)
        # 去除全空行  # English: Remove all empty lines
        df = df.dropna(how='all')

        df.to_excel(out_path, index=False)
