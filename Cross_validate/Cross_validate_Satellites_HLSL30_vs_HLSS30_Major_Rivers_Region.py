# 实现功能：1.读取文件夹D:\UZH\2024\20240122 Nutrient and Organic Carbon references\3_river_mouth_DOC\DOC_update_20250203\HLSL30  # English: Implement functions
# 里面的所有HLSL30_Kolyma_CDOM_*_DOC.csv数据，读取数据列COMID，date和DOC三列，  # English: Everything inside
# 同时读取文件夹D:\UZH\2024\20240122 Nutrient and Organic Carbon references\3_river_mouth_DOC\DOC_update_20250203\HLSS30  # English: Read folders at the same time
# 里面的所有HLSS30_Kolyma_CDOM_*_DOC.csv数据，读取数据列COMID，date和DOC三列，  # English: Everything inside
# 获取量数据中相同COMID和相同date的DOC配对，如果有多个相同日期出现，则计算对应DOC的平均值，将匹配结果按照四列：COMID，date, DOC_HLSL30和DOC_HLSS30保存，  # English: The same amount of data is obtained
# 保存在文件夹D:\UZH\2024\20240122 Nutrient and Organic Carbon references\1_Linear_Regression_DOC_CDOM\4_Cross_Validate_Landsat_5_Landsat7_HLSL30_HLSS30_DOC\Six_Major_Rivers_Regions_Cross_Validation\HLSL30_calibrate_HLSS30中，  # English: Save in folder
# 文件命名为Cross_validate_DOC_Kolyma.csv；  # English: The file name is
# 后面计算两数据的系统偏差 system diff，计算R2，RMSE，Pearson系数和p值。  # English: The system deviation of the two data is calculated later
# 将结果保存在文件夹D:\UZH\2024\20240122 Nutrient and Organic Carbon references\1_Linear_Regression_DOC_CDOM\4_Cross_Validate_Landsat_5_Landsat7_HLSL30_HLSS30_DOC\Six_Major_Rivers_Regions_Cross_Validation\HLSL30_calibrate_HLSS30中，  # English: Save the results in a folder
# 文件命名为Cross_validate_DOC_evaluation_Kolyma.csv.  # English: The file name is

import os
import pandas as pd
from glob import glob
from scipy.stats import pearsonr
from sklearn.metrics import mean_squared_error, r2_score
import numpy as np

# 路径定义  # English: Path definition
hlsl30_dir = r"D:\UZH\2024\20240122 Nutrient and Organic Carbon references\3_river_mouth_DOC\DOC_update_20250203\HLSL30"
hlss30_dir = r"D:\UZH\2024\20240122 Nutrient and Organic Carbon references\3_river_mouth_DOC\DOC_update_20250203\HLSS30"
output_dir = r"D:\UZH\2024\20240122 Nutrient and Organic Carbon references\1_Linear_Regression_DOC_CDOM\4_Cross_Validate_Landsat_5_Landsat7_HLSL30_HLSS30_DOC\Six_Major_Rivers_Regions_Cross_Validation\HLSL30_calibrate_HLSS30"

river = "Yenisey"

# 文件读取  # English: File reading
hlsl30_files = glob(os.path.join(hlsl30_dir, "HLSL30_"+river+"_CDOM_DOC.csv"))
hlss30_files = glob(os.path.join(hlss30_dir, "HLSS30_"+river+"_CDOM_DOC.csv"))

output_csv_path = os.path.join(output_dir, "Cross_validate_DOC_"+river+".csv")
eval_csv_path = os.path.join(output_dir, "Cross_validate_DOC_evaluation_"+river+".csv")

# 读取并合并数据  # English: Read and merge data
def load_and_merge(files, source_label):
    df_list = []
    for file in files:
        df = pd.read_csv(file, usecols=["COMID", "date", "DOC"])
        df["date"] = pd.to_datetime(df["date"])
        df_list.append(df)
    df_all = pd.concat(df_list, ignore_index=True)
    df_all.rename(columns={"DOC": f"DOC_{source_label}"}, inplace=True)
    return df_all

df_hlsl30 = load_and_merge(hlsl30_files, "HLSL30")
df_hlss30 = load_and_merge(hlss30_files, "HLSS30")

# 合并数据，按 COMID 和 date 匹配  # English: Merge data
df_merged = pd.merge(df_hlsl30, df_hlss30, on=["COMID", "date"], how="inner")

# 保存匹配结果  # English: Save the matching results

df_merged.to_csv(output_csv_path, index=False)

# 仅保留 DOC 值都小于等于 20 的记录，剔除异常高值  # English: Keep only
df_merged = df_merged[(df_merged["DOC_HLSL30"] <= 20) & (df_merged["DOC_HLSS30"] <= 20)].copy()

# 计算系统偏差、R2、RMSE、Pearson 相关系数和 p 值  # English: Calculate system deviation
system_diff = (df_merged["DOC_HLSL30"] - df_merged["DOC_HLSS30"]).mean()
r2 = r2_score(df_merged["DOC_HLSS30"], df_merged["DOC_HLSL30"])
rmse = np.sqrt(mean_squared_error(df_merged["DOC_HLSS30"], df_merged["DOC_HLSL30"]))
pearson_r, p_value = pearsonr(df_merged["DOC_HLSS30"], df_merged["DOC_HLSL30"])

# 保存评估结果  # English: Save the evaluation results
eval_df = pd.DataFrame({
    "Metric": ["System Difference", "R2", "RMSE", "Pearson r", "P-value"],
    "Value": [system_diff, r2, rmse, pearson_r, p_value]
})

eval_df.to_csv(eval_csv_path, index=False)

print("匹配结果已保存到：", output_csv_path)
print("评估结果已保存到：", eval_csv_path)
