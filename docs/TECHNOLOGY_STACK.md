# 🔧 COMPLETE TECHNOLOGY STACK
## Portable IoT-Based Hydroponic Monitoring System with AI

---

## 🖥️ **CLOUD PLATFORMS & SERVICES**

### 1. **Firebase (Google Cloud)**
- **Service Type:** Backend-as-a-Service (BaaS)
- **Components Used:**
  - **Firestore Database** - NoSQL document database for sensor data
  - **Realtime Database** - Real-time data synchronization (alternative)
  - **Cloud Storage** - Image storage (optional, using ImgBB instead)
  - **Authentication** - User access control
  - **Cloud Functions** - Serverless backend processing
- **Cost:** FREE (Spark Plan)
- **URL:** https://firebase.google.com
- **Purpose:** Store all sensor data, images metadata, AI results
- **Data Retention:** 30 days historical data
- **Region:** asia-southeast1 (Singapore)

---

### 2. **Google Teachable Machine**
- **Service Type:** AI/ML Platform (Transfer Learning)
- **Technology:** MobileNet v2 (TensorFlow.js)
- **Purpose:** Plant health classification AI model
- **Training:** Browser-based, no coding required
- **Classes:** 4 categories (healthy, nutrient_deficiency, disease, optimal_growth)
- **Deployment:** Cloud-hosted API endpoint
- **Cost:** FREE (unlimited API calls)
- **URL:** https://teachablemachine.withgoogle.com
- **Model Format:** REST API (JSON response)
- **Inference Time:** <1 second per image

---

### 3. **Streamlit Cloud**
- **Service Type:** Web app hosting platform
- **Technology:** Python-based dashboard framework
- **Purpose:** Real-time monitoring dashboard
- **Features:**
  - Auto-deployment from GitHub
  - Mobile-responsive web interface
  - Real-time data visualization
  - Interactive controls
- **Cost:** FREE (Community tier)
- **URL:** https://streamlit.io/cloud
- **Deployment:** Automatic from GitHub push
- **Accessibility:** Public URL, no app installation needed

---

### 4. **GitHub**
- **Service Type:** Version control & code repository
- **Purpose:** 
  - Store dashboard source code
  - Version control for all code
  - Trigger Streamlit auto-deployment
  - Collaboration with team members
- **Repository:** `hydroponic-portable-monitor`
- **Files Stored:**
  - `streamlit_app.py` (dashboard code)
  - `requirements.txt` (Python dependencies)
  - `.gitignore` (security)
  - ESP32 firmware (Arduino sketches)
  - Documentation
- **Cost:** FREE (public repositories)
- **URL:** https://github.com

---

### 5. **ImgBB (Image Hosting)**
- **Service Type:** Free image hosting CDN
- **Purpose:** Store plant images (alternative to Firebase Storage)
- **API:** REST API for image upload
- **Features:**
  - 32MB per image limit
  - Permanent image URLs
  - Fast CDN delivery
  - No storage limits
- **Cost:** FREE
- **URL:** https://api.imgbb.com
- **Integration:** ESP32-CAM uploads directly via API

---

## 🔌 **HARDWARE COMPONENTS**

### **MICROCONTROLLERS**

#### 6. **ESP32 DevKit v1** (Main Controller)
- **Manufacturer:** Espressif Systems
- **Processor:** Dual-core Xtensa LX6, 240MHz
- **Memory:** 520KB SRAM, 4MB Flash
- **Connectivity:** 
  - WiFi 802.11 b/g/n (2.4GHz)
  - Bluetooth 4.2 LE
- **GPIO Pins:** 30+ (digital/analog capable)
- **ADC:** 18 channels, 12-bit resolution (4096 levels)
- **Power:** 3.3V logic, 160-240mA active, <1mA deep sleep
- **Programming:** Arduino IDE, ESP-IDF
- **Cost:** ₱380
- **Purpose:** 
  - Read all sensors
  - Control pumps via relays
  - Send data to Firebase
  - Execute control algorithms
- **Quantity:** 1 unit

---

#### 7. **ESP32-CAM Module**
- **Manufacturer:** AI-Thinker
- **Processor:** ESP32-S (single core)
- **Camera:** OV2640 (2MP, JPEG hardware encoder)
- **Memory:** 520KB SRAM, 4MB Flash, SD card slot
- **Connectivity:** WiFi 802.11 b/g/n
- **Features:**
  - Built-in camera with LED flash
  - Independent operation
  - Direct image upload capability
- **Resolution:** Up to 1600x1200 (UXGA)
- **Power:** 3.3V, 180-310mA (with camera active)
- **Programming:** Arduino IDE
- **Cost:** ₱380
- **Purpose:**
  - Capture hourly plant photos
  - Upload images to cloud
  - Trigger AI classification
- **Quantity:** 1 unit
- **Status:** ✅ Already owned (2 units available)

---

### **SENSORS**

#### 8. **pH Sensor (Analog)**
- **Model:** DFRobot Gravity Analog pH Sensor Kit V2
- **Type:** Glass electrode, analog output
- **Range:** 0-14 pH
- **Resolution:** 0.01 pH
- **Accuracy:** ±0.1 pH (after calibration)
- **Response Time:** <15 seconds
- **Interface:** Analog voltage (0-3.3V)
- **Calibration:** 2-point or 3-point with buffer solutions
- **Waterproof:** Probe only (BNC connector)
- **Lifespan:** 6-12 months (electrode replacement needed)
- **Cost:** ₱850
- **Purpose:** Monitor nutrient solution pH (target: 5.8 ± 0.15)

---

#### 9. **EC/TDS Sensor (Electrical Conductivity)**
- **Type:** Conductivity probe, analog output
- **Range:** 0-5000 ppm (0-10 mS/cm)
- **Resolution:** 1 ppm
- **Accuracy:** ±2% of reading
- **Temperature Compensation:** Required (uses DS18B20 data)
- **Interface:** Analog voltage
- **Probe Type:** Titanium alloy electrodes
- **Calibration:** 1-point with 1413 μS/cm standard solution
- **Cost:** ₱650
- **Purpose:** Monitor nutrient concentration (target: 1.2 ± 0.08 mS/cm)

---

#### 10. **DS18B20 (Water Temperature)**
- **Type:** Digital 1-Wire temperature sensor
- **Range:** -55°C to +125°C
- **Accuracy:** ±0.5°C (-10°C to +85°C)
- **Resolution:** 0.0625°C (12-bit)
- **Interface:** 1-Wire digital protocol
- **Housing:** Waterproof stainless steel probe
- **Cable Length:** 1 meter
- **Response Time:** <1 second
- **Cost:** ₱180
- **Purpose:** Monitor water temperature (target: 18-22°C)
- **Note:** Also used for EC temperature compensation

---

#### 11. **DHT22 (Air Temperature & Humidity)**
- **Type:** Digital capacitive humidity sensor
- **Temperature Range:** -40°C to +80°C
- **Temperature Accuracy:** ±0.5°C
- **Humidity Range:** 0-100% RH
- **Humidity Accuracy:** ±2-5% RH
- **Interface:** Single-wire digital protocol
- **Sampling Rate:** 0.5Hz (one reading per 2 seconds)
- **Power:** 3.3V, 2.5mA typical
- **Cost:** ₱220
- **Purpose:** Monitor ambient growing environment

---

#### 12. **HC-SR04 (Ultrasonic Distance/Water Level)**
- **Type:** Ultrasonic ranging sensor
- **Range:** 2cm to 400cm
- **Accuracy:** ±1cm
- **Resolution:** 0.3cm
- **Frequency:** 40kHz ultrasonic
- **Interface:** Digital trigger/echo pins
- **Power:** 5V, 15mA
- **Beam Angle:** 15 degrees
- **Cost:** ₱95
- **Purpose:** Non-contact water level monitoring
- **Calculation:** Distance to water surface = water level depth

---

### **ACTUATORS & CONTROL**

#### 13. **Peristaltic Pumps (3 units)**
- **Type:** 12V DC peristaltic dosing pump
- **Flow Rate:** 100ml/min (adjustable by PWM)
- **Power:** 12V DC, 150-200mA each
- **Tube Material:** Silicone (food-grade, chemical resistant)
- **Features:**
  - Self-priming
  - Reversible flow
  - Precise volumetric dosing
- **Cost:** ₱450 each (₱1,350 total)
- **Purpose:**
  - Pump 1: pH-UP solution (potassium hydroxide)
  - Pump 2: pH-DOWN solution (phosphoric acid)
  - Pump 3: Concentrated nutrient solution
- **Control:** Via relay module, activated by ESP32

---

#### 14. **4-Channel Relay Module (2 units)**
- **Type:** Optocoupler-isolated relay board
- **Voltage:** 5V control logic
- **Contact Rating:** 10A @ 250VAC / 30VDC
- **Channels:** 4 relays per module (8 total)
- **Isolation:** Optocoupler (protect ESP32 from high voltage)
- **Indicators:** LED per channel
- **Trigger:** Active LOW or HIGH (configurable)
- **Cost:** ₱180 each (₱360 total)
- **Purpose:**
  - Switch pumps ON/OFF
  - Control circulation pump
  - Future expansion (lights, fans)
- **Connections:** 
  - Relay 1-3: Peristaltic pumps
  - Relay 4: Circulation pump
  - Relays 5-8: Reserved

---

### **POWER MANAGEMENT**

#### 15. **LiPo Battery Pack**
- **Type:** Lithium Polymer rechargeable battery
- **Voltage:** 3.7V nominal (4.2V fully charged)
- **Capacity:** 10,000mAh
- **Protection:** Built-in BMS (Battery Management System)
- **Features:**
  - Over-charge protection
  - Over-discharge protection
  - Short-circuit protection
- **Output:** USB 5V (for charging devices)
- **Charging:** Micro-USB/USB-C input
- **Runtime:** Estimated 8-12 hours continuous operation
- **Cost:** ₱1,200
- **Purpose:** Portable power supply for true mobility

---

#### 16. **Solar Panel (Optional)**
- **Type:** Polycrystalline solar panel
- **Power:** 6V, 2W
- **Dimensions:** ~110mm x 60mm
- **Efficiency:** ~17%
- **Features:**
  - Weather-resistant encapsulation
  - Pre-soldered wires
- **Charging Module:** TP4056 (included in system)
- **Cost:** ₱450
- **Purpose:** 
  - Recharge battery during daylight
  - Extend autonomous operation
  - Reduce manual charging needs

---

#### 17. **Voltage Regulators (DC-DC Buck Converters)**
- **Model:** LM2596 (or similar)
- **Type:** Step-down switching regulator
- **Input:** 4.5V - 40V DC
- **Output:** Adjustable 1.25V - 37V DC
- **Current:** 3A maximum
- **Efficiency:** >85%
- **Features:**
  - Overload protection
  - Thermal shutdown
  - LED indicator
- **Cost:** ₱85 each (₱170 for 2 units)
- **Purpose:**
  - Regulator 1: 3.7V battery → 5V (for relays, pumps)
  - Regulator 2: 3.7V battery → 3.3V (for ESP32, sensors)

---

### **SIGNAL CONDITIONING**

#### 18. **Analog Signal Isolators**
- **Model:** ISO124 (or equivalent)
- **Type:** Galvanic isolation amplifier
- **Isolation Voltage:** 1500V
- **Bandwidth:** 50kHz
- **Purpose:** Prevent ground loops between pH and EC sensors
- **Quantity:** 2 units (one per analog sensor)
- **Cost:** ₱320 each (₱640 total)
- **Why Needed:** pH and EC probes in same solution create electrical interference without isolation

---

### **ENCLOSURE & ASSEMBLY**

#### 19. **Waterproof Enclosure**
- **Type:** ABS plastic junction box
- **Rating:** IP65 (dust-tight, water-resistant)
- **Dimensions:** 200mm × 150mm × 75mm
- **Features:**
  - Cable glands for waterproof wire entry
  - Mounting holes
  - Clear/opaque options
- **Cost:** ₱450
- **Purpose:** Protect electronics from water splashes, humidity

---

#### 20. **Breadboard/PCB & Wiring**
- **Components:**
  - Universal perfboard PCB (10cm × 15cm)
  - Screw terminal blocks
  - DuPont jumper wires
  - 20AWG silicone wire (red/black)
  - Heat shrink tubing
  - JST connectors
- **Cost:** ₱385 (complete wiring kit)
- **Purpose:** Professional circuit assembly and organization

---

## 💻 **SOFTWARE & DEVELOPMENT TOOLS**

### **FIRMWARE DEVELOPMENT**

#### 21. **Arduino IDE**
- **Version:** 2.x (latest)
- **Platform:** Windows, macOS, Linux
- **Language:** C/C++ (Arduino framework)
- **Purpose:** Program ESP32 microcontrollers
- **Features:**
  - Code editor with syntax highlighting
  - Serial monitor for debugging
  - Library manager
- **Cost:** FREE (open-source)
- **URL:** https://arduino.cc

---

#### 22. **ESP32 Board Support Package**
- **Provider:** Espressif Systems
- **Version:** 3.0.x
- **Installation:** Via Arduino IDE Board Manager
- **Purpose:** Enable ESP32 programming in Arduino IDE
- **Includes:**
  - Compiler toolchain
  - Upload tools
  - Core libraries (WiFi, Bluetooth, etc.)

---

### **ARDUINO LIBRARIES**

#### 23. **Firebase ESP32 Client**
- **Library:** Firebase-ESP-Client by Mobizt
- **Version:** Latest from Library Manager
- **Purpose:** Connect ESP32 to Firebase services
- **Features:**
  - Realtime Database access
  - Firestore support
  - Cloud Storage upload
  - Authentication

---

#### 24. **Sensor Libraries**
- **OneWire** - DS18B20 communication protocol
- **DallasTemperature** - DS18B20 temperature reading
- **DHT sensor library** - DHT22 interface
- **NewPing** - HC-SR04 ultrasonic ranging
- **ArduinoJson** - JSON parsing/creation for API calls
- **HTTPClient** - Make HTTP requests (Teachable Machine API)
- **Base64** - Encode images for API transmission

---

### **DASHBOARD DEVELOPMENT**

#### 25. **Python**
- **Version:** 3.9 or higher
- **Purpose:** Streamlit dashboard development
- **Cost:** FREE (open-source)

---

#### 26. **Python Libraries**
- **streamlit** (1.28+) - Web dashboard framework
- **firebase-admin** (6.2+) - Firebase Admin SDK for Python
- **plotly** (5.17+) - Interactive data visualization
- **pandas** (2.1+) - Data manipulation and analysis
- **requests** - HTTP library for API calls
- **Pillow** - Image processing

---

### **VERSION CONTROL**

#### 27. **Git**
- **Purpose:** Version control system
- **Platform:** Command-line or GitHub Desktop
- **Cost:** FREE
- **Usage:**
  - Track code changes
  - Collaborate with team
  - Deploy to Streamlit Cloud

---

## 🎯 **SUMMARY STATISTICS**

### **Technology Count:**
- **Cloud Platforms:** 5 services
- **Hardware Components:** 20 items
- **Software Tools:** 15+ libraries/frameworks
- **Total Cost:** ₱6,800 (with owned ESP32 boards)
- **Setup Time:** ~2 hours (cloud), ~8 hours (hardware)
- **Monthly Operating Cost:** ₱0 (all free tiers!)

---

**This is your COMPLETE technology stack - everything needed from cloud to hardware!** 🚀
