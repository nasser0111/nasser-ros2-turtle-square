"""Receive and display the custom phrase published by this package."""

from __future__ import annotations

import rclpy
from rclpy.node import Node
from std_msgs.msg import String


class PhraseSubscriber(Node):
    """Subscribe to ``nasser_phrase`` and log every received message."""

    def __init__(self) -> None:
        super().__init__("nasser_phrase_subscriber")
        self.subscription = self.create_subscription(
            String,
            "nasser_phrase",
            self.receive_phrase,
            10,
        )
        self.get_logger().info("Custom phrase subscriber is waiting for data.")

    def receive_phrase(self, message: String) -> None:
        self.get_logger().info(f'Received: "{message.data}"')


def main(args: list[str] | None = None) -> None:
    rclpy.init(args=args)
    node = PhraseSubscriber()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == "__main__":
    main()

