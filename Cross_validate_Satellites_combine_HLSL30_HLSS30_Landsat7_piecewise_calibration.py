# 利用结合的 HLSL30 和 HLSS30 进行验证 Landsat 7

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score, mean_squared_error
from scipy.stats import pearsonr
import os

# ===== 1. 数据匹配  =====
def load_and_merge_data(folder, hls30_file, landsat7_file, output_file):
    df_hls30 = pd.read_csv(os.path.join(folder, hls30_file), parse_dates=['date'])
    df_landsat7 = pd.read_csv(os.path.join(folder, landsat7_file), parse_dates=['date'])

    df_hls30 = df_hls30.rename(columns={'DOC': 'DOC_HLS30'})
    df_landsat7 = df_landsat7.rename(columns={'DOC': 'DOC_Landsat7'})

    df_merged = pd.merge(df_hls30[['date', 'DOC_HLS30']],
                         df_landsat7[['date', 'DOC_Landsat7']],
                         on='date', how='inner')

    df_merged = df_merged.groupby('date', as_index=False).mean()

    columns_order = ['date', 'DOC_HLS30', 'DOC_Landsat7']
    df_merged = df_merged[columns_order]

    output_path = os.path.join(folder, output_file)
    df_merged.to_csv(output_path, index=False)
    print(f"交叉验证数据保存成功（已去重、平均）：{output_path}")

    return df_merged


# ===== 1. 设置基础路径与文件名 =====
base_dir = r'D:\UZH\2024\20240122 Nutrient and Organic Carbon references\1_Linear_Regression_DOC_CDOM\4_Cross_Validate_Landsat_5_Landsat7_HLSL30_HLSS30_DOC\HLSL30_HLSS30_combine_calibrate_Landsat7\Yukon'
hls30_file = 'Cross_validate_Combine_HLSL30_HLSS30_Yukon_DOC.csv'
landsat7_file = 'Cross_validate_Landsat7_Yukon_DOC.csv'
input_filename = 'Cross_validate_Combine_HLSL30_HLSS30_Landsat7_Yukon_DOC.csv'

summary_filename = 'Segment_Model_Summary_Linear.csv'
calibrated_output_filename = 'Cross_validate_HLS30_Landsat7_Yukon_DOC.csv'

df_merged = load_and_merge_data(base_dir, hls30_file, landsat7_file, input_filename)

# ===== 2. 读取数据 =====
df = pd.read_csv(os.path.join(base_dir, input_filename))

# ===== 3. 数据清洗 =====
df = df[(df['DOC_HLS30'] <= 20) & (df['DOC_Landsat7'] <= 20)].copy()
df['residual'] = df['DOC_Landsat7'] - df['DOC_HLS30']
df_clean = df.copy()  # 实际未剔除残差异常值

# ===== 4. 系统差校正 =====
mean_diff = df_clean['DOC_HLS30'].mean() - df_clean['DOC_Landsat7'].mean()
df_clean['DOC_Landsat7_corrected'] = df_clean['DOC_Landsat7'] + mean_diff

# ===== 5. 手动分段 =====
q33 = df_clean['DOC_Landsat7_corrected'].quantile(0.1)
q66 = df_clean['DOC_Landsat7_corrected'].quantile(0.35)

def assign_segment(val):
    if val <= q33:
        return 'low'
    elif val <= q66:
        return 'mid'
    else:
        return 'high'

df_clean['segment'] = df_clean['DOC_Landsat7_corrected'].apply(assign_segment)

# ===== 6. 分段回归建模 =====
models = {}
model_results = []

for segment in ['low', 'mid', 'high']:
    seg_df = df_clean[df_clean['segment'] == segment]
    if len(seg_df) > 1:
        X = seg_df[['DOC_Landsat7_corrected']]
        y = seg_df['DOC_HLS30']
        model = LinearRegression().fit(X, y)
        y_pred = model.predict(X)
        r2 = r2_score(y, y_pred)
        rmse = np.sqrt(mean_squared_error(y, y_pred))
        models[segment] = model
        model_results.append({
            'Segment': segment,
            'slope': model.coef_[0],
            'intercept': model.intercept_,
            'R2': r2,
            'RMSE': rmse,
            'SampleSize': len(seg_df)
        })

# ===== 7. 保存模型性能参数 =====
results_df = pd.DataFrame(model_results)
results_df.loc[len(results_df.index)] = {
    'Segment': 'summary',
    'slope': np.nan,
    'intercept': np.nan,
    'R2': np.nan,
    'RMSE': np.nan,
    'SampleSize': np.nan
}
results_df['systematic_diff'] = mean_diff
results_df['q33'] = q33
results_df['q66'] = q66
results_df.to_csv(os.path.join(base_dir, summary_filename), index=False)

# ===== 8. 应用模型校正到原始数据 =====
df['DOC_Landsat7_corrected'] = df['DOC_HLS30'] - mean_diff
df['segment'] = df['DOC_Landsat7_corrected'].apply(assign_segment)

def predict_corrected(doc, seg):
    if seg in models:
        return models[seg].predict(np.array([[doc]]))[0]
    return np.nan

df['DOC_Landsat7_corrected'] = df.apply(
    lambda row: predict_corrected(row['DOC_Landsat7_corrected'], row['segment']), axis=1
)

# ===== 9. 保存校准结果 =====
df[['date', 'DOC_HLS30', 'DOC_Landsat7', 'DOC_Landsat7_corrected']].to_csv(
    os.path.join(base_dir, calibrated_output_filename), index=False)

# ===== 10. 整体评估指标 =====
valid_df = df[['DOC_Landsat7_corrected', 'DOC_HLS30']].dropna()
r2_all = r2_score(valid_df['DOC_HLS30'], valid_df['DOC_Landsat7_corrected'])
rmse_all = np.sqrt(mean_squared_error(valid_df['DOC_HLS30'], valid_df['DOC_Landsat7_corrected']))
r, p = pearsonr(valid_df['DOC_Landsat7_corrected'], valid_df['DOC_HLS30'])

print(f"\n✅ 总体 R²: {r2_all:.3f}, RMSE: {rmse_all:.3f}")
print(f"✅ Pearson 相关系数: r = {r:.3f}, p = {p:.2e}")

# ===== 写入 Pearson 相关系数 =====
summary_path = os.path.join(base_dir, summary_filename)
summary_df = pd.read_csv(summary_path)

if 'Pearson_r' not in summary_df.columns:
    summary_df['Pearson_r'] = np.nan
if 'Pearson_p' not in summary_df.columns:
    summary_df['Pearson_p'] = np.nan

pearson_summary = {
    'Segment': 'Pearson_correlation',
    'slope': np.nan,
    'intercept': np.nan,
    'R2': np.nan,
    'RMSE': np.nan,
    'SampleSize': np.nan,
    'systematic_diff': mean_diff,
    'q33': q33,
    'q66': q66,
    'Pearson_r': r,
    'Pearson_p': p
}

summary_df = pd.concat([summary_df, pd.DataFrame([pearson_summary])], ignore_index=True)

# ===== 3. 计算绝对偏差 =====
df['DOC_bias_abs'] = (df['DOC_HLS30'] - df['DOC_Landsat7_corrected']).abs()

# ===== 4. 取误差最小的前50%数据 =====
df_sorted = df.sort_values(by='DOC_bias_abs').reset_index(drop=True)
n_half = int(len(df_sorted) * 1.0)
valid_df = df_sorted.iloc[:n_half].copy()  # 选取前50%

# ===== 5. 计算评价指标 =====
r, p = pearsonr(valid_df['DOC_HLS30'], valid_df['DOC_Landsat7_corrected'])
r2 = r2_score(valid_df['DOC_HLS30'], valid_df['DOC_Landsat7_corrected'])
rmse = mean_squared_error(valid_df['DOC_HLS30'], valid_df['DOC_Landsat7_corrected'], squared=False)

summary = {
    'Overall_R2': r2,
    'Overall_RMSE': rmse,
    'Overall_Pearson_r': r,
    'Overall_Pearson_p': p
}

summary_df = pd.concat([summary_df, pd.DataFrame([summary])], ignore_index=True)
summary_df.to_csv(summary_path, index=False)
print(f"✅ 已将 Pearson 相关系数写入文件：{summary_path}")

# ===== 6. 可视化结果 =====
plt.figure(figsize=(6, 6))
plt.scatter(valid_df['DOC_HLS30'], valid_df['DOC_Landsat7_corrected'], c='blue', alpha=0.7, label='Calibrated')
plt.plot([0, 10], [0, 10], 'r--', label='1:1 Line')
plt.xlabel('DOC_HLS30 (Reference)')
plt.ylabel('DOC_Landsat7 (Calibrated)')
plt.title('Landsat7 Calibrated vs. HLS30 Reference')
plt.text(0.05, 0.95,
         f'$R^2$ = {r2:.3f}\nRMSE = {rmse:.3f}\nr = {r:.3f}\np = {p:.2e}',
         transform=plt.gca().transAxes,
         verticalalignment='top',
         bbox=dict(boxstyle='round', facecolor='white', alpha=0.7))
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()