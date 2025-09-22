from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    # 定义多个静态坐标变换发布器节点
    # 每个节点都有唯一的名称，并描述了其功能
    static_transform_nodes = [
        # 从 base_link 到 livox_frame 的变换 (假设是Livox雷达)
        Node(
            package='tf2_ros',
            executable='static_transform_publisher',
            arguments=['0', '0', '0', '0', '0', '0', 'base_link', 'livox_frame'],
            name='base_link_to_livox_frame_publisher'  # 修改为唯一的名称
        ),
        
        # 从 map 到 base_link 的变换 (通常由定位算法提供，静态发布可能不合适)
        Node(
            package='tf2_ros',
            executable='static_transform_publisher',
            arguments=['0', '0', '0', '0', '0', '0', 'map', 'base_link'],
            name='map_to_base_link_publisher'  # 修改为唯一的名称
        ),
        
        # 从 odom 到 camera_init 的变换 (通常与视觉SLAM相关)
        Node(
            package='tf2_ros',
            executable='static_transform_publisher',
            arguments=['0', '0', '0', '0', '0', '0', 'odom', 'camera_init'],
            name='odom_to_camera_init_publisher'  # 修改为唯一的名称
        ),
        
        # 从 base_link 到 aft_mapped 的变换 (意义需根据你的系统确定)
        Node(
            package='tf2_ros',
            executable='static_transform_publisher',
            arguments=['0', '0', '0', '0', '0', '0', 'aft_mapped', 'base_link'],
            name='base_link_to_aft_mapped_publisher'  # 修改为唯一的名称
        ),

        Node(
            package='tf2_ros',
            executable='static_transform_publisher',
            arguments=['0', '0', '0', '0', '0', '0', 'map', 'odom'],
            name='base_link_to_aft_mapped_publisher'  # 修改为唯一的名称
        ),
        
        # 从 base_link 到 laser_frame 的变换 (假设是激光雷达)
        Node(
            package='tf2_ros',
            executable='static_transform_publisher',
            arguments=['0', '0', '0', '0', '0', '0', 'base_link', 'laser_frame'],
            name='base_link_to_laser_frame_publisher'  # 修改为唯一的名称
        )
        # 注意: 你之前有两个相同的 base_link 到 laser_frame 的变换，我保留了一个。
    ]

    return LaunchDescription(static_transform_nodes)