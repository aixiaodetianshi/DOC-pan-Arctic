# 有1984年1月1日至2018年12月31日北极Ob河流入海口每天的河流流量数据，
# 同时有从卫星Landsat5/7/8/9和Sentinel-2传感器反演得到的1984年至2024年每一天的Ob河流入海口位置的溶解有机碳DOC数据，
# 但是时间不是连续的，并不是每一天都有DOC数据，现在想利用已有的DOC数据本身年内变化规律，
# 同时与对应日期的河流流量数据建立统计学关系或者深度学习模型，用于恢复重建缺失日期河流入海口溶解有机碳DOC。
# 最后使得1984年1月1日至2018年12月31日Ob河流入海口DOC在时间序列上完整，保证每一天都有DOC数据。

import pandas as pd
import numpy as np
import os
import joblib
from sklearn.ensemble import RandomForestRegressor  # 导入随机森林回归模型
from sklearn.metrics import mean_squared_error
from sklearn.impute import SimpleImputer

# 文件夹路径
input_folder = r"D:\UZH\2024\20240122 Nutrient and Organic Carbon references\DOC\DOC_update_20250203\Combination_single_river_combine_discharge\Mackenzie"
output_folder = r"D:\UZH\2024\20240122 Nutrient and Organic Carbon references\DOC\DOC_update_20250203\Combination_single_river_interpolate\Mackenzie"
model_folder = r"D:\UZH\2024\20240122 Nutrient and Organic Carbon references\DOC\DOC_update_20250203\Combination_single_river_interpolate\Mackenzie_model"

os.makedirs(output_folder, exist_ok=True)
os.makedirs(model_folder, exist_ok=True)

# 遍历所有 CSV 文件
for filename in os.listdir(input_folder):
    if not filename.endswith(".csv"):
        continue  # 只处理 CSV 文件

    input_file = os.path.join(input_folder, filename)
    output_file = os.path.join(output_folder, filename)
    model_file = os.path.join(model_folder, f"{filename}_model.pkl")
    model_params_file = os.path.join(model_folder, f"{filename}_model_params.pkl")

    # 读取数据
    df = pd.read_csv(input_file)

    # 解析日期
    df['date'] = pd.to_datetime(df['date'], errors='coerce')
    df.dropna(subset=['date'], inplace=True)

    # **生成完整的时间序列**
    full_dates = pd.date_range(start="1984-01-01", end="2018-12-31", freq='D')
    df_full = pd.DataFrame({'date': full_dates})

    # **合并原始数据，确保完整时间序列**
    df = df_full.merge(df, on="date", how="left")

    # 提取年份 & 计算周期性特征
    df['year'] = df['date'].dt.year
    df['day_of_year'] = df['date'].dt.dayofyear
    df['sin_day'] = np.sin(2 * np.pi * df['day_of_year'] / 365)
    df['cos_day'] = np.cos(2 * np.pi * df['day_of_year'] / 365)

    # **剔除异常大的 DOC 值**
    if 'DOC' in df.columns:
        Q1 = df['DOC'].quantile(0.25)
        Q3 = df['DOC'].quantile(0.75)
        IQR = Q3 - Q1
        threshold = Q3 + 0.5 * IQR
        df.loc[df['DOC'] > threshold, 'DOC'] = np.nan  # 过滤掉异常值
        print(f"{filename}: 异常大 DOC 值剔除完成，阈值: {threshold:.2f}")

    # 选取特征
    features = ['discharge', 'sin_day', 'cos_day']
    target = 'DOC'
    uncertainty_col = 'DOC_uncertainty'

    # 仅使用 1984-2018 年的数据进行训练
    df_train = df[df['year'] <= 2018]

    # 仅使用非空 DOC 进行训练
    train_data = df_train.dropna(subset=[target])
    if train_data.empty:
        print(f"文件 {filename} 没有足够的数据训练模型，跳过")
        continue

    # 处理 NaN 值
    imputer = SimpleImputer(strategy="mean")
    X_train = imputer.fit_transform(train_data[features])
    y_train = train_data[target].values

    # 训练随机森林回归模型
    model = RandomForestRegressor(n_estimators=100, random_state=42)  # 使用 100 棵树
    model.fit(X_train, y_train)

    # 计算模型误差 (RMSE)
    X_test = imputer.transform(train_data[features])
    y_pred = model.predict(X_test)
    mse = mean_squared_error(y_train, y_pred)
    rmse = np.sqrt(mse)  # 计算 RMSE 作为模型预测误差
    print(f"{filename} 随机森林回归模型训练完成，MSE: {mse:.4f}, RMSE: {rmse:.4f}")

    # **补全 1984-2018 年的 DOC**
    missing_doc = df[(df[target].isna()) & (df['year'] <= 2018)]
    if not missing_doc.empty:
        predicted_DOC = model.predict(imputer.transform(missing_doc[features]))

        # **确保 DOC 不能为负值**
        predicted_DOC = np.maximum(predicted_DOC, 0)

        df.loc[(df[target].isna()) & (df['year'] <= 2018), target] = predicted_DOC

        # **计算 DOC_uncertainty**
        if uncertainty_col in df.columns:
            observed_uncertainty = df[uncertainty_col].mean(skipna=True)  # 取已有数据的不确定性均值
            predicted_uncertainty = np.sqrt(rmse ** 2 + observed_uncertainty ** 2)  # 误差传递计算不确定性
            df.loc[(df[uncertainty_col].isna()) & (df['year'] <= 2018), uncertainty_col] = predicted_uncertainty

    # **确保 1984-2018 年的时间序列完整**
    df = df[df['year'] <= 2018]

    # **保存结果**
    df.to_csv(output_file, index=False)

    # **保存模型及其参数**
    model_params = {
        'model': model,
        'mse': mse,
        'rmse': rmse
    }
    joblib.dump(model_params, model_params_file)

    print(f"文件 {filename} 处理完成，已保存至 {output_file}，模型和参数保存在 {model_params_file}")

print("所有文件处理完成！")