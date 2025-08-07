# 计算得到每一parts 1984-2018年期间river discharge年总量

import os
import pandas as pd

# 定义文件夹路径
input_folder = r"D:\UZH\2024\20240122 Nutrient and Organic Carbon references\discharge\river_discharge\Yearly_Proportion_5_10\Mackenzie"
output_folder = r"D:\UZH\2024\20240122 Nutrient and Organic Carbon references\discharge\river_discharge\Yearly_Proportion_5_10"
output_file = os.path.join(output_folder, "Total_discharge_Yearly_Mackenzie_Parts.xlsx")

# 初始化用于存储汇总结果的 DataFrame
Yearly_total = None

# 遍历文件夹内所有 xlsx 文件
for file_name in os.listdir(input_folder):
    if file_name.endswith(".xlsx"):
        file_path = os.path.join(input_folder, file_name)

        # 读取 xlsx 文件，仅选择所需列
        df = pd.read_excel(file_path, usecols=['year', 'Annual_Discharge', 'May-Oct_Discharge'])

        # 按 year 汇总 Annual_Discharge 和 May-Oct_Discharge
        grouped = df.groupby('year', as_index=False).sum()

        # 如果 Yearly_total 是空的，则初始化
        if Yearly_total is None:
            Yearly_total = grouped
        else:
            # 按 year 合并并累加 Annual_Discharge 和 May-Oct_Discharge
            Yearly_total = pd.merge(Yearly_total, grouped, on='year', how='outer', suffixes=('', '_dup'))
            Yearly_total['Annual_Discharge'] = Yearly_total['Annual_Discharge'].fillna(0) + Yearly_total[
                'Annual_Discharge_dup'].fillna(0)
            Yearly_total['May-Oct_Discharge'] = Yearly_total['May-Oct_Discharge'].fillna(0) + Yearly_total[
                'May-Oct_Discharge_dup'].fillna(0)

            # 删除重复列
            Yearly_total = Yearly_total[['year', 'Annual_Discharge', 'May-Oct_Discharge']]

# 按 year 排序
if Yearly_total is not None:
    Yearly_total.sort_values(by='year', inplace=True)
    # 添加新列 Proportion_5_10，计算 May-Oct_Discharge / Annual_Discharge
    Yearly_total['Proportion_5_10'] = Yearly_total['May-Oct_Discharge'] / Yearly_total['Annual_Discharge']
    # 保存为 Excel 文件
    Yearly_total.to_excel(output_file, index=False)
    print(f"结果已保存到 {output_file}")
else:
    print("未找到符合条件的文件，未生成结果文件。")