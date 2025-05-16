import rclpy
from rclpy.node import Node
from std_msgs.msg import String

class ExecutorNode(Node):
    def __init__(self):
        super().__init__('executor_node')
        self.subscription = self.create_subscription(
            String,
            'execute_command',
            self.execute_callback,
            10
        )

    def execute_callback(self, msg):
        command = msg.data
        self.get_logger().info(f'Received: {command}')
        # Execute Python code based on the command
        if command == 'DO_A':
            self.do_task_a()
        elif command == 'DO_B':
            self.do_task_b()
        else:
            self.get_logger().info(f'Unknown command: {command}')

    def do_task_a(self):
        # Example Python code for A button
        self.get_logger().info('Task A: Writing to file')
        # with open('/home/ubuntu/output.txt', 'a') as f:
        #     f.write('A button was pressed!\n')

    def do_task_b(self):
        # Example Python code for B button
        self.get_logger().info('Task B: Doing some math')
        result = 5 + 3
        self.get_logger().info(f'5 + 3 = {result}')

def main():
    rclpy.init()
    node = ExecutorNode()
    rclpy.spin(node)
    rclpy.shutdown()

if __name__ == '__main__':
    main()