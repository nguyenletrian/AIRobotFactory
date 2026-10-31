# AIRobotFactory

A simulation-first, locally operated research project toward an AI-coordinated fabrication workshop.

## Goal

The owner initially builds and configures the first robot. Long term, the system aims to design, fabricate, assemble, inspect and iteratively improve new devices (for example a mini vacuum cleaner) with no manual steps inside a **validated, bounded workcell**. This is a staged research objective, **not an existing autonomous capability**.

## First stage: no hardware required

- Deterministic 2-link planar forward/inverse kinematics (teaching model, **not** a six-axis industrial-arm model).
- Export a small synthetic workspace JSONL dataset for evaluation of future local AI.
- Generate a 20 mm calibration-cube ASCII STL as the first controlled 3D-print experiment.
- Run automated Python unit tests on Windows and Linux.
- Preserve the AIBridge worker/goal contract without assuming the worker is registered or online.

### Quick start (Python 3.10+)

    python -m pip install -e .
    python -m unittest discover -s tests -v
    python -m airobotfactory dataset --output artifacts/workspace.jsonl
    python -m airobotfactory coupon --output artifacts/cube20.stl

Neither command controls a motor, network service, printer or external device. The commands create files only at explicitly supplied paths, refusing to overwrite existing output.

## One-click future-machine setup

**Windows:** double-click `StartSimulation.cmd` to create isolated Python `.venv`, install MuJoCo, run full tests, generate offline evidence, probe optional existing local Ollama and open the 2D browser + 6-axis native MuJoCo scene. Headless CI: `python scripts/bootstrap.py --headless`. See [one-run environment guide](docs/ONE_CLICK_SIMULATION.md).

This is a **simulation-only** environment bootstrap. It does not install models/GPU drivers, train AI, register AIBridge workers or control motors; a passing simulator is not proof of automatic assembly.

## Visual experiments

On Windows, open `OpenVisualizer.cmd` (or open `visualizer/index.html` in a browser) for an **offline two-link interactive arm**: joint sliders, inverse-kinematics targets, an illustrative obstacle and demo trajectory. Optional MuJoCo 3D teaching scene: `simulations/mujoco/two_link.xml`. See `docs/VISUAL_TESTING.md` for usage and evidence limits. No physical device control is enabled.

## Documentation

- docs/ROADMAP.md — gated phases from virtual models through physical workshop.
- docs/ARCHITECTURE.md — component boundaries and evidence contracts.
- docs/PRINT_EXPERIMENTS.md — metrology and 3D-print trial protocol.
- docs/LOCAL_AI.md — local model training/evaluation plan, **not** claimed training results.
- docs/SAFETY.md — hardware authorization and physical safeguards.
- docs/BRIDGE_ONBOARDING.md and AIBRIDGE_GUIDE.md — AIBridge onboarding.

## Status

Bootstrap implementation. No AIBridge worker registration, physical experiment, robot control, local model training or owner-machine test has been verified.
