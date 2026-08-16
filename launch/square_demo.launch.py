"""Start turtlesim and then draw one square automatically."""

from launch import LaunchDescription
from launch.actions import TimerAction
from launch_ros.actions import Node


def generate_launch_description() -> LaunchDescription:
    turtlesim = Node(
        package="turtlesim",
        executable="turtlesim_node",
        name="turtlesim",
        output="screen",
    )
    square_controller = TimerAction(
        period=1.0,
        actions=[
            Node(
                package="nasser_ros2_tasks",
                executable="square_turtle",
                name="nasser_square_turtle",
                output="screen",
                parameters=[
                    {
                        "side_length": 2.0,
                        "linear_speed": 1.0,
                        "angular_speed": 0.7853981633974483,
                    }
                ],
            )
        ],
    )
    return LaunchDescription([turtlesim, square_controller])

