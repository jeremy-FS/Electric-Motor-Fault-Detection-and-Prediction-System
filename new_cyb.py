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
from collections import deque
import pandas as pd

# Simulated user database
user_database = {
    "jeremy": {
        "password": "jeremy1234",
        "image_path": "C:/Users/Jeremy S Obozuwa/Pictures/Camera Roll/WIN_20240921_12_07_33_Pro.jpg"
    },
    "barnabas": {
        "password": "barnabas5678",
        "image_path": "user2_image.jpg"
    }
}


# Authentication Functions
def authenticate_user(username, password):
    print(f"Attempting to authenticate with username: {username} and password: {password}")
    
    # # Print all stored users and passwords for debugging
    # print("Stored Users and Passwords:")
    for user, info in user_database.items():
        print(f"Username: {user}, Password: {info['password']}")

    if username in user_database and user_database[username]["password"] == password:
        print(
            f'Username {username} found...'
        )
        return True
    else:
        print('No such user {username} found..')
        return False


def verify_facial_recognition(stored_image_path):
    stored_image = cv2.imread(stored_image_path)
    if stored_image is None:
        print("Error: Stored image not found.")
        return False

    cap = cv2.VideoCapture(0)
    ret, snapshot = cap.read()
    cap.release()

    if not ret:
        print("Error: Failed to capture image from webcam.")
        return False

    
    stored_image_gray = cv2.cvtColor(stored_image, cv2.COLOR_BGR2GRAY)
    snapshot_gray = cv2.cvtColor(snapshot, cv2.COLOR_BGR2GRAY)

    result = cv2.matchTemplate(stored_image_gray, snapshot_gray, cv2.TM_CCOEFF_NORMED)
    match_value = np.max(result)
    # print(f"Template matching max result: {np.max(result)}")
    print(f"Template matching value: {match_value}")

    # height, width, _ = stored_image.shape  # Get dimensions of the stored image
    snapshot_resized = cv2.resize(snapshot, (350, 350))  # Resize snapshot to match stored image dimensions
    stored_image_resized = cv2.resize(stored_image, (350, 350))

    # Display both the stored image and the captured image side by side
    combined_image = np.hstack((stored_image_resized, snapshot_resized))  # Stack images horizontally
    cv2.imshow('Stored Image (Left) vs Captured Image (Right)', combined_image)

    cv2.waitKey(2000)
    cv2.destroyAllWindows()

    threshold = 0.3
    if match_value > threshold:
        print("Match successful: Images match.")
        return True
    else:
        print("Match failed: Images do not match.")
        return False


def login(username_entry, password_entry, root):

    username = username_entry.get()
    password = password_entry.get()

    print(f"Entered Username: {username}")
    print(f"Entered Password: {password}")

    if authenticate_user(username, password):
        stored_image_path = user_database[username]["image_path"]
        if verify_facial_recognition(stored_image_path):
            messagebox.showinfo("Success", "User verified successfully. Launching the sensor window...")
            root.destroy()  
            open_sensor_window()
        else:
            messagebox.showerror("Error", "Facial recognition failed.")
    else:
        messagebox.showerror("Error", "Authentication failed.")

def open_login_window():
    root = tk.Tk()
    root.title("Login")

    tk.Label(root, text="Username:", font=("Helvetica", 16)).grid(row=0, column=0)  
    username_entry = tk.Entry(root, font=("Helvetica", 16))  
    username_entry.grid(row=0, column=1)

    tk.Label(root, text="Password:", font=("Helvetica", 16)).grid(row=1, column=0)  
    password_entry = tk.Entry(root, show="*", font=("Helvetica", 16))  
    password_entry.grid(row=1, column=1)

    login_button = tk.Button(root, text="Login", font=("Helvetica", 16), command=lambda: login(username_entry, password_entry, root))
    login_button.grid(row=2, column=0, columnspan=2)

    root.mainloop()

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

        self.mean_label = tk.Label(self.root, text="Prediction: ", font=value_font)  
        self.mean_label.grid(row=0, column=2, columnspan=2)

        self.label_predicted_mean = tk.Label(self.root, text="RUL est: ", font=value_font)  
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
        self.continuous_learning_button = tk.Button(self.root, text="Continuous Improvement", command=self.open_continuous_learning_window, font=label_font, bg="brown", fg="white")
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
                # Keep reading serial data until valid (non-empty) data is received
                data = ""
                while not data:
                    data = self.serial_port.readline().decode('utf-8').strip()

                values = list(data.split(','))
                print(values)
                
                if len(values) == 6:
                    self.sensor_values = [float(value) for value in values]
                    # Update the displayed sensor values
                    for i, display_label in enumerate(self.display_labels):
                        display_label.config(text=f"{self.sensor_values[i]:.2f}")
                else:
                    values = values[:-1]
                    self.sensor_values = [float(value) for value in values]
                    # Update the displayed sensor values
                    for i, display_label in enumerate(self.display_labels):
                        display_label.config(text=f"{self.sensor_values[i]:.2f}")
                
                    # print(f"Error: Expected 6 sensor values, got {len(values)}")
            except Exception as e:
                print(f"Error reading serial data: {e}")
            self.root.after(100, self.update_display)
    
    global answer
    def update_prediction(self):
        global answer
        from inport import extract_and_predict
        if self.running:
            try:
                
                if hasattr(self, 'sensor_values') and len(self.sensor_values) == 6:
                    new_sensor_data = pd.DataFrame([self.sensor_values], columns=['accX', 'accY', 'accZ', 'temp', 'hum', 'sound'])
                    
                    print("DataFrame for prediction:", new_sensor_data)

                    # Prediction 
                    predictions = extract_and_predict(new_sensor_data)
                    answer = predictions[0]
                    self.mean_label.config(text=f"Prediction: {predictions[0]}")
                else:
                    print("Error: Sensor values are incomplete for prediction")

            except Exception as e:
                print(f"Error during prediction: {e}")

            self.root.after(4000, self.update_prediction)



    def update_RUL_est(self):
        if self.running:
            try:
                predicted_fault = answer  # This should return a string
                print(predicted_fault)
                RUL_mapping = {
                    "Normal Operation": (1000, 50),
                    "Misalignment": (500, 15),      
                    "Bearing Fault": (300, 15),     
                    "Imbalance": (200, 10),         
                    "Overheating": (100, 10),       
                    "Lubrication Failure": (50, 8), 
                    "Electrical Fault": (20, 5)     
                }

                if predicted_fault in RUL_mapping:
                    mean_rul, std_rul = RUL_mapping[predicted_fault]

                    # This function will update the RUL range every 0.5 seconds
                    def update_RUL_range():
                        if self.running:
                            # Generate a new RUL within the range using a normal distribution
                            RUL_range = np.random.normal(mean_rul, std_rul)
                            # Update the label with the new RUL range
                            self.label_predicted_mean.config(text=f"RUL est: {RUL_range:.2f} hours")
                            # Keep updating every 0.5 seconds
                            self.root.after(500, update_RUL_range)

                    # Finalize the RUL after 3 seconds
                    def finalize_RUL():
                        if self.running:
                            # Final RUL estimate based on the mean
                            final_rul = np.random.normal(mean_rul, std_rul)
                            # Update the label with the final RUL
                            self.label_predicted_mean.config(text=f"Final RUL est: {final_rul:.2f} hours")

                    # Start the RUL range updates every 0.5 seconds
                    update_RUL_range()
                    # After 3 seconds, show the final RUL estimate
                    self.root.after(3000, finalize_RUL)

                else:
                    print(f"Error: Predicted fault '{predicted_fault}' is not in RUL mapping.")

            except Exception as e:
                print(f"Error calculating RUL: {e}")

            # Schedule the next full update after 3 seconds
            self.root.after(3000, self.update_RUL_est)



    def display_graph(self):
        # Ensure the graph window is displayed and interactive
        selected_sensor = self.selected_label.get()  # Get the selected sensor

        if not plt.fignum_exists(self.fig.number):
            # Recreate figure if it was closed
            self.fig, self.ax = plt.subplots()
            self.ax.set_xlabel('Time')
            self.ax.set_ylabel('Sensor Reading')
            self.ax.set_title(f'{selected_sensor} Activity Monitoring')  # Set title based on selected sensor
            self.ax.grid(True)

            self.line, = self.ax.plot(self.x_data, self.y_data, color='blue')
            self.ani = FuncAnimation(self.fig, self.animate, interval=100)

        # Update the title dynamically based on selected sensor
        self.ax.set_title(f'{selected_sensor} Activity Monitoring')

        plt.draw()  # Refresh the plot window
        plt.pause(0.001)  # Small pause to allow the graph to update


    def animate(self, i):
        if not self.running:
            return self.line,

        try:
            sensor_values = [float(label.cget("text")) for label in self.display_labels if label.cget("text")]
            if sensor_values:
                selected_label_index = self.labels.index(self.selected_label.get())  # Dynamically get the sensor value
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
                self.ax.set_title(f'{self.selected_label.get()} Activity Monitoring')  # Update title in animation
                self.ax.grid(True)
        except ValueError:
            pass

        return self.line,

    def open_continuous_learning_window(self):
        # Create a new window for continuous learning
        new_window = tk.Toplevel(self.root)
        new_window.title("Continuous Improvement")

        # Display past 10 seconds of sensor data
        past_data_label = tk.Label(new_window, text="Past 10 seconds of data:", font=("Helvetica", 13))
        past_data_label.pack()

        # Display past 10 seconds' data in the window
        past_data = self.sensor_values
        data_label = tk.Label(new_window, text=str(past_data), font=("Helvetica", 12))
        data_label.pack()

        new_sensor_data = pd.DataFrame([past_data], columns=['accX', 'accY', 'accZ', 'temp', 'hum', 'sound'])
                    

        # Input box to query the new desired label
        label_input = tk.Label(new_window, text="Enter new condtion:", font=("Helvetica", 12))
        label_input.pack()
        label_entry = tk.Entry(new_window, font=("Helvetica", 12))
        label_entry.pack()

        # Start button to trigger continuous learning
        start_button = tk.Button(new_window, text="Re-trian", font=("Helvetica", 14), command=lambda: self.continuous_learning(new_sensor_data, label_entry.get()), bg='blue')
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


def open_sensor_window():
    root = tk.Tk()
    app = SensorDataDisplay(root)
    root.mainloop()

if __name__ == "__main__":
    open_login_window()
