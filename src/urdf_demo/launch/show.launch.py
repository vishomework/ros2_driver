from launch import LaunchDescription
from launch_ros.actions import Node
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration, PathJoinSubstitution
from ament_index_python.packages import get_package_share_directory
import os

def generate_launch_description():
    # 获取功能包共享目录路径
    urdf_file = get_package_share_directory('moveit_resources_panda_description')
    
    # 定义URDF文件路径
    urdf_path = os.path.join(urdf_file, 'urdf', 'panda.urdf')
    with open(urdf_path, 'r') as infp:
        robot_description_config = infp.read()
    
    # 将robot_description设置为一个LaunchConfiguration可能更方便管理
    robot_description = {'robot_description': robot_description_config}
    
    # 定义节点
    robot_state_publisher_node = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        name='robot_state_publisher',
        output='screen',
        parameters=[robot_description]  # 使用相同的参数字典
    )
    
    joint_state_publisher_node = Node(
        package='joint_state_publisher_gui',
        executable='joint_state_publisher_gui',
        name='joint_state_publisher_gui',
        output='screen',
        parameters=[robot_description]  # 关键修改：也为这个节点提供robot_description参数
    )
    
    # 可选：启动RViz2，确保配置文件路径正确
    rviz2_node = Node(
        package='rviz2',
        executable='rviz2',
        name='rviz2',
        arguments=['-d', os.path.join(urdf_file, 'rviz', 'rviz.config.rviz')]
    )
    
    map_to_pandalink0_tf = Node(
        package='tf2_ros',
        executable='static_transform_publisher',
        name='map_to_panda_link0_broadcaster',
        arguments=['0', '0', '0', '0', '0', '0', 'map', 'panda_link0'] 
        # 参数说明: x y z yaw pitch roll parent_frame child_frame [8,10](@ref)
    )

    return LaunchDescription([
        robot_state_publisher_node,
        joint_state_publisher_node,
        rviz2_node,
        map_to_pandalink0_tf
    ])