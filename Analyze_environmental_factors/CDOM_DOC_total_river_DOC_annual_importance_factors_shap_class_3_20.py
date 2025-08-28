import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt
import seaborn as sns
import shap
from matplotlib.ticker import MultipleLocator, FormatStrFormatter

# ========== Step 1: 读取数据 ==========  # English: Read data
df = pd.read_csv(r"D:\UZH\2024\20240122 Nutrient and Organic Carbon references\3_river_mouth_DOC\DOC_update_20250203\Total_DOC_average\All_Properites_DOC.csv")
target_col = 'Average_Total_DOC_1'
df = df.dropna(subset=[target_col])

# ========== Step 1.5: 筛选第一类流域（1–10 km²） ==========  # English: Screening the first type of river basins
df = df[(df['area_km2'] >= 100) & (df['area_km2'] <= 1000)].copy()

drop_cols = ['Average_Total_DOC', 'Average_Total_DOC_Area_Unit', 'Annual_Increase_Rate_1', 'Annual_Increase_Rate_DOC_Area_Unit', 'Average_Total_DOC_Uncertainty', 'center_lon', 'COMID', 'Annual_Increase_Rate', 'Intercept', 'R_Value', 'P_Value', 'Std_Err', 'Num_same_COMID']
df = df.drop(columns=[col for col in drop_cols if col in df.columns], errors='ignore')

X = df.drop(columns=[target_col])
y = df[target_col]
X = X.select_dtypes(include=[np.number])
feature_names = X.columns

# ========== Step 2: 数据预处理 ==========  # English: Data preprocessing
imputer = SimpleImputer(strategy='mean')
X_imputed = imputer.fit_transform(X)

scaler = StandardScaler()
X_scaled = scaler.fit_transform(X_imputed)

X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=42)

# ========== Step 3: 训练模型 ==========  # English: Training the model
model = RandomForestRegressor(n_estimators=200, random_state=42, n_jobs=-1)
model.fit(X_train, y_train)

# ========== Step 4: 特征重要性 ==========  # English: Characteristic importance
importances = model.feature_importances_

top_n = 20
top_indices = np.argsort(importances)[::-1][:top_n]
top_features = feature_names[top_indices]
top_importances = importances[top_indices]

# 相对这20个变量之和的比例（总和为1）  # English: Relative to this
top_importance_sum = np.sum(top_importances)
top_relative_importances = top_importances / top_importance_sum

# ========== Step 5: SHAP 值计算 ==========  # English: Value calculation
explainer = shap.Explainer(model, X_train, feature_perturbation='interventional')
shap_values = explainer(X_train, approximate=True, check_additivity=False)
top_shap_values = shap_values[:, top_indices]
shap_means = np.abs(top_shap_values.values).mean(axis=0)
shap_directions = top_shap_values.values.mean(axis=0)

# ========== Step 6: 构建结果表 ==========  # English: Build the result table
result_df = pd.DataFrame({
    'Feature': top_features,
    'Relative_Importance': top_relative_importances,
    'SHAP_MeanAbs': shap_means,
    'SHAP_Mean': shap_directions,
    'SHAP_Direction': ['+' if val > 0 else '−' for val in shap_directions]
})
result_df = result_df.sort_values(by='Relative_Importance', ascending=False)

# ========== Step 6.1: 保存 CSV ==========  # English: save
output_path_csv = r"D:\UZH\2024\20240122 Nutrient and Organic Carbon references\3_river_mouth_DOC\DOC_update_20250203\Total_DOC_average\Top20_Feature_Importance_class_3.csv"
result_df[['Feature', 'Relative_Importance']].to_csv(output_path_csv, index=False)

# ========== Step 7: 绘图 ==========  # English: Drawing
positive_color = '# e66101'  # 橙色，代表正向 SHAP  # English: orange color
negative_color = '# 5e3c99'  # 紫蓝色，代表负向 SHAP  # English: Purple blue

plt.rcParams["font.family"] = "Arial"
plt.rcParams["font.size"] = 6
plt.figure(figsize=(8.4/2.54, 5/2.54), dpi=600)

colors = [positive_color if val > 0 else negative_color for val in result_df['SHAP_Mean']]

sns.barplot(
    y=result_df['Feature'],
    x=result_df['Relative_Importance'],
    palette=colors
)

plt.grid(True, which='both', linestyle='--', alpha=0.5)
plt.xlabel('Relative Importance (Top 20 Features)')
plt.ylabel('')

# 设置 x 轴刻度间隔为 0.02，保留两位小数  # English: set up
ax = plt.gca()
ax.xaxis.set_major_locator(MultipleLocator(0.02))
ax.xaxis.set_major_formatter(FormatStrFormatter('%.2f'))

plt.tight_layout()

# ========== Step 8: 保存图像 ==========  # English: Save the image
output_path_fig = r"D:\UZH\2024\20240122 Nutrient and Organic Carbon references\3_river_mouth_DOC\DOC_update_20250203\Total_DOC_average\Top20_Feature_Importance_Class3.tif"
plt.savefig(output_path_fig, dpi=600, bbox_inches='tight', pad_inches=0.001, format='tiff')
plt.show()
