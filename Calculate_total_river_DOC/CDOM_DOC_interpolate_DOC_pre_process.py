
# 数据保存为csv格式，文件内有5列数据，分别为日期  # English: Save the data as
# CDOM，CDOM的不确定性，DOC，DOC的不确定性，  # English: Uncertainty
# 对应为：date，CDOM, CDOM_uncertainty， DOC，和  DOC_uncertainty，  # English: Corresponding to
# 同时也使用相同的方法将CDOM, CDOM_uncertainty， 和  DOC_uncertainty 进行处理，  # English: Also use the same method
# 数据处理结果保存为csv格式，相同文件名，  # English: Save the data processing results as
# 只保存每年的5月1日-10月31日的结果。  # English: Save only every year
# 保存在文件夹：D:\UZH\2024\20240122 Nutrient and Organic Carbon references\DOC\DOC_update_20250203\Combination_single_river_sort_date_pre_process  # English: Save in folder

import pandas as pd
import os

# 输入和输出文件夹路径  # English: Input and output folder paths
input_folder = r"D:\UZH\2024\20240122 Nutrient and Organic Carbon references\3_river_mouth_DOC\DOC_update_20250203\Combination_single_river_sort_date"
output_folder = r"D:\UZH\2024\20240122 Nutrient and Organic Carbon references\3_river_mouth_DOC\DOC_update_20250203\Combination_single_river_sort_date_pre_process"
os.makedirs(output_folder, exist_ok=True)

# 遍历整个文件夹内的所有CSV文件  # English: Iterate through all the folders
for filename in os.listdir(input_folder):
    if not filename.endswith(".csv"):
        continue  # 只处理CSV文件  # English: Process only

    input_file = os.path.join(input_folder, filename)
    output_file = os.path.join(output_folder, filename)

    # 检查文件是否为空  # English: Check if the file is empty
    if os.path.getsize(input_file) == 0:
        print(f"跳过空文件: {filename}")
        continue

    try:
        # 读取CSV文件  # English: Read
        df = pd.read_csv(input_file, sep=None, engine='python')

        # 确保存在 'date' 列  # English: Make sure to exist
        if 'date' not in df.columns:
            print(f"文件 {filename} 缺少 'date' 列，跳过处理")
            continue

        # 解析日期列  # English: Analyze date columns
        df['date'] = pd.to_datetime(df['date'], errors='coerce')

        # 移除无法解析的日期  # English: Remove unresolved dates
        df = df.dropna(subset=['date'])

        # 只保留 5 月 1 日至 10 月 31 日的数据  # English: Only retain
        df = df[(df['date'].dt.month >= 5) & (df['date'].dt.month <= 10)]

        # 计算相同日期的均值  # English: Calculate the mean of the same date
        df_grouped = df.groupby('date', as_index=False).mean()

        # 生成每年的5月1日至10月31日的完整日期范围  # English: Generate annual
        date_range = pd.date_range(start='1984-05-01', end='2024-10-31')
        df_full = pd.DataFrame({'date': date_range})

        # 合并数据，确保完整日期范围  # English: Merge data
        df_merged = pd.merge(df_full, df_grouped, on='date', how='left')

        # 对缺失值进行线性插值  # English: Linear interpolation of missing values
        df_merged[['CDOM', 'CDOM_uncertainty', 'DOC', 'DOC_uncertainty']] = df_merged[['CDOM', 'CDOM_uncertainty', 'DOC', 'DOC_uncertainty']].interpolate(method='linear')

        # 删除DOC大于70的行  # English: delete
        df_merged = df_merged[df_merged['DOC'] <= 70]

        # 保存CSV文件  # English: save
        df_merged.to_csv(output_file, index=False)
        print(f"处理完成: {filename} -> {output_file}")

    except Exception as e:
        print(f"处理文件 {filename} 时报错: {e}")

print("所有文件处理完成！")
