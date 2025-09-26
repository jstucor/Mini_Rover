from sensor_msgs.msg import Image
from cv_bridge import CvBridge
import cv2
import numpy as np
from PIL import Image as PILImage, ImageTk

class ControllerCommander(Node):
    def __init__(self):
        super().__init__('controller_commander')

        joystick_device = '/dev/input/js0'
        self.get_logger().info(f"Starting joy_node with device: {joystick_device}")
        subprocess.Popen(['ros2', 'run', 'joy', 'joy_node', '--dev', joystick_device])

        self.joy_sub = self.create_subscription(Joy, 'joy', self.joy_callback, 10)
        self.cmd_pub = self.create_publisher(String, 'execute_command', 10)

        # ROS Image subscriber
        self.image_sub = self.create_subscription(Image, '/image_raw', self.image_callback, 10)
        self.bridge = CvBridge()
        self.current_frame = None

        self.root = tk.Tk()
        self.root.title("Controller Commander")
        self.root.geometry("640x520")

        self.label = tk.Label(self.root, text="Press 'w' or 's' for commands", font=('Arial', 12))
        self.label.pack(pady=10)

        # Video display label
        self.video_label = tk.Label(self.root)
        self.video_label.pack()

        self.command_queue = queue.Queue()

        self.keyboard_listener = Listener(on_press=self.on_key_press)
        self.keyboard_listener.start()

        self.root.after(100, self.update_gui)
        self.root.after(30, self.update_video_frame)

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
            self.get_logger().error(f"Failed to convert image: {e}")

    def update_video_frame(self):
        if self.current_frame is not None:
            img = PILImage.fromarray(self.current_frame)
            imgtk = ImageTk.PhotoImage(image=img)
            self.video_label.imgtk = imgtk
            self.video_label.configure(image=imgtk)
        self.root.after(30, self.update_video_frame)

    def on_key_press(self, key):
        try:
            if key.char == 'w':
                self.send_command('DO_A')
                self.command_queue.put("DO_A")
            elif key.char == 's':
                self.send_command('DO_B')
                self.command_queue.put("DO_B")
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
