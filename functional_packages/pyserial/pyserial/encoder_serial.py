import serial
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import JointState

class HardwareEncoderInterface(Node):
    def __init__(self):
        super().__init__('hardware_encoder_interface')
        
        # 串口参数
        self.declare_parameter('port', '/dev/ttyUSB0')
        self.declare_parameter('baudrate', 115200)
        
        port = self.get_parameter('port').value
        baudrate = self.get_parameter('baudrate').value
        
        # 尝试打开串口
        try:
            self.serial = serial.Serial(port, baudrate, timeout=1)
            self.get_logger().info(f"成功连接到编码器: {port}")
        except serial.SerialException as e:
            self.get_logger().error(f"无法连接到编码器: {str(e)}")
            return
        
        # 发布者
        self.encoder_pub = self.create_publisher(JointState, 'encoder_data', 10)
        
        # 定时器
        self.timer = self.create_timer(0.01, self.read_encoder)  # 100Hz
        
    def read_encoder(self):
        if hasattr(self, 'serial') and self.serial.is_open:
            try:
                # 读取编码器数据
                # 这里需要根据实际编码器的通信协议进行实现
                data = self.serial.readline().decode().strip()
                
                if data:
                    # 解析数据并发布
                    joint_state = JointState()
                    joint_state.header.stamp = self.get_clock().now().to_msg()
                    joint_state.name = ['encoder']
                    # 假设数据格式是 "position,velocity"
                    parts = data.split(',')
                    if len(parts) >= 2:
                        joint_state.position = [float(parts[0])]
                        joint_state.velocity = [float(parts[1])]
                        self.encoder_pub.publish(joint_state)
                        
            except Exception as e:
                self.get_logger().error(f"读取编码器数据错误: {str(e)}")
                
    def destroy_node(self):
        if hasattr(self, 'serial') and self.serial.is_open:
            self.serial.close()
        super().destroy_node()

def main(args=None):
    rclpy.init(args=args)
    node = HardwareEncoderInterface()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()