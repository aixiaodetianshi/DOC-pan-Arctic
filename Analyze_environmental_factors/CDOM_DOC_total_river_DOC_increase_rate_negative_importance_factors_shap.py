
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt
import seaborn as sns
import shap

# ========== Step 1: 读取数据 ==========
df = pd.read_csv(r"D:\UZH\2024\20240122 Nutrient and Organic Carbon references\3_river_mouth_DOC\DOC_update_20250203\Total_DOC_average\All_Properites_DOC.csv")
target_col = 'Annual_Increase_Rate_1'
df = df.dropna(subset=[target_col])
df = df[df[target_col] < 0]  # 只保留增长率为正的记录
df[target_col] = df[target_col].abs()

drop_cols = ['Average_Total_DOC', 'Average_Total_DOC_1', 'Average_Total_DOC_Area_Unit', 'Annual_Increase_Rate_DOC_Area_Unit', 'Average_Total_DOC_Uncertainty', 'center_lon', 'COMID', 'Annual_Increase_Rate', 'Intercept', 'R_Value', 'P_Value', 'Std_Err', 'Num_same_COMID', ]
df = df.drop(columns=[col for col in drop_cols if col in df.columns], errors='ignore')

X = df.drop(columns=[target_col])
y = df[target_col]
X = X.select_dtypes(include=[np.number])
feature_names = X.columns

# ========== Step 2: 数据预处理 ==========
imputer = SimpleImputer(strategy='mean')
X_imputed = imputer.fit_transform(X)

scaler = StandardScaler()
X_scaled = scaler.fit_transform(X_imputed)

X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=42)

# ========== Step 3: 训练模型 ==========
model = RandomForestRegressor(n_estimators=200, random_state=42, n_jobs=-1)
model.fit(X_train, y_train)

# ========== Step 4: 特征重要性 ==========
importances = model.feature_importances_
importance_total = np.sum(importances)
importance_pct = importances / importance_total * 100

top_n = 20
top_indices = np.argsort(importances)[::-1][:top_n]
top_features = feature_names[top_indices]
top_importances = importances[top_indices]
top_pct = importance_pct[top_indices]

# ========== Step 5: SHAP 值计算 ==========
explainer = shap.Explainer(model, X_train, feature_perturbation='interventional')
shap_values = explainer(X_train, approximate=True)
top_shap_values = shap_values[:, top_indices]
shap_means = np.abs(top_shap_values.values).mean(axis=0)
shap_directions = top_shap_values.values.mean(axis=0)

# ========== Step 6: 构建结果表 ==========
result_df = pd.DataFrame({
    'Feature': top_features,
    'RandomForest_Importance': top_importances,
    'Importance (%)': top_pct,
    'SHAP_MeanAbs': shap_means,
    'SHAP_Mean': shap_directions,
    'SHAP_Direction': ['+' if val > 0 else '−' for val in shap_directions]
})
result_df = result_df.sort_values(by='RandomForest_Importance', ascending=False)  # 便于横向 barplot 显示

# ========== Step 7: 绘图 ==========
positive_color = '#e66101'  # 深橙色，代表正向 SHAP
negative_color = '#5e3c99'  # 深蓝色，代表负向 SHAP

plt.rcParams["font.family"] = "Arial"
plt.rcParams["font.size"] = 6
plt.figure(figsize=(8.4/2.54, 5/2.54), dpi=600)

colors = [positive_color if val > 0 else negative_color for val in result_df['SHAP_Mean']]
sns.barplot(
    y=result_df['Feature'],
    x=result_df['RandomForest_Importance'],
    palette=colors
)

# 添加网格
plt.grid(True, which='both', linestyle='--', alpha=0.5)

plt.xlabel('Importance')
plt.ylabel('')
# plt.ylabel('Top 20 Features')
# plt.title('Top 20 Feature Importances with SHAP-based Direction')

plt.tight_layout()

# ========== Step 8: 保存图像 ==========
output_path = r"D:\UZH\2024\20240122 Nutrient and Organic Carbon references\3_river_mouth_DOC\DOC_update_20250203\Total_DOC_increase_rate\Top20_Feature_Importance_negative.tif"
plt.savefig(output_path, dpi=600, bbox_inches='tight', pad_inches=0.001, format='tiff')
plt.show()