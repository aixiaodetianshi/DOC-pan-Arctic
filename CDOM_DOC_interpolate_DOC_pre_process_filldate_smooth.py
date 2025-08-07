
# LOESS 平滑
#
# 采用 局部回归平滑（LOWESS），对 DOC 数据进行非参数回归。
# 参数 frac=0.05 控制平滑程度，可调节使数据 既平滑又保留趋势。
# 迭代 3 次 (it=3) 以增强稳定性。
# 时间连续性
#
# 读取文件中的 date 列，确保时间数据 完整无缺失。
# 确保数据按日期 升序排列 进行平滑。
# 适用性
#
# 适用于 长期环境数据，避免移动平均法可能导致的数据失真。
# 可用于 减少突发性异常波动，但仍保留 DOC 的真实长期变化趋势。


import pandas as pd
import os
from statsmodels.nonparametric.smoothers_lowess import lowess

# 文件夹路径
input_folder = r"D:\UZH\2024\20240122 Nutrient and Organic Carbon references\DOC\DOC_update_20250203\Combination_single_river_sort_date_pre_process_filldate"
output_folder = r"D:\UZH\2024\20240122 Nutrient and Organic Carbon references\DOC\DOC_update_20250203\Combination_single_river_sort_date_pre_process_smooth"
os.makedirs(output_folder, exist_ok=True)

frac = 0.05  # LOESS 平滑参数
num_cols = ['CDOM', 'CDOM_uncertainty', 'DOC', 'DOC_uncertainty']

for filename in os.listdir(input_folder):
    if not filename.endswith(".csv"):
        continue

    input_file = os.path.join(input_folder, filename)
    output_file = os.path.join(output_folder, filename)

    try:
        # 读取数据
        df = pd.read_csv(input_file, dtype=str)

        # 解析日期
        df['date'] = pd.to_datetime(df['date'], errors='coerce')

        # 找出无法解析的日期
        invalid_dates = df[df['date'].isna()]
        if not invalid_dates.empty:
            print(f"⚠️ 文件 {filename} 存在无法解析的日期，跳过以下行：")
            print(invalid_dates.head())

        # 删除无效日期
        df = df.dropna(subset=['date']).sort_values(by='date')

        # 确保日期转换成功
        if df.empty:
            print(f"❌ 文件 {filename} 没有有效的日期数据，跳过")
            continue

        # 确保数值列为 float 类型
        df[num_cols] = df[num_cols].apply(pd.to_numeric, errors='coerce')

        # 转换日期为 Unix 时间戳
        date_numeric = df['date'].astype('int64') // 10**9

        # 对每个变量进行 LOESS 平滑
        for col in num_cols:
            valid_data = df[col].dropna()
            if len(valid_data) > 5:
                smoothed_values = lowess(valid_data, date_numeric[valid_data.index], frac=frac, it=3, return_sorted=False)
                df.loc[valid_data.index, col] = smoothed_values

        # 线性插值填充
        df[num_cols] = df[num_cols].interpolate(method='linear', limit_direction='both')

        # 保存结果
        df.to_csv(output_file, index=False)
        print(f"✅ 平滑完成: {filename} -> {output_file}")

    except Exception as e:
        print(f"❌ 处理文件 {filename} 时报错: {e}")

print("🎉 所有文件处理完成！")
