# Navigate to your workspace directory
cd ~/ros2_ws

# Build the ROS 2 packages
colcon build --packages-select lunabot_telemetry lunabot_bringup

# Source the workspace
source install/setup.bash

# Run the master launch file (starts Telemetry, LiDAR, and WebCam nodes)
ros2 launch lunabot_bringup robot.launch.py