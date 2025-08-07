import matplotlib.pyplot as plt
import matplotlib.image as mpimg

# 定义图片路径（按5月到10月顺序）
image_paths = [
    r"D:\UZH\2024\20240122 Nutrient and Organic Carbon references\DOC\DOC_update_20250203\Total_DOC_monthly\Mackenzie_month\Total_monthly_DOC_Mackenzie_Parts_5.tif",
    r"D:\UZH\2024\20240122 Nutrient and Organic Carbon references\DOC\DOC_update_20250203\Total_DOC_monthly\Mackenzie_month\Total_monthly_DOC_Mackenzie_Parts_6.tif",
    r"D:\UZH\2024\20240122 Nutrient and Organic Carbon references\DOC\DOC_update_20250203\Total_DOC_monthly\Mackenzie_month\Total_monthly_DOC_Mackenzie_Parts_7.tif",
    r"D:\UZH\2024\20240122 Nutrient and Organic Carbon references\DOC\DOC_update_20250203\Total_DOC_monthly\Mackenzie_month\Total_monthly_DOC_Mackenzie_Parts_8.tif",
    r"D:\UZH\2024\20240122 Nutrient and Organic Carbon references\DOC\DOC_update_20250203\Total_DOC_monthly\Mackenzie_month\Total_monthly_DOC_Mackenzie_Parts_9.tif",
    r"D:\UZH\2024\20240122 Nutrient and Organic Carbon references\DOC\DOC_update_20250203\Total_DOC_monthly\Mackenzie_month\Total_monthly_DOC_Mackenzie_Parts_10.tif"
]

# 定义子图标签
labels = ['(a)', '(b)', '(c)', '(d)', '(e)', '(f)']

# 创建 3 行 2 列的子图
fig, axs = plt.subplots(3, 2, figsize=(18/2.54, 24/2.54))  # 调整为 18cm × 24cm，更紧凑

# 循环读取并显示图片
for ax, img_path, label in zip(axs.flat, image_paths, labels):
    img = mpimg.imread(img_path)
    ax.imshow(img)
    ax.axis('off')  # 关闭坐标轴
    # 在左上角添加子图序号
    ax.text(0.02, 0.95, label, transform=ax.transAxes,
            fontsize=6, fontweight='bold', va='top', ha='left')

# 调整布局，使子图更加紧凑
plt.subplots_adjust(wspace=0.05, hspace=0.05)  # 减少水平和垂直间距

# 保存高分辨率.tif图片，符合Nature Communications要求
output_path = r"D:\UZH\2024\20240122 Nutrient and Organic Carbon references\DOC\DOC_update_20250203\Total_DOC_monthly\Mackenzie_month\Total_monthly_DOC_Mackenzie_Parts.tif"
plt.savefig(output_path, dpi=600, bbox_inches='tight', pad_inches=0.02)

# 显示排版结果
plt.show()
