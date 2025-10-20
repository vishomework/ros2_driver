# 基础镜像（ROS Humble 桌面完整版）
FROM osrf/ros:humble-desktop-full

# 用户参数
ARG USERNAME=yutou
ARG USER_UID=1000
ARG USER_GID=$USER_UID

# 安装系统依赖包（以root身份）
RUN apt-get update && \
    apt-get install -y \
        wget \
        git \
        ros-humble-nav2-bringup \
        ros-$ROS_DISTRO-joint-state-publisher-gui \
        ros-$ROS_DISTRO-robot-state-publisher \
        fish \
        gedit \
        ros-humble-joy \
        ros-humble-rqt-tf-tree \
        ros-humble-rmw-cyclonedds-cpp \
        ros-humble-foxglove-bridge \
        nautilus \
        curl \
        sudo \
        libpcap-dev \
        python3-pip && \
    pip3 install pyserial rosbags && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# 创建用户并配置权限
RUN groupadd --gid $USER_GID $USERNAME && \
    useradd --uid $USER_UID --gid $USER_GID -m $USERNAME && \
    echo "$USERNAME ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers && \
    usermod -a -G dialout $USERNAME

# 设置工作目录并克隆代码（以root身份，确保有权限）
WORKDIR /home/$USERNAME

RUN mkdir -p packages && \
    cd packages && \
    git clone https://github.com/wyq123-star/oradar_ros.git && \
    mkdir -p AIRY && \
    cd AIRY && \
    git clone https://github.com/RoboSense-LiDAR/rslidar_sdk.git && \
    git clone https://github.com/RoboSense-LiDAR/rslidar_msg.git

# 初始化并更新子模块（以root身份）
RUN cd /home/$USERNAME/packages/AIRY/rslidar_sdk && \
    git submodule init && \
    git submodule update

# 切换到非root用户
USER $USERNAME
WORKDIR /home/$USERNAME

# 设置环境变量
ENV ROS2_DISTRO=humble
ENV ROS2_SETUP_BASH="/opt/ros/humble/setup.bash"

# 配置bashrc
RUN echo "source $ROS2_SETUP_BASH" >> /home/$USERNAME/.bashrc && \
    echo "export ROS_LOCALHOST_ONLY=2" >> /home/$USERNAME/.bashrc

# --- 修复权限问题的关键步骤 ---
# 确保在用户切换后，修正工作目录的所有权
USER root
RUN chown -R $USERNAME:$USERNAME /home/$USERNAME/packages
USER $USERNAME
# --- 修复结束 ---

# 构建工作空间（使用非root用户）
WORKDIR /home/$USERNAME/packages
RUN bash -c "source /opt/ros/$ROS2_DISTRO/setup.bash && colcon build"

# ... 省略之后的代码 ...

# 将构建结果添加到bashrc
RUN echo "source /home/$USERNAME/packages/install/setup.bash" >> /home/$USERNAME/.bashrc

# 默认启动命令
CMD ["/bin/bash"]