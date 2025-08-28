import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error
import matplotlib.pyplot as plt
import numpy as np
import os
import scipy.stats as stats

river = 'Yukon'
satellite = 'Landsat7'

# Set the font to Times New Roman and adjust other aesthetics
plt.rcParams['font.family'] = 'Times New Roman'
plt.rcParams['axes.labelsize'] = 12
plt.rcParams['axes.titlesize'] = 14
plt.rcParams['xtick.labelsize'] = 10
plt.rcParams['ytick.labelsize'] = 10
plt.rcParams['legend.fontsize'] = 10
plt.rcParams['figure.figsize'] = (6, 6)
plt.rcParams['lines.linewidth'] = 2

# Load the data from Excel
file_path = r'D:\UZH\2024\20240122 Nutrient and Organic Carbon references\Arctic\ArcticGRO\CDOM_DOC_in_situ\May_October_CDOM_DOC\matchup_insitu_remotesensing_CDOM_Landsat57_xlsx\SPP_River_' + river + '_surround_' + satellite + '_10Points_insitu_DOC_CDOM.xlsx'
data = pd.read_excel(file_path)

# Extract file name for saving the figure and coefficients later
file_name = os.path.basename(file_path).replace('.xlsx', '')

# Define the features and target variable
features = ['blue', 'green', 'red', 'NIR', 'ln(blue)', 'ln(green)', 'ln(red)', 'ln(NIR)',
            'blue/NIR', 'green/red', 'green/NIR', 'ln(green/NIR)']
target = 'CDOM'

# Prepare the features and target variable
X = data[features]
y = data[target]

# Take the natural logarithm of the target variable for exponential fitting
y_log = np.log(y)

# Split the data into training and testing sets
X_train, X_test, y_train_log, y_test_log = train_test_split(X, y_log, test_size=0.2, random_state=42)

# Initialize and fit the linear regression model on the log-transformed target variable
model = LinearRegression()
model.fit(X_train, y_train_log)

# Make predictions on the entire dataset and exponentiate the predicted values to convert them back
data['rs_CDOM'] = np.exp(model.predict(X))  # Apply the model to all data and back-transform predictions

# Calculate residuals for performance metrics
y_pred = data['rs_CDOM']
residuals = y - y_pred

# Set a threshold for outlier removal (1 standard deviation from the mean)
threshold = 1*np.std(residuals)

# Filter out data points with large residuals (outliers)
mask = np.abs(residuals) <= threshold
X_filtered = X[mask]
y_filtered = y[mask]
y_pred_filtered = y_pred[mask]

# Calculate performance metrics on filtered data
mse = mean_squared_error(y_filtered, y_pred_filtered)
rmse = np.sqrt(mse)
r2 = r2_score(y_filtered, y_pred_filtered)
mae = mean_absolute_error(y_filtered, y_pred_filtered)
bias = np.mean(residuals)

# Plotting the results
plt.figure()

# Scatter plot of the true vs. predicted values after filtering
plt.scatter(y_filtered, y_pred_filtered, color='dodgerblue', edgecolor='black', alpha=0.6, s=70, label='CDOM')
plt.plot([min(y_filtered), max(y_filtered)], [min(y_filtered), max(y_filtered)],
         color='crimson', linestyle='--', linewidth=2, label='1:1 Line')

# Add a regression line
z = np.polyfit(y_filtered, y_pred_filtered, 1)
p = np.poly1d(z)
plt.plot(y_filtered, p(y_filtered), color='forestgreen', linestyle='-', linewidth=2, label='Regression Line')

# 获取当前轴对象并获取y轴的最小值和最大值  # English: Get the current axis object and get
ax = plt.gca()
y_min, y_max = ax.get_ylim()

# Display river and satellite information at the top left corner of the plot, inside the plot frame
plt.text(min(y_filtered) + 0.02 * (max(y_filtered) - min(y_filtered)),  # 水平位置稍微离边缘有点距离  # English: Horizontal position is slightly away from the edge
         y_max - 0.05 * (y_max - y_min),  # 垂直位置稍微离图像顶部有点距离  # English: The vertical position is slightly away from the top of the image
         f'{river} - {satellite}', fontsize=12,
         bbox=dict(facecolor='white', edgecolor='none', alpha=0.7))

# Display RMSE, R², and the number of filtered records on the plot, below river-satellite info with some padding
plt.text(min(y_filtered) + 0.02 * (max(y_filtered) - min(y_filtered)),  # 同样水平对齐  # English: Same horizontal alignment
         y_max - 0.3 * (y_max - y_min),  # 统计信息位置比river-satellite低一些  # English: Statistical information position ratio
         f'RMSE: {rmse:.2f}\nMAE: {mae:.2f}\nBias: {bias:.2f}\nR²: {r2:.2f}',
         fontsize=10, bbox=dict(facecolor='white', edgecolor='none', alpha=0.7))

# f'RMSE: {rmse:.2f}\nMAE: {mae:.2f}\nBias: {bias:.2f}\nR²: {r2:.2f}\nRecords: {len(y_filtered)}',

# Customize grid and layout for improved appearance
plt.grid(True, which='both', linestyle='--', linewidth=0.5, alpha=0.7)
plt.tight_layout()

# Save the figure as a TIFF file with 300 dpi resolution
output_figure_folder = r'D:\UZH\2024\20240122 Nutrient and Organic Carbon references\Arctic\ArcticGRO\CDOM_DOC_in_situ\May_October_CDOM_DOC\matchup_insitu_remotesensing_CDOM_Landsat57_xlsx'
output_figure_file = os.path.join(output_figure_folder, f"{file_name}.tif")
plt.savefig(output_figure_file, format='tif', dpi=300)

# Show the plot
plt.show()
