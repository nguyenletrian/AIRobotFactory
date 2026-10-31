"""Optional full MuJoCo runtime compile/step gate; no GUI or hardware."""
from pathlib import Path
import math
import unittest

try:
    import mujoco
except ImportError:
    mujoco = None

SCENE = Path(__file__).resolve().parents[1] / "simulations/mujoco/two_link.xml"


@unittest.skipUnless(mujoco is not None, "Install optional mujoco to validate dynamics")
class MuJoCoSceneTests(unittest.TestCase):
    def test_compiles_and_steps_without_invalid_state(self):
        model = mujoco.MjModel.from_xml_path(str(SCENE))
        self.assertEqual(model.nq, 2)
        self.assertEqual(model.nu, 2)
        data = mujoco.MjData(model)
        for _ in range(500):
            mujoco.mj_step(model, data)
        self.assertTrue(all(math.isfinite(float(x)) for x in data.qpos))
        self.assertTrue(all(math.isfinite(float(x)) for x in data.qvel))
        self.assertEqual(model.nsite, 1)


if __name__ == "__main__":
    unittest.main()
