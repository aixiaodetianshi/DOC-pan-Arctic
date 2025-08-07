# 递归遍历所有子文件夹 (os.walk())
# 正确读取 .csv 文件
# 匹配正确的列名 (Total_DOC 和 Total_DOC_uncertainty)
# 同时计算 Total_DOC 和 Total_DOC_uncertainty 的平均值
# 输出带 COMID（河流编号）的 CSV


import os
import pandas as pd

# 定义文件夹路径
input_folder = r"D:\UZH\2024\20240122 Nutrient and Organic Carbon references\3_river_mouth_DOC\DOC_update_20250203\Total_DOC_annual"
output_folder = r"D:\UZH\2024\20240122 Nutrient and Organic Carbon references\3_river_mouth_DOC\DOC_update_20250203\Total_DOC_average"
output_file = os.path.join(output_folder, "average_Total_DOC.csv")

# 确保输出文件夹存在
os.makedirs(output_folder, exist_ok=True)

# 用于存储结果的列表
results = []

# 遍历所有子文件夹和文件
for root, _, files in os.walk(input_folder):
    for file_name in files:
        if file_name.endswith(".csv"):
            file_path = os.path.join(root, file_name)

            # 读取CSV文件
            df = pd.read_csv(file_path)

            # 检查是否存在所需列
            if 'Total_DOC' in df.columns and 'Total_DOC_uncertainty' in df.columns:
                # 计算平均值
                avg_doc = df['Total_DOC'].mean()
                avg_uncertainty = df['Total_DOC_uncertainty'].mean()

                # 获取河流编号（文件名去掉扩展名）
                river_id = os.path.splitext(file_name)[0]

                # 添加到结果列表
                results.append({
                    'COMID': river_id,
                    'Average_Total_DOC': avg_doc,
                    'Average_Total_DOC_Uncertainty': avg_uncertainty
                })
            else:
                print(f"警告: 文件 {file_name} 缺少所需列")

# 将结果转换为 DataFrame
results_df = pd.DataFrame(results)

# 保存为 CSV 文件
results_df.to_csv(output_file, index=False)

print(f"结果已保存到 {output_file}")

