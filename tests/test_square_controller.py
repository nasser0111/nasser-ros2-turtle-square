"""Unit tests for the ROS-independent square state machine."""

from math import pi
import unittest

from nasser_ros2_tasks.square_controller import MotionPhase, SquareController


class SquareControllerTests(unittest.TestCase):
    def setUp(self) -> None:
        self.controller = SquareController(
            side_length=2.0,
            linear_speed=1.0,
            angular_speed=pi / 4,
        )

    def test_initial_command_moves_straight(self) -> None:
        command = self.controller.command
        self.assertEqual(command.linear_x, 1.0)
        self.assertEqual(command.angular_z, 0.0)
        self.assertEqual(self.controller.phase, MotionPhase.MOVING)

    def test_one_side_is_followed_by_a_left_turn(self) -> None:
        command = self.controller.advance(self.controller.move_duration)
        self.assertEqual(self.controller.phase, MotionPhase.TURNING)
        self.assertEqual(command.linear_x, 0.0)
        self.assertAlmostEqual(command.angular_z, pi / 4)

    def test_one_turn_completes_one_side(self) -> None:
        self.controller.advance(self.controller.move_duration)
        command = self.controller.advance(self.controller.turn_duration)
        self.assertEqual(self.controller.completed_sides, 1)
        self.assertEqual(self.controller.phase, MotionPhase.MOVING)
        self.assertEqual(command.linear_x, 1.0)

    def test_four_cycles_finish_with_zero_velocity(self) -> None:
        cycle_duration = (
            self.controller.move_duration + self.controller.turn_duration
        )
        command = self.controller.advance(4 * cycle_duration)
        self.assertTrue(self.controller.finished)
        self.assertEqual(self.controller.completed_sides, 4)
        self.assertEqual(command.linear_x, 0.0)
        self.assertEqual(command.angular_z, 0.0)

    def test_small_time_steps_complete_the_same_square(self) -> None:
        for _ in range(320):
            self.controller.advance(0.05)
        self.assertTrue(self.controller.finished)
        self.assertEqual(self.controller.completed_sides, 4)

    def test_reset_returns_to_first_side(self) -> None:
        self.controller.advance(16.0)
        self.controller.reset()
        self.assertFalse(self.controller.finished)
        self.assertEqual(self.controller.completed_sides, 0)
        self.assertEqual(self.controller.phase, MotionPhase.MOVING)

    def test_invalid_values_are_rejected(self) -> None:
        with self.assertRaises(ValueError):
            SquareController(side_length=0.0)
        with self.assertRaises(ValueError):
            SquareController(linear_speed=-1.0)
        with self.assertRaises(ValueError):
            SquareController(angular_speed=0.0)
        with self.assertRaises(ValueError):
            self.controller.advance(-0.1)


if __name__ == "__main__":
    unittest.main()

