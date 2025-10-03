import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Joy
from std_msgs.msg import String
from pynput.keyboard import Listener
import tkinter as tk
import threading
import queue
import subprocess

class ControllerCommander(Node):
    def __init__(self):
        super().__init__('controller_commander')

        # Specify the device path for the Xbox controller (use your actual device path)
        joystick_device = '/dev/input/js0'  # Change this to the correct device if needed
        self.get_logger().info(f"Starting joy_node with device: {joystick_device}")

        # Start joy_node with specified device using subprocess
        subprocess.Popen(['ros2', 'run', 'joy', 'joy_node', '--dev', joystick_device])

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

        # Create a Tkinter window
        self.root = tk.Tk()
        self.root.title("Controller Commander")
        self.root.geometry("3000x100")

        # Label to display the current command
        self.label = tk.Label(self.root, text="Press 'w' or 's' for commands", font=('Arial', 12))
        self.label.pack(pady=20)

        # Start listening to keyboard events in a separate thread
        self.keyboard_listener = Listener(on_press=self.on_key_press)
        self.keyboard_listener.start()

        # Queue for inter-thread communication (used to pass commands to the GUI)
        self.command_queue = queue.Queue()

        # Run Tkinter GUI event loop in the main thread
        self.root.after(100, self.update_gui)  # Start periodic GUI updates

    def joy_callback(self, msg):
        # Map controller inputs to command codes based on Xbox controller
        # self.get_logger().info('Received joystick input')
        if msg.buttons[0] == 1:  # A button pressed
            self.send_command('GO_FORWARD')
        elif msg.buttons[1] == 1:  # B button pressed
            self.send_command('GO_BACKWARD')
        elif msg.buttons[2] == 1:  # X button pressed
            self.send_command('SLOW_SPEED')
        elif msg.buttons[3] == 1:  # Y button pressed
            self.send_command('MEDIUM_SPEED')
        else:
            self.send_command('STOP')
        
        # # Example of detecting axis movements (left joystick)
        # if msg.axes[0] > 0.1:  # Left Stick X (right direction)
        #     self.send_command('MOVE_RIGHT')
        # elif msg.axes[0] < -0.1:  # Left Stick X (left direction)
        #     self.send_command('MOVE_LEFT')
        
        # if msg.axes[1] > 0.1:  # Left Stick Y (down direction)
        #     self.send_command('MOVE_DOWN')
        # elif msg.axes[1] < -0.1:  # Left Stick Y (up direction)
        #     self.send_command('MOVE_UP')
        
        # # Example for Right Stick or Triggers
        # if msg.axes[4] > 0.1:  # Left Trigger pressed
        #     self.send_command('LEFT_TRIGGER')
        # elif msg.axes[5] > 0.1:  # Right Trigger pressed
        #     self.send_command('RIGHT_TRIGGER')

    def send_command(self, command_str):
        command = String()
        command.data = command_str  # Instruction for Pi 2
        self.cmd_pub.publish(command)
        self.get_logger().info(f'Sent: {command_str}')

    def update_gui(self):
        # Update the label in the Tkinter GUI with the latest command from the queue
        try:
            command = self.command_queue.get_nowait()  # Get the latest command from the queue
            self.label.config(text=f"Last Command: {command}")
        except queue.Empty:
            pass

        # Continue running the Tkinter event loop
        self.root.after(100, self.update_gui)  # Call this method again after 100ms

    def run_ros_spin(self):
        # Spin ROS 2 in a separate thread to prevent blocking the GUI
        rclpy.spin(self)

def main():
    rclpy.init()
    node = ControllerCommander()

    # Run ROS 2 spin in a separate thread
    ros_thread = threading.Thread(target=node.run_ros_spin)
    ros_thread.start()

    # Run Tkinter GUI event loop in the main thread
    node.root.mainloop()

    # Ensure ROS 2 shuts down gracefully
    ros_thread.join()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
