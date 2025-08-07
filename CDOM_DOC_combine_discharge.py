import os
import pandas as pd

# 定义文件夹路径
river = "Yukon"
doc_folder = r"D:\UZH\2024\20240122 Nutrient and Organic Carbon references\3_river_mouth_DOC\DOC_update_20250203\Combination_single_river_sort_date_pre_process_6_Parts\\" + river
discharge_folder = r"D:\UZH\2024\20240122 Nutrient and Organic Carbon references\0_0_river_mouth_discharge\river_discharge\\" + river
output_folder = r"D:\UZH\2024\20240122 Nutrient and Organic Carbon references\3_river_mouth_DOC\DOC_update_20250203\Combination_single_river_sort_date_pre_process_filldate_combine_discharge\\" + river

# 创建目标文件夹（如果不存在）
os.makedirs(output_folder, exist_ok=True)

# 获取 DOC 目录下的所有 CSV 文件
doc_files = [f for f in os.listdir(doc_folder) if f.endswith('.csv')]

# 处理每个 DOC 文件
for doc_file in doc_files:
    doc_path = os.path.join(doc_folder, doc_file)
    discharge_path = os.path.join(discharge_folder, doc_file.replace('.csv', '.xlsx'))
    output_path = os.path.join(output_folder, doc_file)

    # 检查对应的 discharge 文件是否存在
    if not os.path.exists(discharge_path):
        print(f"⚠️ 未找到对应的 discharge 文件: {discharge_path}, 跳过 {doc_file}")
        continue

    # 读取 DOC 数据
    try:
        doc_df = pd.read_csv(doc_path)
    except Exception as e:
        print(f"❌ 读取 DOC 文件失败: {doc_file}, 错误: {e}")
        continue

    # 读取 discharge 数据
    try:
        discharge_df = pd.read_excel(discharge_path)
    except Exception as e:
        print(f"❌ 读取 discharge 文件失败: {discharge_path}, 错误: {e}")
        continue

    # 确保列名正确
    expected_doc_columns = ['date', 'CDOM', 'CDOM_uncertainty', 'DOC', 'DOC_uncertainty']
    expected_discharge_columns = ['time', 'discharge']

    if list(doc_df.columns)[:5] != expected_doc_columns:
        print(
            f"⚠️ DOC 文件列名不匹配: {doc_file}, 期望: {expected_doc_columns}, 但读取到: {list(doc_df.columns)}，跳过。")
        continue

    if list(discharge_df.columns)[:2] != expected_discharge_columns:
        print(
            f"⚠️ Discharge 文件列名不匹配: {doc_file}, 期望: {expected_discharge_columns}, 但读取到: {list(discharge_df.columns)}，跳过。")
        continue

    # 格式化日期
    doc_df['date'] = pd.to_datetime(doc_df['date'])
    discharge_df['time'] = pd.to_datetime(discharge_df['time'])

    # 合并数据（左连接，确保所有 DOC 数据保留）
    merged_df = pd.merge(doc_df, discharge_df, left_on='date', right_on='time', how='left')

    # 删除 time 列，仅保留 discharge
    merged_df.drop(columns=['time'], inplace=True)

    # 保存合并后的文件
    try:
        merged_df.to_csv(output_path, index=False)
        print(f"✅ 合并完成: {output_path}")
    except Exception as e:
        print(f"❌ 保存文件失败: {output_path}, 错误: {e}")

print("🎉 所有匹配的 DOC 文件已成功合并并保存！")

