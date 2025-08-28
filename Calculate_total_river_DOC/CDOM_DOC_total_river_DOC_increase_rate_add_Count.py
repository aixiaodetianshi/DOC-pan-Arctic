import pandas as pd

# 输入文件路径  # English: Enter file path
input_file = r'D:\UZH\2024\20240122 Nutrient and Organic Carbon references\3_river_mouth_DOC\DOC_update_20250203\Total_DOC_increase_rate\Annual_increase_rate_DOC_All_Property.csv'

# 读取数据  # English: Read data
df = pd.read_csv(input_file)

# 检查是否存在COMID列  # English: Check if it exists
if 'COMID' not in df.columns:
    raise ValueError("文件中未找到 'COMID' 列，请检查列名是否正确。")

# 统计每个COMID出现的次数  # English: Statistics for each
comid_counts = df['COMID'].value_counts()

# 映射每一行对应COMID的计数  # English: Map each row corresponding
df['Num_same_COMID'] = df['COMID'].map(comid_counts)

# 或者保存为新文件：  # English: Or save as a new file
output_file = input_file.replace('.csv', '_with_COMID_count.csv')
df.to_csv(output_file, index=False)

print(f"处理完成，文件已保存至：{output_file}")
