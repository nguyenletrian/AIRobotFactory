"""Create provenance-labeled synthetic data from the two-link analytic model."""
import json
from pathlib import Path

from .kinematics import forward_kinematics

GRID_DEG = (-90, -45, 0, 45, 90)


def sample_workspace(link1_mm: float = 120.0, link2_mm: float = 90.0) -> list[dict]:
    """Deterministic 25-sample grid, not real robot observations."""
    rows = []
    for a1 in GRID_DEG:
        for a2 in GRID_DEG:
            x, y = forward_kinematics(a1, a2, link1_mm, link2_mm)
            rows.append({
                "source": "analytic_2link_planar_v0",
                "link1_mm": float(link1_mm),
                "link2_mm": float(link2_mm),
                "joint1_deg": a1,
                "joint2_deg": a2,
                "tcp_x_mm": round(x, 6),
                "tcp_y_mm": round(y, 6),
            })
    return rows


def export_workspace_jsonl(path: str | Path, link1_mm: float = 120.0,
                           link2_mm: float = 90.0) -> int:
    """Write dataset exclusively to a new file, refusing to overwrite."""
    rows = sample_workspace(link1_mm, link2_mm)
    destination = Path(path)
    destination.parent.mkdir(parents=True, exist_ok=True)
    with destination.open("x", encoding="utf-8", newline="\n") as handle:
        for row in rows:
            handle.write(json.dumps(row, sort_keys=True, allow_nan=False) + "\n")
    return len(rows)
