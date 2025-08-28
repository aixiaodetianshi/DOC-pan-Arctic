
import pandas as pd
import os

# 输入文件夹路径  # English: Enter the folder path
input_folder = r'D:\UZH\2024\20240122 Nutrient and Organic Carbon references\DOC\Combination_sort_date'

out_file_path = r'D:\UZH\2024\20240122 Nutrient and Organic Carbon references\DOC\CDOM_DOC_stastics_date_count.xlsx'
desired_colume = []

# 遍历文件夹中的所有文件  # English: Iterate through all files in the folder
for filename in os.listdir(input_folder):
    in_file_path = os.path.join(input_folder, filename)
    print(f'文件 {in_file_path} 正在准备')

    COMID = filename[0:8]

    # 读取 Excel 文件  # English: Read
    df_DOC = pd.read_excel(in_file_path)
    # 检查 DataFrame 是否为空  # English: examine
    if df_DOC.empty:
        print(f"文件 {filename} 数据为空，跳过该文件。")

        count = 0
        start_date = '1984-01-01'
        end_date = '1984-01-01'
        desired_colume.append([COMID, count, start_date, end_date])

        continue  # 跳过为空的文件  # English: Skip empty files

    # calculate
    count = len(df_DOC)  # 记录条数  # English: Number of records
    start_date = df_DOC['date'].min()  # 第一个日期  # English: The first date
    end_date = df_DOC['date'].max()  # 最后一个日期  # English: Last date

    desired_colume.append([COMID, count, start_date, end_date])

# 将结果转换为 DataFrame  # English: Convert the result to
results_df = pd.DataFrame(desired_colume, columns=['COMID', 'count', 'start_date', 'end_date'])

# 保存到新的 Excel 文件  # English: Save to new
results_df.to_excel(out_file_path, index=False)

print("所有文件已成功生成！")