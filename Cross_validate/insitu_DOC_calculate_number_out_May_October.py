import pandas as pd

# 读取Excel文件  # English: Read
file2 = r'D:\UZH\2024\20240122 Nutrient and Organic Carbon references\Arctic\ArcticGRO\insitu_DOC\ArcticGRO_Mackenzie_Discharge_DOC_insitu.xlsx'
df = pd.read_excel(file2)

# 假设日期列名为 'Date'，可以根据实际列名进行修改  # English: Assume that the date column is
df['Date'] = pd.to_datetime(df['Date'], errors='coerce')  # 转换为日期时间格式  # English: Convert to date and time format

# 过滤出日期有效的记录  # English: Filter out records with valid dates
df = df.dropna(subset=['Date'])

# 提取年份和月份  # English: Extract year and month
df['Year'] = df['Date'].dt.year
df['Month'] = df['Date'].dt.month

# 过滤出1月至4月和11月至12月的数据  # English: Filter out
filtered_df = df[(df['Month'] >= 1) & (df['Month'] <= 4) | (df['Month'] >= 11) & (df['Month'] <= 12)]

# 计算每一年1月至4月和11月至12月的记录天数  # English: Calculate every year
record_days_per_year = filtered_df.groupby('Year').size()

# 计算所有年份的总天数  # English: Calculate the total number of days for all years
total_days = record_days_per_year.sum()

# 输出每一年记录天数以及总天数  # English: Output the number of recorded days and total days per year
print("每一年1月至4月和11月至12月的记录天数：")
print(record_days_per_year)
print(f"\n所有年份的总天数：{total_days}")


