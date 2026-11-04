# Lunabot: Autonomous Lunar Exploration Rover

![Lunabot System Architecture](image_42b045.jpg)

Lunabot is an autonomous 4-wheel drive (4WD) robotic lunar exploration platform built to operate in simulated planetary environments. It features an edge computing architecture, dynamic spatial perception via 3D LiDAR and vision sensors, custom motor driving circuitry, and a comprehensive environmental/electrical telemetry suite.

---

## 📑 Table of Contents
- [System Architecture](#system-architecture)
- [Hardware Specifications](#hardware-specifications)
- [System Block Diagram](#system-block-diagram)
- [Software & Repositories](#software--repositories)
- [Getting Started](#getting-started)
- [Telemetry & Diagnostics](#telemetry--diagnostics)
- [License](#license)

---

## 🚁 System Architecture

Lunabot operates on a dual-layer computing topology:
1. **High-Level Compute (Perception & Navigation):** Executes spatial mapping, point cloud processing, path planning, and vision analysis.
2. **Low-Level Compute (Real-Time Control & Telemetry):** Manages closed-loop motor velocity control, high-torque DC motor encoders, and real-time analog/digital sensor polling.

---

## 🛠️ Hardware Specifications

### 1. Drive System & Chassis
- **Chassis:** 4WD aluminum robotic rover chassis ($300 \times 250\text{ mm}$)
- **Wheels:** $100\text{–}120\text{ mm}$ compliant wheels with custom yellow structural hub plates
- **Actuators:** $4\times$ 12V High-Torque DC Geared Motors with integrated quadrature encoders
- **Motor Controllers:** BTS7960 High-Power H-Bridge Motor Drivers

### 2. Computing Suite
- **Primary Compute Host:** NVIDIA Jetson Orin Nano / Raspberry Pi 5
- **Real-Time Co-Processor:** ESP32 Microcontroller
- **Inter-Bus Communication:** USB-A to Micro-USB Serial / UART Protocol

### 3. Navigation & Perception Suite
- **Navigation Mast:** Vertical structural mount for elevated spatial view
- **3D LiDAR:** High-resolution spatial 3D mapping and obstacle avoidance
- **Vision:** Dual RGB Logitech Webcams (mast-mounted for terrain viewing, body-mounted for workspace monitoring)

### 4. Science & Environmental Telemetry Suite
- **Temperature Sensor:** DHT11 ($0\text{–}50^\circ\text{C}$)
- **Barometric Pressure Sensor:** BMP280 ($300\text{–}1100\text{ hPa}$)
- **Ambient Light Sensor:** LM393 Photoresistor module
- **Current Monitor:** ACS712 Hall-Effect Current Sensor
- **Voltage Monitor:** DC0-25V Voltage Divider Module
- **Visual Status Panel:** LED Perimeter Science Panel for status output

### 5. Power Distribution
- **Main Power Unit:** 12V 12Ah Rechargeable Sealed Battery Package

---

## 📐 System Block Diagram

```
                        ┌─────────────────────────┐
                        │   3D LiDAR / RGB Cams   │
                        └────────────┬────────────┘
                                     │ (USB 3.0 / Video)
                                     ▼
                      ┌──────────────────────────────┐
                      │    PRIMARY COMPUTE HOST      │
                      │ (Jetson Orin Nano / Pi 5)    │
                      │  ROS 2 / SLAM / Perception   │
                      └──────────────┬───────────────┘
                                     │ (UART / Serial)
                                     ▼
                      ┌──────────────────────────────┐
                      │    CO-PROCESSOR (ESP32)      │
                      │ Real-Time Control & Sensor Hub│
                      └──────┬────────────────┬──────┘
                             │                │
            ┌────────────────┴┐              ┌┴───────────────────────────┐
            │                 │              │                            │
            ▼                 ▼              ▼                            ▼
   ┌─────────────────┐ ┌─────────────┐ ┌───────────┐ ┌───────────────────────────┐
   │ BTS7960 Drivers │ │  DC Motors  │ │ Encoders  │ │    TELEMETRY SUITE        │
   │   (PWM Control) │ │  (12V 4WD)  │ │ (Feedback)│ │ (DHT11, BMP280, LM393,    │
   └─────────────────┘ └─────────────┘ └───────────┘ │  ACS712, DC0-25V)         │
                                                     └───────────────────────────┘
```

---

## 💻 Software & Repositories

The software system relies on **ROS 2 (Robot Operating System)** for core messaging and package orchestration.

### Key Dependencies
* ROS 2 (Humble / Iron)
* OpenCV & Point Cloud Library (PCL)
* PlatformIO / Arduino IDE (ESP32 Firmware)
* Python 3.10+ / C++17

---

## 🚀 Getting Started

### 1. Repository Setup
Clone the repository and set up your workspace environment:
```bash
git clone https://github.com/your-username/lunabot-rover.git
cd lunabot-rover
```

### 2. Flash ESP32 Microcontroller
Flash the low-level motor driver and telemetry firmware:
```bash
cd firmware/esp32
platformio run --target upload
```

### 3. Build ROS 2 Workspace
Compile the high-level ROS 2 packages on the primary compute board:
```bash
cd ~/ros2_ws
colcon build --symlink-install
source install/setup.bash
```

### 4. Launching the System
Bring up the motor nodes, LiDAR, and vision pipelines:
```bash
ros2 launch lunabot_bringup robot.launch.py
```

To initialize SLAM and navigation mapping:
```bash
ros2 launch lunabot_navigation slam_navigation.launch.py
```

---

## 📊 Telemetry & Diagnostics

The science payload streams continuous telemetry across ROS topics:

| Topic Name | Message Type | Description |
| :--- | :--- | :--- |
| `/lunabot/telemetry/temp` | `sensor_msgs/Temperature` | Ambient temperature reading ($\text{°C}$) |
| `/lunabot/telemetry/pressure` | `sensor_msgs/FluidPressure` | Barometric pressure ($\text{hPa}$) |
| `/lunabot/telemetry/power` | `custom_msgs/PowerStatus` | Bus voltage ($\text{V}$) and current draw ($\text{A}$) |
| `/lunabot/cmd_vel` | `geometry_msgs/Twist` | Velocity command vectors for drive control |

---

## 📜 License

Distributed under the MIT License. See `LICENSE` for more information.