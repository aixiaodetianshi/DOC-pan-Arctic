# ///////////////////-----------------建立河流端点文件 -------------------/////////////////////////  # English: Create a river endpoint file
# ///////////////////-----------------establish the river endpoints files -------------------/////////////////////////

import pandas as pd
import os

# 输出文件夹路径  # English: Output folder path
output_folder = r'D:\UZH\2024\20240122 Nutrient and Organic Carbon references\DOC\DOC_update_20250203\Combination_single_river'

# 如果输出文件夹不存在，则创建  # English: If the output folder does not exist
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# ///////////////////-----------------建立河流端点文件 -------------------/////////////////////////  # English: Create a river endpoint file
river_endpoints_files = r'D:\UZH\2024\20240122 Nutrient and Organic Carbon references\DOC\DOC_greater_50\riv_pfaf_MERIT_Hydro_v07_Basins_v01_endpoints_COMID.xlsx'

# 读取包含河流 COMID 编号的 Excel 文件  # English: Read contains rivers
df1 = pd.read_excel(river_endpoints_files)

# 检查是否存在 COMID 列  # English: Check if it exists
if 'COMID' not in df1.columns:
    raise ValueError("Excel文件中没有找到 'COMID' 列，请检查文件内容")

# 按行读取 COMID，并为每个 COMID 创建一个空的 CSV 文件  # English: Read by line
for comid in df1['COMID']:
    # 确保 COMID 为整数，并转换为字符串  # English: make sure
    comid_str = str(int(comid))

    # 定义每个文件的输出路径（CSV格式）  # English: Define the output path for each file
    output_file = os.path.join(output_folder, f"{comid_str}.csv")

    # 创建一个空的 DataFrame 并保存到 CSV 文件  # English: Create an empty
    pd.DataFrame().to_csv(output_file, index=False)

    print(f"文件已创建: {output_file}")

print("所有文件已创建完毕。")
# ///////////////////-----------------建立河流端点文件 -------------------/////////////////////////  # English: Create a river endpoint file
