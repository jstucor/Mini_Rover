#!/bin/bash
source /opt/ros/jazzy/setup.bash

# Navigate to the ROS 2 workspace (replace with your actual workspace path if needed)
cd ~/ros2_ws  # Replace with the path to your ROS 2 workspace if it's different

# Build the specific package
colcon build --packages-select joystick_drive

# Source the ROS 2 workspace setup file
source install/setup.bash

# Run the joystick node
ros2 run joystick_drive joystick_node


