# separate the river discharge/ DOC dataset into 6 rivers parts


import os
import shutil

# 定义路径
river = "Yukon"
comid_folder = r"D:\UZH\2024\20240122 Nutrient and Organic Carbon references\0_2_6large_rivers_watersheds\6River_Parts_river_reachs\\"+river+"_COMID"
discharge_folder = r"D:\UZH\2024\20240122 Nutrient and Organic Carbon references\3_river_mouth_DOC\DOC_update_20250203\Combination_single_river_sort_date_pre_process_filldate"
destination_folder = r"D:\UZH\2024\20240122 Nutrient and Organic Carbon references\3_river_mouth_DOC\DOC_update_20250203\Combination_single_river_sort_date_pre_process_6_Parts\\"+river

# 创建目标文件夹（如果不存在）
os.makedirs(destination_folder, exist_ok=True)

# 读取 COMID 文件夹中的文件名（去掉扩展名，并存入集合以提高匹配效率）
try:
    comid_files = {os.path.splitext(file)[0] for file in os.listdir(comid_folder) if file.endswith('.xlsx')}
    print(f"✅ 读取 COMID 文件夹完成，共 {len(comid_files)} 个文件")
except Exception as e:
    print(f"❌ 读取 COMID 文件夹时发生错误: {e}")
    exit(1)  # 终止程序

# 计数器
copied_count = 0

# 遍历 discharge 文件夹中的 CSV 文件
try:
    for file_name in os.listdir(discharge_folder):
        if file_name.endswith('.csv'):
            file_base_name = os.path.splitext(file_name)[0]

            # 仅处理匹配的文件
            if file_base_name in comid_files:
                source_path = os.path.join(discharge_folder, file_name)
                destination_path = os.path.join(destination_folder, file_name)

                # 复制文件
                shutil.copy2(source_path, destination_path)  # `copy2` 保留元数据
                copied_count += 1
                print(f"✅ 已复制: {file_name} → {destination_folder}")

except Exception as e:
    print(f"❌ 处理 CSV 文件时发生错误: {e}")
    exit(1)  # 终止程序

# 最终输出
if copied_count == 0:
    print("⚠️ 没有找到匹配的文件，未进行复制。")
else:
    print(f"🎉 复制完成，共 {copied_count} 个文件已成功复制到 {destination_folder}")
