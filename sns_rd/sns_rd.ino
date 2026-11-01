#include <Wire.h>
#include <Adafruit_Sensor.h>
#include <Adafruit_ADXL345_U.h>
#include "DHT.h"
#include <TimeLib.h>

// Pin definitions
#define DHT22_PIN 12
#define DHTTYPE DHT22

// Create objects
Adafruit_ADXL345_Unified accel = Adafruit_ADXL345_Unified(12345);
DHT dht(DHT22_PIN, DHTTYPE);

// Variables for DHT22
float humidity = 0.0;
float temperature = 0.0;

// Status variables
bool dhtStatus = false;
bool accelStatus = false;

// Initial time (set to 0:0:0)
unsigned long previousMillis = 0;
const long interval = 1000; // 1 second interval

void setup() {
  // Initialize Serial Monitor
  Serial.begin(9600);

  // Initialize ADXL345
  if (accel.begin()) {
    accel.setRange(ADXL345_RANGE_16_G);
    accelStatus = true;
  } else {
    Serial.println("Failed to find ADXL345 chip");
    accelStatus = false;
  }

  // Initialize DHT22
  dht.begin();

  // Initialize time to 00:00:00
  setTime(0, 0, 0, 1, 1, 2024); // HH, MM, SS, Day, Month, Year
  Serial.println("humidity,temperature,sound,accX,accY,accZ,Time");
}

void loop() {
  unsigned long currentMillis = millis();

  // Read ADXL345 data
  sensors_event_t event;
  if (accelStatus) {
    accel.getEvent(&event);
  } else {
    event.acceleration.x = event.acceleration.y = event.acceleration.z = 0;
  }

  // Read DHT22 data
  humidity = dht.readHumidity();
  temperature = dht.readTemperature();

  if (isnan(humidity) || isnan(temperature)) {
    dhtStatus = false;
    humidity = 0;
    temperature = 0;
  } else {
    dhtStatus = true;
  }

  // Read sound sensor data
  int soundValue = analogRead(A2);

  // Update time every second
  if (currentMillis - previousMillis >= interval) {
    previousMillis = currentMillis;
    // Display data on Serial Monitor
    Serial.print(event.acceleration.x);
    Serial.print(", ");
    Serial.print(event.acceleration.y);
    Serial.print(", ");
    Serial.print(event.acceleration.z);
    Serial.print(", ");
    Serial.print(temperature);
    Serial.print(", ");
    Serial.print(humidity);
    Serial.print(", ");
    Serial.print(soundValue);
    Serial.print(", ");
    Serial.print(hour());
    Serial.print(":");
    Serial.print(minute());
    Serial.print(":");
    Serial.print(second());
    Serial.println();

    // Increment time by 1 second
    setTime(hour(), minute(), second() + 1, day(), month(), year());
  }
}
