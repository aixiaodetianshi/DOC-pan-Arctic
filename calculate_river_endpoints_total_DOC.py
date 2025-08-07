import pandas as pd
import os

# 设置存放DOC文件的文件夹路径
in_folder = r'D:\UZH\2024\20240122 Nutrient and Organic Carbon references\DOC'
# 设置存放 river endpoints DOC 文件的文件夹路径
out_folder = r'D:\UZH\2024\20240122 Nutrient and Organic Carbon references\DOC_river_endpoint_COMID'

# 如果存储 river endpoints DOC 文件的文件夹不存在，则创建
if not os.path.exists(out_folder):
    os.makedirs(out_folder)

# 指定要排序的列顺序
desired_columns = ['date', 'COMID', 'CDOM', 'DOC']

# 日期格式
date_format = '%Y-%m-%d'

# 遍历CSV文件夹中的所有CSV文件
for filename in os.listdir(csv_folder):
    if filename.endswith(".csv"):  # 只处理CSV文件
        # 构造完整的CSV文件路径
        csv_file_path = os.path.join(csv_folder, filename)

        # 读取CSV文件
        df = pd.read_csv(csv_file_path)

        # 如果 'system:index' 和 '.geo' 列存在，删除它们
        df = df.drop(columns=['system:index', '.geo'], errors='ignore')

        # 转换 'date' 列为日期格式（如果存在这些列）
        if 'date' in df.columns:
            df['date'] = pd.to_datetime(df['date'], errors='coerce').dt.strftime(date_format)

        # 仅计算非空 CDOM 的 DOC 值并添加为新列
        if 'CDOM' in df.columns:
            # 删除 CDOM 为空值的行
            df = df.dropna(subset=['CDOM'])
            # 计算 DOC
            df['DOC'] = 138.36818 * df['CDOM'] + 1.77048

        # 确保数据框中只包含所需的列，并按指定顺序排列
        # 使用intersection方法来确保只选择数据框中存在的列，防止列缺失时出错
        sorted_columns = [col for col in desired_columns if col in df.columns]
        df = df[sorted_columns]

        # 将CSV扩展名替换为XLSX
        new_filename = filename.replace('.csv', '_DOC.xlsx')

        # 构造XLSX文件的完整路径
        xlsx_file_path = os.path.join(xlsx_folder, new_filename)

        # 保存为XLSX文件
        df.to_excel(xlsx_file_path, index=False)

        print(f'文件 {filename} 已成功转换并存储为 {new_filename}')

print("批量转换完成！")

