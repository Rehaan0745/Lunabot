#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from std_msgs.msg import Float32MultiArray
import serial
import json

class TelemetryNode(Node):
    def __init__(self):
        super().__init__('telemetry_node')
        self.publisher_ = self.create_publisher(Float32MultiArray, '/lunabot/sensors', 10)
        self.port = self.declare_parameter('port', '/dev/ttyUSB0').get_parameter_value().string_value
        self.baud = self.declare_parameter('baud', 115200).get_parameter_value().integer_value
        
        try:
            self.ser = serial.Serial(self.port, self.baud, timeout=1.0)
            self.get_logger().info(f'Connected to ESP32 telemetry on {self.port}')
        except Exception as e:
            self.get_logger().error(f'Failed to open serial port {self.port}: {e}')
            self.ser = None

        self.timer = self.create_timer(0.2, self.read_telemetry)

    def read_telemetry(self):
        if self.ser and self.ser.in_waiting > 0:
            try:
                line = self.ser.readline().decode('utf-8').strip()
                data = json.loads(line)
                
                msg = Float32MultiArray()
                # Published format: [temp, humidity, pressure, light, current, voltage]
                msg.data = [
                    float(data.get('temp', 0.0)),
                    float(data.get('humidity', 0.0)),
                    float(data.get('pressure', 0.0)),
                    float(data.get('light', 0.0)),
                    float(data.get('current', 0.0)),
                    float(data.get('voltage', 0.0))
                ]
                self.publisher_.publish(msg)
            except Exception as e:
                self.get_logger().warn(f'Telemetry parse error: {e}')

def main(args=None):
    rclpy.init(args=args)
    node = TelemetryNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()