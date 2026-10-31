"""Generate a simple, closed calibration-cube ASCII STL in millimeters."""
import math
from pathlib import Path


def calibration_cube_stl(size_mm: float = 20.0) -> str:
    """Return 12 consistently outward-facing triangles for a cube at z >= 0."""
    side = float(size_mm)
    if not math.isfinite(side) or side <= 0:
        raise ValueError("Cube size must be positive finite millimeters")
    p = ((0, 0, 0), (side, 0, 0), (side, side, 0), (0, side, 0),
         (0, 0, side), (side, 0, side), (side, side, side), (0, side, side))
    faces = ((0, 3, 2, 1), (4, 5, 6, 7), (0, 1, 5, 4),
             (1, 2, 6, 5), (2, 3, 7, 6), (3, 0, 4, 7))
    result = ["solid calibration_cube_mm"]
    for i, j, k, m in faces:
        for a, b, c in ((i, j, k), (i, k, m)):
            v0, v1, v2 = p[a], p[b], p[c]
            e1 = [v1[n] - v0[n] for n in range(3)]
            e2 = [v2[n] - v0[n] for n in range(3)]
            nvec = (e1[1] * e2[2] - e1[2] * e2[1],
                    e1[2] * e2[0] - e1[0] * e2[2],
                    e1[0] * e2[1] - e1[1] * e2[0])
            length = math.sqrt(sum(v * v for v in nvec))
            normal = [v / length for v in nvec]
            result.append("  facet normal " + " ".join(f"{v:.9g}" for v in normal))
            result.append("    outer loop")
            for vert in (v0, v1, v2):
                result.append("      vertex " + " ".join(f"{v:.9g}" for v in vert))
            result.extend(("    endloop", "  endfacet"))
    result.append("endsolid calibration_cube_mm")
    return "\n".join(result) + "\n"


def export_coupon_stl(path: str | Path, size_mm: float = 20.0) -> Path:
    """Create a new STL file; never overwrite an existing experiment."""
    data = calibration_cube_stl(size_mm)
    destination = Path(path)
    destination.parent.mkdir(parents=True, exist_ok=True)
    with destination.open("x", encoding="utf-8", newline="\n") as handle:
        handle.write(data)
    return destination
