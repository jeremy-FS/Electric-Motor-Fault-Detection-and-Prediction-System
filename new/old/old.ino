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

const int sampleWindow = 50;                              // Sample window width in mS (50 mS = 20Hz)
unsigned int sample;
 
#define SENSOR_PIN A2

// Variables for DHT22
float humidity = 0.0;
float temperature = 0.0;

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

  // setting up new sound
  pinMode (SENSOR_PIN, INPUT); // Set the signal pin as input  
  

  // Show initial status on LCD
  delay(2000);
  lcd.clear();
  lcd.setCursor(0, 0);
  lcd.print("final year project");
  lcd.setCursor(0, 1);
  lcd.print("Jeremy & Barnabas");
  delay(3000);

  // Initialize time (Assume this sets the correct time for now)
  setTime(0, 0, 0, 0, 0, 2024);  // HH, MM, SS, Day, Month, Year
  Serial.println("accX(m/s),accY(m/s),accZ(m/s),temperature(C),humidity(H),sound(db),Time(s)");
}

void loop() {
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
  //  int soundValue = analogRead(A2);
   unsigned long startMillis= millis();                   // Start of sample window
   float peakToPeak = 0;                                  // peak-to-peak level
  
   unsigned int signalMax = 0;                            //minimum value
   unsigned int signalMin = 1024;                         //maximum value
  
                                                          // collect data for 50 mS
   while (millis() - startMillis < sampleWindow)
   {
      sample = analogRead(SENSOR_PIN);                    //get reading from microphone
      if (sample < 1024)                                  // toss out spurious readings
      {
         if (sample > signalMax)
         {
            signalMax = sample;                           // save just the max levels
         }
         else if (sample < signalMin)
         {
            signalMin = sample;                           // save just the min levels
         }
      }
   }
  
   peakToPeak = signalMax - signalMin;                    // max - min = peak-peak amplitude
   int db = map(peakToPeak,20,900,49.5,90);             //calibrate for deciBels
  // Display data on Serial Monitor
  String status = (dhtStatus && accelStatus) ? "OK" : "Error";


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

  // Display data on LCD
  lcd.clear();
  lcd.setCursor(0, 0);
  lcd.print("SenStatus: ");
  lcd.print(status);
  
  delay(2000);

  lcd.clear();
  lcd.setCursor(0, 0);
  lcd.print("H:");
  lcd.print(humidity);
  lcd.print(" T:");
  lcd.print(temperature);

  delay(2000);

  lcd.clear();
  lcd.setCursor(0, 0);
  lcd.print("Snd:");
  lcd.print(db);
  lcd.setCursor(0, 1);
  lcd.print("AccX:");
  lcd.print(event.acceleration.x);
  lcd.print("AccY:");
  lcd.print(event.acceleration.y);
  lcd.print("AccZ:");
  lcd.print(event.acceleration.z);

  delay(2000);
}
