"""Offline six-revolute-joint MuJoCo workcell. No physical device drivers."""
import json
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
MODEL_PATH = ROOT / "simulations" / "mujoco" / "workcell_6dof.xml"
JOINT_NAMES = ("j1_base_yaw", "j2_shoulder", "j3_elbow", "j4_roll", "j5_pitch", "j6_tool_yaw")


def _load():
    try:
        import mujoco
    except ImportError as exc:
        raise RuntimeError("MuJoCo unavailable: install airobotfactory[sim] first") from exc
    model = mujoco.MjModel.from_xml_path(str(MODEL_PATH))
    data = mujoco.MjData(model)
    return mujoco, model, data


def run_demo(steps=700):
    """Run prescribed target angles, return numerically checked SIMULATION evidence."""
    if not isinstance(steps, int) or isinstance(steps, bool) or not 50 <= steps <= 10000:
        raise ValueError("steps must be an integer between 50 and 10000")
    mj, model, data = _load()
    if model.nu != 8 or model.njnt != 9:
        raise RuntimeError(f"Unexpected model joints/actuators: {model.njnt}/{model.nu}")
    mj.mj_forward(model, data)
    trajectories = [(-20, -35, 55, 0, -25, 0),
                    (18, -28, 68, 0, -35, 20),
                    (0, -20, 38, 0, -15, 0)]
    for step in range(steps):
        index = min(2, step * 3 // steps)
        for j, degrees in enumerate(trajectories[index]):
            data.ctrl[j] = math.radians(degrees)
        data.ctrl[6] = data.ctrl[7] = 0.008 if index == 1 else 0.0
        mj.mj_step(model, data)
        if not all(math.isfinite(float(x)) for x in data.qpos) or not all(math.isfinite(float(x)) for x in data.qvel):
            raise RuntimeError("Non-finite state; simulator result invalid")
    mj.mj_forward(model, data)
    site_id = mj.mj_name2id(model, mj.mjtObj.mjOBJ_SITE, "tool_center")
    tcp = [float(v) for v in data.site_xpos[site_id]]
    angles = {}
    for name in JOINT_NAMES:
        joint_id = mj.mj_name2id(model, mj.mjtObj.mjOBJ_JOINT, name)
        if joint_id < 0:
            raise RuntimeError(f"Missing virtual joint {name}")
        angles[name] = round(math.degrees(float(data.qpos[model.jnt_qposadr[joint_id]])), 3)
    return {
        "evidence_class": "mujoco_headless_simulation", "model": MODEL_PATH.name,
        "steps": steps, "simulated_time_s": round(float(data.time), 4),
        "arm_revolute_joints": 6, "gripper_prismatic_joints": 2,
        "actuators": model.nu, "tool_center_xyz_m": [round(v, 5) for v in tcp],
        "final_arm_degrees": angles,
        "claim": "scripted pose sequence only; no verified grasp or physical robot",
    }


def save_demo(path, steps=700):
    data = run_demo(steps)
    target = Path(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    with target.open("x", encoding="utf-8") as file:
        json.dump(data, file, indent=2, sort_keys=True)
        file.write("\n")
    return data
