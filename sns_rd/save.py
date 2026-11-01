import serial
import csv
import time
import keyboard
import logging
import os

# Setup logging
log_file_path = 'sensor_data.log'
logging.basicConfig(filename=log_file_path, level=logging.INFO, format='%(asctime)s %(message)s')

# Setup the serial connection (adjust the COM port and baud rate as needed)
arduino_port = 'COM4'  # Replace with your Arduino's port
baud_rate = 9600
ser = serial.Serial(arduino_port, baud_rate, timeout=1)

# Define the CSV file path
csv_file_path = 'DC_series_motor.csv'

# Get the absolute path of the CSV file
abs_csv_file_path = os.path.abspath(csv_file_path)

# Open the CSV file for writing
with open(csv_file_path, mode='w', newline='') as file:
    writer = csv.writer(file)
    # Write the header row, including the new "fault_type" column
    writer.writerow(["accX", "accY", "accZ", "temp", "hum", "sound", "Time", "Condition"])
    
    print(f"CSV file created at: {abs_csv_file_path}")
    logging.info(f"CSV file created at: {abs_csv_file_path}")
    
    try:
        while True:
            if keyboard.is_pressed('Q'):
                print("Exiting program...")
                break
            
            # Read data from Arduino
            if ser.in_waiting > 0:
                data_line = ser.readline().decode('utf-8').strip()
                if data_line:
                    # Split the data line into individual sensor values
                    sensor_data = data_line.split(',')
                    if len(sensor_data) == 7:
                        # Add the "fault_type" as "normal" to the sensor data
                        sensor_data.append("Normal Operation")
                        # Write the sensor data with "fault_type" to the CSV file
                        writer.writerow(sensor_data)
                        logging.info(f"Data written: {sensor_data}")
                        print(f"Data written: {sensor_data}")
            
            # Wait for a second before reading again
            time.sleep(1)
    
    except Exception as e:
        logging.error(f"An error occurred: {str(e)}")
    
    finally:
        # Close the serial connection
        ser.close()

print(f"Log file created at: {os.path.abspath(log_file_path)}")