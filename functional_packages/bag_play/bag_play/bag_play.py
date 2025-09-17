import rclpy
import rosbag2_py
import os
import glob
import subprocess

from rclpy.node import Node
from std_msgs.msg import String
from rosidl_runtime_py.utilities import get_message
from ament_index_python.packages import get_package_share_directory

class ros2bag_play(Node):
    def __init__(self):
        super().__init__('ros2bag_play')

        # 数据包放置路径
        dataBagpath = get_package_share_directory("bag_play")
        self.declare_parameter('bag_path', os.path.join(dataBagpath, "ros2bag"))
        # 播放速率
        self.declare_parameter('rate', 1)
        # 是否循环播放
        self.declare_parameter('loop', True)

        self.rosbag_path = ''
        self.find_bag()

    def find_bag(self):
        # 寻找.db3的数据包
        bag_path = self.get_parameter('bag_path').value

        db3_files = []
        
        for root, dirs, files in os.walk(bag_path):
            db3_files.extend(glob.glob(os.path.join(root, "*.db3")))

            if db3_files:
                break
        
        if db3_files:
            self.rosbag_path = db3_files[0]
            self.get_logger().info(f'找到db3文件: {self.rosbag_path}')
        else:
            self.get_logger().error(f"在 {bag_path} 中未找到.db3文件")

    def play_bag(self):
        
        if not self.rosbag_path:
            self.get_logger().error("无可播放的数据包！")
            return
        
        CMD = ['ros2', 'bag', 'play', self.rosbag_path, '--rate', str(self.get_parameter('rate').value)]
        
        if self.get_parameter('loop').value:
            CMD.append('--loop')

        self.get_logger().info("正在播放")

        try:
            subprocess.run(CMD, check=True)
        except subprocess.CalledProcessError as e:
            self.get_logger().error("播放失败")

def main(args=None):
        rclpy.init(args=args)
        node = ros2bag_play()
        node.play_bag()
        rclpy.shutdown()

if __name__ == '__main__':
    main()    