#读取D:\UZH\2024\20240122 Nutrient and Organic Carbon references\Arctic\ArcticGRO\ArcticGRO_Absorbance\ArcticGRO Absorbance Data.xlsx  # English: Read
# 文件中的数据，共计做出6幅河流wavelength与CDOM吸收率的变化折线图； 分别存储在sheet：Ob, Yenisey, Lena, Kolyma, Yukon, Mackenzie中，  # English: Data in the file
# 每个sheet文件中，第一列是变量波长wavelength数值，为x轴，后面列为不同时间CDOM吸收率数据列，  # English: Each
# 计算这些不同时间CDOM吸收率数据列的平均值，为y轴，画出美观，学术价值非常高的图像，将6条河流的的CDOM随着wavelength的变化，使用不同的mark和color科学美观的显示在同一张图上  # English: Calculate these different times
# 并保存在文件夹中D:\UZH\2024\20240122 Nutrient and Organic Carbon references\Arctic\ArcticGRO\ArcticGRO_Absorbance，  # English: and save it in a folder
# 保存格式为tif，为300dpi，文件名以河流名称命名  # English: Save format as

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib as mpl
import os

# 设置全局字体为Times New Roman  # English: Set the global font to
mpl.rcParams['font.family'] = 'Times New Roman'

# 文件路径  # English: File path
file_path = r'D:\UZH\2024\20240122 Nutrient and Organic Carbon references\Arctic\ArcticGRO\ArcticGRO_Absorbance\ArcticGRO Absorbance Data.xlsx'
output_dir = r'D:\UZH\2024\20240122 Nutrient and Organic Carbon references\Arctic\ArcticGRO\ArcticGRO_Absorbance'

# 确保输出目录存在  # English: Make sure the output directory exists
os.makedirs(output_dir, exist_ok=True)

# 定义河流和对应的sheet名  # English: Define rivers and corresponding
rivers = ['Ob', 'Yenisey', 'Lena', 'Kolyma', 'Yukon', 'Mackenzie']
colors = ['b', 'g', 'r', 'c', 'm', 'y']  # 定义颜色  # English: Define the color
# markers = ['o', 's', '^', 'D', 'v', 'x']  # 定义标记样式  # English: Define tag styles

# 绘制综合图  # English: Draw a comprehensive picture
plt.figure(figsize=(10, 6))

for i, river in enumerate(rivers):
    # 读取数据  # English: Read data
    df = pd.read_excel(file_path, sheet_name=river)

    # 假设第一列是波长，其他列是不同时间的CDOM吸收率  # English: Assume that the first column is the wavelength
    wavelength = df.iloc[:, 0]
    cdom_absorbance = df.iloc[:, 1:]

    # 计算不同时间CDOM吸收率数据的平均值  # English: Calculate different times
    cdom_mean = cdom_absorbance.mean(axis=1)

    # 在同一张图中绘制不同河流的数据  # English: Draw data for different rivers in the same graph
    plt.plot(wavelength, cdom_mean, label=f'{river}', color=colors[i], linewidth=2)

# 设置x轴和y轴范围  # English: set up
plt.xlim([430, 800])
plt.ylim([0, 0.025])

# 添加图表标题、标签和图例  # English: Add a chart title
plt.title('CDOM Absorbance for Arctic Rivers', fontsize=14)
plt.xlabel('Wavelength (nm)', fontsize=12)
plt.ylabel('Average CDOM Absorbance', fontsize=12)
plt.grid(True)
plt.legend(title='Rivers')

# 保存综合图像，格式为tif，300dpi  # English: Save comprehensive image
output_path = os.path.join(output_dir, 'All_Rivers_CDOM_vs_Wavelength_430_800.tif')
plt.savefig(output_path, format='tif', dpi=300)
plt.close()

print("综合图像已保存完毕。")
