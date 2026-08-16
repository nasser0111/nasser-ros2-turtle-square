"""Launch the custom phrase publisher and subscriber together."""

from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description() -> LaunchDescription:
    return LaunchDescription(
        [
            Node(
                package="nasser_ros2_tasks",
                executable="phrase_publisher",
                name="nasser_phrase_publisher",
                output="screen",
            ),
            Node(
                package="nasser_ros2_tasks",
                executable="phrase_subscriber",
                name="nasser_phrase_subscriber",
                output="screen",
            ),
        ]
    )

