#include <Wire.h>
#include <DHT.h>
#include <Adafruit_BMP280.h>

// Sensor Pins
#define DHTPIN 4
#define DHTTYPE DHT11
#define LIGHT_SENSOR_PIN 34
#define CURRENT_SENSOR_PIN 35
#define VOLTAGE_SENSOR_PIN 36

// Motor Driver Pins (BTS7960)
#define MOTOR_LEFT_PWM 18
#define MOTOR_LEFT_DIR 19
#define MOTOR_RIGHT_PWM 22
#define MOTOR_RIGHT_DIR 23

DHT dht(DHTPIN, DHTTYPE);
Adafruit_BMP280 bmp; // I2C interface (SDA/SCL)

void setup() {
  Serial.begin(115200);
  dht.begin();
  
  if (!bmp.begin(0x76)) {
    Serial.println("Warning: BMP280 sensor not detected!");
  }

  pinMode(MOTOR_LEFT_PWM, OUTPUT);
  pinMode(MOTOR_LEFT_DIR, OUTPUT);
  pinMode(MOTOR_RIGHT_PWM, OUTPUT);
  pinMode(MOTOR_RIGHT_DIR, OUTPUT);
}

void loop() {
  // Read Sensors
  float temp = dht.readTemperature();
  float humidity = dht.readHumidity();
  float pressure = bmp.readPressure() / 100.0F; // hPa
  int lightRaw = analogRead(LIGHT_SENSOR_PIN);
  
  // Electrical Telemetry
  float currentRaw = analogRead(CURRENT_SENSOR_PIN);
  float voltageRaw = analogRead(VOLTAGE_SENSOR_PIN);
  float current = (currentRaw / 4095.0) * 3.3 * 10.0;          // ACS712 scaling
  float voltage = (voltageRaw / 4095.0) * 3.3 * (25.0 / 3.3);   // DC0-25V divider formula

  // Send JSON over USB-Serial to Raspberry Pi
  Serial.printf("{\"temp\":%.2f,\"humidity\":%.2f,\"pressure\":%.2f,\"light\":%d,\"current\":%.2f,\"voltage\":%.2f}\n",
                temp, humidity, pressure, lightRaw, current, voltage);

  delay(200); // 5 Hz update rate
}