import pandas as pd
import os

# Folder paths
input_folder_path = r"D:\UZH\2024\20240122 Nutrient and Organic Carbon references\DOC\Combination_interpolating_date"
output_folder_path = r"D:\UZH\2024\20240122 Nutrient and Organic Carbon references\DOC\Combination_interpolating_date_supplement_heading_data"

# Ensure the output folder exists
if not os.path.exists(output_folder_path):
    os.makedirs(output_folder_path)

# Function to interpolate missing DOC values at the start of the time series
def interpolate_missing_start(df):
    # Interpolate missing values at the start of the DOC data
    df['DOC'] = df['DOC'].interpolate(method='linear', limit_direction='both')
    return df

# Process each file in the folder
for file_name in os.listdir(input_folder_path):
    if file_name.endswith('.xlsx'):
        input_file_path = os.path.join(input_folder_path, file_name)

        # Read the file (two rows: 'date' and 'DOC')
        df = pd.read_excel(input_file_path)
        df.columns = ['date', 'DOC']  # Ensuring consistent column names

        # Convert 'date' to datetime format
        df['date'] = pd.to_datetime(df['date'])

        # Interpolate missing values at the start
        df = interpolate_missing_start(df)

        # Save processed data to the output folder with the same filename
        output_file_path = os.path.join(output_folder_path, file_name)
        df.to_excel(output_file_path, index=False)

print("Interpolation complete. Files saved in 'Combination_interpolating_date_supplement_heading_data' folder.")
