import unittest
from unittest.mock import patch
from airobotfactory.local_ai import validate_plan, detect_ollama, ask_ollama


class LocalPlanTests(unittest.TestCase):
    def test_inspect(self):
        result = validate_plan({"task": "inspect_virtual_part", "parameters": {}})
        self.assertEqual(result["mode"], "simulation_preview_only")

    def test_virtual_pose_and_gripper(self):
        self.assertEqual(validate_plan({"task": "preview_joint_pose", "parameters":
                                       {"degrees": [0, -35, 50, 0, 0, 5]}})["task"], "preview_joint_pose")
        self.assertEqual(validate_plan({"task": "preview_gripper", "parameters":
                                       {"opening": .5}})["task"], "preview_gripper")

    def test_reject_untrusted_and_out_of_bounds(self):
        proposals = [
            {"task": "run_shell", "parameters": {}},
            {"task": "preview_gripper", "parameters": {"opening": 2}},
            {"task": "preview_joint_pose", "parameters": {"degrees": [0, 0, 0, 0, 0, 180]}},
            {"task": "preview_joint_pose", "parameters": {"degrees": [True, 0, 0, 0, 0, 0]}},
            {"task": "inspect_virtual_part", "parameters": {"url": "x"}},
            {"task": "inspect_virtual_part", "parameters": {}, "execute": True},
        ]
        for item in proposals:
            with self.subTest(proposal=item), self.assertRaises(ValueError):
                validate_plan(item)

    def test_probe_absent_service(self):
        with patch("urllib.request.urlopen", side_effect=OSError("offline")):
            self.assertEqual(detect_ollama(), {"reachable": False, "models": []})

    def test_reject_untrusted_model_url(self):
        with self.assertRaises(ValueError):
            ask_ollama("http://evil", "inspect")


if __name__ == "__main__":
    unittest.main()
