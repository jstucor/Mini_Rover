#import rclpy
#from rclpy.node import Node
#from std_msgs.msg import String
import serial
import serial.tools.list_ports
import time

class ExecutorNode():
    def __init__(self):
        #super().__init__('executor_node')
        """self.subscription = self.create_subscription(
            String,
            'execute_command',
            self.execute_callback,
            10
        )"""

        ports = list(serial.tools.list_ports.grep("ttyACM0"))
        
        if len(ports) > 0:
            print(ports[0].device)
            self.serial = serial.Serial(ports[0].device, baudrate=115200, timeout=1)
        else:
            print("Unable to find Arduino")

    def execute_callback(self, msg):
        command = msg.data
        #self.get_logger().info(f'Received: {command}')
        # Execute Python code based on the command
        if command == 'W':
            self.do_forward()
        elif command == 'S':
            self.do_back()
        elif command == 'A':
            self.do_left()
        elif command == 'D':
            self.do_right()
        elif command == 'STOP_MOVING':
            self.motor_stop()
            #self.get_logger().info(f'Unknown command: {command}')
        print(self.serial.read_until())

    def do_forward(self):
        #self.get_logger().info('Doing W: forward')
        self.serial.write(bytes('forward', 'utf-8'))

    def do_back(self):
        #self.get_logger().info('Doing S: back')
        self.serial.write(bytes('back', 'utf-8'))

    def do_left(self):
        self.serial.write(bytes('left', 'utf-8'))

    def do_right(self):
        #self.get_logger().info('Doing D: right')
        self.serial.write(bytes('right', 'utf-8'))
    
    def motor_stop(self):
        #self.get_logger().info('Stopping')
        self.serial.write(bytes('stop', 'utf-8'))

class Res():
    def __init__(self, data):
        self.data = data

def main():
    #rclpy.init()
    node = ExecutorNode()
    #rclpy.spin(node)
    #rclpy.shutdown()

    node.execute_callback(Res('W'))
    time.sleep(2)
    node.execute_callback(Res('stop'))

if __name__ == '__main__':
    main()