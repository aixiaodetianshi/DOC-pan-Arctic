import pandas as pd
import matplotlib.pyplot as plt
import os

# 文件路径
input_file_path = r"D:\UZH\2024\20240122 Nutrient and Organic Carbon references\discharge\Annual_river_discharge\83017880.xlsx"
output_folder_path = r"D:\UZH\2024\20240122 Nutrient and Organic Carbon references\discharge\Annual_river_discharge_figure"

# 设置字体为 Times New Roman
plt.rcParams['font.family'] = 'Times New Roman'

# 读取数据
try:
    # 从 Excel 文件中读取数据
    df = pd.read_excel(input_file_path, names=['year', 'annual_discharge'])

    # 检查输出文件夹是否存在，不存在则创建
    if not os.path.exists(output_folder_path):
        os.makedirs(output_folder_path)

    # 获取文件名（不带扩展名）作为河流编号
    river_id = os.path.splitext(os.path.basename(input_file_path))[0]
    output_file_path = os.path.join(output_folder_path, f"{river_id}.tif")

    # 创建图表
    plt.figure(figsize=(10, 6))  # 图表大小
    plt.plot(df['year'], df['annual_discharge'], marker='o', color='b', linewidth=1.5, markersize=5,
             label='annual discharge')

    # 动态标题包含河流编号
    plt.title(f"annual discharge Over Time - River {river_id}", fontsize=16)
    plt.xlabel("Year", fontsize=14)
    plt.ylabel("annual_discharge (m3/s)", fontsize=14)  # 可根据需要调整单位
    plt.grid(True, linestyle='--', alpha=0.6)
    plt.legend(fontsize=12)

    # 保存图表为 TIFF 格式，300 dpi
    plt.savefig(output_file_path, format='tif', dpi=300)
    plt.close()  # 关闭图表

    print(f"图表已保存为: {output_file_path}")

except FileNotFoundError:
    print(f"文件 {input_file_path} 不存在，请检查文件路径是否正确。")
except Exception as e:
    print(f"处理文件时发生错误: {e}")
