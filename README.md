# 🌱 Portable IoT-Based Hydroponic Monitoring System with AI

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://your-app-name.streamlit.app)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A complete IoT solution for real-time hydroponic system monitoring with AI-powered plant health classification. Built with ESP32 microcontrollers, Firebase cloud backend, and Streamlit web dashboard.

---

## 📋 Table of Contents

- [Features](#-features)
- [System Architecture](#-system-architecture)
- [Hardware Requirements](#-hardware-requirements)
- [Software Requirements](#-software-requirements)
- [Installation & Setup](#-installation--setup)
- [Usage](#-usage)
- [Project Structure](#-project-structure)
- [Configuration](#-configuration)
- [Troubleshooting](#-troubleshooting)
- [Contributing](#-contributing)
- [License](#-license)

---

## ✨ Features

### 🔬 **Comprehensive Sensor Monitoring**
- **pH Level** - Track nutrient solution acidity (target: 5.8 ± 0.15)
- **EC/TDS** - Monitor nutrient concentration (target: 1.2 ± 0.08 mS/cm)
- **Water Temperature** - DS18B20 digital sensor (target: 18-22°C)
- **Air Temperature & Humidity** - DHT22 environmental monitoring
- **Water Level** - Ultrasonic distance measurement (HC-SR04)

### 🤖 **AI-Powered Plant Health Classification**
- Google Teachable Machine integration
- 4 classification categories: healthy, nutrient_deficiency, disease, optimal_growth
- Hourly automated image capture via ESP32-CAM
- Confidence scoring and recommendations

### ⚡ **Automated Control System**
- Automatic pH adjustment (pH-UP/pH-DOWN pumps)
- Automatic nutrient dosing
- Configurable setpoints and tolerances
- 5-minute cooldown safety mechanism

### 📊 **Real-Time Web Dashboard**
- Live sensor readings with gauge charts
- Historical data trends (24h/48h/7d views)
- AI classification results display
- Manual control interface
- CSV data export functionality

### ☁️ **Cloud Integration**
- Firebase Firestore real-time database
- ImgBB image hosting (free CDN)
- Streamlit Cloud web hosting
- Accessible from any device (desktop, tablet, mobile)

### 🔋 **Portable & Energy Efficient**
- LiPo battery powered (10,000mAh)
- Optional solar panel charging
- Deep sleep modes for power savings
- Autonomous operation capability

---

## 🏗️ System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    CLOUD SERVICES                            │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │   Firebase   │  │ Teachable    │  │  Streamlit   │      │
│  │  Firestore   │  │   Machine    │  │    Cloud     │      │
│  └──────────────┘  └──────────────┘  └──────────────┘      │
└─────────────────────────────────────────────────────────────┘
           ▲                  ▲                  ▲
           │                  │                  │
           │ WiFi             │ HTTPS            │ HTTPS
           │                  │                  │
┌──────────┴──────────────────┴──────────────────┴─────────────┐
│                    LOCAL HARDWARE                             │
│  ┌──────────────┐                    ┌──────────────┐        │
│  │  ESP32 Main  │◄──────────────────►│ ESP32-CAM    │        │
│  │  Controller  │    Independent      │   Module     │        │
│  └──────────────┘                    └──────────────┘        │
│         │                                    │                │
│         │                                    │                │
│    ┌────┴────┐                          ┌───┴───┐            │
│    │ Sensors │                          │Camera │            │
│    └─────────┘                          └───────┘            │
│    • pH                                                       │
│    • EC/TDS                          ┌──────────────┐        │
│    • DS18B20                         │   Actuators  │        │
│    • DHT22                           │  (Relays +   │        │
│    • HC-SR04                         │    Pumps)    │        │
│                                      └──────────────┘        │
└───────────────────────────────────────────────────────────────┘
```

---

## 🛠️ Hardware Requirements

### **Microcontrollers**
- **ESP32 DevKit v1** (1x) - Main controller - ₱380
- **ESP32-CAM AI-Thinker** (1x) - Image capture - ₱380

### **Sensors**
- **pH Sensor** - Analog pH meter (DFRobot Gravity) - ₱850
- **EC/TDS Sensor** - Electrical conductivity probe - ₱650
- **DS18B20** - Waterproof temperature sensor - ₱180
- **DHT22** - Air temperature & humidity - ₱220
- **HC-SR04** - Ultrasonic water level sensor - ₱95

### **Actuators & Control**
- **Peristaltic Pumps** (3x) - 12V DC dosing pumps - ₱1,350
- **4-Channel Relay Modules** (2x) - 5V relay boards - ₱360

### **Power Management**
- **LiPo Battery** - 10,000mAh, 3.7V - ₱1,200
- **LM2596 Buck Converters** (2x) - Voltage regulators - ₱170
- **Solar Panel** (optional) - 6V 2W - ₱450

### **Miscellaneous**
- **Waterproof Enclosure** - IP65 ABS box - ₱450
- **Wiring & PCB** - Breadboard, terminals, wires - ₱385
- **Analog Isolators** (2x) - ISO124 signal isolation - ₱640

**Total Hardware Cost: ~₱6,800** (₱6,420 with owned ESP32s)

---

## 💻 Software Requirements

### **Cloud Platforms (All FREE)**
- [Firebase](https://firebase.google.com) - Backend database
- [Google Teachable Machine](https://teachablemachine.withgoogle.com) - AI model training
- [Streamlit Cloud](https://streamlit.io/cloud) - Dashboard hosting
- [GitHub](https://github.com) - Version control & deployment
- [ImgBB](https://imgbb.com) - Image hosting

### **Development Tools**
- [Arduino IDE](https://www.arduino.cc/en/software) (v2.x) - ESP32 firmware development
- [Python](https://www.python.org/downloads) (3.9+) - Dashboard development
- [Git](https://git-scm.com/downloads) - Version control

### **Arduino Libraries**
```cpp
// Install via Arduino IDE Library Manager
- Firebase-ESP-Client by Mobizt
- OneWire
- DallasTemperature
- DHT sensor library
- ArduinoJson
- ESP32 Camera (built-in)
```

### **Python Libraries**
```bash
# Install via pip (see requirements.txt)
pip install -r requirements.txt
```

---

## 🚀 Installation & Setup

### **1. Clone Repository**

```bash
git clone https://github.com/yourusername/hydroponic-portable-monitor.git
cd hydroponic-portable-monitor
```

### **2. Firebase Setup**

#### Create Firebase Project
1. Go to [Firebase Console](https://console.firebase.google.com)
2. Click "Add project" and follow the wizard
3. Enable **Firestore Database** (Start in production mode)
4. Enable **Authentication** (Email/Password)

#### Get Firebase Credentials
1. Go to Project Settings → Service Accounts
2. Click "Generate new private key"
3. Save the JSON file securely (for Streamlit Cloud)

#### Get Firebase API Key
1. Go to Project Settings → General
2. Scroll to "Your apps" section
3. Add Web App and copy the API key

#### Create Firestore Collections
```
sensors/
  ├── current/ (document for latest readings)
  └── history/ (collection for time-series data)

images/
  ├── latest/ (document for latest image)
  └── history/ (collection for image history)

control/
  └── settings/ (document for system configuration)
```

### **3. ImgBB Setup**

1. Visit [ImgBB API](https://api.imgbb.com/v1)
2. Sign up for a free account
3. Get your API key from the dashboard
4. Copy the API key for ESP32-CAM configuration

### **4. Teachable Machine AI Model**

#### Train Your Model
1. Go to [Teachable Machine](https://teachablemachine.withgoogle.com)
2. Choose "Image Project" → "Standard image model"
3. Create 4 classes:
   - `healthy`
   - `nutrient_deficiency`
   - `disease`
   - `optimal_growth`
4. Upload/capture training images for each class (minimum 50 per class)
5. Click "Train Model"
6. After training, click "Export Model" → "Upload my model"
7. Copy the model URL provided

### **5. ESP32 Main Firmware Configuration**

Open `firmware/esp32_main/esp32_main.ino` and update:

```cpp
// WiFi Credentials
#define WIFI_SSID "Your_WiFi_Name"
#define WIFI_PASSWORD "Your_WiFi_Password"

// Firebase Configuration
#define FIREBASE_PROJECT_ID "your-project-id"
#define FIREBASE_API_KEY "AIzaSyXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
#define FIREBASE_USER_EMAIL "your-email@example.com"
#define FIREBASE_USER_PASSWORD "your-password"
```

#### Upload to ESP32
1. Open Arduino IDE
2. Select Board: **ESP32 Dev Module**
3. Select Port: (your ESP32's COM port)
4. Click **Upload**

### **6. ESP32-CAM Firmware Configuration**

Open `firmware/esp32_cam/esp32_cam.ino` and update:

```cpp
// WiFi Credentials (same as ESP32 Main)
#define WIFI_SSID "Your_WiFi_Name"
#define WIFI_PASSWORD "Your_WiFi_Password"

// Firebase Configuration (same as ESP32 Main)
#define FIREBASE_PROJECT_ID "your-project-id"
#define FIREBASE_API_KEY "AIzaSyXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
#define FIREBASE_USER_EMAIL "your-email@example.com"
#define FIREBASE_USER_PASSWORD "your-password"

// ImgBB API
#define IMGBB_API_KEY "your_imgbb_api_key"

// Teachable Machine Model
#define TEACHABLE_MACHINE_URL "https://teachablemachine.withgoogle.com/models/YOUR_MODEL_ID/"
```

#### Upload to ESP32-CAM
1. Connect ESP32-CAM with USB-to-TTL adapter
2. Connect GPIO 0 to GND (programming mode)
3. Select Board: **AI Thinker ESP32-CAM**
4. Select Port: (your adapter's COM port)
5. Click **Upload**
6. After upload, disconnect GPIO 0 from GND
7. Press RESET button

### **7. Streamlit Cloud Deployment**

#### Push Code to GitHub
```bash
git add .
git commit -m "Initial hydroponic monitoring system"
git push origin main
```

#### Configure Streamlit Cloud
1. Go to [Streamlit Cloud](https://streamlit.io/cloud)
2. Sign in with GitHub
3. Click "New app"
4. Select your repository: `hydroponic-portable-monitor`
5. Main file path: `streamlit_app.py`
6. Click "Advanced settings"

#### Add Secrets (Firebase Credentials)
In the secrets section, paste your Firebase JSON:

```toml
[firebase]
type = "service_account"
project_id = "your-project-id"
private_key_id = "xxxxxxxxxxxxxxxxxxxxx"
private_key = "-----BEGIN PRIVATE KEY-----\nYOUR_PRIVATE_KEY_HERE\n-----END PRIVATE KEY-----\n"
client_email = "firebase-adminsdk-xxxxx@your-project-id.iam.gserviceaccount.com"
client_id = "xxxxxxxxxxxxxxxxxxxx"
auth_uri = "https://accounts.google.com/o/oauth2/auth"
token_uri = "https://oauth2.googleapis.com/token"
auth_provider_x509_cert_url = "https://www.googleapis.com/oauth2/v1/certs"
client_x509_cert_url = "https://www.googleapis.com/robot/v1/metadata/x509/firebase-adminsdk-xxxxx%40your-project-id.iam.gserviceaccount.com"
```

7. Click "Deploy"
8. Wait 2-3 minutes for deployment to complete
9. Access your dashboard at: `https://your-app-name.streamlit.app`

---

## 📖 Usage

### **Hardware Assembly**

1. **Sensor Connections**
   - pH Sensor → ESP32 GPIO 34 (ADC1_CH6)
   - EC Sensor → ESP32 GPIO 35 (ADC1_CH7)
   - DS18B20 → ESP32 GPIO 4
   - DHT22 → ESP32 GPIO 15
   - HC-SR04 Trig → ESP32 GPIO 5
   - HC-SR04 Echo → ESP32 GPIO 18

2. **Relay Connections**
   - Relay 1 (pH-UP) → ESP32 GPIO 25
   - Relay 2 (pH-DOWN) → ESP32 GPIO 26
   - Relay 3 (Nutrient) → ESP32 GPIO 27
   - Relay 4 (Reserved) → ESP32 GPIO 14

3. **Power Supply**
   - LiPo Battery → Buck Converter 1 (5V output) → Relays, Sensors
   - LiPo Battery → Buck Converter 2 (3.3V output) → ESP32, DHT22

### **Calibration**

#### pH Sensor Calibration
1. Prepare pH 4.0, 7.0, and 10.0 buffer solutions
2. Run Arduino Serial Monitor
3. Place probe in pH 7.0 buffer
4. Record voltage reading
5. Update `phCalibration_voltage` in firmware
6. Repeat for pH 4.0 to calculate slope

#### EC Sensor Calibration
1. Prepare 1413 µS/cm calibration solution
2. Place probe in solution
3. Record reading
4. Calculate calibration factor: `1.413 / measured_value`
5. Update `ecCalibration_factor` in firmware

### **Dashboard Access**

1. Open web browser (desktop, tablet, or mobile)
2. Navigate to: `https://your-app-name.streamlit.app`
3. Use navigation sidebar to switch between pages:
   - **Dashboard** - Real-time sensor readings
   - **Historical Trends** - Data analysis and charts
   - **AI Plant Health** - Image and AI classification
   - **System Control** - Manual controls and setpoints
   - **Data Export** - Download CSV reports

### **Monitoring**

- **Real-Time:** Dashboard auto-refreshes every 5 seconds
- **Alerts:** Visual indicators show optimal/warning/critical status
- **Trends:** View 24h, 48h, or 7-day historical data
- **AI Analysis:** Hourly plant health updates

---

## 📁 Project Structure

```
hydroponic-portable-monitor/
│
├── firmware/
│   ├── esp32_main/
│   │   └── esp32_main.ino          # Main controller firmware
│   └── esp32_cam/
│       └── esp32_cam.ino            # Camera module firmware
│
├── dashboard/
│   └── (unused - code in root)
│
├── docs/
│   └── TECHNOLOGY_STACK.md          # Complete tech stack documentation
│
├── config/
│   └── secrets.example              # Template for credentials
│
├── streamlit_app.py                 # Main dashboard application
├── requirements.txt                 # Python dependencies
├── README.md                        # This file
├── .gitignore                       # Git ignore rules
└── LICENSE                          # MIT License

```

---

## ⚙️ Configuration

### **Target Setpoints**

Default values in firmware (adjustable via dashboard):

| Parameter | Target | Tolerance | Range |
|-----------|--------|-----------|-------|
| pH | 5.8 | ± 0.15 | 4.0 - 8.0 |
| EC | 1.2 mS/cm | ± 0.08 | 0.5 - 3.0 |
| Water Temp | 20°C | ± 2°C | 18 - 22°C |
| Air Temp | 25°C | ± 3°C | 18 - 30°C |
| Humidity | 60% | ± 10% | 40 - 80% |

### **Data Collection Intervals**

- **Sensor Readings:** Every 5 seconds
- **Firebase Updates:** Every 5 seconds
- **Image Capture:** Every 1 hour
- **AI Classification:** After each image capture

### **Safety Mechanisms**

- **Pump Cooldown:** 5 minutes between dosing actions
- **Brownout Detection:** Disabled on ESP32-CAM to prevent reset
- **WiFi Reconnection:** Automatic retry on connection loss
- **Error Handling:** Graceful fallback values

---

## 🔧 Troubleshooting

### **ESP32 Not Connecting to WiFi**
- Verify SSID and password are correct
- Ensure 2.4GHz WiFi (ESP32 doesn't support 5GHz)
- Check router settings (disable AP isolation if needed)
- Verify ESP32 is within WiFi range

### **Sensors Reading Incorrect Values**
- **pH/EC:** Perform calibration with buffer solutions
- **DS18B20:** Check 4.7kΩ pull-up resistor on data line
- **DHT22:** Ensure proper power supply (3.3V, adequate current)
- **HC-SR04:** Verify trigger/echo pin connections

### **Firebase Connection Issues**
- Verify API key and project ID are correct
- Ensure Firebase Authentication is enabled
- Check user credentials (email/password)
- Verify Firestore security rules allow read/write

### **Dashboard Not Loading**
- Check Streamlit Cloud deployment status
- Verify secrets are configured correctly
- Check browser console for JavaScript errors
- Ensure Firebase credentials in secrets are valid

### **ESP32-CAM Not Capturing Images**
- Verify camera initialization (check serial monitor)
- Ensure adequate power supply (camera requires ~300mA)
- Check GPIO 0 is NOT connected to GND during operation
- Try reducing JPEG quality or frame size

### **AI Classification Not Working**
- Verify Teachable Machine model URL is correct
- Ensure model is publicly accessible
- Check ImgBB image upload is successful
- Verify image URL is accessible from browser

---

## 🤝 Contributing

Contributions are welcome! Please follow these guidelines:

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/AmazingFeature`
3. Commit your changes: `git commit -m 'Add some AmazingFeature'`
4. Push to the branch: `git push origin feature/AmazingFeature`
5. Open a Pull Request

### **Development Roadmap**

- [ ] Add SMS/Email alert notifications
- [ ] Implement data backup to SD card
- [ ] Add grow light control (relay + timer)
- [ ] Integrate with Home Assistant
- [ ] Mobile app (React Native or Flutter)
- [ ] Multi-tank support (multiple systems)
- [ ] Advanced analytics (ML predictions)

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 📧 Contact & Support

**Project Maintainer:** Your Name
**Email:** your.email@example.com
**GitHub:** [@yourusername](https://github.com/yourusername)

**Issues:** Please report bugs or request features via [GitHub Issues](https://github.com/yourusername/hydroponic-portable-monitor/issues)

---

## 🙏 Acknowledgments

- **Espressif Systems** - ESP32 platform and documentation
- **Google** - Firebase, Teachable Machine
- **Streamlit** - Dashboard framework and cloud hosting
- **DFRobot** - Sensor documentation and libraries
- **Arduino Community** - Libraries and support

---

## 📚 References

1. Resh, H. M. (2012). *Hydroponic Food Production*. CRC Press.
2. Jones, J. B. (2016). *Hydroponics: A Practical Guide for the Soilless Grower*. CRC Press.
3. ESP32 Technical Reference Manual - Espressif Systems
4. Firebase Realtime Database Documentation - Google
5. Streamlit Documentation - Streamlit Inc.

---

## ⭐ Star This Project

If you find this project helpful, please give it a star on GitHub! Your support helps others discover this work.

[![GitHub stars](https://img.shields.io/github/stars/yourusername/hydroponic-portable-monitor.svg?style=social&label=Star&maxAge=2592000)](https://github.com/yourusername/hydroponic-portable-monitor/stargazers)

---

**Made with 💚 for sustainable agriculture and open-source IoT**
