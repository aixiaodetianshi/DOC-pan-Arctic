import pandas as pd

# 读取Excel文件
file2 = r'D:\UZH\2024\20240122 Nutrient and Organic Carbon references\Arctic\ArcticGRO\insitu_DOC\ArcticGRO_Mackenzie_Discharge_DOC_insitu.xlsx'
df = pd.read_excel(file2)

# 假设日期列名为 'Date'，可以根据实际列名进行修改
df['Date'] = pd.to_datetime(df['Date'], errors='coerce')  # 转换为日期时间格式

# 过滤出日期有效的记录
df = df.dropna(subset=['Date'])

# 提取年份和月份
df['Year'] = df['Date'].dt.year
df['Month'] = df['Date'].dt.month

# 过滤出1月至4月和11月至12月的数据
filtered_df = df[(df['Month'] >= 1) & (df['Month'] <= 4) | (df['Month'] >= 11) & (df['Month'] <= 12)]

# 计算每一年1月至4月和11月至12月的记录天数
record_days_per_year = filtered_df.groupby('Year').size()

# 计算所有年份的总天数
total_days = record_days_per_year.sum()

# 输出每一年记录天数以及总天数
print("每一年1月至4月和11月至12月的记录天数：")
print(record_days_per_year)
print(f"\n所有年份的总天数：{total_days}")


