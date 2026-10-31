"""Regression checks for the 2D analytical teaching model."""
import math
import unittest

from airobotfactory.kinematics import forward_kinematics, inverse_kinematics


class TestKinematics(unittest.TestCase):
    def test_straight_reach(self):
        x, y = forward_kinematics(0, 0, 120, 90)
        self.assertAlmostEqual(x, 210)
        self.assertAlmostEqual(y, 0)

    def test_right_angle(self):
        x, y = forward_kinematics(0, 90, 120, 90)
        self.assertAlmostEqual(x, 120)
        self.assertAlmostEqual(y, 90)

    def test_inverse_both_branches_round_trip(self):
        x, y = forward_kinematics(45, -60)
        for elbow_up in (False, True):
            a1, a2 = inverse_kinematics(x, y, elbow_up=elbow_up)
            rx, ry = forward_kinematics(a1, a2)
            self.assertAlmostEqual(rx, x, places=7)
            self.assertAlmostEqual(ry, y, places=7)

    def test_unreachable_outer_and_inner(self):
        with self.assertRaises(ValueError):
            inverse_kinematics(300, 0)
        with self.assertRaises(ValueError):
            inverse_kinematics(0, 0, 120, 90)

    def test_invalid_inputs(self):
        for a, b in ((0, 90), (90, -1), (math.inf, 2)):
            with self.assertRaises(ValueError):
                forward_kinematics(0, 0, a, b)
        with self.assertRaises(ValueError):
            inverse_kinematics(math.nan, 10)
        with self.assertRaises(ValueError):
            forward_kinematics(math.inf, 0)


if __name__ == "__main__":
    unittest.main()
