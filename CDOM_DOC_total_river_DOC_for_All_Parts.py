import os
import pandas as pd

# 输入和输出路径
input_folder = r"D:\UZH\2024\20240122 Nutrient and Organic Carbon references\3_river_mouth_DOC\DOC_update_20250203\Total_DOC_average"
output_file = r"D:\UZH\2024\20240122 Nutrient and Organic Carbon references\3_river_mouth_DOC\DOC_update_20250203\Total_DOC_average\Total_DOC_annual_All_Parts.csv"

# 指定6个目标文件
target_files = [
    "Total_DOC_annual_Ob_Parts.csv",
    "Total_DOC_annual_Yenisey_Parts.csv",
    "Total_DOC_annual_Lena_Parts.csv",
    "Total_DOC_annual_Kolyma_Parts.csv",
    "Total_DOC_annual_Yukon_Parts.csv",
    "Total_DOC_annual_Mackenzie_Parts.csv"
]

# 初始化列表
total_doc_list = []
total_doc_uncertainty_list = []

# 遍历指定文件
for file in target_files:
    file_path = os.path.join(input_folder, file)
    if os.path.exists(file_path):
        df = pd.read_csv(file_path)

        # 检查列名是否符合预期
        if set(['year', 'Total_DOC_Annual', 'Total_DOC_Annual_Uncertainty']).issubset(df.columns):
            df['year'] = df['year'].astype(int)
            total_doc_list.append(df[['year', 'Total_DOC_Annual']])
            total_doc_uncertainty_list.append(df[['year', 'Total_DOC_Annual_Uncertainty']])
        else:
            print(f"文件 {file} 缺少所需列，已跳过。")
    else:
        print(f"文件 {file} 不存在，已跳过。")

# 合并并按年聚合
doc_df = pd.concat(total_doc_list, ignore_index=True).groupby('year', as_index=False).sum()
uncertainty_df = pd.concat(total_doc_uncertainty_list, ignore_index=True).groupby('year', as_index=False).sum()

# 合并两个 DataFrame
final_df = pd.merge(doc_df, uncertainty_df, on='year', how='inner')

# 保存结果
final_df.to_csv(output_file, index=False)
print(f"汇总结果已保存至：{output_file}")
