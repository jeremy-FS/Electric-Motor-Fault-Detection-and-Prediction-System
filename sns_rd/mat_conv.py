import scipy.io
import pandas as pd

# Function to load .mat file and convert to CSV
def mat_to_csv(mat_file_path, csv_file_path):
    # Load the .mat file
    mat_data = scipy.io.loadmat(mat_file_path)
    
    # Extract variable names (ignoring MATLAB's default metadata variables)
    keys = [key for key in mat_data.keys() if not key.startswith('__')]
    
    # Assuming there is only one key with actual data
    if len(keys) == 1:
        # Convert to DataFrame
        df = pd.DataFrame(mat_data[keys[0]])
    else:
        raise ValueError("Multiple data variables found in .mat file. Specify which one to convert.")
    
    # Save the DataFrame as a CSV file
    df.to_csv(csv_file_path, index=False)
    print(f"Converted {mat_file_path} to {csv_file_path}")

# Example usage
mat_file_path = "C:/Users/Jeremy S Obozuwa/Desktop/C-A-2.mat"  # Path to your .mat file
csv_file_path = 'C:/Users/Jeremy S Obozuwa/Documents/Arduino/sns_rd/sensor_data.csv'  # Path where you want to save the CSV file

mat_data = scipy.io.loadmat(mat_file_path)
print(mat_data)

mat_to_csv(mat_file_path, csv_file_path)
