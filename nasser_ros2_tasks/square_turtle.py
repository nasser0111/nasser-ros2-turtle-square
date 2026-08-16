"""Drive the default turtlesim turtle around one square."""

from __future__ import annotations

from math import pi

import rclpy
from geometry_msgs.msg import Twist
from rclpy.node import Node

from .square_controller import SquareController


class SquareTurtle(Node):
    """Publish velocity commands for four sides and four 90-degree turns."""

    TIMER_PERIOD = 0.05

    def __init__(self) -> None:
        super().__init__("nasser_square_turtle")
        self.declare_parameter("side_length", 2.0)
        self.declare_parameter("linear_speed", 1.0)
        self.declare_parameter("angular_speed", pi / 4)

        self.controller = SquareController(
            side_length=float(self.get_parameter("side_length").value),
            linear_speed=float(self.get_parameter("linear_speed").value),
            angular_speed=float(self.get_parameter("angular_speed").value),
        )
        self.velocity_publisher = self.create_publisher(
            Twist,
            "/turtle1/cmd_vel",
            10,
        )
        self.timer = self.create_timer(self.TIMER_PERIOD, self.update_motion)
        self.get_logger().info(
            "Drawing one square with four straight sides and four 90-degree turns."
        )

    def update_motion(self) -> None:
        command = self.controller.advance(self.TIMER_PERIOD)
        twist = Twist()
        twist.linear.x = command.linear_x
        twist.angular.z = command.angular_z
        self.velocity_publisher.publish(twist)

        if self.controller.finished:
            self.timer.cancel()
            self.get_logger().info(
                "Square complete. The turtle has stopped after four sides."
            )


def main(args: list[str] | None = None) -> None:
    rclpy.init(args=args)
    node = SquareTurtle()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        stop = Twist()
        node.velocity_publisher.publish(stop)
        node.destroy_node()
        rclpy.shutdown()


if __name__ == "__main__":
    main()

