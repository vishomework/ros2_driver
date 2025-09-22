from launch import LaunchDescription
from launch_ros.actions import Node
from launch.actions import IncludeLaunchDescription, TimerAction
from launch.launch_description_sources import PythonLaunchDescriptionSource
from ament_index_python import get_package_share_directory
import os

def generate_launch_description():


    airy_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(
                get_package_share_directory('rslidar_sdk'),
                'launch',
                'humble_start.py',
            )
        ),
        launch_arguments={
            'config_file': '~/ros2_driver/src/all/config/config.yaml'
        }.items()
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

    return LaunchDescription([
        airy_launch,
        ms200_launch,
        tf_launch,
    ])