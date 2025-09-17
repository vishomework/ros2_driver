from launch import LaunchDescription
from launch_ros.actions import Node
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration # 导入LaunchConfiguration
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
import os
from ament_index_python.packages import get_package_share_directory


def generate_launch_description():

    bag_save_path_arg = DeclareLaunchArgument(
        'bag_save_path',
        default_value='my_bag', # 默认路径
        description='Path to save the recorded bag files'
    )


    mutli_recorder_node = Node(
        package='bags_record',
        executable='multi_recorder', # 请确保此可执行文件名与你的CMakeLists.txt中设置的一致
        name='multi_bag_recorder',
        output='screen',
        parameters=[{'bag_file_path': LaunchConfiguration('bag_save_path')}] # 正确引用启动参数
    )

    mid360_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(
                get_package_share_directory('livox_ros_driver2'), # 替换为你的包名
                'launch_ROS2',
                # 'rviz_MID360_launch.py' # 替换为你的launch文件名
                'msg_MID360_launch.py' # 替换为你的launch文件名
            )
        )
    )

    return LaunchDescription([
        bag_save_path_arg, # 必须将参数声明也添加到LaunchDescription中
        mutli_recorder_node,
        mid360_launch
    ])