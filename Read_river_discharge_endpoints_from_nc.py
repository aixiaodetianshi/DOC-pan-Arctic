import numpy as np
import netCDF4 as nc
import pandas as pd
import datetime
import os

# 定义起始时间
start_date = datetime.datetime(1984, 1, 1)

# 文件路径
reach_file_path = 'D:/UZH/2024/20240122 Nutrient and Organic Carbon references/discharge/riv_pfaf_MERIT_Hydro_v07_Basins_v01_endpoints_COMID.xlsx'
nc_file_path = 'D:/UZH/2024/20240122 Nutrient and Organic Carbon references/discharge/RADR_v1.0.0.nc'
output_folder = 'D:/UZH/2024/20240122 Nutrient and Organic Carbon references/discharge/river_discharge'

# 确保输出文件夹存在
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# 读取河流编号 Excel 文件
reach_numbers_df = pd.read_excel(reach_file_path)
reach_numbers = reach_numbers_df['COMID'].astype(int).tolist()  # 假设 Excel 中编号列名为 'COMID'

# 读取 NetCDF 文件
file_obj = nc.Dataset(nc_file_path)

# 获取时间和流量变量
days = np.arange(0, 12784)
dates = [start_date + datetime.timedelta(days=int(day)) for day in days]  # 计算每一天的日期
discharge = file_obj.variables['discharge']
reach_data = file_obj.variables['reach'][:].astype(int)   # 将 reach_data 转换为整型数组

# 循环读取每个 reach 编号的数据
for reach_no in reach_numbers:
    try:
        # 找到对应的 reach 编号的索引
        reach_index = np.where(reach_data == reach_no)[0][0]
        discharge_v = discharge[0:12784, reach_index]  # 获取该 reach 编号的流量数据

        # 创建 DataFrame 并保存为 Excel 文件
        df = pd.DataFrame({
            'time': dates,
            'discharge': discharge_v
        })

        # 保存文件，文件名格式为 reach_no.xlsx
        output_file = os.path.join(output_folder, f"{reach_no}.xlsx")
        df.to_excel(output_file, index=False)  #
        print(f"Data for reach number {reach_no} saved to {output_file}")

    except IndexError:
        print(f"Reach number {reach_no} not found in NetCDF file.")

# 关闭 NetCDF 文件
file_obj.close()