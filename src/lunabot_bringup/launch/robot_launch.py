import os
from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    return LaunchDescription([
        # 1. Start Telemetry Node (Serial Bridge to ESP32)
        Node(
            package='lunabot_telemetry',
            executable='telemetry_node.py',
            name='telemetry_node',
            output='screen',
            parameters=[{
                'port': '/dev/ttyUSB0',
                'baud': 115200
            }]
        ),

        # 2. Start 3D LiDAR Driver Node
        Node(
            package='rplidar_ros', # Replace with your specific 3D LiDAR driver package if different
            executable='rplidar_composition',
            name='lidar_3d_node',
            output='screen',
            parameters=[{
                'serial_port': '/dev/ttyUSB1',
                'frame_id': 'laser_frame'
            }]
        ),

        # 3. Start Front RGB Webcam Node
        Node(
            package='v4l2_camera',
            executable='v4l2_camera_node',
            name='front_camera',
            parameters=[{
                'video_device': '/dev/video0',
                'image_size': [640, 480]
            }]
        )
    ])
