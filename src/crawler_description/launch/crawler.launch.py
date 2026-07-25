import os
import xacro

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description():
    pkg_path = get_package_share_directory('crawler_description')
    xacro_file = os.path.join(pkg_path, 'urdf', 'crawler.urdf.xacro')
    rviz_config_file = os.path.join(pkg_path, 'rviz', 'default.rviz')  
    doc = xacro.process_file(xacro_file)

    robot_description = {
        'robot_description': doc.toxml()
    }

    return LaunchDescription([
        Node(
            package='robot_state_publisher',
            executable='robot_state_publisher',
            parameters=[robot_description],
        ),
        Node(
            package='joint_state_publisher_gui',
            executable='joint_state_publisher_gui',
        ),
        Node(
            package='rviz2',
            executable='rviz2',
            arguments=['-d', rviz_config_file],   
        ),
    ])