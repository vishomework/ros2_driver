# Repository ROS2_DRIVER

## Part One : Sensor Drivers

**⭐️The intergration work of the driver package is completed by [@wyq123-star](https://github.com/wyq123-star)**

**Author: Xiaomo Wen $\qquad$ Date : 2025-09-21**

**Introduction : Container `ros2_driver` is a container that integrates multiple sensor drivers, and now supports the RoboSense series and MS200.**

If your vscode has the extension `devcontainer`, when you open the folder for the first time, choose `Reopen in Container` can accomplish the image building & container creation automatically.

>There is a problem that you should pay attention to: for  `devcontainer` and `docker-compose`, you can only choose one ( Default `devcontainer` ). If you want to use `docker-compose` to build image and create a container, you should use `docker-compose -p ros2-driver-project up -d` to avoid covering the containers created before, even they don't belong to this repository.

#### In container:
```bash
cd ros2_ws/
source /opt/ros/humble/setup.bash
colcon build
source install/setup.bash
```

Then, use `ros2 launch all run.launch.py` to launch the drivers. Normally, this version of code can driver `robosense_airy` and `ms200`, then bring up the topic `/livox_lidar`, `/livox_imu`, `/MS200/scan` and  `/tf`. **Make sure your hardware device has been properly.**

>[notice] The iPv4 address of robosense lidar in UP70 is `192.168.1.102`, with the subnet mask `255.255.255.0`. Manually set these parameters before running the code. 

## Part Two : Related Functional Packages
**Author : Xiaomo Wen $\qquad$ Date : 2025-09-17** 

### 1. ROS1-ROS2 Bridge
This package ( In `/functional_packages/ROS1-ROS2_Bridge` )  is pre-complied , you can use scripts in folder `/install` directly. 

#### - Here are the steps to use it. Be sure you are in Ubuntu 22.04 ROS2-Humble System.
```bash
source /opt/ros/humble/setup.bash
source /ROS1-ROS2_Bridge/install/local_setup.bash
ros2 run ros1_bridge dynamic_bridge --bridge-all-topics
```
**[notice]**

(1) You need to source `local_setup.bash` but NOT `setup.bash`, because the bridge was compiled in a docker container that may have different underlay locations.

(2) For parameter `--bridge-all-topics`, due to the principle of ROS Bridge -- "For efficiency reasons, topics will only be bridged when matching publisher-subscriber pairs are active for a topic on either side of the bridge.", so adding this parameter can ensure that the ROS topics will be conveyed.

#### - Addtionally, there are simple method to check if the topics are conveyed.
**（1）Open a ROS1 Noetic terminal, then:**
```bash
  source /opt/ros/noetic/setup.bash
  rosrun rospy_tutorials talker
```
**(2) Open a ROS2 Humble terminal, then:**
```bash
  source /opt/ros/humble/setup.bash
  ros2 run demo_nodes_cpp listener
```

#### - For efficiency, to avoid running this node every time, you can create a systemd service to achieve auto-start.

**(1) Create a service script.**
```bash
  sudo nano /etc/systemd/system/ros1_bridge.service
```

**(2) Write Content.**

The `ros1_bridge.service` can be found in folder `/functional_packages/SystemdServices`.

**⭐️[notice] (Must Done) Be sure to modify the paths in `User`, `WorkingDirectory` and `ExecStart` according to your actual situation.** 

**(3) Reload "Systemd" and enable the service**

```bash
  sudo systemctl daemon-reload
  sudo systemctl enable ros1_bridge.service # Enable auto-start.
  sudo systemctl start ros1_bridge.service  # Enable service immediately.
```

**(4) Check the operating status**
```bash
  sudo systemctl status ros1_bridge.service
```
### 2. Foxglove Bridge
You can install Foxglove-Bridge ROS node by `sudo apt install`. Similarly, you can create a systemd service to achieve auto-start **just like the above**, this introduction will not go into details here. **Remember to modify the paths in `User`, `WorkingDirectory` and `ExecStart` according to your actual situation.**

And the `foxglove_bridge.service` can be found in folder `/functional_packages/SystemdServices`.

