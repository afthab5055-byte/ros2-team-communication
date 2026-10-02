from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description():
    return LaunchDescription([
        Node(
            package='ros_team',
            executable='team_gui',
            name='team_gui',
            output='screen'
        ),
    ])