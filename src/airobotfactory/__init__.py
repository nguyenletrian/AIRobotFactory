"""Offline computation and geometry foundations for AIRobotFactory.

No device/motor commands are exposed in this package.
"""
from .kinematics import forward_kinematics, inverse_kinematics

__all__ = ["forward_kinematics", "inverse_kinematics"]
