import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
import pickle
from scipy.fft import fft
import datetime

# Load data from CSV
data = pd.read_csv('sensor_data.csv')

# Function to perform FFT on a signal
def perform_fft(signal):
    N = len(signal)
    T = 1.0 / 1.0  # Sampling frequency (1 Hz)
    yf = fft(signal)
    xf = np.fft.fftfreq(N, T)[:N//2]
    return np.abs(yf[0:N//2])

# Extract time series features and perform FFT
data['AccX_fft'] = data['AccX'].rolling(window=10).apply(lambda x: perform_fft(x)[1], raw=True)
data['AccY_fft'] = data['AccY'].rolling(window=10).apply(lambda x: perform_fft(x)[1], raw=True)
data['AccZ_fft'] = data['AccZ'].rolling(window=10).apply(lambda x: perform_fft(x)[1], raw=True)
data['Sound_fft'] = data['Sound'].rolling(window=10).apply(lambda x: perform_fft(x)[1], raw=True)

# Drop rows with NaN values created by rolling window
data = data.dropna()

# Convert time column to datetime format and extract features
data['Time'] = pd.to_datetime(data['Time'], format='%H:%M:%S')
data['Hour'] = data['Time'].dt.hour
data['Minute'] = data['Time'].dt.minute
data['Second'] = data['Time'].dt.second

# Map Fault_Type to numeric values
fault_mapping = {'normal': 0}  # Extend this mapping as needed
data['Fault_Type'] = data['Fault_Type'].map(fault_mapping)

# Features and target
features = ['Humidity', 'Temperature', 'Sound', 'AccX', 'AccY', 'AccZ', 'AccX_fft', 'AccY_fft', 'AccZ_fft', 'Sound_fft', 'Hour', 'Minute', 'Second']
X = data[features]
y = data['Fault_Type']

# Split the data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train a Random Forest Classifier
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Evaluate the model
y_pred = model.predict(X_test)
print(classification_report(y_test, y_pred))

# Save the model to a pickle file
with open('fault_prediction_model.pkl', 'wb') as f:
    pickle.dump(model, f)

print("Model saved to 'fault_prediction_model.pkl'")
