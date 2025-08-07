import os
import pandas as pd
from glob import glob
from scipy.stats import pearsonr
from sklearn.metrics import mean_squared_error, r2_score
import numpy as np
from tqdm import tqdm

# 路径定义
hlsl30_dir = r"D:\UZH\2024\20240122 Nutrient and Organic Carbon references\3_river_mouth_DOC\DOC_update_20250203\HLSL30"
landsat7_dir = r"D:\UZH\2024\20240122 Nutrient and Organic Carbon references\3_river_mouth_DOC\DOC_update_20250203\Landsat7"
output_dir = r"D:\UZH\2024\20240122 Nutrient and Organic Carbon references\1_Linear_Regression_DOC_CDOM\4_Cross_Validate_Landsat_5_Landsat7_HLSL30_HLSS30_DOC\Six_Major_Rivers_Regions_Cross_Validation\HLSL30_calibrate_Landsat7"

river = 'Yenisey'

# 查找文件
hlsl30_files = glob(os.path.join(hlsl30_dir, f"HLSL30_{river}_CDOM_DOC.csv"))
landsat7_files = glob(os.path.join(landsat7_dir, f"Landsat7_{river}_CDOM_DOC.csv"))

output_csv_path = os.path.join(output_dir, f"Cross_validate_DOC_{river}.csv")
eval_csv_path = os.path.join(output_dir, f"Cross_validate_DOC_evaluation_{river}.csv")

# 读取并合并数据
def load_and_merge(files, source_label):
    df_list = []
    for file in files:
        df = pd.read_csv(file, usecols=["COMID", "date", "DOC"])
        df["date"] = pd.to_datetime(df["date"])
        df_list.append(df)
    df_all = pd.concat(df_list, ignore_index=True)
    df_all = df_all.groupby(["COMID", "date"]).mean().reset_index()
    df_all.rename(columns={"DOC": f"DOC_{source_label}"}, inplace=True)
    return df_all

df_hlsl30 = load_and_merge(hlsl30_files, "HLSL30")
df_landsat7 = load_and_merge(landsat7_files, "Landsat7")

# 创建索引以加速匹配
df_landsat7.set_index("COMID", inplace=True)
results = []

# 按照±1天范围匹配相同 COMID 的数据
print("开始匹配数据（±1天）...")
for _, row in tqdm(df_hlsl30.iterrows(), total=len(df_hlsl30)):
    comid = row["COMID"]
    date = row["date"]
    doc_hlsl30 = row["DOC_HLSL30"]

    if comid not in df_landsat7.index:
        continue

    sub_df = df_landsat7.loc[[comid]]
    if isinstance(sub_df, pd.Series):  # 若只有一条记录则转为DataFrame
        sub_df = pd.DataFrame([sub_df])

    # 筛选±1天的数据
    sub_df = sub_df[(sub_df["date"] >= date - pd.Timedelta(days=1)) &
                    (sub_df["date"] <= date + pd.Timedelta(days=1))]

    if not sub_df.empty:
        doc_landsat7_mean = sub_df["DOC_Landsat7"].mean()
        results.append({
            "COMID": comid,
            "date": date.strftime("%Y-%m-%d"),
            "DOC_HLSL30": doc_hlsl30,
            "DOC_Landsat7": doc_landsat7_mean
        })

# 转换为 DataFrame 并保存
df_result = pd.DataFrame(results)

# 仅保留 DOC 值都小于等于 20 的记录，剔除异常高值
df_result = df_result[(df_result["DOC_HLSL30"] <= 20) & (df_result["DOC_Landsat7"] <= 20)].copy()

df_result.to_csv(output_csv_path, index=False)
print("匹配结果已保存到：", output_csv_path)

# 评估指标计算
if not df_result.empty:

    system_diff = (df_result["DOC_HLSL30"] - df_result["DOC_Landsat7"]).mean()
    r2 = r2_score(df_result["DOC_Landsat7"], df_result["DOC_HLSL30"])
    rmse = np.sqrt(mean_squared_error(df_result["DOC_Landsat7"], df_result["DOC_HLSL30"]))
    pearson_r, p_value = pearsonr(df_result["DOC_Landsat7"], df_result["DOC_HLSL30"])

    eval_df = pd.DataFrame({
        "Metric": ["System Difference", "R2", "RMSE", "Pearson r", "P-value"],
        "Value": [system_diff, r2, rmse, pearson_r, p_value]
    })
    eval_df.to_csv(eval_csv_path, index=False)
    print("评估结果已保存到：", eval_csv_path)
else:
    print("未匹配到任何数据，评估结果未生成。")
