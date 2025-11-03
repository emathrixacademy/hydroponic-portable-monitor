/*
 * ========================================
 * ESP32 MAIN CONTROLLER - HYDROPONIC MONITORING SYSTEM
 * ========================================
 *
 * Purpose: Read sensors, control pumps, send data to Firebase
 * Board: ESP32 DevKit v1
 *
 * Sensors:
 * - pH Sensor (Analog) - GPIO 34
 * - EC/TDS Sensor (Analog) - GPIO 35
 * - DS18B20 (Water Temperature) - GPIO 4
 * - DHT22 (Air Temp & Humidity) - GPIO 15
 * - HC-SR04 (Ultrasonic) - Trigger: GPIO 5, Echo: GPIO 18
 *
 * Actuators (via 4-Channel Relay Module):
 * - Relay 1 (GPIO 25) - pH-UP Pump
 * - Relay 2 (GPIO 26) - pH-DOWN Pump
 * - Relay 3 (GPIO 27) - Nutrient Pump
 * - Relay 4 (GPIO 14) - Circulation Pump (reserved)
 *
 * ========================================
 */

#include <WiFi.h>
#include <Firebase_ESP_Client.h>
#include <addons/TokenHelper.h>
#include <addons/RTDBHelper.h>
#include <OneWire.h>
#include <DallasTemperature.h>
#include <DHT.h>
#include <ArduinoJson.h>
#include "time.h"

// ========================================
// CONFIGURATION - UPDATE THESE!
// ========================================
#define WIFI_SSID "YOUR_WIFI_SSID"
#define WIFI_PASSWORD "YOUR_WIFI_PASSWORD"

// Firebase Configuration
#define FIREBASE_PROJECT_ID "your-project-id"
#define FIREBASE_API_KEY "YOUR_FIREBASE_API_KEY"
#define FIREBASE_USER_EMAIL "your-email@example.com"
#define FIREBASE_USER_PASSWORD "your-password"

// ========================================
// PIN DEFINITIONS
// ========================================
// Analog Sensors
#define PH_SENSOR_PIN 34
#define EC_SENSOR_PIN 35

// Digital Sensors
#define DS18B20_PIN 4
#define DHT_PIN 15
#define ULTRASONIC_TRIG_PIN 5
#define ULTRASONIC_ECHO_PIN 18

// Relay Pins (Active LOW)
#define RELAY_PH_UP 25
#define RELAY_PH_DOWN 26
#define RELAY_NUTRIENT 27
#define RELAY_CIRCULATION 14

// ========================================
// SENSOR OBJECTS
// ========================================
#define DHT_TYPE DHT22
DHT dht(DHT_PIN, DHT_TYPE);

OneWire oneWire(DS18B20_PIN);
DallasTemperature ds18b20(&oneWire);

// ========================================
// FIREBASE OBJECTS
// ========================================
FirebaseData fbdo;
FirebaseAuth auth;
FirebaseConfig config;

// ========================================
// GLOBAL VARIABLES
// ========================================
unsigned long lastSensorRead = 0;
unsigned long lastFirebaseUpdate = 0;
const unsigned long SENSOR_INTERVAL = 5000;  // 5 seconds
const unsigned long FIREBASE_INTERVAL = 5000; // 5 seconds

// Target setpoints
const float TARGET_PH = 5.8;
const float PH_TOLERANCE = 0.15;
const float TARGET_EC = 1.2; // mS/cm
const float EC_TOLERANCE = 0.08;
const float TARGET_WATER_TEMP_MIN = 18.0;
const float TARGET_WATER_TEMP_MAX = 22.0;

// Calibration constants (UPDATE AFTER CALIBRATION!)
float phCalibration_neutral = 7.0;
float phCalibration_voltage = 1.65; // Voltage at pH 7
float phCalibration_slope = 3.5;    // Slope (mV per pH unit)

float ecCalibration_factor = 1.0;   // EC calibration multiplier

// Sensor data structure
struct SensorData {
  float pH;
  float ec;           // mS/cm
  float tds;          // ppm
  float waterTemp;    // Celsius
  float airTemp;      // Celsius
  float humidity;     // %
  float waterLevel;   // cm
  unsigned long timestamp;
} currentData;

// Control flags
bool autoControlEnabled = true;
unsigned long lastPumpAction = 0;
const unsigned long PUMP_COOLDOWN = 300000; // 5 minutes between pump actions

// ========================================
// NTP TIME SERVER
// ========================================
const char* ntpServer = "pool.ntp.org";
const long gmtOffset_sec = 28800;  // GMT+8 (Philippines)
const int daylightOffset_sec = 0;

// ========================================
// SETUP
// ========================================
void setup() {
  Serial.begin(115200);
  Serial.println("\n========================================");
  Serial.println("ESP32 Hydroponic Monitor - Starting...");
  Serial.println("========================================");

  // Initialize relay pins (Active LOW - set HIGH to turn OFF)
  pinMode(RELAY_PH_UP, OUTPUT);
  pinMode(RELAY_PH_DOWN, OUTPUT);
  pinMode(RELAY_NUTRIENT, OUTPUT);
  pinMode(RELAY_CIRCULATION, OUTPUT);

  digitalWrite(RELAY_PH_UP, HIGH);
  digitalWrite(RELAY_PH_DOWN, HIGH);
  digitalWrite(RELAY_NUTRIENT, HIGH);
  digitalWrite(RELAY_CIRCULATION, HIGH);

  Serial.println("✓ Relays initialized (all OFF)");

  // Initialize ultrasonic sensor
  pinMode(ULTRASONIC_TRIG_PIN, OUTPUT);
  pinMode(ULTRASONIC_ECHO_PIN, INPUT);
  Serial.println("✓ Ultrasonic sensor initialized");

  // Initialize DHT22
  dht.begin();
  Serial.println("✓ DHT22 initialized");

  // Initialize DS18B20
  ds18b20.begin();
  Serial.println("✓ DS18B20 initialized");

  // Connect to WiFi
  connectWiFi();

  // Initialize time
  configTime(gmtOffset_sec, daylightOffset_sec, ntpServer);
  Serial.println("✓ NTP time synchronized");

  // Initialize Firebase
  initFirebase();

  Serial.println("========================================");
  Serial.println("System ready! Starting monitoring...");
  Serial.println("========================================\n");
}

// ========================================
// MAIN LOOP
// ========================================
void loop() {
  unsigned long currentMillis = millis();

  // Read sensors periodically
  if (currentMillis - lastSensorRead >= SENSOR_INTERVAL) {
    lastSensorRead = currentMillis;
    readAllSensors();
    printSensorData();

    // Execute automatic control
    if (autoControlEnabled) {
      executeAutoControl();
    }
  }

  // Update Firebase periodically
  if (currentMillis - lastFirebaseUpdate >= FIREBASE_INTERVAL) {
    lastFirebaseUpdate = currentMillis;
    updateFirebase();
  }

  // Small delay to prevent watchdog issues
  delay(10);
}

// ========================================
// WIFI CONNECTION
// ========================================
void connectWiFi() {
  Serial.print("Connecting to WiFi: ");
  Serial.println(WIFI_SSID);

  WiFi.begin(WIFI_SSID, WIFI_PASSWORD);

  int attempts = 0;
  while (WiFi.status() != WL_CONNECTED && attempts < 30) {
    delay(500);
    Serial.print(".");
    attempts++;
  }

  if (WiFi.status() == WL_CONNECTED) {
    Serial.println("\n✓ WiFi connected!");
    Serial.print("IP Address: ");
    Serial.println(WiFi.localIP());
  } else {
    Serial.println("\n✗ WiFi connection failed!");
  }
}

// ========================================
// FIREBASE INITIALIZATION
// ========================================
void initFirebase() {
  Serial.println("Initializing Firebase...");

  config.api_key = FIREBASE_API_KEY;
  auth.user.email = FIREBASE_USER_EMAIL;
  auth.user.password = FIREBASE_USER_PASSWORD;

  config.token_status_callback = tokenStatusCallback;

  Firebase.begin(&config, &auth);
  Firebase.reconnectWiFi(true);

  Serial.println("✓ Firebase initialized");
}

// ========================================
// READ ALL SENSORS
// ========================================
void readAllSensors() {
  // Read pH sensor
  currentData.pH = readPH();

  // Read water temperature (needed for EC compensation)
  currentData.waterTemp = readWaterTemperature();

  // Read EC/TDS sensor (with temperature compensation)
  currentData.ec = readEC(currentData.waterTemp);
  currentData.tds = currentData.ec * 700; // Approximate conversion (EC * 700 = TDS ppm)

  // Read air temperature and humidity
  currentData.airTemp = dht.readTemperature();
  currentData.humidity = dht.readHumidity();

  // Read water level
  currentData.waterLevel = readWaterLevel();

  // Get timestamp
  currentData.timestamp = getTimestamp();
}

// ========================================
// READ pH SENSOR
// ========================================
float readPH() {
  // Take multiple readings and average
  int samples = 10;
  float sum = 0;

  for (int i = 0; i < samples; i++) {
    int rawValue = analogRead(PH_SENSOR_PIN);
    float voltage = rawValue * (3.3 / 4095.0);
    sum += voltage;
    delay(10);
  }

  float avgVoltage = sum / samples;

  // Convert voltage to pH using calibration
  // pH = neutral_pH - ((voltage - neutral_voltage) / slope)
  float pH = phCalibration_neutral - ((avgVoltage - phCalibration_voltage) / (phCalibration_slope / 1000.0));

  // Bounds checking
  if (pH < 0) pH = 0;
  if (pH > 14) pH = 14;

  return pH;
}

// ========================================
// READ EC SENSOR (with temperature compensation)
// ========================================
float readEC(float temperature) {
  // Take multiple readings and average
  int samples = 10;
  float sum = 0;

  for (int i = 0; i < samples; i++) {
    int rawValue = analogRead(EC_SENSOR_PIN);
    float voltage = rawValue * (3.3 / 4095.0);
    sum += voltage;
    delay(10);
  }

  float avgVoltage = sum / samples;

  // Convert voltage to EC (simplified linear conversion)
  // This needs calibration with known EC solution
  float ec_raw = avgVoltage * ecCalibration_factor;

  // Temperature compensation (standard factor: 2% per degree C)
  float ec_compensated = ec_raw / (1.0 + 0.02 * (temperature - 25.0));

  return ec_compensated;
}

// ========================================
// READ WATER TEMPERATURE (DS18B20)
// ========================================
float readWaterTemperature() {
  ds18b20.requestTemperatures();
  float temp = ds18b20.getTempCByIndex(0);

  // Error checking
  if (temp == DEVICE_DISCONNECTED_C || temp < -50 || temp > 100) {
    return 20.0; // Default fallback
  }

  return temp;
}

// ========================================
// READ WATER LEVEL (HC-SR04)
// ========================================
float readWaterLevel() {
  // Send ultrasonic pulse
  digitalWrite(ULTRASONIC_TRIG_PIN, LOW);
  delayMicroseconds(2);
  digitalWrite(ULTRASONIC_TRIG_PIN, HIGH);
  delayMicroseconds(10);
  digitalWrite(ULTRASONIC_TRIG_PIN, LOW);

  // Read echo duration
  long duration = pulseIn(ULTRASONIC_ECHO_PIN, HIGH, 30000); // 30ms timeout

  // Calculate distance (cm)
  // Speed of sound = 343 m/s = 0.0343 cm/µs
  // Distance = (duration / 2) * 0.0343
  float distance = (duration / 2.0) * 0.0343;

  // Convert to water level (assuming sensor is mounted at fixed height)
  // Tank height = 30cm, sensor mounted at top
  float tankHeight = 30.0;
  float waterLevel = tankHeight - distance;

  if (waterLevel < 0) waterLevel = 0;
  if (waterLevel > tankHeight) waterLevel = tankHeight;

  return waterLevel;
}

// ========================================
// GET UNIX TIMESTAMP
// ========================================
unsigned long getTimestamp() {
  time_t now;
  time(&now);
  return (unsigned long)now;
}

// ========================================
// PRINT SENSOR DATA TO SERIAL
// ========================================
void printSensorData() {
  Serial.println("\n--- SENSOR READINGS ---");
  Serial.printf("pH: %.2f (Target: %.2f ± %.2f)\n", currentData.pH, TARGET_PH, PH_TOLERANCE);
  Serial.printf("EC: %.2f mS/cm (Target: %.2f ± %.2f)\n", currentData.ec, TARGET_EC, EC_TOLERANCE);
  Serial.printf("TDS: %.0f ppm\n", currentData.tds);
  Serial.printf("Water Temp: %.1f°C (Target: %.0f-%.0f°C)\n", currentData.waterTemp, TARGET_WATER_TEMP_MIN, TARGET_WATER_TEMP_MAX);
  Serial.printf("Air Temp: %.1f°C\n", currentData.airTemp);
  Serial.printf("Humidity: %.1f%%\n", currentData.humidity);
  Serial.printf("Water Level: %.1f cm\n", currentData.waterLevel);
  Serial.printf("Timestamp: %lu\n", currentData.timestamp);
  Serial.println("----------------------");
}

// ========================================
// AUTOMATIC CONTROL LOGIC
// ========================================
void executeAutoControl() {
  unsigned long currentMillis = millis();

  // Enforce cooldown period between pump actions
  if (currentMillis - lastPumpAction < PUMP_COOLDOWN) {
    return;
  }

  // pH Control
  if (currentData.pH < TARGET_PH - PH_TOLERANCE) {
    // pH too low - add pH-UP
    Serial.println(">>> AUTO-CONTROL: pH too low, activating pH-UP pump");
    activatePump(RELAY_PH_UP, 1000); // 1 second dose
    lastPumpAction = currentMillis;
  }
  else if (currentData.pH > TARGET_PH + PH_TOLERANCE) {
    // pH too high - add pH-DOWN
    Serial.println(">>> AUTO-CONTROL: pH too high, activating pH-DOWN pump");
    activatePump(RELAY_PH_DOWN, 1000); // 1 second dose
    lastPumpAction = currentMillis;
  }

  // EC Control
  if (currentData.ec < TARGET_EC - EC_TOLERANCE) {
    // EC too low - add nutrients
    Serial.println(">>> AUTO-CONTROL: EC too low, activating nutrient pump");
    activatePump(RELAY_NUTRIENT, 2000); // 2 second dose
    lastPumpAction = currentMillis;
  }

  // Note: No auto-dosing for EC too high (requires water addition)
}

// ========================================
// ACTIVATE PUMP
// ========================================
void activatePump(int relayPin, unsigned long duration) {
  digitalWrite(relayPin, LOW);  // Activate relay (Active LOW)
  delay(duration);
  digitalWrite(relayPin, HIGH); // Deactivate relay
  Serial.printf("Pump on pin %d activated for %lu ms\n", relayPin, duration);
}

// ========================================
// UPDATE FIREBASE
// ========================================
void updateFirebase() {
  if (WiFi.status() != WL_CONNECTED) {
    Serial.println("✗ WiFi not connected, skipping Firebase update");
    return;
  }

  if (!Firebase.ready()) {
    Serial.println("✗ Firebase not ready");
    return;
  }

  // Create JSON document
  FirebaseJson json;
  json.set("pH", currentData.pH);
  json.set("ec", currentData.ec);
  json.set("tds", currentData.tds);
  json.set("waterTemp", currentData.waterTemp);
  json.set("airTemp", currentData.airTemp);
  json.set("humidity", currentData.humidity);
  json.set("waterLevel", currentData.waterLevel);
  json.set("timestamp", currentData.timestamp);

  // Update Firestore document: sensors/current
  String documentPath = "sensors/current";

  if (Firebase.Firestore.patchDocument(&fbdo, FIREBASE_PROJECT_ID, "", documentPath.c_str(), json.raw(), "")) {
    Serial.println("✓ Firebase updated successfully");
  } else {
    Serial.println("✗ Firebase update failed: " + fbdo.errorReason());
  }

  // Optional: Also add to history collection (for time-series data)
  String historyPath = "sensors/history/" + String(currentData.timestamp);
  Firebase.Firestore.createDocument(&fbdo, FIREBASE_PROJECT_ID, "", historyPath.c_str(), json.raw());
}
