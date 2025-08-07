# 实现功能：1.读取文件夹D:\UZH\2024\20240122 Nutrient and Organic Carbon references\3_river_mouth_DOC\DOC_update_20250203\HLSL30
# 里面的所有HLSL30_Kolyma_CDOM_*_DOC.csv数据，读取数据列COMID，date和DOC三列，
# 同时读取文件夹D:\UZH\2024\20240122 Nutrient and Organic Carbon references\3_river_mouth_DOC\DOC_update_20250203\HLSS30
# 里面的所有HLSS30_Kolyma_CDOM_*_DOC.csv数据，读取数据列COMID，date和DOC三列，
# 获取量数据中相同COMID和相同date的DOC配对，如果有多个相同日期出现，则计算对应DOC的平均值，将匹配结果按照四列：COMID，date, DOC_HLSL30和DOC_HLSS30保存，
# 保存在文件夹D:\UZH\2024\20240122 Nutrient and Organic Carbon references\1_Linear_Regression_DOC_CDOM\4_Cross_Validate_Landsat_5_Landsat7_HLSL30_HLSS30_DOC\Six_Major_Rivers_Regions_Cross_Validation\HLSL30_calibrate_HLSS30中，
# 文件命名为Cross_validate_DOC_Kolyma.csv；
# 后面计算两数据的系统偏差 system diff，计算R2，RMSE，Pearson系数和p值。
# 将结果保存在文件夹D:\UZH\2024\20240122 Nutrient and Organic Carbon references\1_Linear_Regression_DOC_CDOM\4_Cross_Validate_Landsat_5_Landsat7_HLSL30_HLSS30_DOC\Six_Major_Rivers_Regions_Cross_Validation\HLSL30_calibrate_HLSS30中，
# 文件命名为Cross_validate_DOC_evaluation_Kolyma.csv.

import os
import pandas as pd
from glob import glob
from scipy.stats import pearsonr
from sklearn.metrics import mean_squared_error, r2_score
import numpy as np

# 路径定义
hlsl30_dir = r"D:\UZH\2024\20240122 Nutrient and Organic Carbon references\3_river_mouth_DOC\DOC_update_20250203\HLSL30"
landsat7_dir = r"D:\UZH\2024\20240122 Nutrient and Organic Carbon references\3_river_mouth_DOC\DOC_update_20250203\Landsat7"
output_dir = r"D:\UZH\2024\20240122 Nutrient and Organic Carbon references\1_Linear_Regression_DOC_CDOM\4_Cross_Validate_Landsat_5_Landsat7_HLSL30_HLSS30_DOC\Six_Major_Rivers_Regions_Cross_Validation\HLSL30_calibrate_Landsat7"

# 文件读取
river = "Yenisey"
hlsl30_files = glob(os.path.join(hlsl30_dir, "HLSL30_"+river+"_CDOM_*DOC.csv"))
landsat7_files = glob(os.path.join(landsat7_dir, "Landsat7_"+river+"_CDOM_*DOC.csv"))

output_csv_path = os.path.join(output_dir, "Cross_validate_DOC_"+river+".csv")
eval_csv_path = os.path.join(output_dir, "Cross_validate_DOC_evaluation_"+river+".csv")

# 读取并合并数据
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
df_landsat7 = load_and_merge(landsat7_files, "Landsat7")

# 合并数据，按 COMID 和 date 匹配
df_merged = pd.merge(df_hlsl30, df_landsat7, on=["COMID", "date"], how="inner")

# 保存匹配结果

df_merged.to_csv(output_csv_path, index=False)

# 仅保留 DOC 值都小于等于 20 的记录，剔除异常高值
df_merged = df_merged[(df_merged["DOC_HLSL30"] <= 20) & (df_merged["DOC_Landsat7"] <= 20)].copy()

# 计算系统偏差、R2、RMSE、Pearson 相关系数和 p 值
system_diff = (df_merged["DOC_HLSL30"] - df_merged["DOC_Landsat7"]).mean()
r2 = r2_score(df_merged["DOC_Landsat7"], df_merged["DOC_HLSL30"])
rmse = np.sqrt(mean_squared_error(df_merged["DOC_Landsat7"], df_merged["DOC_HLSL30"]))
pearson_r, p_value = pearsonr(df_merged["DOC_Landsat7"], df_merged["DOC_HLSL30"])

# 保存评估结果
eval_df = pd.DataFrame({
    "Metric": ["System Difference", "R2", "RMSE", "Pearson r", "P-value"],
    "Value": [system_diff, r2, rmse, pearson_r, p_value]
})

eval_df.to_csv(eval_csv_path, index=False)

print("匹配结果已保存到：", output_csv_path)
print("评估结果已保存到：", eval_csv_path)
