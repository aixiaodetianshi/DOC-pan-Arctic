import pandas as pd
import os

# 设置存放CSV文件的文件夹路径
csv_folder = r'D:\UZH\2024\20240122 Nutrient and Organic Carbon references\Arctic\ArcticGRO\CDOM_DOC_in_situ\May_October_CDOM_DOC\matchup_insitu_remotesensing_CDOM_HLSS30_csv'
# 设置存放转换后XLSX文件的文件夹路径
xlsx_folder = r'D:\UZH\2024\20240122 Nutrient and Organic Carbon references\Arctic\ArcticGRO\CDOM_DOC_in_situ\May_October_CDOM_DOC\matchup_insitu_remotesensing_CDOM_HLSS30_xlsx'

# 如果存储XLSX文件的文件夹不存在，则创建
if not os.path.exists(xlsx_folder):
    os.makedirs(xlsx_folder)

# 指定要排序的列顺序
desired_columns = ['date', 'insitu_date', 'ultra_blue', 'blue', 'green', 'red', 'NIR',
                   'ln(ultra_blue)', 'ln(blue)', 'ln(green)', 'ln(red)', 'ln(NIR)',
                   'blue/NIR', 'green/red', 'green/NIR', 'ln(green/NIR)', 'CDOM', 'DOC']

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

        # 转换 'date' 和 'insitu_date' 列为日期格式（如果存在这些列）
        if 'date' in df.columns:
            df['date'] = pd.to_datetime(df['date'], errors='coerce').dt.strftime(date_format)
        if 'insitu_date' in df.columns:
            df['insitu_date'] = pd.to_datetime(df['insitu_date'], errors='coerce').dt.strftime(date_format)

        df['ultra_blue'] = df['ultra_blue']/10000
        df['blue'] = df['blue']/10000
        df['green'] = df['green']/10000
        df['red'] = df['red']/10000
        df['NIR'] = df['NIR']/10000

        df['ln(ultra_blue)'] = df['ln(ultra_blue)']-9.21034037198
        df['ln(blue)'] = df['ln(blue)']-9.21034037198
        df['ln(green)'] = df['ln(green)']-9.21034037198
        df['ln(red)'] = df['ln(red)']-9.21034037198
        df['ln(NIR)'] = df['ln(NIR)']-9.21034037198

        # 确保数据框中只包含所需的列，并按指定顺序排列
        # 使用intersection方法来确保只选择数据框中存在的列，防止列缺失时出错
        sorted_columns = [col for col in desired_columns if col in df.columns]
        df = df[sorted_columns]

        # 将CSV扩展名替换为XLSX
        new_filename = filename.replace('.csv', '.xlsx')

        # 构造XLSX文件的完整路径
        xlsx_file_path = os.path.join(xlsx_folder, new_filename)

        # 保存为XLSX文件
        df.to_excel(xlsx_file_path, index=False)

        print(f'文件 {filename} 已成功转换并存储为 {new_filename}')

print("批量转换完成！")
