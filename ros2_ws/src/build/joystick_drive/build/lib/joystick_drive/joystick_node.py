import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Joy
from std_msgs.msg import String

class ControllerCommander(Node):
    def __init__(self):
        super().__init__('controller_commander')
        # Subscribe to joystick data
        self.joy_sub = self.create_subscription(
            Joy,
            'joy',
            self.joy_callback,
            10
        )
        # Publisher for commands
        self.cmd_pub = self.create_publisher(
            String,
            'execute_command',
            10
        )

    def joy_callback(self, msg):
        # Map controller inputs to command codes
        if msg.buttons[0] == 1:  # A button pressed
            command = String()
            command.data = 'DO_A'  # Instruction for Pi 2
            self.cmd_pub.publish(command)
            self.get_logger().info('Sent: DO_A')
        elif msg.buttons[1] == 1:  # B button pressed
            command = String()
            command.data = 'DO_B'  # Instruction for Pi 2
            self.cmd_pub.publish(command)
            self.get_logger().info('Sent: DO_B')

def main():
    rclpy.init()
    node = ControllerCommander()
    rclpy.spin(node)
    rclpy.shutdown()

if __name__ == '__main__':
    main()