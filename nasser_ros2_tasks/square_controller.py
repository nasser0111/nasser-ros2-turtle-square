"""ROS-independent timing logic for a four-sided square path."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from math import pi


class MotionPhase(str, Enum):
    MOVING = "moving"
    TURNING = "turning"
    FINISHED = "finished"


@dataclass(frozen=True)
class VelocityCommand:
    """Linear and angular velocity values for a ROS ``Twist`` message."""

    linear_x: float
    angular_z: float


class SquareController:
    """Alternate straight movement and 90-degree turns four times."""

    SIDE_COUNT = 4

    def __init__(
        self,
        side_length: float = 2.0,
        linear_speed: float = 1.0,
        angular_speed: float = pi / 4,
    ) -> None:
        if side_length <= 0:
            raise ValueError("side_length must be greater than zero")
        if linear_speed <= 0:
            raise ValueError("linear_speed must be greater than zero")
        if angular_speed <= 0:
            raise ValueError("angular_speed must be greater than zero")

        self.side_length = float(side_length)
        self.linear_speed = float(linear_speed)
        self.angular_speed = float(angular_speed)
        self.move_duration = self.side_length / self.linear_speed
        self.turn_duration = (pi / 2) / self.angular_speed
        self.reset()

    def reset(self) -> None:
        self.phase = MotionPhase.MOVING
        self.phase_elapsed = 0.0
        self.completed_sides = 0

    @property
    def finished(self) -> bool:
        return self.phase is MotionPhase.FINISHED

    @property
    def command(self) -> VelocityCommand:
        if self.phase is MotionPhase.MOVING:
            return VelocityCommand(self.linear_speed, 0.0)
        if self.phase is MotionPhase.TURNING:
            return VelocityCommand(0.0, self.angular_speed)
        return VelocityCommand(0.0, 0.0)

    def advance(self, elapsed_seconds: float) -> VelocityCommand:
        """Advance the state machine and return the next velocity command."""

        if elapsed_seconds < 0:
            raise ValueError("elapsed_seconds cannot be negative")

        remaining = float(elapsed_seconds)
        tolerance = 1e-12
        while remaining > tolerance and not self.finished:
            duration = (
                self.move_duration
                if self.phase is MotionPhase.MOVING
                else self.turn_duration
            )
            time_left = duration - self.phase_elapsed

            if remaining + tolerance < time_left:
                self.phase_elapsed += remaining
                remaining = 0.0
                continue

            remaining = max(0.0, remaining - time_left)
            self.phase_elapsed = 0.0
            if self.phase is MotionPhase.MOVING:
                self.phase = MotionPhase.TURNING
            else:
                self.completed_sides += 1
                self.phase = (
                    MotionPhase.FINISHED
                    if self.completed_sides == self.SIDE_COUNT
                    else MotionPhase.MOVING
                )

        return self.command

