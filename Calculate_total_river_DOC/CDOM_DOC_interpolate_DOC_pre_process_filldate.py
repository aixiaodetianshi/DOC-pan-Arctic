
# 计算 DOC 阈值  # English: calculate
#
# 取 2018-05-01 至 2024-10-31 的 第二大 DOC 值 作为阈值。  # English: Pick
# 若无足够数据，则取最大值。  # English: If there is no sufficient data
# 如果阈值大于 70，则设定阈值为 70。  # English: If the threshold is greater than
# 数据过滤  # English: Data filtering
#
# 删除 DOC 超过阈值 的数据行。  # English: delete
# 插值补全  # English: Interpolation Completion
#
# 生成 1984-01-01 至 2024-12-31 的完整日期范围。  # English: generate
# 进行 线性插值填补 CDOM, CDOM_uncertainty, DOC, DOC_uncertainty。  # English: conduct
# 文件存储  # English: File storage
#
# 处理后的文件保存在 Combination_single_river_sort_date_pre_process_filldate 文件夹。  # English: The processed file is saved in


import pandas as pd
import os

# 输入和输出文件夹路径  # English: Input and output folder paths
input_folder = r"D:\UZH\2024\20240122 Nutrient and Organic Carbon references\3_river_mouth_DOC\DOC_update_20250203\Combination_single_river_sort_date_pre_process"
output_folder = r"D:\UZH\2024\20240122 Nutrient and Organic Carbon references\3_river_mouth_DOC\DOC_update_20250203\Combination_single_river_sort_date_pre_process_filldate"
os.makedirs(output_folder, exist_ok=True)

# 遍历文件夹内的所有 CSV 文件  # English: Iterate through all the folders
for filename in os.listdir(input_folder):
    if not filename.endswith(".csv"):
        continue  # 只处理 CSV 文件  # English: Process only

    input_file = os.path.join(input_folder, filename)
    output_file = os.path.join(output_folder, filename)

    try:
        # 读取 CSV 文件  # English: Read
        df = pd.read_csv(input_file)

        # 确保包含必要的列  # English: Make sure to include the necessary columns
        required_columns = {'date', 'CDOM', 'CDOM_uncertainty', 'DOC', 'DOC_uncertainty'}
        if not required_columns.issubset(df.columns):
            print(f"文件 {filename} 缺少必要的列，跳过处理")
            continue

        # 转换日期列  # English: Convert date column
        df['date'] = pd.to_datetime(df['date'], errors='coerce')
        df = df.dropna(subset=['date'])  # 移除无效日期  # English: Remove invalid date

        # 获取 2018-05-01 至 2024-10-31 期间的 DOC 值  # English: Get
        df_2018_2024 = df[(df['date'] >= '2018-05-01') & (df['date'] <= '2024-10-31')]

        # 计算 DOC 的第二大值（如果不足两个值，则取最大值）  # English: calculate
        if not df_2018_2024.empty:
            doc_values = df_2018_2024['DOC'].dropna().unique()  # 获取唯一值  # English: Get unique value
            doc_values.sort()  # 排序  # English: Sort
            doc_threshold = doc_values[-2] if len(doc_values) > 1 else doc_values[-1]  # 取第二大值  # English: Take the second largest value
            doc_threshold = min(doc_threshold, 70)  # 若超过 70，则取 70  # English: If more than
        else:
            doc_threshold = 70  # 若无数据，默认阈值 70  # English: If there is no data

        # 过滤掉超过阈值的 DOC 数据行  # English: Filter out those that exceed the threshold
        df = df[df['DOC'] <= doc_threshold]

        # 生成 1984-01-01 至 2024-12-31 的完整日期范围  # English: generate
        full_date_range = pd.date_range(start='1984-01-01', end='2024-12-31')
        df_full = pd.DataFrame({'date': full_date_range})

        # 合并数据，确保完整日期范围  # English: Merge data
        df_merged = pd.merge(df_full, df, on='date', how='left')

        # **进行两次插值**  # English: Perform two interpolations
        # 1. 先进行普通线性插值（对1984年1月1日之后的空缺值补全）  # English: Normal linear interpolation is performed first
        df_merged[['CDOM', 'CDOM_uncertainty', 'DOC', 'DOC_uncertainty']] = df_merged[
            ['CDOM', 'CDOM_uncertainty', 'DOC', 'DOC_uncertainty']].interpolate(method='linear')

        # 2. 向前填充（对于1984年1月1日至最早观测日期之前的数据）  # English: Fill forward
        df_merged[['CDOM', 'CDOM_uncertainty', 'DOC', 'DOC_uncertainty']] = df_merged[
            ['CDOM', 'CDOM_uncertainty', 'DOC', 'DOC_uncertainty']].bfill()

        # 保存 CSV 文件  # English: save
        df_merged.to_csv(output_file, index=False)
        print(f"处理完成: {filename} -> {output_file}")

    except Exception as e:
        print(f"处理文件 {filename} 时报错: {e}")

print("所有文件处理完成！")
