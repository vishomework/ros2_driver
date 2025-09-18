# ros2_driver

<!-- ## 前提条件一定要先开启slam，不然没有roscore 运行桥接会报错 -->
<!-- ## 拉下来之后先编译工作空间，这个应该会编译除了ros1bridge的所有功能包 -->
<!-- ```
colcon build
```




如果用这个分支上的桥接，需要另开一个终端
进入~/ros2_ws/ros1_bridge/ros1_bridge_ws
```
source install/setup.bash
```

如果不用这里的ros1_bridge一定一定不要source ros1 的环境 -->
<!-- ## 进入packages目录编译
cd ~/packages
```
colcon build && source install/setup.bash
``` -->
驱动已经在镜像里编译了，只需要编译自己的功能包

在ros2ws下编译然后运行launch就行

直接运行run.launch.py(开启了两个雷达和一个tf)
```
ros2 launch all run.launch.py
```

该容器未加入ros1bridge