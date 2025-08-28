import pandas as pd
import os

# Folder paths
doc_folder_path = r"D:\UZH\2024\20240122 Nutrient and Organic Carbon references\DOC\Combination_interpolating_date_supplement_heading_data"
discharge_folder_path = r"D:\UZH\2024\20240122 Nutrient and Organic Carbon references\discharge\river_discharge"
output_folder_path = r"D:\UZH\2024\20240122 Nutrient and Organic Carbon references\DOC\Total_river_DOC"

# Ensure the output folder exists
if not os.path.exists(output_folder_path):
    os.makedirs(output_folder_path)

# Process each DOC file in the folder
for file_name in os.listdir(doc_folder_path):
    if file_name.endswith('.xlsx'):
        # Paths for DOC and discharge files
        doc_file_path = os.path.join(doc_folder_path, file_name)
        discharge_file_path = os.path.join(discharge_folder_path, file_name)

        # Check if corresponding discharge file exists
        if os.path.exists(discharge_file_path):
            # Read DOC and discharge data
            doc_df = pd.read_excel(doc_file_path, names=['date', 'DOC'])
            discharge_df = pd.read_excel(discharge_file_path, names=['time', 'discharge'])

            # Convert date columns to datetime
            doc_df['date'] = pd.to_datetime(doc_df['date'])
            discharge_df['time'] = pd.to_datetime(discharge_df['time'])

            # Merge DOC and discharge data on matching dates
            merged_df = pd.merge(doc_df, discharge_df, left_on='date', right_on='time')

            # Calculate total_DOC as DOC * discharge * 86400
            merged_df['total_DOC'] = merged_df['DOC'] * merged_df['discharge'] * 86400 / 1000000

            # Select only the date and total_DOC columns for output
            result_df = merged_df[['date', 'total_DOC']]

            # Output path for saving the result
            output_file_path = os.path.join(output_folder_path, file_name)

            # Save the result to the output folder
            result_df.to_excel(output_file_path, index=False)

print("Processing complete. Total DOC files saved in 'Total_river_DOC' folder.")
