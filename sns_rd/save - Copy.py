import serial
import csv
import time
import keyboard

# Setup the serial connection (adjust the COM port and baud rate as needed)
arduino_port = 'COM4'  # Replace with your Arduino's port
baud_rate = 9600
ser = serial.Serial(arduino_port, baud_rate, timeout=1)

# Define the CSV file path
csv_file_path = 'sensor_data.csv'

# Open the CSV file for writing
with open(csv_file_path, mode='w', newline='') as file:
    writer = csv.writer(file)
    # Write the header row, including the new "fault_type" column
    writer.writerow(["accX", "accY", "accZ","temp", "hum", "sound", "Time", "Condition",])

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
                        sensor_data.append("normal")
                        # Write the sensor data with "fault_type" to the CSV file
                        writer.writerow(sensor_data)
                        print("Data written: ", sensor_data)

            # Wait for a second before reading again
            # time.sleep(1)q

    except KeyboardInterrupt:
        print("Program interrupted by user.")

    finally:
        # Close the serial connection
        ser.close()
