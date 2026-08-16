"""Publish a custom phrase once per second on a ROS 2 topic."""

from __future__ import annotations

import rclpy
from rclpy.node import Node
from std_msgs.msg import String

from .phrase_content import PROJECT_MESSAGE


class PhrasePublisher(Node):
    """Publish a numbered custom message to ``nasser_phrase``."""

    def __init__(self) -> None:
        super().__init__("nasser_phrase_publisher")
        self.publisher = self.create_publisher(String, "nasser_phrase", 10)
        self.counter = 1
        self.timer = self.create_timer(1.0, self.publish_phrase)
        self.get_logger().info("Custom phrase publisher started.")

    def publish_phrase(self) -> None:
        message = String()
        message.data = f"{PROJECT_MESSAGE} | message {self.counter}"
        self.publisher.publish(message)
        self.get_logger().info(f'Published: "{message.data}"')
        self.counter += 1


def main(args: list[str] | None = None) -> None:
    rclpy.init(args=args)
    node = PhrasePublisher()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == "__main__":
    main()

