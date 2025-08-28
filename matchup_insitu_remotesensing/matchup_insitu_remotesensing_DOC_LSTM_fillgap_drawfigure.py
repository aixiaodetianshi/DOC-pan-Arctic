import os
os.environ["PATH"] += os.pathsep + r'C:\Program Files\Graphviz\bin'

from tensorflow.keras.models import Sequential, load_model
from tensorflow.keras.utils import plot_model

import matplotlib as mpl

# 设置全局字体为Times New Roman  # English: Set the global font to
mpl.rcParams['font.family'] = 'Times New Roman'

model_file = r'D:\UZH\2024\20240122 Nutrient and Organic Carbon references\Arctic\ArcticGRO\insitu_DOC\doc_lstm_model_Yensiey.h5'
model_plot_file = r'D:\UZH\2024\20240122 Nutrient and Organic Carbon references\Arctic\ArcticGRO\insitu_DOC\lstm_model_structure.png'

# 从文件中加载LSTM模型  # English: Load from file
model = load_model(model_file)

# 绘制模型结构并保存为图像  # English: Draw the model structure and save it as an image
plot_model(model, to_file=model_plot_file, show_shapes=True, show_layer_names=True)

print(f"LSTM模型的结构图已保存为 {model_plot_file}")

