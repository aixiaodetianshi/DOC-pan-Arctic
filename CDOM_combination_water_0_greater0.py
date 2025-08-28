import pandas as pd
import xlsxwriter
import os

# 设置存放CSV文件的文件夹路径
water_0_folder = r'D:\UZH\2024\20240122 Nutrient and Organic Carbon references\CDOM\water_0\HLSL30_water_0'
# 设置存放转换后XLSX文件的文件夹路径
water_greater_0_folder = r'D:\UZH\2024\20240122 Nutrient and Organic Carbon references\CDOM\water_greater_0\HLSL30'

# 指定要排序的列顺序
desired_columns = ['COMID', 'CDOM', 'date']

# 遍历CSV文件夹中的所有CSV文件
for filename in os.listdir(water_0_folder):
    if filename.endswith(".csv"):  # 只处理CSV文件
        csv_file_path = os.path.join(water_0_folder, filename)

        print(f'文件 {csv_file_path} 正在计算')

        # 读取CSV文件
        df = pd.read_csv(csv_file_path)

        # 如果 'system:index' 和 '.geo' 列存在，删除它们
        df = df.drop(columns=['system:index', '.geo'], errors='ignore')

        # 仅计算非空 CDOM 的 DOC 值并添加为新列
        if 'CDOM' in df.columns:
            df = df.dropna(subset=['CDOM'])
            df['DOC'] = 0.60082 * df['CDOM'] + 1.77043

        # 确保数据框中只包含所需的列，并按指定顺序排列
        sorted_columns = [col for col in desired_columns if col in df.columns]
        df = df[sorted_columns]

        # 构造XLSX文件的文件名和路径
        new_filename = filename.replace('.csv', '_DOC.xlsx')
        xlsx_file_path = os.path.join(xlsx_folder, new_filename)

        # 保存为 XLSX 文件，并在保存后立即释放内存
        with pd.ExcelWriter(xlsx_file_path, engine='xlsxwriter') as writer:
            df.to_excel(writer, index=False)

        # 删除数据框以释放内存
        del df

        print(f'文件 {filename} 已成功转换并存储为 {new_filename}')

print("批量转换完成！")
