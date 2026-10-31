"""Static structural checks; not browser rendering or MuJoCo dynamics."""
from pathlib import Path
import unittest
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]


class VisualAssetsTests(unittest.TestCase):
    def test_browser_assets_present_without_external_scripts(self):
        html = (ROOT / "visualizer/index.html").read_text(encoding="utf-8")
        self.assertIn('src="kinematics.js"', html)
        self.assertIn('id="view"', html)
        self.assertIn('id="go"', html)
        self.assertNotIn('<script src="http', html)
        self.assertTrue((ROOT / "visualizer/kinematics.js").is_file())

    def test_mujoco_structure(self):
        tree = ET.parse(ROOT / "simulations/mujoco/two_link.xml")
        self.assertEqual(tree.getroot().tag, "mujoco")
        self.assertEqual(len(tree.findall(".//joint")), 2)
        self.assertEqual(len(tree.findall("./actuator/position")), 2)
        self.assertIsNotNone(tree.find(".//site[@name='tcp']"))


if __name__ == "__main__":
    unittest.main()
