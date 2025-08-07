# separate the river discharge dataset into 6 rivers parts

import os
import shutil

# 定义路径
comid_folder = r"D:\UZH\2024\20240122 Nutrient and Organic Carbon references\6large_rivers_watersheds\6River_Parts_river_reachs\Yukon_COMID"
discharge_folder = r"D:\UZH\2024\20240122 Nutrient and Organic Carbon references\DOC\Combination_interpolating_date"
destination_folder = r"D:\UZH\2024\20240122 Nutrient and Organic Carbon references\DOC\Yukon"

# 创建目标文件夹（如果不存在）
os.makedirs(destination_folder, exist_ok=True)

# 获取 COMID 文件夹中的文件名（去掉扩展名）
comid_files = [os.path.splitext(file)[0] for file in os.listdir(comid_folder) if file.endswith('.xlsx')]

# 遍历 discharge 文件夹中的文件
for file_name in os.listdir(discharge_folder):
    if file_name.endswith('.xlsx'):
        file_base_name = os.path.splitext(file_name)[0]

        # 检查文件名是否匹配
        if file_base_name in comid_files:
            source_path = os.path.join(discharge_folder, file_name)
            destination_path = os.path.join(destination_folder, file_name)

            # 复制文件到目标文件夹
            shutil.copy(source_path, destination_path)
            print(f"已复制: {file_name} 到 {destination_folder}")

print("所有匹配的文件已复制完成！")
