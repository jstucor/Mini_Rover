import rclpy
from rclpy.node import Node
from std_msgs.msg import String
import serial
import time

class ExecutorNode(Node):
    def __init__(self):
        super().__init__('executor_node')
        self.subscription = self.create_subscription(
            String,
            'execute_command',
            self.execute_callback,
            10
        )
        self.initialized = False
        self.serial_port = serial.Serial('/dev/ttyACM0', baudrate=115200, timeout=1)
        time.sleep(2)  # Give time for Arduino to initialize
        self.initialized = True

    def execute_callback(self, msg):
        command = msg.data
        #self.get_logger().info(f'Received UPDATED CODE: {command}')

       

        if command == 'GO_FORWARD':
            self.send_serial_command("forward")
        elif command == 'GO_BACKWARD':
            self.send_serial_command("backward")
        elif command == 'STOP':
            self.send_serial_command("stop")
        elif command == 'MEDIUM_SPEED':
            self.send_serial_command("medium")
        elif command == 'SLOW_SPEED':
            self.send_serial_command("slow")
        elif command == 'TURN_RIGHT':
            self.send_serial_command("right")
        elif command == 'TURN_LEFT':
            self.send_serial_command("left")
        else:
            self.get_logger().info(f'Unknown command: {command}')

    def send_serial_command(self, command):
        #self.get_logger().info(f'Sent to Arduino: {command} {self.initialized}')
        if self.initialized:
            try:
                self.serial_port.write((f"{command}\n").encode())
            except Exception as e:
                self.get_logger().error(f'Error sending command: {e}')

    def destroy_node(self):
        self.serial_port.close()
        super().destroy_node()

def main():
    rclpy.init()
    node = ExecutorNode()
    try:
        rclpy.spin(node)
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
