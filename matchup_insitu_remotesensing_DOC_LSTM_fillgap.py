import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import Sequential, load_model
from tensorflow.keras.layers import LSTM, Dense, Dropout
import tensorflow as tf

import matplotlib as mpl

# 设置全局字体为Times New Roman
mpl.rcParams['font.family'] = 'Times New Roman'

# 检查 GPU 是否可用
print("Num GPUs Available: ", len(tf.config.list_physical_devices('GPU')))

# 定义文件路径
input_file = r'D:\UZH\2024\20240122 Nutrient and Organic Carbon references\Arctic\ArcticGRO\insitu_DOC\SPP_Yukon_remotesensing_Landsat_DOC.xlsx'
output_file = r'D:\UZH\2024\20240122 Nutrient and Organic Carbon references\Arctic\ArcticGRO\insitu_DOC\SPP_Yukon_remotesensing_Landsat_DOC_filled.xlsx'
model_file = r'D:\UZH\2024\20240122 Nutrient and Organic Carbon references\Arctic\ArcticGRO\insitu_DOC\doc_lstm_model_Yukon.h5'

# 读取数据
df = pd.read_excel(input_file, usecols=['Date', 'DOC'])

# 将日期列转换为日期格式
df['Date'] = pd.to_datetime(df['Date'])

# 处理重复日期: 取平均值
df = df.groupby('Date').mean().reset_index()

# 以日期为索引
df.set_index('Date', inplace=True)

# 剔除异常值
lower_bound = df['DOC'].quantile(0.025)
upper_bound = df['DOC'].quantile(0.975)
df = df[(df['DOC'] >= lower_bound) & (df['DOC'] <= upper_bound)]

# 填补日期缺失值，使用插值法进行填充，或者简单前向填充
df = df.asfreq('D')
df['DOC'] = df['DOC'].interpolate(method='linear')

# 标记缺失值以备后续填补
missing_values_mask = df['DOC'].isna()

# 归一化处理
scaler = MinMaxScaler(feature_range=(0, 1))
scaled_data = scaler.fit_transform(df[['DOC']].values)

# 准备训练数据
def create_dataset(data, look_back=1):
    X, Y = [], []
    for i in range(len(data) - look_back):
        X.append(data[i:(i + look_back), 0])
        Y.append(data[i + look_back, 0])
    return np.array(X), np.array(Y)

look_back = 100  # 增加look_back的值以捕获更多的时间依赖性
X, Y = create_dataset(scaled_data, look_back)

# 调整X的形状以适应LSTM的输入要求
X = np.reshape(X, (X.shape[0], X.shape[1], 1))

# 创建LSTM模型
model = Sequential()
model.add(LSTM(100, return_sequences=True, input_shape=(look_back, 1)))
model.add(Dropout(0.2))
model.add(LSTM(100))
model.add(Dropout(0.2))
model.add(Dense(1))
model.compile(loss='mean_squared_error', optimizer='adam')

# 使用GPU进行训练
with tf.device('/GPU:0'):
    model.fit(X, Y, epochs=50, batch_size=32, verbose=2)  # 增加epochs和batch_size以加强模型学习

# 保存模型
model.save(model_file)

# 创建输入数据用于预测
def predict_fill_gaps(data, model, look_back):
    X_pred = []
    predictions = []
    for i in range(len(data)):
        if i >= look_back:
            X_pred = data[i-look_back:i].reshape(1, look_back, 1)
            pred = model.predict(X_pred)[0, 0]
            predictions.append(pred)
            data[i] = pred  # 更新输入数据
        else:
            predictions.append(data[i, 0])
    return np.array(predictions)

# 填补缺失值
scaled_data = scaled_data.reshape(-1, 1)
predicted = predict_fill_gaps(scaled_data, model, look_back)

# 反归一化以得到原始尺度的值
predicted_full = scaler.inverse_transform(predicted.reshape(-1, 1))

# 只填补原缺失值
df['DOC_filled'] = df['DOC'].copy()
df.loc[missing_values_mask, 'DOC_filled'] = predicted_full[missing_values_mask.values]

# 限制 DOC_filled 的值在原始 DOC 的最大值和最小值之间
max_value = df['DOC'].max()
min_value = df['DOC'].min()
df['DOC_filled'] = df['DOC_filled'].clip(lower=min_value, upper=max_value)

# 保存到 Excel 文件
df.to_excel(output_file)

print(f"填补后的数据已成功保存到 {output_file} 中。")

# 绘制原始和填补后的DOC时间序列
plt.figure(figsize=(14, 7))
plt.plot(df.index, df['DOC'], label='Original DOC')
plt.plot(df.index, df['DOC_filled'], label='Filled DOC', linestyle='--')
plt.legend()
plt.title('Yukon')
plt.xlabel('Date')
plt.ylabel('DOC/(mg/L)')
plt.grid(True)
plt.show()
