
# 计算 DOC 阈值
#
# 取 2018-05-01 至 2024-10-31 的 第二大 DOC 值 作为阈值。
# 若无足够数据，则取最大值。
# 如果阈值大于 70，则设定阈值为 70。
# 数据过滤
#
# 删除 DOC 超过阈值 的数据行。
# 插值补全
#
# 生成 1984-01-01 至 2024-12-31 的完整日期范围。
# 进行 线性插值填补 CDOM, CDOM_uncertainty, DOC, DOC_uncertainty。
# 文件存储
#
# 处理后的文件保存在 Combination_single_river_sort_date_pre_process_filldate 文件夹。


import pandas as pd
import os

# 输入和输出文件夹路径
input_folder = r"D:\UZH\2024\20240122 Nutrient and Organic Carbon references\3_river_mouth_DOC\DOC_update_20250203\Combination_single_river_sort_date_pre_process"
output_folder = r"D:\UZH\2024\20240122 Nutrient and Organic Carbon references\3_river_mouth_DOC\DOC_update_20250203\Combination_single_river_sort_date_pre_process_filldate"
os.makedirs(output_folder, exist_ok=True)

# 遍历文件夹内的所有 CSV 文件
for filename in os.listdir(input_folder):
    if not filename.endswith(".csv"):
        continue  # 只处理 CSV 文件

    input_file = os.path.join(input_folder, filename)
    output_file = os.path.join(output_folder, filename)

    try:
        # 读取 CSV 文件
        df = pd.read_csv(input_file)

        # 确保包含必要的列
        required_columns = {'date', 'CDOM', 'CDOM_uncertainty', 'DOC', 'DOC_uncertainty'}
        if not required_columns.issubset(df.columns):
            print(f"文件 {filename} 缺少必要的列，跳过处理")
            continue

        # 转换日期列
        df['date'] = pd.to_datetime(df['date'], errors='coerce')
        df = df.dropna(subset=['date'])  # 移除无效日期

        # 获取 2018-05-01 至 2024-10-31 期间的 DOC 值
        df_2018_2024 = df[(df['date'] >= '2018-05-01') & (df['date'] <= '2024-10-31')]

        # 计算 DOC 的第二大值（如果不足两个值，则取最大值）
        if not df_2018_2024.empty:
            doc_values = df_2018_2024['DOC'].dropna().unique()  # 获取唯一值
            doc_values.sort()  # 排序
            doc_threshold = doc_values[-2] if len(doc_values) > 1 else doc_values[-1]  # 取第二大值
            doc_threshold = min(doc_threshold, 70)  # 若超过 70，则取 70
        else:
            doc_threshold = 70  # 若无数据，默认阈值 70

        # 过滤掉超过阈值的 DOC 数据行
        df = df[df['DOC'] <= doc_threshold]

        # 生成 1984-01-01 至 2024-12-31 的完整日期范围
        full_date_range = pd.date_range(start='1984-01-01', end='2024-12-31')
        df_full = pd.DataFrame({'date': full_date_range})

        # 合并数据，确保完整日期范围
        df_merged = pd.merge(df_full, df, on='date', how='left')

        # **进行两次插值**
        # 1. 先进行普通线性插值（对1984年1月1日之后的空缺值补全）
        df_merged[['CDOM', 'CDOM_uncertainty', 'DOC', 'DOC_uncertainty']] = df_merged[
            ['CDOM', 'CDOM_uncertainty', 'DOC', 'DOC_uncertainty']].interpolate(method='linear')

        # 2. 向前填充（对于1984年1月1日至最早观测日期之前的数据）
        df_merged[['CDOM', 'CDOM_uncertainty', 'DOC', 'DOC_uncertainty']] = df_merged[
            ['CDOM', 'CDOM_uncertainty', 'DOC', 'DOC_uncertainty']].bfill()

        # 保存 CSV 文件
        df_merged.to_csv(output_file, index=False)
        print(f"处理完成: {filename} -> {output_file}")

    except Exception as e:
        print(f"处理文件 {filename} 时报错: {e}")

print("所有文件处理完成！")
