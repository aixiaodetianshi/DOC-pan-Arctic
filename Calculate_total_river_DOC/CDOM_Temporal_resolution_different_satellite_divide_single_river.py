# 输入文件类型：代码现在专门处理 .csv 文件。  # English: Enter file type
# 必要列检查：确保每个文件包含 COMID 和 date 两列，缺少时会提示错误并跳过该文件。  # English: Necessary column check
# 日期格式化：将 date 列转换为 datetime 格式，确保日期处理无误。  # English: Date formatting
# 数据去重：在保存之前，确保每个 COMID 的日期数据无重复。  # English: Data removal
# 输出文件命名：以 COMID 命名的 .xlsx 文件保存到目标文件夹。  # English: Output file naming

import pandas as pd
import os

# 输入文件夹路径  # English: Enter the folder path
in_folder = r'D:\UZH\2024\20240122 Nutrient and Organic Carbon references\CDOM\temporal_resolution\HLSL30'
# 输出文件夹路径  # English: Output folder path
output_folder = r'D:\UZH\2024\20240122 Nutrient and Organic Carbon references\CDOM\temporal_resolution\HLSL30_COMID'

# 如果输出文件夹不存在，则创建  # English: If the output folder does not exist
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# 遍历CSV文件夹中的所有CSV文件  # English: Traversal
for filename in os.listdir(in_folder):
    if filename.endswith(".csv"):
        in_file_path = os.path.join(in_folder, filename)
        print(f'正在处理文件: {in_file_path}')

        # 检查文件是否为空  # English: Check if the file is empty
        if os.stat(in_file_path).st_size == 0:
            print(f"文件 {filename} 是空文件，跳过处理。")
            continue

        # 读取CSV文件  # English: Read
        try:
            df = pd.read_csv(in_file_path)
        except pd.errors.EmptyDataError:
            print(f"文件 {filename} 是空文件，跳过处理。")
            continue
        except Exception as e:
            print(f"文件 {filename} 无法读取: {e}")
            continue

        # 检查数据是否包含必要的列  # English: Check if the data contains the necessary columns
        if 'COMID' not in df.columns or 'date' not in df.columns:
            print(f"文件 {filename} 缺少必要的列 'COMID' 或 'date'，请检查文件结构。")
            continue

        # 确保 COMID 转换为整数  # English: make sure
        try:
            df['COMID'] = df['COMID'].astype(int)
        except Exception as e:
            print(f"文件 {filename} 的 'COMID' 列无法转换为整数类型: {e}")
            continue

        # 确保日期列格式正确  # English: Make sure the date column is formatted correctly
        try:
            df['date'] = pd.to_datetime(df['date'])
        except Exception as e:
            print(f"文件 {filename} 的日期格式有问题: {e}")
            continue

        # 按河流 COMID 分组  # English: By river
        grouped = df.groupby('COMID')

        # 遍历每个 COMID 分组，将数据日期保存为单独的 Excel 文件  # English: Iterate through each
        for comid, group_data in grouped:
            # 创建输出文件路径  # English: Create output file path
            output_file = os.path.join(output_folder, f'{comid}.xlsx')

            # 仅保留日期列并去重，按日期排序  # English: Only keep the date column and deduplicate it
            unique_dates = group_data[['date']].drop_duplicates().sort_values(by='date')

            # 保存到 Excel 文件  # English: Save to
            try:
                unique_dates.to_excel(output_file, index=False)
                print(f'文件 {output_file} 已成功保存。')
            except Exception as e:
                print(f"文件 {output_file} 保存失败: {e}")

print("所有文件已成功生成！")
