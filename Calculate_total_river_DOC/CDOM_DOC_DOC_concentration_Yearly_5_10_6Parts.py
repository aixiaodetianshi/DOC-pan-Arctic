# 计算 1984-2018年期间河流中DOC concentration  # English: calculate
# 5-10月  # English: moon

import os
import pandas as pd

# 设置文件夹路径  # English: Set folder path
input_folder = r"D:\UZH\2024\20240122 Nutrient and Organic Carbon references\DOC\DOC_update_20250203\Combination_single_river_sort_date_pre_process_filldate_combine_discharge\Mackenzie"
output_file = r"D:\UZH\2024\20240122 Nutrient and Organic Carbon references\DOC\DOC_update_20250203\DOC_concentration\Mackenzie_DOC_concentration.csv"

# 初始化存储年均值的字典  # English: Initialize the dictionary that stores annual averages
avg_per_year = {}

# 遍历文件夹中的所有 CSV 文件  # English: Iterate through all the folders
for file in os.listdir(input_folder):
    if file.endswith(".csv"):
        file_path = os.path.join(input_folder, file)

        # 读取 CSV 文件  # English: Read
        df = pd.read_csv(file_path, parse_dates=["date"])

        # 确保包含所需列  # English: Make sure to include the required columns
        required_columns = {"date", "DOC", "CDOM", "CDOM_uncertainty", "DOC_uncertainty", "discharge"}
        if required_columns.issubset(df.columns):
            df["year"] = df["date"].dt.year
            df["month"] = df["date"].dt.month

            # 筛选 5-10 月数据  # English: filter
            df_filtered = df[(df["month"] >= 5) & (df["month"] <= 10)]

            # 计算每年 5-10 月的平均值  # English: Calculate annually
            yearly_avg = df_filtered.groupby("year")[
                ["DOC", "CDOM", "CDOM_uncertainty", "DOC_uncertainty", "discharge"]].mean()

            # 存储到字典  # English: Store to dictionary
            for year, row in yearly_avg.iterrows():
                if 1984 <= year <= 2018:
                    if year not in avg_per_year:
                        avg_per_year[year] = {"DOC": [], "CDOM": [], "CDOM_uncertainty": [], "DOC_uncertainty": [],
                                              "discharge": []}
                    for col in ["DOC", "CDOM", "CDOM_uncertainty", "DOC_uncertainty", "discharge"]:
                        avg_per_year[year][col].append(row[col])

# 计算每年的总体平均值  # English: Calculate the overall average for each year
final_data = {year: {col: sum(values) / len(values) for col, values in data.items()} for year, data in
              avg_per_year.items()}

# 转换为 DataFrame 并保存  # English: Convert to
output_df = pd.DataFrame.from_dict(final_data, orient="index").reset_index()
output_df.rename(columns={"index": "year"}, inplace=True)
output_df.sort_values(by="year", inplace=True)
output_df.to_csv(output_file, index=False)

print("计算完成，结果已保存到", output_file)