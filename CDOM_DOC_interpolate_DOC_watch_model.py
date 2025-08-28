import joblib

# 你的 .pkl 文件路径
model_file = r"D:\UZH\2024\20240122 Nutrient and Organic Carbon references\DOC\DOC_update_20250203\Combination_single_river_interpolate\Ob_model\25000002.csv_model.pkl"

# 加载模型
model = joblib.load(model_file)

# 查看模型参数
print(model)
print(model.coef_)  # 线性回归的系数
print(model.intercept_)  # 线性回归的截距
