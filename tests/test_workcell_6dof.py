"""MuJoCo model smoke on supported platforms; physics gated on installed extra."""
import math
import unittest
import xml.etree.ElementTree as ET
from airobotfactory.workcell import MODEL_PATH, JOINT_NAMES, run_demo


class WorkcellStaticTests(unittest.TestCase):
    def test_xml_structure(self):
        root = ET.parse(MODEL_PATH).getroot()
        self.assertEqual(root.tag, "mujoco")
        joints = [j.attrib["name"] for j in root.findall(".//joint") if "name" in j.attrib]
        self.assertEqual(joints[:6], list(JOINT_NAMES))
        self.assertEqual(len(joints), 8)
        self.assertEqual(len(root.findall("./actuator/position")), 8)
        self.assertIsNotNone(root.find('.//site[@name="tool_center"]'))

    def test_step_bounds(self):
        for value in (0, True, 10001):
            with self.assertRaises(ValueError):
                run_demo(value)


try:
    import mujoco
except ImportError:
    mujoco = None


@unittest.skipUnless(mujoco is not None, "Install simulation extra to validate physics")
class WorkcellPhysicsTests(unittest.TestCase):
    def test_six_axis_load_and_run(self):
        result = run_demo(700)
        self.assertEqual(result["arm_revolute_joints"], 6)
        self.assertEqual(result["gripper_prismatic_joints"], 2)
        self.assertEqual(result["actuators"], 8)
        self.assertEqual(len(result["final_arm_degrees"]), 6)
        self.assertTrue(all(math.isfinite(x) for x in result["tool_center_xyz_m"]))


if __name__ == "__main__":
    unittest.main()
