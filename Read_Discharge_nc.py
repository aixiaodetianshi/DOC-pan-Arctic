import numpy as np
import netCDF4 as nc
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import datetime

plt.rcParams['font.family'] = 'Times New Roman'
plt.rcParams['font.size'] = 14  # 设置默认字体大小为14

# 定义起始时间
start_date = datetime.datetime(1984, 1, 1)

file_path = 'D:/UZH/2024/20240122 Nutrient and Organic Carbon references/discharge/RADR_v1.0.0.nc'
file_obj = nc.Dataset(file_path)
file_obj

print(file_obj.variables.keys())  # 在Python2.7版本中输出结果为列表

time = file_obj.variables['time']
days = np.arange(0, 12784)

# 计算每一天对应的日期
dates = [start_date + datetime.timedelta(days=int(day)) for day in days]

reach = file_obj.variables['reach']
Nnm = 0
reach_no = int(reach[Nnm])
print('reach number is : ')
print(reach_no)

discharge = file_obj.variables['discharge']
print(discharge)

discharge_v = discharge[0:12784, Nnm]
print(discharge_v)

# 创建图表
fig, ax = plt.subplots(figsize=(14.0, 7.0))

ax.plot(dates, discharge_v)

# 设置标题和标签
ax.set_title('The daily discharge of river (No=' + str(reach_no) + ') from 1984', fontsize=16)
ax.set_xlabel('Date', fontsize=14)
ax.set_ylabel('River Discharge(m3/s)', fontsize=14)

# 美化日期显示
ax.xaxis.set_major_locator(mdates.YearLocator())
ax.xaxis.set_minor_locator(mdates.MonthLocator(bymonth=[1, 1]))
ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))
ax.grid(True, linestyle='--')

# 自动旋转日期标签以避免重叠
fig.autofmt_xdate()

# 保存图像为300dpi的tif格式
file_name = str(reach_no)
save_path = fr'D:\UZH\2024\20240122 Nutrient and Organic Carbon references\discharge\{reach_no}.tif'
plt.savefig(save_path, dpi=300, format='tiff')

plt.show()