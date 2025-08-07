import pandas as pd
import matplotlib.pyplot as plt
import os

# 文件路径
input_file_path = r"D:\UZH\2024\20240122 Nutrient and Organic Carbon references\DOC\DOC_greater_equal_0\Combination_uncertainty_DOC_sort_date\25000307.xlsx"
output_folder_path = r"D:\UZH\2024\20240122 Nutrient and Organic Carbon references\DOC\DOC_greater_equal_0\Combination_uncertainty_DOC_sort_date_timeseries_figures"

# 设置字体为 Times New Roman
plt.rcParams['font.family'] = 'Times New Roman'

# 读取数据
try:
    # 从 Excel 文件中读取数据
    df = pd.read_excel(input_file_path, usecols=['date', 'DOC', 'DOC_uncertainty'])

    # 确保 date 列为 datetime 类型
    # df['date'] = pd.to_datetime(df['date'])

    # 筛选出 2010 到 2015 年的数据
    df = df[(df['date'] >= '2010-01-01') & (df['date'] <= '2015-12-31')]

    # 检查输出文件夹是否存在，不存在则创建
    if not os.path.exists(output_folder_path):
        os.makedirs(output_folder_path)

    # 获取文件名（不带扩展名）作为图表名称
    file_name = os.path.splitext(os.path.basename(input_file_path))[0]
    output_file_path = os.path.join(output_folder_path, f"{file_name}.tif")

    # 创建图表
    plt.figure(figsize=(12, 8))  # 图表大小
    plt.plot(df['date'], df['DOC'], marker='o', color='b', linewidth=1.5, markersize=5, label='DOC')
    plt.fill_between(df['date'], df['DOC'] - df['DOC_uncertainty'], df['DOC'] + df['DOC_uncertainty'], color='b', alpha=0.2, label='DOC Uncertainty')

    # 设置图表标题和标签
    plt.title(f"DOC Time Series with Uncertainty - {file_name}", fontsize=16)
    plt.xlabel("Date", fontsize=14)
    plt.ylabel("DOC (mg/L)", fontsize=14)
    plt.grid(True, linestyle='--', alpha=0.6)
    plt.legend(fontsize=12)

    # 设置时间轴格式
    plt.gcf().autofmt_xdate()

    # 保存图表为 TIFF 格式，600 dpi
    plt.savefig(output_file_path, format='tif', dpi=600)
    plt.close()  # 关闭图表

    print(f"图表已保存为: {output_file_path}")

except FileNotFoundError:
    print(f"文件 {input_file_path} 不存在，请检查文件路径是否正确。")
except Exception as e:
    print(f"处理文件时发生错误: {e}")

