# 基础镜像（ROS Humble 桌面完整版）
FROM osrf/ros:humble-desktop-full

# 用户参数
ARG USERNAME=yutou
ARG USER_UID=1000
ARG USER_GID=$USER_UID


RUN echo "deb [trusted=yes arch=amd64] http://deb.repo.autolabor.com.cn jammy main" | sudo tee /etc/apt/sources.list.d/autolabor.list && \
    sudo apt-get update && \
    sudo apt-get install -y ros-noetic-autolabor

RUN apt-get update && \
    apt-get install -y \
        wget \
        ros-humble-nav2-bringup \
        ros-$ROS_DISTRO-joint-state-publisher-gui \
        ros-$ROS_DISTRO-robot-state-publisher \
        fish \
        gedit \
        ros-humble-rqt-tf-tree \
        ros-humble-rmw-cyclonedds-cpp \
        ros-humble-foxglove-bridge \
        nautilus \
        curl \
        sudo \
        libpcap-dev \
        pip && \
        pip install pyserial \
        rosbags && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# ------------------------------
# 创建用户并配置权限
# ------------------------------
RUN groupadd --gid $USER_GID $USERNAME && \
    useradd --uid $USER_UID --gid $USER_GID -m $USERNAME && \
    echo "$USERNAME ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers && \
    usermod -a -G dialout $USERNAME
    # usermod -a -G dialout $USERNAME
# ------------------------------
# 安装 Fisher 和 bass（在用户目录下）
# ------------------------------
# 切换到用户目录安装
USER $USERNAME
WORKDIR /home/$USERNAME

# # 创建 Fish 配置目录
# RUN mkdir -p .config/fish/functions && \
#     curl -sL https://git.io/fisher > .config/fish/functions/fisher.fish
    
# # 安装 bass 插件
# RUN /usr/bin/fish -c "fisher install edc/bass"

ENV ROS2_DISTRO=humble
ENV ROS1_DISTRO=noetic
ENV ROS2_SETUP_BASH="/opt/ros/humble/setup.bash"
ENV ROS1_SETUP_BASH="/opt/ros/noetic/setup.bash"
# ENV LD_LIBRARY_PATH=/usr/local/lib:$LD_LIBRARY_PATH
ENV ROBOSENSE_AIRY_BASH="~/ros2_ws/packages/AIRY/install/setup.bash"
ENV ROS1_BRIDGE_BASH="~/ros2_ws/packages/ros_bridge_ws/install/setup.bash"

# # 为bash用户自动加载ROS环境
RUN echo "source $ROS2_SETUP_BASH" >> /home/$USERNAME/.bashrc
    # echo "source $ROS1_SETUP_BASH" >> /home/$USERNAME/.bashrc && \
    # echo "source $ROBOSENSE_AIRY_BASH" >> /home/$USERNAME/.bashrc && \
    # echo "source $ROS1_BRIDGE_BASH" >> /home/$USERNAME/.bashrc 
#     echo "source /home/yutou/ros2_ws/install/setup.bash" >> /home/$USERNAME/.bashrc && \
#     echo "source /home/yutou/packages/lidar_ros_ws/install/setup.bash" >> /home/$USERNAME/.bashrc && \
#     echo "source /home/yutou/packages/ws_livox/install/local_setup.bash" >> /home/$USERNAME/.bashrc

# # # 为fish用户配置ROS环境（可选）
# RUN echo 'bass source /opt/ros/humble/setup.bash' >> /home/$USERNAME/.config/fish/config.fish && \
#     echo 'bass source ~/ros2_ws/install/setup.bash' >> /home/$USERNAME/.config/fish/config.fish && \
#     echo 'source ~/ros2_ws/.config/fish/completions/ros2.fish' >> /home/$USERNAME/.config/fish/config.fish


WORKDIR /home/$USERNAME

# 默认启动命令
CMD ["/usr/bin/bash"]

        # ros-humble-gazebo-ros-pkgs \
        # ros-humble-cartographer \
        # ros-humble-cartographer-ros \
        # ros-noetic-ros-core  \
        # ros-humble-ros1-bridge \
        # gazebo \
        # libgazebo-dev \