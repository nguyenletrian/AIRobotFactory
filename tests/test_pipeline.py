"""Offline dataset and STL geometry checks: no devices accessed."""
import json
from pathlib import Path
import tempfile
import unittest

from airobotfactory.cad import calibration_cube_stl, export_coupon_stl
from airobotfactory.simulation import export_workspace_jsonl, sample_workspace


class TestPipeline(unittest.TestCase):
    def test_workspace_grid_deterministic(self):
        rows = sample_workspace()
        self.assertEqual(len(rows), 25)
        self.assertEqual(rows, sample_workspace())
        self.assertEqual(rows[12]["joint1_deg"], 0)
        self.assertEqual(rows[12]["joint2_deg"], 0)
        self.assertEqual(rows[12]["tcp_x_mm"], 210)
        self.assertEqual(rows[12]["source"], "analytic_2link_planar_v0")

    def test_jsonl_export_and_no_overwrite(self):
        with tempfile.TemporaryDirectory() as folder:
            target = Path(folder) / "data.jsonl"
            self.assertEqual(export_workspace_jsonl(target), 25)
            lines = target.read_text(encoding="utf-8").splitlines()
            self.assertEqual(len(lines), 25)
            self.assertEqual(json.loads(lines[12])["tcp_x_mm"], 210)
            with self.assertRaises(FileExistsError):
                export_workspace_jsonl(target)

    def test_cube_normals_and_bounds(self):
        stl = calibration_cube_stl(20)
        self.assertEqual(stl.count("facet normal"), 12)
        self.assertEqual(stl.count("endfacet"), 12)
        verts = [list(map(float, line.split()[1:])) for line in stl.splitlines()
                 if line.strip().startswith("vertex ")]
        self.assertEqual(len(verts), 36)
        for axis in range(3):
            self.assertEqual(min(v[axis] for v in verts), 0)
            self.assertEqual(max(v[axis] for v in verts), 20)

    def test_cube_export_no_overwrite(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "coupon.stl"
            export_coupon_stl(path)
            self.assertTrue(path.read_text(encoding="utf-8").startswith("solid "))
            with self.assertRaises(FileExistsError):
                export_coupon_stl(path)

    def test_reject_invalid_geometry(self):
        with self.assertRaises(ValueError):
            calibration_cube_stl(0)
        with self.assertRaises(ValueError):
            sample_workspace(link1_mm=-5)


if __name__ == "__main__":
    unittest.main()
