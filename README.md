# Repository ROS2_DRIVER

## Part : Related Functional Packages
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

