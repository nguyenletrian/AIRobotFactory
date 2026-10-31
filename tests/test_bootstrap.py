import importlib.util
from pathlib import Path
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("airobot_bootstrap", ROOT / "scripts/bootstrap.py")
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


class BootstrapTests(unittest.TestCase):
    def test_scoped_to_repo(self):
        self.assertEqual(MODULE.ROOT, ROOT)
        self.assertEqual(MODULE.STATUS.name, "environment_report.json")
        self.assertTrue((ROOT / "StartSimulation.cmd").is_file())

    def test_headless_no_gui(self):
        with patch.object(MODULE, "prepare"), patch.object(MODULE, "create_evidence"), patch.object(MODULE, "launch") as launch:
            self.assertEqual(MODULE.main(["--headless", "--skip-install"]), 0)
            launch.assert_not_called()

    def test_failure_is_not_ready(self):
        with patch.object(MODULE, "prepare", side_effect=RuntimeError("missing dependency")):
            self.assertEqual(MODULE.main(["--headless"]), 1)


if __name__ == "__main__":
    unittest.main()
