import numpy as np
import pandas as pd
import scipy.stats as stats
from scipy.fftpack import fft

def extract_features(data):
    features = []

    for i in range(len(data)):
        row = data.iloc[i]

        accX = np.array([row['accX']])
        accY = np.array([row['accY']])
        accZ = np.array([row['accZ']])
        sound = np.array([row['sound']])

        # Ensure arrays are not empty before processing
        if accX.size == 0 or accY.size == 0 or accZ.size == 0 or sound.size == 0:
            # Handle the empty array situation (e.g., skip this row)
            continue

        # Time-domain features (only if arrays are not empty)
        time_features = {
            "mean_accX": np.mean(accX),
            "mean_accY": np.mean(accY),
            "mean_accZ": np.mean(accZ),
            "mean_sound": np.mean(sound),
            "rms_accX": np.sqrt(np.mean(accX**2)),
            "rms_accY": np.sqrt(np.mean(accY**2)),
            "rms_accZ": np.sqrt(np.mean(accZ**2)),
            "rms_sound": np.sqrt(np.mean(sound**2)),
            "kurtosis_accX": stats.kurtosis(accX),
            "kurtosis_accY": stats.kurtosis(accY),
            "kurtosis_accZ": stats.kurtosis(accZ),
            "kurtosis_sound": stats.kurtosis(sound),
            "skewness_accX": stats.skew(accX),
            "skewness_accY": stats.skew(accY),
            "skewness_accZ": stats.skew(accZ),
            "skewness_sound": stats.skew(sound),
            "temp": row['temp'],
            "hum": row['hum'],
            "sound": row['sound'],
        }

        

        # Find max frequency
        sampling_rate = 1000  # Adjust this based on your data acquisition rate

        # Frequency-domain features using FFT (check that array is not empty)
        accX_fft = np.fft.fft(accX) 
        accY_fft = np.fft.fft(accY)
        accZ_fft = np.fft.fft(accZ) 
        sound_fft = np.fft.fft(sound) 

        magnitudeX = np.abs(accX_fft)
        magnitudeY = np.abs(accY_fft)
        magnitudeZ = np.abs(accZ_fft)
        magnitudeS = np.abs(sound_fft)

        max_indexX = np.argmax(magnitudeX)
        max_indexY = np.argmax(magnitudeY)
        max_indexZ = np.argmax(magnitudeZ)
        max_indexS = np.argmax(magnitudeS)

        normalized_magnitudeX = magnitudeX / np.sum(magnitudeX)
        normalized_magnitudeY = magnitudeY / np.sum(magnitudeY)
        normalized_magnitudeZ = magnitudeZ / np.sum(magnitudeZ)
        normalized_magnitudeS = magnitudeS / np.sum(magnitudeS)


        freq_features = {
            "max_freq_accX": max_indexX * sampling_rate / len(accX), 
            "max_freq_accY": max_indexY * sampling_rate / len(accY),
            "max_freq_accZ": max_indexZ * sampling_rate / len(accZ),
            "max_freq_sound": max_indexS * sampling_rate / len(sound),
            "spectral_entropy_accX": -np.sum(normalized_magnitudeX * np.log2(normalized_magnitudeX + 1e-10)),
            "spectral_entropy_accY": -np.sum(normalized_magnitudeY * np.log2(normalized_magnitudeY + 1e-10)),
            "spectral_entropy_accZ": -np.sum(normalized_magnitudeZ * np.log2(normalized_magnitudeZ + 1e-10)),
            "spectral_entropy_sound": -np.sum(normalized_magnitudeS * np.log2(normalized_magnitudeS + 1e-10)),
        }

        # Combine all features
        combined_features = {**time_features, **freq_features}
        features.append(combined_features)

        
    return pd.DataFrame(features)

from keras.models import load_model
import joblib

# Load scaler and model using joblib and Keras
scaler = joblib.load('new_vector2.pkl')
model = load_model('new_model2.h5')
global conditions
# Function to extract features for new data
def extract_and_predict(new_data):
    global conditions
    # Extract features from new data
    features_new = extract_features(new_data)
    features_new = features_new.fillna(0)
    
    # Standardize the new features
    features_new_scaled = scaler.transform(features_new)
    
    # If the model expects 3D input, reshape Nx
    if len(model.input_shape) == 3 and features_new_scaled.ndim == 2:
        features_new_scaled = features_new_scaled.reshape(features_new_scaled.shape[0], features_new_scaled.shape[1], 1)
        print("Shape of features_new_scaled after reshaping:", features_new_scaled.shape)
    
    # Reshape for LSTM input
    features_new_scaled = features_new_scaled.reshape(features_new_scaled.shape[0], features_new_scaled.shape[1], 1)
    
    # Predict the condition
    predictions = model.predict(features_new_scaled)
    predicted_classes = np.argmax(predictions, axis=1)
    

    # Condition labels
    conditions = ["Normal Operation", "Misalignment", "Bearing Fault", "Imbalance", 
                "Overheating", "Lubrication Failure", "Electrical Fault"]

    # Step 2: Map predicted class indices to actual condition labels
    predicted_conditions = [conditions[class_index] for class_index in predicted_classes]

    # Step 3: Print the predicted probabilities and conditions for each sample
    for i, (probs, condition) in enumerate(zip(predictions, predicted_conditions)):
        print(f"Sample {i+1}:"), '\n',
        print(f"Predicted probabilities: {probs}"), '\n',
        print(f"Predicted condition: {condition}\n")

    return predicted_conditions
    
new_data = pd.DataFrame({
    'accX': [-7.988939059, -0.034567],
    'accY': [-0.426416139, 0.023456],
    'accZ': [24.56, 0.012345],
    'temp': [35.00, 41.56789],
    'hum': [59.6, 52.34567],
    'sound': [49, 59.76543],
})

extract_and_predict(new_data)