import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Joy, Image as ROSImage
from std_msgs.msg import String
from pynput.keyboard import Listener
import tkinter as tk
import threading
import queue
import subprocess

from cv_bridge import CvBridge
import cv2
from PIL import Image as PILImage, ImageTk


class ControllerCommander(Node):
    def __init__(self):
        super().__init__('controller_commander')

        joystick_device = '/dev/input/js0'
        self.get_logger().info(f"Starting joy_node with device: {joystick_device}")
        subprocess.Popen(['ros2', 'run', 'joy', 'joy_node', '--dev', joystick_device])

        self.joy_sub = self.create_subscription(Joy, 'joy', self.joy_callback, 10)
        self.cmd_pub = self.create_publisher(String, 'execute_command', 10)

        # ROS Image subscriber and conversion
        self.bridge = CvBridge()
        self.current_frame = None
        self.image_sub = self.create_subscription(ROSImage, '/image_raw', self.image_callback, 10)

        # Tkinter GUI setup
        self.root = tk.Tk()
        self.root.title("Controller Commander")
        self.root.geometry("900x700")

        self.label = tk.Label(self.root, text="Press 'w' or 's' for commands", font=('Arial', 12))
        self.label.pack(pady=20)

        # Video display label
        self.video_label = tk.Label(self.root)
        self.video_label.pack(pady=10)

        self.command_queue = queue.Queue()

        self.keyboard_listener = Listener(on_press=self.on_key_press)
        self.keyboard_listener.start()

        self.root.after(100, self.update_gui)           # Command text updater
        self.root.after(30, self.update_video_frame)    # Video updater

    def joy_callback(self, msg):
        if msg.buttons[0] == 1:
            self.send_command('GO_FORWARD')
        elif msg.buttons[1] == 1:
            self.send_command('GO_BACKWARD')
        elif msg.buttons[2] == 1:
            self.send_command('SLOW_SPEED')
        elif msg.buttons[3] == 1:
            self.send_command('MEDIUM_SPEED')
        else:
            self.send_command('STOP')

    def image_callback(self, msg):
        try:
            cv_image = self.bridge.imgmsg_to_cv2(msg, desired_encoding='bgr8')
            self.current_frame = cv2.cvtColor(cv_image, cv2.COLOR_BGR2RGB)
        except Exception as e:
            self.get_logger().error(f"Image conversion error: {e}")

    def update_video_frame(self):
        if self.current_frame is not None:
            img = PILImage.fromarray(self.current_frame)
            imgtk = ImageTk.PhotoImage(image=img)
            self.video_label.imgtk = imgtk  # Prevent garbage collection
            self.video_label.configure(image=imgtk)
        self.root.after(30, self.update_video_frame)

    def on_key_press(self, key):
        try:
            if key.char == 'w':
                self.send_command('GO_FORWARD')
                self.command_queue.put("GO_FORWARD")
            elif key.char == 's':
                self.send_command('STOP')
                self.command_queue.put("STOP")
            elif key.char == 'a':
                self.send_command('TURN_LEFT')
                self.command_queue.put("TURN_LEFT")
            elif key.char == 'd':
                self.send_command('TURN_RIGHT')
                self.command_queue.put("TURN_RIGHT")
            elif key.char == 'z':
                self.send_command('SLOW_SPEED')
                self.command_queue.put("SLOW_SPEED")
            elif key.char == 'x':
                self.send_command('MEDIUM_SPEED')
                self.command_queue.put("MEDIUM_SPEED")
        except AttributeError:
            pass

    def send_command(self, command_str):
        command = String()
        command.data = command_str
        self.cmd_pub.publish(command)
        self.get_logger().info(f'Sent: {command_str}')

    def update_gui(self):
        try:
            command = self.command_queue.get_nowait()
            self.label.config(text=f"Last Command: {command}")
        except queue.Empty:
            pass
        self.root.after(100, self.update_gui)

    def run_ros_spin(self):
        rclpy.spin(self)


def main():
    rclpy.init()
    node = ControllerCommander()

    ros_thread = threading.Thread(target=node.run_ros_spin)
    ros_thread.start()

    node.root.mainloop()

    ros_thread.join()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
