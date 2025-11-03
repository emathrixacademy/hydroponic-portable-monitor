/*
 * ========================================
 * ESP32-CAM - PLANT HEALTH AI MONITORING
 * ========================================
 *
 * Purpose: Capture plant images, upload to cloud, AI classification
 * Board: ESP32-CAM (AI-Thinker)
 *
 * Features:
 * - Capture high-quality images (UXGA 1600x1200)
 * - Upload to ImgBB API (free image hosting)
 * - Send to Google Teachable Machine for AI classification
 * - Store results in Firebase Firestore
 * - Hourly automatic capture schedule
 *
 * ========================================
 */

#include <WiFi.h>
#include <HTTPClient.h>
#include <Firebase_ESP_Client.h>
#include <addons/TokenHelper.h>
#include "esp_camera.h"
#include "soc/soc.h"
#include "soc/rtc_cntl_reg.h"
#include <ArduinoJson.h>
#include <base64.h>
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

// ImgBB API Configuration
#define IMGBB_API_KEY "YOUR_IMGBB_API_KEY"
#define IMGBB_UPLOAD_URL "https://api.imgbb.com/1/upload"

// Google Teachable Machine Configuration
#define TEACHABLE_MACHINE_URL "https://teachablemachine.withgoogle.com/models/YOUR_MODEL_ID/model.json"

// ========================================
// ESP32-CAM PIN DEFINITION (AI-Thinker)
// ========================================
#define PWDN_GPIO_NUM     32
#define RESET_GPIO_NUM    -1
#define XCLK_GPIO_NUM      0
#define SIOD_GPIO_NUM     26
#define SIOC_GPIO_NUM     27

#define Y9_GPIO_NUM       35
#define Y8_GPIO_NUM       34
#define Y7_GPIO_NUM       39
#define Y6_GPIO_NUM       36
#define Y5_GPIO_NUM       21
#define Y4_GPIO_NUM       19
#define Y3_GPIO_NUM       18
#define Y2_GPIO_NUM        5
#define VSYNC_GPIO_NUM    25
#define HREF_GPIO_NUM     23
#define PCLK_GPIO_NUM     22

#define FLASH_LED_PIN      4

// ========================================
// GLOBAL VARIABLES
// ========================================
FirebaseData fbdo;
FirebaseAuth auth;
FirebaseConfig config;

unsigned long lastCaptureTime = 0;
const unsigned long CAPTURE_INTERVAL = 3600000; // 1 hour (3600000 ms)

String latestImageURL = "";
String latestAIResult = "";
float latestAIConfidence = 0.0;

// NTP Time Server
const char* ntpServer = "pool.ntp.org";
const long gmtOffset_sec = 28800;  // GMT+8 (Philippines)
const int daylightOffset_sec = 0;

// ========================================
// SETUP
// ========================================
void setup() {
  WRITE_PERI_REG(RTC_CNTL_BROWN_OUT_REG, 0); // Disable brownout detector

  Serial.begin(115200);
  Serial.println("\n========================================");
  Serial.println("ESP32-CAM Plant Health Monitor - Starting...");
  Serial.println("========================================");

  // Initialize camera
  if (initCamera()) {
    Serial.println("✓ Camera initialized successfully");
  } else {
    Serial.println("✗ Camera initialization failed!");
    ESP.restart();
  }

  // Initialize flash LED
  pinMode(FLASH_LED_PIN, OUTPUT);
  digitalWrite(FLASH_LED_PIN, LOW);

  // Connect to WiFi
  connectWiFi();

  // Initialize time
  configTime(gmtOffset_sec, daylightOffset_sec, ntpServer);
  Serial.println("✓ NTP time synchronized");

  // Initialize Firebase
  initFirebase();

  Serial.println("========================================");
  Serial.println("System ready! Waiting for next capture...");
  Serial.println("========================================\n");

  // Take initial photo immediately
  captureAndProcess();
}

// ========================================
// MAIN LOOP
// ========================================
void loop() {
  unsigned long currentMillis = millis();

  // Check if it's time to capture a new image
  if (currentMillis - lastCaptureTime >= CAPTURE_INTERVAL) {
    lastCaptureTime = currentMillis;
    captureAndProcess();
  }

  delay(1000); // Check every second
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
// INITIALIZE CAMERA
// ========================================
bool initCamera() {
  camera_config_t camera_config;

  camera_config.ledc_channel = LEDC_CHANNEL_0;
  camera_config.ledc_timer = LEDC_TIMER_0;
  camera_config.pin_d0 = Y2_GPIO_NUM;
  camera_config.pin_d1 = Y3_GPIO_NUM;
  camera_config.pin_d2 = Y4_GPIO_NUM;
  camera_config.pin_d3 = Y5_GPIO_NUM;
  camera_config.pin_d4 = Y6_GPIO_NUM;
  camera_config.pin_d5 = Y7_GPIO_NUM;
  camera_config.pin_d6 = Y8_GPIO_NUM;
  camera_config.pin_d7 = Y9_GPIO_NUM;
  camera_config.pin_xclk = XCLK_GPIO_NUM;
  camera_config.pin_pclk = PCLK_GPIO_NUM;
  camera_config.pin_vsync = VSYNC_GPIO_NUM;
  camera_config.pin_href = HREF_GPIO_NUM;
  camera_config.pin_sscb_sda = SIOD_GPIO_NUM;
  camera_config.pin_sscb_scl = SIOC_GPIO_NUM;
  camera_config.pin_pwdn = PWDN_GPIO_NUM;
  camera_config.pin_reset = RESET_GPIO_NUM;
  camera_config.xclk_freq_hz = 20000000;
  camera_config.pixel_format = PIXFORMAT_JPEG;

  // Image quality settings
  if (psramFound()) {
    camera_config.frame_size = FRAMESIZE_UXGA; // 1600x1200
    camera_config.jpeg_quality = 10;           // 0-63 (lower = better quality)
    camera_config.fb_count = 2;
  } else {
    camera_config.frame_size = FRAMESIZE_SVGA; // 800x600
    camera_config.jpeg_quality = 12;
    camera_config.fb_count = 1;
  }

  // Initialize camera
  esp_err_t err = esp_camera_init(&camera_config);
  if (err != ESP_OK) {
    Serial.printf("Camera init failed with error 0x%x\n", err);
    return false;
  }

  // Adjust camera sensor settings for plant imaging
  sensor_t * s = esp_camera_sensor_get();
  s->set_brightness(s, 0);     // -2 to 2
  s->set_contrast(s, 0);       // -2 to 2
  s->set_saturation(s, 0);     // -2 to 2
  s->set_special_effect(s, 0); // 0 = No effect
  s->set_whitebal(s, 1);       // 0 = disable, 1 = enable
  s->set_awb_gain(s, 1);       // 0 = disable, 1 = enable
  s->set_wb_mode(s, 0);        // 0 to 4
  s->set_exposure_ctrl(s, 1);  // 0 = disable, 1 = enable
  s->set_aec2(s, 0);           // 0 = disable, 1 = enable
  s->set_ae_level(s, 0);       // -2 to 2
  s->set_aec_value(s, 300);    // 0 to 1200
  s->set_gain_ctrl(s, 1);      // 0 = disable, 1 = enable
  s->set_agc_gain(s, 0);       // 0 to 30
  s->set_gainceiling(s, (gainceiling_t)0); // 0 to 6
  s->set_bpc(s, 0);            // 0 = disable, 1 = enable
  s->set_wpc(s, 1);            // 0 = disable, 1 = enable
  s->set_raw_gma(s, 1);        // 0 = disable, 1 = enable
  s->set_lenc(s, 1);           // 0 = disable, 1 = enable
  s->set_hmirror(s, 0);        // 0 = disable, 1 = enable
  s->set_vflip(s, 0);          // 0 = disable, 1 = enable
  s->set_dcw(s, 1);            // 0 = disable, 1 = enable
  s->set_colorbar(s, 0);       // 0 = disable, 1 = enable

  return true;
}

// ========================================
// CAPTURE AND PROCESS IMAGE
// ========================================
void captureAndProcess() {
  Serial.println("\n========================================");
  Serial.println("Starting image capture and processing...");
  Serial.println("========================================");

  // Step 1: Capture image
  camera_fb_t * fb = captureImage();
  if (fb == NULL) {
    Serial.println("✗ Image capture failed!");
    return;
  }
  Serial.println("✓ Image captured");

  // Step 2: Upload to ImgBB
  String imageURL = uploadToImgBB(fb);
  if (imageURL == "") {
    Serial.println("✗ Image upload failed!");
    esp_camera_fb_return(fb);
    return;
  }
  Serial.println("✓ Image uploaded to ImgBB");
  Serial.println("URL: " + imageURL);
  latestImageURL = imageURL;

  // Step 3: Send to Teachable Machine for AI classification
  String aiResult = "";
  float aiConfidence = 0.0;
  classifyWithAI(fb, aiResult, aiConfidence);
  latestAIResult = aiResult;
  latestAIConfidence = aiConfidence;

  // Return frame buffer
  esp_camera_fb_return(fb);

  // Step 4: Save results to Firebase
  saveResultsToFirebase(imageURL, aiResult, aiConfidence);

  Serial.println("========================================");
  Serial.println("Capture and processing complete!");
  Serial.println("========================================\n");
}

// ========================================
// CAPTURE IMAGE
// ========================================
camera_fb_t* captureImage() {
  // Turn on flash LED
  digitalWrite(FLASH_LED_PIN, HIGH);
  delay(200); // Let camera adjust to light

  // Capture image
  camera_fb_t * fb = esp_camera_fb_get();

  // Turn off flash LED
  digitalWrite(FLASH_LED_PIN, LOW);

  if (!fb) {
    Serial.println("Camera capture failed");
    return NULL;
  }

  Serial.printf("Image size: %d bytes\n", fb->len);
  return fb;
}

// ========================================
// UPLOAD TO IMGBB
// ========================================
String uploadToImgBB(camera_fb_t * fb) {
  if (WiFi.status() != WL_CONNECTED) {
    Serial.println("✗ WiFi not connected");
    return "";
  }

  HTTPClient http;

  // Encode image to base64
  String base64Image = base64::encode(fb->buf, fb->len);

  // Prepare POST data
  String postData = "key=" + String(IMGBB_API_KEY) + "&image=" + base64Image;

  // Send POST request
  http.begin(IMGBB_UPLOAD_URL);
  http.addHeader("Content-Type", "application/x-www-form-urlencoded");

  Serial.println("Uploading to ImgBB...");
  int httpResponseCode = http.POST(postData);

  String imageURL = "";

  if (httpResponseCode > 0) {
    String response = http.getString();
    Serial.println("ImgBB Response Code: " + String(httpResponseCode));

    // Parse JSON response
    DynamicJsonDocument doc(4096);
    deserializeJson(doc, response);

    if (doc["success"]) {
      imageURL = doc["data"]["url"].as<String>();
      Serial.println("✓ Upload successful!");
    } else {
      Serial.println("✗ ImgBB upload failed");
    }
  } else {
    Serial.println("✗ HTTP POST failed: " + String(httpResponseCode));
  }

  http.end();
  return imageURL;
}

// ========================================
// AI CLASSIFICATION (Teachable Machine)
// ========================================
void classifyWithAI(camera_fb_t * fb, String &result, float &confidence) {
  if (WiFi.status() != WL_CONNECTED) {
    Serial.println("✗ WiFi not connected");
    result = "error";
    confidence = 0.0;
    return;
  }

  HTTPClient http;

  // Note: Teachable Machine typically requires a hosted image URL
  // We'll use the ImgBB URL for classification

  // For direct image classification, you may need to use TensorFlow Lite on ESP32
  // This is a placeholder showing the API structure

  String apiURL = String(TEACHABLE_MACHINE_URL) + "?image=" + latestImageURL;

  http.begin(apiURL);
  int httpResponseCode = http.GET();

  if (httpResponseCode > 0) {
    String response = http.getString();

    // Parse JSON response
    DynamicJsonDocument doc(2048);
    deserializeJson(doc, response);

    // Extract top prediction
    result = doc["predictions"][0]["className"].as<String>();
    confidence = doc["predictions"][0]["probability"].as<float>();

    Serial.println("✓ AI Classification Complete");
    Serial.println("Result: " + result);
    Serial.printf("Confidence: %.2f%%\n", confidence * 100);
  } else {
    Serial.println("✗ AI classification failed: " + String(httpResponseCode));
    result = "error";
    confidence = 0.0;
  }

  http.end();
}

// ========================================
// SAVE RESULTS TO FIREBASE
// ========================================
void saveResultsToFirebase(String imageURL, String aiResult, float aiConfidence) {
  if (!Firebase.ready()) {
    Serial.println("✗ Firebase not ready");
    return;
  }

  // Get current timestamp
  time_t now;
  time(&now);
  unsigned long timestamp = (unsigned long)now;

  // Create JSON document
  FirebaseJson json;
  json.set("imageURL", imageURL);
  json.set("aiClass", aiResult);
  json.set("aiConfidence", aiConfidence);
  json.set("timestamp", timestamp);

  // Update Firestore document: images/latest
  String documentPath = "images/latest";

  if (Firebase.Firestore.patchDocument(&fbdo, FIREBASE_PROJECT_ID, "", documentPath.c_str(), json.raw(), "")) {
    Serial.println("✓ Firebase updated successfully");
  } else {
    Serial.println("✗ Firebase update failed: " + fbdo.errorReason());
  }

  // Also save to history collection
  String historyPath = "images/history/" + String(timestamp);
  Firebase.Firestore.createDocument(&fbdo, FIREBASE_PROJECT_ID, "", historyPath.c_str(), json.raw());
}

// ========================================
// GET UNIX TIMESTAMP
// ========================================
unsigned long getTimestamp() {
  time_t now;
  time(&now);
  return (unsigned long)now;
}
