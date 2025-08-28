import os
import pandas as pd

# 定义输入文件路径
in_situ_file = r'D:\UZH\2024\20240122 Nutrient and Organic Carbon references\Arctic\ArcticGRO\CDOM_DOC_in_situ\May_October_CDOM_DOC\ArcticGRO_DOC_CDOM_insitu_Ob.xlsx'
remotesensing_file = r'D:\UZH\2024\20240122 Nutrient and Organic Carbon references\Arctic\ArcticGRO\CDOM_DOC_in_situ\May_October_CDOM_DOC\remote_sensing_10points_bands_Ln_divide\SPP_River_Ob_Surround_Landsat5_10Points.xlsx'

# 定义输出文件夹路径
output_folder = r'D:\UZH\2024\20240122 Nutrient and Organic Carbon references\Arctic\ArcticGRO\CDOM_DOC_in_situ\May_October_CDOM_DOC\matchup_insitu_remotesensing_CDOM'

# 如果输出文件夹不存在，则创建
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# 读取 in_situ_file 文件
in_situ_data = pd.read_excel(in_situ_file, usecols=['Date', 'DOC', 'CDOM'])

# 将日期列转换为日期格式
in_situ_data['Date'] = pd.to_datetime(in_situ_data['Date'])

# 读取 remotesensing_file 文件
remote_sensing_data = pd.read_excel(remotesensing_file)

# 确保 remotesensing_file 中的日期列也是日期格式
remote_sensing_data['date'] = pd.to_datetime(remote_sensing_data['date'])

# 创建一个新的DataFrame，用于存放匹配后的数据
matched_data = remote_sensing_data.copy()


# 函数：找到最接近的日期
def find_closest_date(target_date, in_situ_df):
    time_diffs = (in_situ_df['Date'] - target_date).abs()
    closest_idx = time_diffs.idxmin()
    return in_situ_df.loc[closest_idx]


# 遍历 remotesensing_file 中的每条记录
for idx, row in remote_sensing_data.iterrows():
    sensing_date = row['date']

    # 查找 in_situ_file 中最近的日期
    closest_row = find_closest_date(sensing_date, in_situ_data)

    # 将 in_situ_file 中的日期、DOC 和 CDOM 添加到 matched_data 中
    matched_data.loc[idx, 'in_situ_Date'] = closest_row['Date']
    matched_data.loc[idx, 'DOC'] = closest_row['DOC']
    matched_data.loc[idx, 'CDOM'] = closest_row['CDOM']

# 构造输出文件路径（保持与 remotesensing_file 相同的文件名）
output_file_name = os.path.basename(remotesensing_file)
output_file_path = os.path.join(output_folder, output_file_name)

# 将匹配后的数据写入新的Excel文件
matched_data.to_excel(output_file_path, index=False)

print(f'匹配结果已保存为 {output_file_path}')
