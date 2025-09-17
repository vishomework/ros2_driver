# ros2_driver

## 前提条件一定要先开启slam，不然没有roscore 运行桥接会报错
进入容器之后,在一个终端中
```
source install/setup.bash
```
直接运行run.launch.py(开启了两个雷达和一个tf)
```
ros2 launch all run.launch.py
```

如果用这个分支上的桥接，需要另开一个终端
进入~/ros2_ws/ros1_bridge/ros1_bridge_ws
```
source install/setup.bash
```

