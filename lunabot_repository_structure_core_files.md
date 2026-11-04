# Lunabot GitHub Repository Architecture

To turn the Lunabot project into a production-grade, professional GitHub repository, you should organize your files into a clean workspace directory tree containing configuration, firmware, high-level ROS 2 packages, and documentation.

---

## 📂 Recommended Directory Tree

```text
lunabot-rover/
├── .gitignore                   # Ignores build files, sensitive data, and environments
├── LICENSE                      # Open-source license file (MIT)
├── README.md                    # Primary project documentation (generated previously)
├── docs/                        # Diagrams, photos, and hardware schematics
│   ├── system_architecture.png
│   └── hardware_wiring.pdf
├── firmware/                    # Low-level ESP32 micro-controller code
│   ├── platformio.ini           # PlatformIO environment config
│   └── src/
│       └── main.cpp             # Telemetry collection & motor control firmware
├── ros2_ws/                     # High-level computing ROS 2 workspace
│   └── src/
│       ├── lunabot_bringup/     # Master launch files and configurations
│       │   ├── CMakeLists.txt
│       │   ├── package.xml
│       │   ├── config/
│       │   │   └── params.yaml  # Motor speeds, sensor pins, and PID params
│       │   └── launch/
│       │       └── robot.launch.py
│       ├── lunabot_description/ # URDF / CAD robot visual representation
│       │   └── urdf/
│       │       └── lunabot.urdf
│       ├── lunabot_navigation/  # LiDAR SLAM and navigation config
│       │   └── config/
│       │       └── nav2_params.yaml
│       └── lunabot_telemetry/   # Sensor nodes (DHT11, BMP280, ACS712)
│           ├── package.xml
│           └── lunabot_telemetry/
│               └── sensor_node.py
```

---

## 📄 Essential Top-Level Repository Files

### 1. `.gitignore`
Prevents temporary build files, ROS 2 binaries, Python caches, and platform builds from cluttering your repository.

```gitignore
# Python & Bytecode
__pycache__/
*.py[cod]
*$py.class
.venv/
env/

# ROS 2 Build Artifacts
ros2_ws/build/
ros2_ws/install/
ros2_ws/log/

# Embedded Systems & PlatformIO
.pio/
.vscode/
.idea/
*.bin
*.elf

# OS specific
.DS_Store
Thumbs.db
```

---

### 2. `LICENSE` (MIT License Template)

```text
MIT License

Copyright (c) 2026 Lunabot Team

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

---

### 3. `ros2_ws/src/lunabot_bringup/config/params.yaml`
Configuration parameter file for driving parameters and hardware pins.

```yaml
lunabot_driver:
  ros__parameters:
    serial_port: "/dev/ttyUSB0"
    baud_rate: 115200
    wheel_diameter: 0.12  # in meters (120mm)
    max_wheel_speed: 1.5   # m/s

telemetry_node:
  ros__parameters:
    temp_sensor_pin: 4
    publish_rate_hz: 5.0
    voltage_divider_ratio: 5.0
```

---

### 4. `ros2_ws/src/lunabot_telemetry/package.xml`
ROS 2 package manifest detailing package metadata, dependencies, and maintainer information.

```xml
<?xml version="1.0"?>
<?xml-model href="http://download.ros.org/schema/package_format3.xsd" schematypens="http://www.w3.org/2001/XMLSchema"?>
<package format="3">
  <name>lunabot_telemetry</name>
  <version>1.0.0</version>
  <description>Sensor data acquisition for DHT11, BMP280, ACS712 on Lunabot</description>
  <maintainer email="developer@example.com">Lunabot Team</maintainer>
  <license>MIT</license>

  <depend>rclpy</depend>
  <depend>sensor_msgs</depend>
  <depend>std_msgs</depend>

  <export>
    <build_type>ament_python</build_type>
  </export>
</package>
```

---

### 5. `firmware/platformio.ini`
PlatformIO configuration for compiling and uploading low-level microcontroller software to the ESP32 co-processor.

```ini
[env:esp32dev]
platform = espressif32
board = esp32dev
framework = arduino
monitor_speed = 115200

lib_deps =
    adafruit/Adafruit BMP280 Library @ ^2.6.8
    adafruit/DHT sensor library @ ^1.4.6
    robtillaart/ACS712 @ ^0.3.9
```