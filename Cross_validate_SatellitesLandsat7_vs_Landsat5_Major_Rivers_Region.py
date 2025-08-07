# 使用系统偏差校准过得Landsat7 来验证Landsat 5
import os
import pandas as pd
from glob import glob
from scipy.stats import pearsonr
from sklearn.metrics import mean_squared_error, r2_score
import numpy as np
from tqdm import tqdm

# 路径定义
landsat7_dir = r"D:\UZH\2024\20240122 Nutrient and Organic Carbon references\3_river_mouth_DOC\DOC_update_20250203\Landsat7"
landsat5_dir = r"D:\UZH\2024\20240122 Nutrient and Organic Carbon references\3_river_mouth_DOC\DOC_update_20250203\Landsat5"
output_dir = r"D:\UZH\2024\20240122 Nutrient and Organic Carbon references\1_Linear_Regression_DOC_CDOM\4_Cross_Validate_Landsat_5_Landsat7_HLSL30_HLSS30_DOC\Six_Major_Rivers_Regions_Cross_Validation\L7_calibrate_L5"

river = "Yenisey"
HLSL30_L7_system_dif = -10.03296352

# 查找文件
landsat7_files = glob(os.path.join(landsat7_dir, f"Landsat7_{river}_CDOM_DOC.csv"))
landsat5_files = glob(os.path.join(landsat5_dir, f"Landsat5_{river}_CDOM_DOC.csv"))

output_csv_path = os.path.join(output_dir, f"Cross_validate_DOC_{river}.csv")
eval_csv_path = os.path.join(output_dir, f"Cross_validate_DOC_evaluation_{river}.csv")

# 读取并合并数据
def load_and_merge(files, sys_dif, source_label):
    df_list = []
    for file in files:
        df = pd.read_csv(file, usecols=["COMID", "date", "DOC"])
        df["date"] = pd.to_datetime(df["date"])
        df["DOC"] = df["DOC"] + sys_dif
        df_list.append(df)
    df_all = pd.concat(df_list, ignore_index=True)
    df_all = df_all.groupby(["COMID", "date"]).mean().reset_index()
    df_all.rename(columns={"DOC": f"DOC_{source_label}"}, inplace=True)
    return df_all

df_landsat7 = load_and_merge(landsat7_files, HLSL30_L7_system_dif, "Landsat7")
df_landsat5 = load_and_merge(landsat5_files, 0, "Landsat5")

# 创建索引以加速匹配
df_landsat5.set_index("COMID", inplace=True)
results = []

# 按照±1天范围匹配相同 COMID 的数据
print("开始匹配数据（±1天）...")
for _, row in tqdm(df_landsat7.iterrows(), total=len(df_landsat7)):
    comid = row["COMID"]
    date = row["date"]
    doc_landsat7 = row["DOC_Landsat7"]

    if comid not in df_landsat5.index:
        continue

    sub_df = df_landsat5.loc[[comid]]
    if isinstance(sub_df, pd.Series):  # 若只有一条记录则转为DataFrame
        sub_df = pd.DataFrame([sub_df])

    # 筛选±1天的数据
    sub_df = sub_df[(sub_df["date"] >= date - pd.Timedelta(days=1)) &
                    (sub_df["date"] <= date + pd.Timedelta(days=1))]

    if not sub_df.empty:
        doc_landsat5_mean = sub_df["DOC_Landsat5"].mean()
        results.append({
            "COMID": comid,
            "date": date.strftime("%Y-%m-%d"),
            "DOC_Landsat7": doc_landsat7,
            "DOC_Landsat5": doc_landsat5_mean
        })

# 转换为 DataFrame 并保存
df_result = pd.DataFrame(results)

# 仅保留 DOC 值都小于等于 30 的记录，剔除异常高值
df_result = df_result[(df_result["DOC_Landsat7"] <= 30) & (df_result["DOC_Landsat5"] <= 30)].copy()
df_result = df_result[(df_result["DOC_Landsat7"] >= 0) & (df_result["DOC_Landsat5"] >= 0)].copy()

df_result.to_csv(output_csv_path, index=False)
print("匹配结果已保存到：", output_csv_path)

# 评估指标计算
if not df_result.empty:
    system_diff = (df_result["DOC_Landsat7"] - df_result["DOC_Landsat5"]).mean()
    r2 = r2_score(df_result["DOC_Landsat5"], df_result["DOC_Landsat7"])
    rmse = np.sqrt(mean_squared_error(df_result["DOC_Landsat5"], df_result["DOC_Landsat7"]))
    pearson_r, p_value = pearsonr(df_result["DOC_Landsat5"], df_result["DOC_Landsat7"])

    eval_df = pd.DataFrame({
        "Metric": ["System Difference", "R2", "RMSE", "Pearson r", "P-value"],
        "Value": [system_diff, r2, rmse, pearson_r, p_value]
    })
    eval_df.to_csv(eval_csv_path, index=False)
    print("评估结果已保存到：", eval_csv_path)
else:
    print("未匹配到任何数据，评估结果未生成。")
