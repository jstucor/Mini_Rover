import sys
if sys.prefix == '/usr':
    sys.real_prefix = sys.prefix
    sys.prefix = sys.exec_prefix = '/home/spacecraft/ros2_ws/src/motor_controller/install/motor_controller'
