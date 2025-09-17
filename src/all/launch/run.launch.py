from launch import LaunchDescription
from launch_ros.actions import Node
from launch.actions import IncludeLaunchDescription, TimerAction
from launch.launch_description_sources import PythonLaunchDescriptionSource
from ament_index_python import get_package_share_directory
import os

def generate_launch_description():

    # ros1_bridge_node = Node(
    #     package='ros1_bridge',
    #     executable='dynamic_bridge',
    #     name='ros1_bridge_node',
    #     arguments=['--bridge-all-topics'],
    # )

    airy_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(
                get_package_share_directory('rslidar_sdk'),
                'launch',
                'humble_start.py',
            )
        )
    )

    ms200_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(
                get_package_share_directory('oradar_lidar'),
                'launch',
                'ms200_scan.launch.py',
            )
        )
    )

    tf_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(
                get_package_share_directory('all'),
                'launch',
                'tf.launch.py',
            )
        )
    )
    # 简单地延迟启动 ros1_bridge_node
    # delayed_bridge = TimerAction(
    #     period=5.0, # 延迟5秒。这个时间需要根据rslidar_sdk实际启动时间调整
    #     actions=[ros1_bridge_node]
    # )

    return LaunchDescription([
        airy_launch,
        # delayed_bridge,
        ms200_launch,
        tf_launch,
    ])