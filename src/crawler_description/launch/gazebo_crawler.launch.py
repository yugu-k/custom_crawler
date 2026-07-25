import os
import xacro

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node


def generate_launch_description():
    desc_pkg = get_package_share_directory('crawler_description')
    gazebo_ros_pkg = get_package_share_directory('gazebo_ros')

    xacro_file = os.path.join(desc_pkg, 'urdf', 'crawler.urdf.xacro')
    rviz_config_file = os.path.join(desc_pkg, 'rviz', 'default.rviz')

    from launch.actions import SetEnvironmentVariable

    gazebo_model_path = SetEnvironmentVariable(
        name='GAZEBO_MODEL_PATH',
        value='/home/yugi/crawler_ws/install/crawler_description/share'
    )   

    doc = xacro.process_file(xacro_file)
    robot_description = {'robot_description': doc.toxml()}

    gazebo = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(gazebo_ros_pkg, 'launch', 'gazebo.launch.py')
        )
    )

    robot_state_publisher = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        parameters=[robot_description],
    )

    joint_state_publisher = Node(
        package='joint_state_publisher_gui',
        executable='joint_state_publisher_gui',
    )

    spawn_entity = Node(
        package='gazebo_ros',
        executable='spawn_entity.py',
        arguments=['-topic', 'robot_description', '-entity', 'crawler', '-z', '0.5'],
        output='screen',
    )

    rviz = Node(
        package='rviz2',
        executable='rviz2',
        arguments=['-d', rviz_config_file],
    )

    return LaunchDescription([
        gazebo_model_path,
        gazebo,
        robot_state_publisher,
        joint_state_publisher,
        spawn_entity,
        rviz,
    ])