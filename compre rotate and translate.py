# import numpy as np
# import pandas as pd

# # Function to generate synthetic sensor data
# def generate_data(condition, num_samples, freq=50):
#     data = []
    
#     for _ in range(num_samples):
#         # Simulate sensor data with one value per feature
#         accX = np.random.normal(0, 0.1)
#         accY = np.random.normal(0, 0.1)
#         accZ = np.random.normal(0, 0.1)
#         temp = np.random.normal(40, 2)
#         hum = np.random.normal(50, 5)
#         sound = np.random.normal(60, 3)
        
#         # Append the data as a row with the condition label
#         data.append([accX, accY, accZ, temp, hum, sound, condition])
    
#     return data

# # Define conditions and number of samples per condition
# conditions = ["Normal Operation", "Misalignment", "Bearing Fault", "Imbalance", 
#               "Overheating", "Lubrication Failure", "Electrical Fault"]
# num_samples = 1000  # Set this to the desired number of samples per condition

# # Initialize an empty list to hold all the data
# all_data = []

# # Loop over each condition and generate data
# for condition in conditions:
#     data = generate_data(condition, num_samples)
#     all_data.extend(data)  # Add the generated data to the list

# # Convert the list to a DataFrame
# columns = ['accX', 'accY', 'accZ', 'temp', 'hum', 'sound', 'condition']
# df = pd.DataFrame(all_data, columns=columns)

# # Save the DataFrame to CSV
# try:
#     df.to_csv('sensor_data_features1.csv', index=False)
#     print('Saved to CSV in the format: accX, accY, accZ, temp, hum, sound, condition')
# except Exception as e:
#     print(f"Failed to save CSV: {e}")


# import numpy as np
# import pandas as pd

# # Function to generate synthetic sensor data
# def generate_data(condition, num_samples, freq=50):
#     data = []
    
#     for _ in range(num_samples):
#         t = np.linspace(0, 1, freq)
        
#         if condition == "Normal Operation":
#             accX = np.random.normal(0, 0.1, freq)
#             accY = np.random.normal(0, 0.1, freq)
#             accZ = np.random.normal(0, 0.1, freq)
#             temp = np.random.normal(40, 2)
#             hum = np.random.normal(50, 5)
#             sound = np.random.normal(60, 3)
        
#         elif condition == "Misalignment":
#             accX = np.sin(2 * np.pi * 5 * t) + np.random.normal(0, 0.5, freq)
#             accY = np.sin(2 * np.pi * 5 * t) + np.random.normal(0, 0.3, freq)
#             accZ = np.sin(2 * np.pi * 5 * t) + np.random.normal(0, 0.5, freq)
#             temp = np.random.normal(45, 3)
#             hum = np.random.normal(52, 5)
#             sound = np.random.normal(65, 5)
        
#         elif condition == "Bearing Fault":
#             accX = np.random.normal(0.3, 0.7, freq) + np.sin(2 * np.pi * 10 * t)
#             accY = np.random.normal(0.3, 0.7, freq) + np.sin(2 * np.pi * 10 * t)
#             accZ = np.random.normal(0.3, 0.7, freq) + np.sin(2 * np.pi * 10 * t)
#             temp = np.random.normal(50, 4)
#             hum = np.random.normal(55, 5)
#             sound = np.random.normal(70, 7)
        
#         elif condition == "Imbalance":
#             accX = 0.4 * np.sin(2 * np.pi * 3 * t) + np.random.normal(0, 0.6, freq)
#             accY = 0.4 * np.sin(2 * np.pi * 3 * t) + np.random.normal(0, 0.6, freq)
#             accZ = 0.4 * np.sin(2 * np.pi * 3 * t) + np.random.normal(0, 0.6, freq)
#             temp = np.random.normal(42, 3)
#             hum = np.random.normal(53, 5)
#             sound = np.random.normal(68, 6)
        
#         elif condition == "Overheating":
#             accX = np.random.normal(0.2, 0.2, freq)
#             accY = np.random.normal(0.2, 0.2, freq)
#             accZ = np.random.normal(0.2, 0.2, freq)
#             temp = np.random.normal(80, 5)
#             hum = np.random.normal(40, 4)
#             sound = np.random.normal(72, 5)
        
#         elif condition == "Lubrication Failure":
#             accX = 0.5 * np.random.normal(0, 0.3, freq) + np.cos(2 * np.pi * 7 * t)
#             accY = 0.5 * np.random.normal(0, 0.3, freq) + np.cos(2 * np.pi * 7 * t)
#             accZ = 0.5 * np.random.normal(0, 0.3, freq) + np.cos(2 * np.pi * 7 * t)
#             temp = np.random.normal(60, 4)
#             hum = np.random.normal(45, 5)
#             sound = np.random.normal(75, 6)
        
#         elif condition == "Electrical Fault":
#             accX = np.random.normal(0.1, 0.1, freq)
#             accY = np.random.normal(0.1, 0.1, freq)
#             accZ = np.random.normal(0.1, 0.1, freq)
#             temp = np.random.normal(65, 5)
#             hum = np.random.normal(50, 5)
#             sound = np.random.normal(80, 10)
        
#         data.append([accX.mean(), accY.mean(), accZ.mean(), temp, hum, sound])
    
#     return pd.DataFrame(data, columns=['accX', 'accY', 'accZ', 'temp', 'hum', 'sound'])

# # Conditions and number of samples
# conditions = ["Normal Operation", "Misalignment", "Bearing Fault", "Imbalance", 
#               "Overheating", "Lubrication Failure", "Electrical Fault"]
# num_samples = 20000
# freq = 50

# all_features = []

# for condition in conditions:
#     # Generate data for the given condition
#     data = generate_data(condition, num_samples, freq)
    
#     # Add labels to the data
#     data['condition'] = condition
    
#     # Append to the all_features list
#     all_features.append(data)

# # Concatenate all features into one DataFrame
# final_features = pd.concat(all_features, ignore_index=True)

# # Save to CSV with a try-except block
# try:
#     final_features.to_csv('sensor_data_features.csv', index=False)
#     print('Saved to CSV')  # Print confirmation after saving

#     # Print the first 5 rows as required in the specified format
#     print("First 5 rows of the dataset:")
#     print(final_features.head(5).to_string(index=False, header=False))  # Print without index and headers

# except Exception as e:
#     print(f"Failed to save CSV: {e}")


import numpy as np
import pandas as pd

# Function to generate synthetic sensor data
def generate_data(condition, num_samples, freq=50):
    data = []
    
    for _ in range(num_samples):
        t = np.linspace(0, 1, freq)
        
        if condition == "Normal Operation":
            accX = np.random.normal(-7, 2, freq)
            accY = np.random.normal(-2, 2, freq)
            accZ = np.random.normal(22, 2, freq)
            temp = np.random.normal(40, 2)
            hum = np.random.normal(50, 5)
            sound = np.random.normal(50, 3)
        
        elif condition == "Misalignment":
            accX = np.sin(2 * np.pi * 5 * t) + np.random.normal(-10, 5, freq)
            accY = np.sin(2 * np.pi * 5 * t) + np.random.normal(-5, 3, freq)
            accZ = np.sin(2 * np.pi * 5 * t) + np.random.normal(25, 5, freq)
            temp = np.random.normal(45, 3)
            hum = np.random.normal(52, 5)
            sound = np.random.normal(55, 5)
        
        elif condition == "Bearing Fault":
            accX = np.random.normal(-13, 7, freq) + np.sin(2 * np.pi * 10 * t)
            accY = np.random.normal(-7, 7, freq) + np.sin(2 * np.pi * 10 * t)
            accZ = np.random.normal(30, 5, freq) + np.sin(2 * np.pi * 10 * t)
            temp = np.random.normal(50, 4)
            hum = np.random.normal(55, 5)
            sound = np.random.normal(60, 7)
        
        elif condition == "Imbalance":
            accX = 0.4 * np.sin(2 * np.pi * 3 * t) + np.random.normal(-14, 6, freq)
            accY = 0.4 * np.sin(2 * np.pi * 3 * t) + np.random.normal(-9, 6, freq)
            accZ = 0.4 * np.sin(2 * np.pi * 3 * t) + np.random.normal(30, 7, freq)
            temp = np.random.normal(42, 3)
            hum = np.random.normal(53, 5)
            sound = np.random.normal(58, 6)
        
        elif condition == "Overheating":
            accX = np.random.normal(-7, 2, freq)
            accY = np.random.normal(-2, 2, freq)
            accZ = np.random.normal(22, 2, freq)
            temp = np.random.normal(42, 5)
            hum = np.random.normal(35, 4)
            sound = np.random.normal(72, 5)
        
        elif condition == "Lubrication Failure":
            accX = 0.5 * np.random.normal(-14, 6, freq) + np.cos(2 * np.pi * 7 * t)
            accY = 0.5 * np.random.normal(-9, 6, freq) + np.cos(2 * np.pi * 7 * t)
            accZ = 0.5 * np.random.normal(30, 6, freq) + np.cos(2 * np.pi * 7 * t)
            temp = np.random.normal(42, 4)
            hum = np.random.normal(35, 5)
            sound = np.random.normal(55, 6)
        
        elif condition == "Electrical Fault":
            accX = np.random.normal(-5, 2, freq)
            accY = np.random.normal(-3, 2, freq)
            accZ = np.random.normal(20, 3, freq)
            temp = np.random.normal(45, 5)
            hum = np.random.normal(30, 5)
            sound = np.random.normal(60, 10)
        
        data.append([accX.mean(), accY.mean(), accZ.mean(), temp, hum, sound])
    
    return pd.DataFrame(data, columns=['accX', 'accY', 'accZ', 'temp', 'hum', 'sound'])

# Conditions and number of samples
conditions = ["Normal Operation", "Misalignment", "Bearing Fault", "Imbalance", 
              "Overheating", "Lubrication Failure", "Electrical Fault"]
num_samples = 2
freq = 50

all_features = []

for condition in conditions:
    # Generate data for the given condition
    data = generate_data(condition, num_samples, freq)
    
    # Add labels to the data
    data['condition'] = condition
    
    # Append to the all_features list
    all_features.append(data)

# Concatenate all features into one DataFrame
final_features = pd.concat(all_features, ignore_index=True)

# Save to CSV with a try-except block
try:
    final_features.to_csv('new_sensor__features.csv', index=False)
    print('Saved to CSV')  # Print confirmation after saving

    # Print the first 5 rows as required in the specified format
    print("First 5 rows of the dataset:")
    print(final_features.head(5).to_string(index=False, header=False))  # Print without index and headers

except Exception as e:
    print(f"Failed to save CSV: {e}")