#####--------COMPARE IMAGE WITH TEMPLATE MATCH----------#######
#####--------COMPARE IMAGE WITH TEMPLATE MATCH----------#######

import cv2
import numpy as np


stored_image_1 = cv2.imread("C:/Users/Jeremy S Obozuwa/OneDrive/Pictures/Camera Roll/WIN_20250618_05_38_59_Pro.jpg")
stored_image_2 = cv2.imread("C:/Users/Jeremy S Obozuwa/OneDrive/Pictures/Camera Roll/WIN_20250618_05_39_00_Pro.jpg")

cap = cv2.VideoCapture(0)
ret, snapshot = cap.read()
cap.release()

if not ret:
    print("Error: Failed to capture image from webcam.")


stored_image_1 = cv2.cvtColor(stored_image_1, cv2.COLOR_BGR2GRAY)
stored_image_2 = cv2.cvtColor(stored_image_2, cv2.COLOR_BGR2GRAY)

snapshot = cv2.cvtColor(snapshot, cv2.COLOR_BGR2GRAY)

# height, width = stored_image_1.shape  # Get dimensions of the stored image
stored_image_1_resized = cv2.resize(stored_image_1, (350, 350))  # Resize snapshot to match stored image dimensions

# height, width = stored_image_2.shape  # Get dimensions of the stored image
stored_image_2_resized = cv2.resize(stored_image_2, (350, 350))  # Resize snapshot to match stored image dimensions

# height, width = stored_image_2.shape  # Get dimensions of the stored image
snapshot_resized = cv2.resize(snapshot, (350, 350))  # Resize snapshot to match stored image dimensions


result = cv2.matchTemplate(stored_image_1_resized, snapshot_resized, cv2.TM_CCOEFF_NORMED)
match_value = np.max(result)
print(f"Template matching value: {match_value}")


# Display both the stored image and the captured image side by side

# cv2.imshow trowing error i had to block the block hehehehe
"""
combined_image = np.hstack((stored_image_1_resized, snapshot_resized))  # Stack images horizontally
cv2.imshow('Stored Image (Left) vs Captured Image (Right)', combined_image)

cv2.waitKey(10000)
cv2.destroyAllWindows()
"""
threshold = 0.6
if match_value > threshold:
    print("Match successful: Images match.")
else:
    print("Match failed: Images do not match.")

#####--------GENARATE DATA BASE ON NORMAL OPERATION----------#######
#####--------GENARATE DATA BASE ON NORMAL OPERATION----------#######

# import pandas as pd
# import numpy as np

# # Define the fault conditions
# conditions = ["Normal Operation", "Misalignment", "Bearing Fault", "Imbalance", 
#               "Overheating", "Lubrication Failure", "Electrical Fault"]

# # Function to generate random data based on a normal distribution with mean and variance
# def generate_fault_data(base_data, fault_type, start_time, num_samples=20000):
#     fault_data = []
    
#     for i in range(num_samples):
#         new_entry = base_data.copy()
        
        
#         # Introduce variations depending on the fault type
#         if fault_type == "Normal Operation":
#             new_entry['accX'] += np.random.normal(2, 1)  # Increase accX by a certain amount
#             new_entry['accY'] += np.random.normal(2, 1)  # Slight increase in accY
#             new_entry['accZ'] += np.random.normal(2, 2)  # Higher vibration in Z-axis
#             new_entry['temp'] += np.random.normal(4, 1)    # Temperature fluctuation
#             new_entry['hum'] += np.random.normal(2, 1)    # Temperature fluctuation
#             new_entry['sound'] += np.random.normal(3, 2)  # Increase in sound levels

#         elif fault_type == "Misalignment":
#             new_entry['accX'] += np.random.normal(3, 1)  # Increase accX by a certain amount
#             new_entry['accY'] += np.random.normal(2, 1)  # Slight increase in accY
        
#         elif fault_type == "Bearing Fault":
#             new_entry['accZ'] += np.random.normal(5, 2)  # Higher vibration in Z-axis
            
#         elif fault_type == "Imbalance":
#             new_entry['accX'] += np.random.normal(4, 1.5)
#             new_entry['accY'] += np.random.normal(4, 1.5)
#             new_entry['accZ'] += np.random.normal(4, 1.5)  # Significant increase in all axes
            
#         elif fault_type == "Overheating":
#             new_entry['temp'] += np.random.normal(10, 2)  # Higher temperature
        
#         elif fault_type == "Lubrication Failure":
#             new_entry['accZ'] += np.random.normal(2, 0.5)  # Slight increase in vibration
#             new_entry['temp'] += np.random.normal(5, 1)    # Temperature rise over time
            
#         elif fault_type == "Electrical Fault":
#             new_entry['sound'] += np.random.normal(20, 5)  # Increase in sound levels
#             new_entry['temp'] += np.random.normal(2, 1)    # Temperature fluctuation
        
#         # Add the condition label
#         new_entry['Condition'] = fault_type
        
#         # Increment the time by 1 second for each entry
#         time_in_seconds = start_time + i
#         hours = time_in_seconds // 3600
#         minutes = (time_in_seconds % 3600) // 60
#         seconds = time_in_seconds % 60
#         new_entry['Time'] = f"{hours}:{minutes}:{seconds}"
        
#         # Append the new entry to fault_data list
#         fault_data.append(new_entry)
    
#     return fault_data

# # Define base data structure from normal operation
# base_data = {
#     'accX': -9.96,
#     'accY': -2.96,
#     'accZ': 24.56,
#     'temp': 35,
#     'hum': 59.6,
#     'sound': 49,
#     'Time': '0:0:0',
#     'Condition': 'Normal Operation'
# }

# # Create a dataframe to store the final dataset
# columns = ['accX', 'accY', 'accZ', 'temp', 'hum', 'sound', 'Time', 'Condition']
# all_data = pd.DataFrame(columns=columns)

# # Set the initial time in seconds (starting from 0)
# start_time = 0

# # Generate 20000 data points for each condition
# for condition in conditions:
#     fault_data = generate_fault_data(base_data, condition, start_time, num_samples=20000)
#     all_data = pd.concat([all_data, pd.DataFrame(fault_data)])
    
#     # Update start_time to continue the time sequence for the next fault condition
#     start_time += 20000

# # Reset index
# all_data.reset_index(drop=True, inplace=True)

# # Save to CSV
# output_file = "C:/Users/Jeremy S Obozuwa/Desktop/fine_proj/fault_conditions_dataset.csv"
# all_data.to_csv(output_file, index=False)

# output_file


#####--------ADD NEW COLUMN OF DATE TIME ON XLSX FILE----------#######
#####--------ADD NEW COLUMN OF DATE TIME ON XLSX FILE----------#######

# import openpyxl
# from datetime import datetime, timedelta

# # Load the Excel file
# file_path = 'C:/Users/Jeremy S Obozuwa/Desktop/fine_proj/sensor_data_features.xlsx'
# workbook = openpyxl.load_workbook(file_path)
# sheet = workbook.active

# # Insert a new column at the beginning for Datetime (adjust the index as needed)
# sheet.insert_cols(1)

# # Add the datetime header to the new column
# sheet.cell(row=1, column=1).value = "Datetime"

# # Define the start and end dates
# start_date = datetime(2024, 3, 1)   # 1st March 2024
# end_date = datetime(2024, 11, 12)   # 12th November 2024

# # Calculate the total number of rows in the sheet (excluding the header row)
# num_rows = sheet.max_row - 1  # Exclude the header

# # Generate a list of dates between the start and end date
# date_range = [start_date + timedelta(days=i) for i in range((end_date - start_date).days + 1)]

# # Ensure we have enough dates to cover the number of rows
# if len(date_range) < num_rows:
#     print("Error: Not enough dates to cover the rows")
# else:
#     # Add the dates to the first column in 'yy-dd-mm' format
#     for i, row in enumerate(sheet.iter_rows(min_row=2, min_col=1, max_col=1), start=0):
#         if i < len(date_range):
#             date_str = date_range[i].strftime("%y-%d-%m")  # Format the date as yy-dd-mm
#             row[0].value = date_str

# # Save the modified workbook with a new filename
# output_file_path = 'C:/Users/Jeremy S Obozuwa/Desktop/fine_proj/sensor_data_with_datetime.xlsx'
# workbook.save(output_file_path)

# print("Datetime column added and file saved successfully!")

#####--------ADD NEW COLUMN OF DATE TIME ON CSV FILE----------#######
#####--------ADD NEW COLUMN OF DATE TIME ON CSV FILE----------#######

# import pandas as pd
# from datetime import datetime, timedelta

# # Load the CSV file into a DataFrame
# csv_file_path = 'C:/Users/Jeremy S Obozuwa/Desktop/fine_proj/sensor_data_features.csv'
# df = pd.read_csv(csv_file_path)

# # Define the start and end dates
# start_date = datetime(2000, 3, 1)  # 1st March 2024
# end_date = datetime(2024, 11, 12)  # 12th November 2024

# # Calculate the total number of rows in the DataFrame
# num_rows = len(df)

# # Generate a list of dates between the start and end date
# date_range = [start_date + timedelta(days=i) for i in range((end_date - start_date).days + 1)]

# # Ensure we have enough dates to cover the number of rows
# if len(date_range) < num_rows:
#     raise ValueError("Error: Not enough dates to cover all the rows in the CSV file")
# else:
#     # Limit the date range to match the number of rows
#     date_range = date_range[:num_rows]

# # Add the 'Datetime' column to the DataFrame, formatting the date as 'yy-dd-mm'
# df.insert(0, 'Datetime', [date.strftime('%y-%d-%m') for date in date_range])

# # Save the modified DataFrame back to a new CSV file
# output_csv_file_path = 'C:/Users/Jeremy S Obozuwa/Desktop/fine_proj/sensor_data_with_datetime.csv'
# df.to_csv(output_csv_file_path, index=False)

# print("Datetime column added and file saved successfully!")

#####--------ADD NEW COLUMN OF DATE TIME ON CSV FILE REPEAT DATE IF NECESSARY----------#######
#####--------ADD NEW COLUMN OF DATE TIME ON CSV FILE REPEAT DATE IF NECESSARY----------#######

# import pandas as pd
# from datetime import datetime, timedelta

# # Load the CSV file into a DataFrame
# csv_file_path = 'C:/Users/Jeremy S Obozuwa/Desktop/fine_proj/sensor_data_features.csv'
# df = pd.read_csv(csv_file_path)

# # Define the start and end dates
# start_date = datetime(2024, 3, 1)  # 1st March 2024
# end_date = datetime(2024, 11, 12)  # 12th November 2024

# # Calculate the total number of rows in the DataFrame
# num_rows = len(df)

# # Generate a list of dates between the start and end date
# date_range = [start_date + timedelta(days=i) for i in range((end_date - start_date).days + 1)]

# # If there are not enough dates to cover all rows, repeat the date range
# if len(date_range) < num_rows:
#     # Repeat the date range enough times to match the number of rows
#     repeated_dates = (date_range * (num_rows // len(date_range) + 1))[:num_rows]
# else:
#     repeated_dates = date_range[:num_rows]  # Trim the date range if it's larger than needed

# # Add the 'Datetime' column to the DataFrame, formatting the date as 'yy-dd-mm'
# df.insert(0, 'Datetime', [date.strftime('%y-%d-%m') for date in repeated_dates])

# # Save the modified DataFrame back to a new CSV file
# output_csv_file_path = 'C:/Users/Jeremy S Obozuwa/Desktop/fine_proj/sensor_data_with_datetime.csv'
# df.to_csv(output_csv_file_path, index=False)

# print("Datetime column added and file saved successfully!")

#####--------ADD NEW COLUMN OF INDEX TO CSV FILE----------#######
#####--------ADD NEW COLUMN OF INDEX TO CSV FILE----------#######

# import pandas as pd

# # Load the CSV file into a DataFrame
# csv_file_path = 'C:/Users/Jeremy S Obozuwa/Desktop/fine_proj/sensor_data_features.csv'
# df = pd.read_csv(csv_file_path)

# # Generate an index starting from 1 to the length of the DataFrame
# df.insert(0, 'Index', range(1, len(df) + 1))

# # Save the modified DataFrame back to a new CSV file
# output_csv_file_path = 'C:/Users/Jeremy S Obozuwa/Desktop/fine_proj/sensor_data_with_index.csv'
# df.to_csv(output_csv_file_path, index=False)

# print("Index column added and file saved successfully!")

#####--------ADD NEW COLUMN OF INDEX AND DATE TIME FROM 0,0 TO CSV FILE----------#######
#####--------ADD NEW COLUMN OF INDEX AND DATE TIME FROM 0,0 TO CSV FILE----------#######

# import pandas as pd
# from datetime import datetime, timedelta

# # Load the CSV file into a DataFrame
# csv_file_path = 'C:/Users/Jeremy S Obozuwa/Desktop/fine_proj/fault_conditions_dataset.csv'
# df = pd.read_csv(csv_file_path)

# # Generate an index starting from 1 to the length of the DataFrame
# df.insert(0, 'Index', range(1, len(df) + 1))

# # Define the start datetime (1st January 2024, at 00:00:00)
# start_datetime = datetime(2024, 1, 1, 0, 0, 0)

# # Generate a list of datetimes, incrementing by 1 second for each row
# datetime_range = [start_datetime + timedelta(seconds=i) for i in range(len(df))]

# # Format the datetimes in the 'year-month-day-hour-minute-second' format
# df.insert(1, 'datatime', [dt.strftime('%Y-%m-%d-%H-%M-%S') for dt in datetime_range])

# # Save the modified DataFrame back to a new CSV file
# output_csv_file_path = 'C:/Users/Jeremy S Obozuwa/Desktop/fine_proj/fault_datetime.csv'
# df.to_csv(output_csv_file_path, index=False)

# print("Index and Datetime columns added successfully, and file saved!")


# import pandas as pd
# import numpy as np

# def fill_missing_values_with_column_average(df):
#     # Create a copy of the DataFrame to avoid modifying the original
#     df_filled = df.copy()

#     # Iterate over each column
#     for col in df_filled.columns:
#         if pd.api.types.is_numeric_dtype(df_filled[col]):
#             # Calculate the column average, excluding missing values
#             col_avg = df_filled[col].dropna().mean()

#             # Fill missing values with the average and replace zeros with the average
#             df_filled[col] = df_filled[col].fillna(col_avg).replace(0, col_avg)

#     return df_filled

# # Read CSV file
# csv_file_path = "C:/Users/Jeremy S Obozuwa/Downloads/synthetic-csv-data (1)/2.2KW MOTOR/2.2KW MOTOR.csv"
# df = pd.read_csv(csv_file_path)

# # Fill missing values and replace zeros with column averages
# df_filled = fill_missing_values_with_column_average(df)

# # Save the filled DataFrame to a new CSV file
# output_file_path = "C:/Users/Jeremy S Obozuwa/Downloads/synthetic-csv-data (1)/2.2KW MOTOR/2.2KW_MOTOR_filled.csv"
# df_filled.to_csv(output_file_path, index=False)

# # Print the filled DataFrame
# print(df_filled)
