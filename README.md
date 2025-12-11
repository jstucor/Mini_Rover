# Mini Rover
A project from the BYU Spacecraft Club. Here is our [OnShape file](https://cad.onshape.com/documents?nodeId=455888d2b202b0785466f0e2&resourceType=folder&column=modifiedAt&order=desc&viewMode=0)

# Club Semester Goals and Tasks
    Focus more on the goals and tasks made 


- [ ] **Hike the Y trail and locate EB**
 - [ ] __Range Test__ (Communicating with the rover 2 miles away)
  - [ ] Confiure and test equipment via short range tests
    - [x] Purchase RF equipment (Jacob)
  - [x] Fix ROS bugs on both ground station and rover
    - [x] Abstract away joystick.node in ROS code
    - [x] Update controller connection to be stable
    - [x] Change Joystick node to act as a service with Motor node (Ian)
    - [x] Fix servo bug with Arduino (Collin)

- [ ] __Ruggedness Test__ (Pass dust-proof test)
 - [ ] Encase all equipment in water/dust tight case
  - [x] Print first design
 - [ ]  Get basic temperature readings
  - [ ]   Make temperature part of the ROS scripts ()
- [ ]  __Battery Distance__ (Drive rover 1 mile up a 30 deg incline)
 - [ ] Do smaller simulations on treadmil and scale to mile distance
   - [ ] Wire battery, run basic diagnostics to ensure no short circuiting
    - [x]  Purchase battery
     - [x]  Choose battery (post Rocket installation)


## Potential Future Goals

- [x] Custom PCB for rover
- [ ] Sensor integration
 - [ ] IMU
 - [ ] Pin drill
 - [ ] Sonar
- [ ] Robotic arm


## Onshape files
All of our onshape files can be found [here](https://cad.onshape.com/documents?nodeId=455888d2b202b0785466f0e2&resourceType=folder&column=modifiedAt&order=desc&viewMode=0) 

## Setting up the pis
Boot the pis with Ubuntu 24.02 and follow the install section of the [ros2 website](https://docs.ros.org/en/jazzy/Installation/Ubuntu-Install-Debs.html)

Connect the 2 pis together via an ethernet cable and open the wired communication settings
- Navigate to the IPv4 settings and make the connection manual
- On the base station
    - IP address : 192.168.0.1 Netmask: 255.255.255.0 Gateway: 192.168.0.1
- On the rover:
    - IP address : 192.168.0.2 Netmask: 255.255.255.0 Gateway: 192.168.0.1
 
Then to initialize ROS:
 mkdir ros2_ws/src
 source /opt/ros/jazzy/setup.bash
 colcon build (if colcon not installed, check the installation)
 
Modify the setup bash scripts:
 sudo nano ~/.bashrc
 
At the bottom of the file add:
 source /opt/ros/jazzy/setup.bash
 source ~/ros2_ws/install/setup.bash

Under the ros2_ws./src directory you begin editing your code
 To make your first ros2 script, follow the steps from [this documentation](https://docs.ros.org/en/jazzy/Tutorials/Beginner-Client-Libraries/Creating-Your-First-ROS2-Package.html)

Run the turtle sim!
On one 
 ros2 run turtlesim turtlesim_node
On the other
 ros2 run turtlesim turtle_teleop_key

