cmake_minimum_required(VERSION 3.5)
project(moveit_resources_panda_description)

# 查找ament_cmake（ROS 2的构建系统）
find_package(ament_cmake REQUIRED)

# 安装URDF文件和资源
install(DIRECTORY urdf meshes cmake environment rviz
  DESTINATION share/${PROJECT_NAME}
)

# 声明这是一个ROS 2包
ament_package()