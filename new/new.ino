#include <Wire.h>
#include <Adafruit_Sensor.h>
#include <Adafruit_ADXL345_U.h>
#include "DHT.h"
#include <LiquidCrystal.h>
#include <TimeLib.h>

// Pin definitions
#define DHT22_PIN 12
#define DHTTYPE DHT22

// Create objects
Adafruit_ADXL345_Unified accel = Adafruit_ADXL345_Unified(12345);
DHT dht(DHT22_PIN, DHTTYPE);
LiquidCrystal lcd(7, 6, 2, 3, 4, 5);

const int sampleWindow = 50;  // Sample window width in mS (50 mS = 20Hz)
unsigned int sample;

#define SENSOR_PIN A2

// Variables for DHT22
float humidity = 0.0;
float temperature = 0.0;

// Timing variables for non-blocking loop2
unsigned long previousMillisLCD = 0;
unsigned long lcdInterval = 2000;  // 2 seconds interval between LCD updates
int lcdState = 0;                  // To keep track of the current LCD display state

// Status variables
bool dhtStatus = false;
bool accelStatus = false;

void setup() {
  // Initialize Serial Monitor
  Serial.begin(9600);

  // Initialize LCD
  lcd.begin(16, 2);
  lcd.print("Initializing...");

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

  lcd.setCursor(0, 1);
  lcd.print("Ready");

  // Setting up sound sensor pin
  pinMode(SENSOR_PIN, INPUT);

  // Show project info on LCD briefly
  lcd.clear();
  lcd.setCursor(0, 0);
  lcd.print("Final Year Project");
  lcd.setCursor(0, 1);
  lcd.print("Jeremy & Barnabas");
  delay(2000);

  // Initialize time
  setTime(0, 0, 0, 0, 0, 2024);  // HH, MM, SS, Day, Month, Year
}

void loop1() {
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
  unsigned long startMillis = millis();
  float peakToPeak = 0;
  unsigned int signalMax = 0;
  unsigned int signalMin = 1024;

  while (millis() - startMillis < sampleWindow) {
    sample = analogRead(SENSOR_PIN);
    if (sample < 1024) {
      if (sample > signalMax) {
        signalMax = sample;
      } else if (sample < signalMin) {
        signalMin = sample;
      }
    }
  }

  peakToPeak = signalMax - signalMin;
  int db = map(peakToPeak, 20, 900, 49.5, 90);

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
  Serial.print(db);
  Serial.print(", ");
  Serial.print(hour());
  Serial.print(":");
  Serial.print(minute());
  Serial.print(":");
  Serial.print(second());
  Serial.println();
  delay(1000);
}

void loop2() {
  unsigned long currentMillis = millis();

  // Update LCD every `lcdInterval` milliseconds
  if (currentMillis - previousMillisLCD >= lcdInterval) {
    previousMillisLCD = currentMillis;

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
    unsigned long startMillis = millis();
    float peakToPeak = 0;
    unsigned int signalMax = 0;
    unsigned int signalMin = 1024;

    while (millis() - startMillis < sampleWindow) {
      sample = analogRead(SENSOR_PIN);
      if (sample < 1024) {
        if (sample > signalMax) {
          signalMax = sample;
        } else if (sample < signalMin) {
          signalMin = sample;
        }
      }
    }

    peakToPeak = signalMax - signalMin;
    int db = map(peakToPeak, 20, 900, 49.5, 90);

    // Cycle through different states of the LCD display
    switch (lcdState) {
      case 0:
        lcd.clear();
        lcd.setCursor(0, 0);
        lcd.print("SenStatus: ");
        lcd.print((dhtStatus && accelStatus) ? "OK" : "Error");
        lcdState = 1;
        break;

      case 1:
        lcd.clear();
        lcd.setCursor(0, 0);
        lcd.print("H:");
        lcd.print(humidity);
        lcd.print(" T:");
        lcd.print(temperature);
        lcd.setCursor(0, 1);
        lcd.print("Snd:");
        lcd.print(db);
        lcdState = 2;
        break;

      case 2:
        lcd.clear();
        lcd.setCursor(0, 0);
        lcd.print("AccX:");
        lcd.print(event.acceleration.x);
        lcd.setCursor(0, 1);
        lcd.print("AccY:");
        lcd.print(event.acceleration.y);
        lcd.print("AccZ:");
        lcd.print(event.acceleration.z);
        lcdState = 0;  // Reset the state to loop back
        break;
    }
  }
}

void loop() {
  loop1();  // Serial print loop
  loop2();  // LCD display loop with non-blocking delay
}
