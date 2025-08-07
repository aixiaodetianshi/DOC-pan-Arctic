import matplotlib.pyplot as plt
import numpy as np

# 设置全局字体
plt.rcParams["font.family"] = "Arial"

# 数据
basins = ["Ob", "Yenisey", "Lena", "Kolyma", "Yukon", "Mackenzie"]
rivers = [2360, 125, 643, 631, 331, 6466]
watersheds = [10097, 399, 2356, 2070, 1706, 21853]
wedge_colors = ["#8dd3cf", "#ffffb3", "#bebaba", "#fb8072", "#80b1d3", "#fdb462"]

# 计算比例
river_percentages = np.array(rivers) / sum(rivers) * 100
watershed_percentages = np.array(watersheds) / sum(watersheds) * 100

# 绘制河流数量饼状图
fig1, ax1 = plt.subplots(figsize=(7, 7))
wedges1, texts1, autotexts1 = ax1.pie(
    rivers,
    labels=None,  # 取消默认标签
    autopct=lambda p: f'{p:.1f}%\n({int(p*sum(rivers)/100)})',
    colors=wedge_colors,
    startangle=140,
    textprops={"fontsize": 6},
    labeldistance=0.6  # 使百分比文本靠近中心
)
ax1.set_title("Distribution of Rivers Across Major Arctic Basins", fontsize=6, pad=-160)

# 在饼图内部添加标签
for i, (wedge, label) in enumerate(zip(wedges1, basins)):
    angle = (wedge.theta2 + wedge.theta1) / 2  # 计算角度
    x = 0.75 * np.cos(np.radians(angle))
    y = 0.75 * np.sin(np.radians(angle))
    ax1.text(x, y, label, ha='center', va='center', fontsize=6, color='black')

# 保存河流数量饼状图
save_path_rivers = "D:/UZH/2024/20240122 Nutrient and Organic Carbon references/DOC/DOC_update_20250203/nature_comm_piechart_rivers.tif"
plt.savefig(save_path_rivers, dpi=600, bbox_inches='tight', format='tiff')
plt.close()

# 绘制流域数量饼状图
fig2, ax2 = plt.subplots(figsize=(7, 7))
wedges2, texts2, autotexts2 = ax2.pie(
    watersheds,
    labels=None,  # 取消默认标签
    autopct=lambda p: f'{p:.1f}%\n({int(p*sum(watersheds)/100)})',
    colors=wedge_colors,
    startangle=140,
    textprops={"fontsize": 6},
    labeldistance=0.6  # 使百分比文本靠近中心
)
ax2.set_title("Distribution of Watersheds Across Major Arctic Basins", fontsize=6, pad=-200)

# 在饼图内部添加标签
for i, (wedge, label) in enumerate(zip(wedges2, basins)):
    angle = (wedge.theta2 + wedge.theta1) / 2  # 计算角度
    x = 0.75 * np.cos(np.radians(angle))
    y = 0.75 * np.sin(np.radians(angle))
    ax2.text(x, y, label, ha='center', va='center', fontsize=6, color='black')

# 保存流域数量饼状图
save_path_watersheds = "D:/UZH/2024/20240122 Nutrient and Organic Carbon references/DOC/DOC_update_20250203/nature_comm_piechart_watersheds.tif"
plt.savefig(save_path_watersheds, dpi=600, bbox_inches='tight', format='tiff')
plt.close()
