import cv2
import numpy as np
import os
import tkinter as tk
from tkinter import messagebox
import serial
from datetime import datetime
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
from collections import deque


# Sensor Window
class SensorDataDisplay:
    def __init__(self, root):
        self.root = root
        self.root.title("ELECTRIC MOTOR FAULT PREDICTOR")

        self.model = LinearRegression()
        
        # Serial connection (adjust the port and baudrate as needed)
        self.serial_port = serial.Serial('COM4', 9600, timeout=1)

        
        title_font = ("Helvetica", 18, "bold")
        label_font = ("Helvetica", 14)
        value_font = ("Helvetica", 14, "bold")

        self.mean_label = tk.Label(self.root, text="Prediction: ", font=value_font)  # Increased font size
        self.mean_label.grid(row=0, column=2, columnspan=2)

        self.label_predicted_mean = tk.Label(self.root, text="RUL est: ", font=value_font)  # Increased font size
        self.label_predicted_mean.grid(row=1, column=2, columnspan=2, pady=10)

        self.labels = ["AccX", "AccY", "AccZ", "Temperature", "Humidity", "Sound"]
        self.display_labels = []
        
        for i, label_text in enumerate(self.labels):
            label = tk.Label(self.root, text=f"{label_text}: ", font=label_font)
            label.grid(row=i+1, column=0, padx=10, pady=5, sticky='w')
            self.display_labels.append(tk.Label(self.root, text="", font=value_font))
            self.display_labels[-1].grid(row=i+1, column=1, padx=10, pady=5, sticky='w')


        self.selected_label = tk.StringVar()
        self.label_dropdown = tk.OptionMenu(self.root, self.selected_label, *self.labels)
        self.label_dropdown.config(font=label_font)
        self.label_dropdown.grid(row=6, column=2, columnspan=8, pady=10)

        self.start_button = tk.Button(self.root, text="Start", command=self.start, font=label_font, bg="green", fg="white")
        self.start_button.grid(row=7, column=0, columnspan=2, pady=10)

        self.stop_button = tk.Button(self.root, text="Stop", command=self.stop, state=tk.DISABLED, font=label_font, bg="red", fg="white")
        self.stop_button.grid(row=7, column=2, columnspan=6, pady=10)

        self.graph_button = tk.Button(self.root, text="Display Graph", command=self.display_graph, font=label_font, bg="blue", fg="white")
        self.graph_button.grid(row=8, column=0, columnspan=4, pady=10)

        # Add the new "Continuous Learning" button
        self.continuous_learning_button = tk.Button(self.root, text="Continuous Learning", command=self.open_continuous_learning_window, font=label_font, bg="brown", fg="white")
        self.continuous_learning_button.grid(row=9, column=0, columnspan=4)


        self.fig, self.ax = plt.subplots()
        self.ax.set_xlabel('Time')
        self.ax.set_ylabel('Sensor Reading')
        self.ax.set_title('Sensor Activity Monitoring')
        self.ax.grid(True)

        self.x_data = deque(maxlen=100)
        self.y_data = deque(maxlen=100)
        self.line, = self.ax.plot(self.x_data, self.y_data, color='blue')

        self.timestamps = deque(maxlen=100)

        self.ani = FuncAnimation(self.fig, self.animate, interval=100)


    def start(self):
        self.running = True
        self.start_button.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.NORMAL)
        self.update_display()
        self.update_prediction()
        self.update_RUL_est()

    def stop(self):
        self.running = False
        self.stop_button.config(state=tk.DISABLED)
        self.start_button.config(state=tk.NORMAL)

    def update_display(self):
        if self.running:
            try:
                data = self.serial_port.readline().decode('utf-8').strip()
                values = list(data.split(','))
                # values = values[:-1]
                values = [float(value) for value in values]
                # print(values)
                
                self.sensor_values = values
                for i, display_label in enumerate(self.display_labels):
                    display_label.config(text=f"{self.sensor_values[i]:.2f}")
            except Exception as e:
                print(f"Error reading serial data: {e}")
            self.root.after(100, self.update_display)

    def update_prediction(self):
        import pandas as pd
        from inport import extract_and_predict
        if self.running:
            try:
                # Simulating sensor data stream (Replace this with actual sensor data in real-time)
                data = self.serial_port.readline().decode('utf-8').strip()
                new_sensor_data = list(data.split(','))
                
                # new_sensor_data = new_sensor_data[:-1]
                # print(new_sensor_data)

                # Ensure the data is converted to float and check for correct length
                if len(new_sensor_data) == 6:
                    new_sensor_data = [float(value) for value in new_sensor_data]  # Convert all values to floats

                    # Convert list to DataFrame with correct column names
                    new_sensor_data = pd.DataFrame([new_sensor_data], columns=['accX', 'accY', 'accZ', 'temp', 'hum', 'sound'])
                    
                    print("data frame", new_sensor_data)

                    # Perform prediction using the extracted features from the sensor data
                    predictions = extract_and_predict(new_sensor_data)

                    # Update the GUI with the latest prediction
                    self.mean_label.config(text=f"Prediction: {predictions[0]}")
                else:
                    print(f"Error: Expected 6 sensor values, got {len(new_sensor_data)}")

            except Exception as e:
                print(f"Error during prediction: {e}")

            self.root.after(4000, self.update_prediction)


    def update_RUL_est(self):
        if self.running:
            # Retrieve the latest prediction and map it to RUL estimation
            try:
                predicted_fault = 0  # This should be the latest prediction (e.g., from `extract_and_predict`)
                RUL_mapping = {
                    0: 1000,  # Normal operation
                    1: 500,   # Misalignment
                    2: 300,   # Bearing fault
                    3: 200,   # Imbalance
                    4: 100,   # Overheating
                    5: 50,    # Lubrication failure
                    6: 20     # Electrical fault
                }
                # Estimate RUL in hours
                RUL_hours = RUL_mapping.get(predicted_fault, 1000)
                self.label_predicted_mean.config(text=f"RUL est: {RUL_hours} hours")
            except Exception as e:
                print(f"Error calculating RUL: {e}")

            self.root.after(3000, self.update_RUL_est)

    def display_graph(self):
        # Ensure the graph window is displayed and interactive
        if not plt.fignum_exists(self.fig.number):
            # Recreate figure if it was closed
            self.fig, self.ax = plt.subplots()
            self.ax.set_xlabel('Time')
            self.ax.set_ylabel('Sensor Reading')
            self.ax.set_title('Sensor Activity Monitoring')
            self.ax.grid(True)

            self.line, = self.ax.plot(self.x_data, self.y_data, color='blue')
            self.ani = FuncAnimation(self.fig, self.animate, interval=100)

        plt.draw()  # Refresh the plot window
        plt.pause(0.001)  # Small pause to allow the graph to update

    def animate(self, i):
        if not self.running:
            return self.line,

        try:
            sensor_values = [float(label.cget("text")) for label in self.display_labels if label.cget("text")]
            if sensor_values:
                selected_label_index = self.labels.index(self.selected_label.get())
                value = sensor_values[selected_label_index]

                new_timestamp = datetime.now().strftime("%M:%S.%f")[:7]
                self.timestamps.append(new_timestamp)
                self.x_data.append(new_timestamp)
                self.y_data.append(value)

                if len(self.timestamps) > 100:
                    self.timestamps.pop(0)
                    self.x_data.pop(0)
                    self.y_data.pop(0)

                self.ax.clear()
                self.ax.plot(self.x_data, self.y_data, color='blue')
                self.ax.set_xlabel('Time')
                self.ax.set_ylabel('Sensor Readings')
                self.ax.set_title('Sensor Activity Monitoring')
                self.ax.grid(True)
        except ValueError:
            pass

        return self.line,

    def open_continuous_learning_window(self):
        # Create a new window for continuous learning
        new_window = tk.Toplevel(self.root)
        new_window.title("Continuous Learning")

        # Display past 10 seconds of sensor data
        past_data_label = tk.Label(new_window, text="Past 10 seconds of data:", font=("Helvetica", 12))
        past_data_label.pack()

        # Display past 10 seconds' data in the window
        past_data = self.random_numbers
        data_label = tk.Label(new_window, text=str(past_data), font=("Helvetica", 12))
        data_label.pack()

        # Input box to query the new desired label
        label_input = tk.Label(new_window, text="Enter new label:", font=("Helvetica", 12))
        label_input.pack()
        label_entry = tk.Entry(new_window, font=("Helvetica", 12))
        label_entry.pack()

        # Start button to trigger continuous learning
        start_button = tk.Button(new_window, text="Start", font=("Helvetica", 12), command=lambda: self.continuous_learning(past_data, label_entry.get()))
        start_button.pack()

    def continuous_learning(self, new_data, new_label):
        from inport import scaler, model, conditions
        # Reshape and scale the new data
        new_data = np.array(new_data).reshape(-1, 1)
        new_data = scaler.transform(new_data)

        # Convert label to categorical
        new_labels = [conditions.index(new_label)]  # Map label to index
        # new_labels = to_categorical(new_labels, num_classes=len(conditions))

        # Further train the model with new data
        model.fit(new_data, new_labels, epochs=5, batch_size=32)

root = tk.Tk()
app = SensorDataDisplay(root)
root.mainloop()

