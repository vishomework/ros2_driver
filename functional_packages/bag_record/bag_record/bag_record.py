import os
import time
import rclpy
from rclpy.node import Node
from rclpy.qos import QoSProfile, QoSDurabilityPolicy, QoSReliabilityPolicy
from rosbag2_py import SequentialWriter, StorageOptions, ConverterOptions, TopicMetadata
from rclpy.serialization import serialize_message
from rosidl_runtime_py.utilities import get_message
import shutil

class BagRecorder(Node):
    def __init__(self):
        super().__init__('bag_recorder')
        
        # 参数配置
        self.max_size_bytes = int(self.declare_parameter('max_size_gb', 5.0).value * 1024**3)
        self.max_folder_num = self.declare_parameter('max_folder_num', 10).value
        self.use_mcap = self.declare_parameter('mcap', True).value
        self.record_nav = self.declare_parameter('record_nav', True).value
        
        # 存储路径管理
        self.record_dir_root = os.path.expanduser('~/ros2_driver/functional_packages/bag_record/ros2bag')
        self.bag_path = self.prepare_record_path()
        self.get_logger().info(f'📁 Recording to: {self.bag_path}')
        
        # 初始化录制器
        self.writer = SequentialWriter()
        storage_id = 'mcap' if self.use_mcap else 'sqlite3'
        self.writer.open(
            StorageOptions(uri=self.bag_path, storage_id=storage_id),
            ConverterOptions('cdr', 'cdr')
        )
        self.get_logger().info(f'📦 Using {storage_id.upper()} format')
        
        self.subscribers = []
        self.subscribed_topics = set()
        
        self.subscribe_topics()

        self.create_timer(3.0, self.timer_callback)

    def prepare_record_path(self):
        """准备存储路径并清理旧数据"""
        os.makedirs(self.record_dir_root, exist_ok=True)
        
        # 获取所有记录目录并按创建时间排序
        dirs = [d for d in os.listdir(self.record_dir_root) 
                if os.path.isdir(os.path.join(self.record_dir_root, d))]
        dirs.sort(key=lambda d: os.path.getctime(os.path.join(self.record_dir_root, d)))
        
        # 删除最旧的记录
        while len(dirs) >= self.max_folder_num:
            old_path = os.path.join(self.record_dir_root, dirs.pop(0))
            self.get_logger().info(f'🗑️ Removing oldest folder: {old_path}')
            shutil.rmtree(old_path)
        
        # 创建新目录
        new_dir = time.strftime("%m-%d-%H-%M", time.localtime())
        return os.path.join(self.record_dir_root, new_dir)

    def create_callback(self, topic_name):
        """创建消息回调函数"""
        return lambda msg: self.writer.write(
            topic_name, 
            serialize_message(msg), 
            self.get_clock().now().nanoseconds
        )

    def subscribe_topic(self, topic_name, msg_type_str, qos=None):
        """订阅话题并添加到录制器"""
        if topic_name in self.subscribed_topics:
            return
            
        try:
            msg_type = get_message(msg_type_str)
            topic_info = TopicMetadata(
                name=topic_name, 
                type=msg_type_str, 
                serialization_format='cdr'
            )
            
            sub = self.create_subscription(
                msg_type, 
                topic_name, 
                self.create_callback(topic_name), 
                qos or 10
            )
            
            self.writer.create_topic(topic_info)
            self.subscribers.append(sub)
            self.subscribed_topics.add(topic_name)
            self.get_logger().info(f'✅ Recording: {topic_name}')
        except Exception as e:
            self.get_logger().error(f'⛔ Failed to subscribe to {topic_name}: {e}')

    def subscribe_topics(self):
        """订阅所有需要的话题"""
        # 特殊话题处理
        self.subscribe_topic('/tf', 'tf2_msgs/msg/TFMessage')
        
        # /tf_static 需要特殊 QoS
        static_qos = QoSProfile(
            depth=10,
            durability=QoSDurabilityPolicy.TRANSIENT_LOCAL,
            reliability=QoSReliabilityPolicy.RELIABLE
        )
        self.subscribe_topic('/tf_static', 'tf2_msgs/msg/TFMessage', static_qos)
        
        # 导航相关话题
        if self.record_nav:
            nav_types = [
                'geometry_msgs/msg/Twist', 'geometry_msgs/msg/TwistStamped',
                'geometry_msgs/msg/PoseStamped', 'sensor_msgs/msg/Imu',
                'sensor_msgs/msg/PointCloud2', 'sensor_msgs/msg/LaserScan',
                'geometry_msgs/msg/Vector3Stamped', 'std_msgs/msg/String',
                'nav_msgs/msg/Path', 'nav_msgs/msg/OccupancyGrid'
            ]
            
            for topic_name, types in self.get_topic_names_and_types():
                if types and types[0] in nav_types:
                    self.subscribe_topic(topic_name, types[0])

    def check_size_limit(self):
        """检查存储大小限制"""
        total_size = 0
        for root, _, files in os.walk(self.bag_path):
            for f in files:
                total_size += os.path.getsize(os.path.join(root, f))
                
        if total_size > self.max_size_bytes:
            self.get_logger().error('🚫 Reached size limit. Shutting down...')
            rclpy.shutdown()

    def timer_callback(self):
        """定时器回调函数"""
        self.check_size_limit()
        # 动态发现新话题
        self.subscribe_topics()

def main(args=None):
    rclpy.init(args=args)
    recorder = BagRecorder()
    
    try:
        rclpy.spin(recorder)
    except KeyboardInterrupt:
        recorder.get_logger().info("Recording stopped by user.")
    finally:
        recorder.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()