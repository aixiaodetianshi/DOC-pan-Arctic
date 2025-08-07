import xarray as xr
import pandas as pd

file_path = 'D:/UZH/2024/20240122 Nutrient and Organic Carbon references/discharge/RADR_v1.0.0.nc'
# 使用xarray打开NetCDF文件
dataset = xr.open_dataset(file_path)

# 提取 'reach' 数据，并将其转换为 NumPy 数组
reach_data = dataset['reach'].values

# 将 'reach' 数据转换为 Pandas DataFrame
reach_df = pd.DataFrame(reach_data, columns=['reach'])

# 打印出DataFrame的前几行查看数据结构
print(reach_df.head())

# 将 'reach' 数据写入Excel文件
output_file = 'D:/UZH/2024/20240122 Nutrient and Organic Carbon references/discharge/reach_data.xlsx'
reach_df.to_excel(output_file, index=False)

print(f"'reach' 数据已成功保存到 {output_file}")
