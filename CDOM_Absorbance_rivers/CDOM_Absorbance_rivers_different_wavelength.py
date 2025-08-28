#读取D:\UZH\2024\20240122 Nutrient and Organic Carbon references\Arctic\ArcticGRO\ArcticGRO_Absorbance\ArcticGRO Absorbance Data.xlsx  # English: Read
# 文件中的数据，共计做出6幅河流wavelength与CDOM吸收率的变化折线图； 分别存储在sheet：Ob, Yenisey, Lena, Kolyma, Yukon, Mackenzie中，  # English: Data in the file
# 每个sheet文件中，第一列是变量波长wavelength数值，为x轴，后面列为不同时间CDOM吸收率数据列，  # English: Each
# 计算这些不同时间CDOM吸收率数据列的平均值，为y轴，画出美观，学术价值非常高的图像，  # English: Calculate these different times
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

# 读取每一个sheet中的数据，并绘制图像  # English: Read each
for river in rivers:
    # 读取数据  # English: Read data
    df = pd.read_excel(file_path, sheet_name=river)

    # 假设第一列是波长，其他列是不同时间的CDOM吸收率  # English: Assume that the first column is the wavelength
    wavelength = df.iloc[:, 0]
    cdom_absorbance = df.iloc[:, 1:]

    # 计算不同时间CDOM吸收率数据的平均值  # English: Calculate different times
    cdom_mean = cdom_absorbance.mean(axis=1)

    # 绘制图像  # English: Draw an image
    plt.figure(figsize=(10, 6))
    plt.plot(wavelength, cdom_mean, label=f'Average CDOM Absorbance', color='b', linewidth=2)
    plt.title(f'{river} River', fontsize=14)
    plt.xlabel('Wavelength (nm)', fontsize=12)
    plt.ylabel('CDOM Absorbance', fontsize=12)
    plt.grid(True)
    plt.legend()

    # 保存图像，格式为tif，300dpi  # English: Save the image
    output_path = os.path.join(output_dir, f'{river}.tif')
    plt.savefig(output_path, format='tif', dpi=300)
    plt.close()

print("所有河流的图像已保存完毕。")
