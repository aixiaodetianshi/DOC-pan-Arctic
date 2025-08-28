import numpy as np
import netCDF4 as nc
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import datetime
import pandas as pd  # 新增 pandas 导入  # English: New

plt.rcParams['font.family'] = 'Times New Roman'
plt.rcParams['font.size'] = 14  # 设置默认字体大小为14  # English: Set the default font size to

# 定义起始时间  # English: Define the start time
start_date = datetime.datetime(1984, 1, 1)

file_path = 'D:/UZH/2024/20240122 Nutrient and Organic Carbon references/discharge/RADR_v1.0.0.nc'
file_obj = nc.Dataset(file_path)

print(file_obj.variables.keys())  # 打印可用变量  # English: Print available variables

# 获取时间变量  # English: Get time variables
time = file_obj.variables['time']
days = np.arange(0, len(time))

# 计算每一天对应的日期  # English: Calculate the corresponding date for each day
dates = [start_date + datetime.timedelta(days=int(day)) for day in days]

# 获取 reach 和 discharge 变量  # English: Get
reach = file_obj.variables['reach'][:]
discharge = file_obj.variables['discharge']

# 找到 reach 数值为 25000004 的索引  # English: turn up
target_reach_no = 25000004
Nnm = np.where(reach == target_reach_no)[0]

# 检查是否找到了该 reach 数值  # English: Check if the
if len(Nnm) == 0:
    print(f"Reach number {target_reach_no} not found.")
else:
    Nnm = Nnm[0]  # 选择第一个匹配的索引  # English: Select the first matching index
    print(f'Reach number is : {target_reach_no}')

    # 获取相应的 discharge 数据  # English: Get the corresponding
    discharge_v = discharge[:, Nnm]
    print(discharge_v)

    # 保存时间和流量数据到 Excel 文件  # English: Save time and traffic data to
    df = pd.DataFrame({'Date': dates, 'Discharge': discharge_v})
    save_path_excel = fr'D:\UZH\2024\20240122 Nutrient and Organic Carbon references\discharge\{target_reach_no}.xlsx'
    df.to_excel(save_path_excel, index=False)
    print(f"Data saved to {save_path_excel}")

    # 创建图表  # English: Create a chart
    fig, ax = plt.subplots(figsize=(14.0, 7.0))

    ax.plot(dates, discharge_v)

    # 设置标题和标签  # English: Set titles and tags
    ax.set_title(f'The daily discharge of river (No={target_reach_no}) from 1984', fontsize=16)
    ax.set_xlabel('Date', fontsize=14)
    ax.set_ylabel('River Discharge(m3/s)', fontsize=14)

    # 美化日期显示  # English: Beautify date display
    ax.xaxis.set_major_locator(mdates.YearLocator())
    ax.xaxis.set_minor_locator(mdates.MonthLocator(bymonth=[1, 1]))
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))
    ax.grid(True, linestyle='--')

    # 自动旋转日期标签以避免重叠  # English: Automatically rotate date labels to avoid overlap
    fig.autofmt_xdate()

    # 保存图像为300dpi的tif格式  # English: Save the image as
    save_path_tif = fr'D:\UZH\2024\20240122 Nutrient and Organic Carbon references\discharge\{target_reach_no}.tif'
    plt.savefig(save_path_tif, dpi=300, format='tiff')
    print(f"Image saved to {save_path_tif}")

    plt.show()
