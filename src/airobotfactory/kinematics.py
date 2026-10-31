"""Analytic 2-link planar arm model. Lengths are millimeters, angles degrees.

This is a teaching and dataset model, not a physical robot safety controller.
"""
import math


def _valid_lengths(link1_mm: float, link2_mm: float) -> tuple[float, float]:
    a, b = float(link1_mm), float(link2_mm)
    if not all(math.isfinite(v) and v > 0 for v in (a, b)):
        raise ValueError("Both link lengths must be positive finite millimeters")
    return a, b


def forward_kinematics(theta1_deg: float, theta2_deg: float,
                       link1_mm: float = 120.0, link2_mm: float = 90.0) -> tuple[float, float]:
    """Return (x_mm, y_mm) of the tool center in a 2D plane."""
    l1, l2 = _valid_lengths(link1_mm, link2_mm)
    a1, a2 = float(theta1_deg), float(theta2_deg)
    if not math.isfinite(a1) or not math.isfinite(a2):
        raise ValueError("Angles must be finite degrees")
    t1 = math.radians(a1)
    t12 = math.radians(a1 + a2)
    return l1 * math.cos(t1) + l2 * math.cos(t12), l1 * math.sin(t1) + l2 * math.sin(t12)


def inverse_kinematics(x_mm: float, y_mm: float,
                       link1_mm: float = 120.0, link2_mm: float = 90.0,
                       elbow_up: bool = False) -> tuple[float, float]:
    """Find joint angles for a reachable 2D target; raise for unreachable targets.

    Two possible elbow branches exist away from singular configurations.
    """
    l1, l2 = _valid_lengths(link1_mm, link2_mm)
    x, y = float(x_mm), float(y_mm)
    if not math.isfinite(x) or not math.isfinite(y):
        raise ValueError("Target coordinates must be finite millimeters")
    cos2 = (x * x + y * y - l1 * l1 - l2 * l2) / (2 * l1 * l2)
    if cos2 < -1 - 1e-10 or cos2 > 1 + 1e-10:
        raise ValueError("Target is outside the two-link workspace")
    cos2 = max(-1.0, min(1.0, cos2))
    t2 = math.acos(cos2) * (-1 if elbow_up else 1)
    t1 = math.atan2(y, x) - math.atan2(l2 * math.sin(t2), l1 + l2 * math.cos(t2))
    return math.degrees(t1), math.degrees(t2)
