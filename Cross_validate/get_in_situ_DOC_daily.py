# read DOC from ArcticGRO water quality

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib as mpl

# 设置全局字体为Times New Roman  # English: Set the global font to
mpl.rcParams['font.family'] = 'Times New Roman'

# 读取原始Excel文件并跳过第二行（单位行）  # English: Read original
input_file = 'D:/UZH/2024/20240122 Nutrient and Organic Carbon references/Arctic/ArcticGRO/ArcticGRO_Discharge_DOC.xlsx'
data = pd.read_excel(input_file, sheet_name='Lena', skiprows=[1])  # 跳过第二行单位行  # English: Skip the second line of unit row

# 检查读取的列名  # English: Check the read column name
print("列名：", data.columns)

# 提取所需的列：Date, Discharge, DOC  # English: Extract the required columns
# 根据实际列名修改代码  # English: Modify the code according to the actual column name
selected_columns = data[['Date', 'Discharge', 'DOC']]

# 将Date列转换为datetime类型  # English: Will
selected_columns.loc[:, 'Date'] = pd.to_datetime(selected_columns['Date'])

# A4纸的尺寸（单位：cm），左右边距3.18 cm，上下边距2.54 cm  # English: Paper size
page_width_cm = 21
page_height_cm = 29.7
left_margin_cm = 3.18
right_margin_cm = 3.18
top_margin_cm = 2.54
bottom_margin_cm = 2.54

# 图形尺寸计算  # English: Graphic size calculation
fig_width_cm = page_width_cm - left_margin_cm - right_margin_cm
fig_height_cm = page_height_cm - top_margin_cm - bottom_margin_cm

# 创建图形和子图  # English: Create graphics and sub-graphs
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(fig_width_cm / 2.54, fig_height_cm / 2.54), sharex=True)
dpi = 300  # 较低的DPI值以减小文件大小  # English: Lower

# 绘制第一个图：Discharge  # English: Draw the first picture
ax1.plot(selected_columns['Date'], selected_columns['Discharge'], color='blue', linewidth=2)
ax1.set_ylabel('Discharge/(m3/s)', fontsize=14)
ax1.grid(True)

# 绘制第二个图：DOC  # English: Draw the second figure
ax2.plot(selected_columns['Date'], selected_columns['DOC'], color='green', linewidth=2)
ax2.set_xlabel('Date', fontsize=14)
ax2.set_ylabel('DOC(mg/L)', fontsize=14)
ax2.grid(True)

# 调整日期标签的角度以便于阅读  # English: Adjust the angle of date labels for easy reading
plt.xticks(rotation=45)

# 自动调整布局以适应标签  # English: Automatically adjust the layout to fit the label
plt.tight_layout()

# 显示图表  # English: Show charts
plt.show()

# 保存图表为300 dpi的TIFF文件  # English: Save the chart as
output_file = 'D:/UZH/2024/20240122 Nutrient and Organic Carbon references/Arctic/ArcticGRO/ArcticGRO_Discharge_DOC.tif'
plt.savefig(output_file, dpi=dpi, format='tiff')

# 关闭图形以释放内存  # English: Close the graphics to free up memory
plt.close()

# 将提取的数据保存到新的Excel文件中  # English: Save the extracted data to a new one
output_file = 'D:/UZH/2024/20240122 Nutrient and Organic Carbon references/Arctic/ArcticGRO/ArcticGRO_discharge_DOC_1.xlsx'
selected_columns.to_excel(output_file, index=False)

print(f"数据已成功提取并保存到 {output_file} 中")
