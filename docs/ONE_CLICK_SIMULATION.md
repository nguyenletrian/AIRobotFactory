# AIRobotFactory — One-run simulation environment

Install 64-bit Python 3.10–3.13 (3.12 recommended) and keep an Internet connection for initial Python package installation. On the future local-AI workstation, clone/unzip the repository and **double-click StartSimulation.cmd**.

This single entrypoint:
1. Creates isolated project .venv (no global pip installs or administrator rights).
2. Installs AIRobotFactory and MuJoCo if not ready, then runs all deterministic Python tests.
3. Generates or preserves the 2-link synthetic dataset and 3D-print calibration cube.
4. Runs an offline **six-revolute-joint** MuJoCo demo with **two sliding gripper fingers**, a virtual table and a sample block; saves a new JSON report.
5. Probes existing localhost Ollama models read-only at 127.0.0.1:11434 (absence is not an error).
6. Opens the existing 2D HTML viewer and official MuJoCo native 6-axis viewer.

For CI or no graphics: StartSimulation.cmd --headless. After first install, add --skip-install to verify a complete environment with no pip installation. The environment snapshot is artifacts/environment_report.json. Both .venv and artifacts are ignored by Git.

The script **does not install GPU drivers, Ollama, model weights, Windows system components, Bridge or equipment drivers**. When the future local-AI PC is ready and Ollama is installed separately, the same script detects existing local models. It never downloads or trains a model automatically.

Optional, explicit read-only proposal request from existing Ollama:

    .venv\Scripts\python.exe -m airobotfactory ai-status
    .venv\Scripts\python.exe -m airobotfactory ai-propose --model qwen2.5-coder:3b --text "Inspect the virtual part"

Only three strict simulation intent names are accepted: inspect_virtual_part, preview_joint_pose (six bounded angles) and preview_gripper (opening 0..1). All returned plans are JSON proposals; **none is executed**, including in MuJoCo. Remote API URLs and physical robot actions are not supported.

## What is actually simulated

The six-axis scene has approximate shapes/masses and deterministic scripted joint target poses. It does **not yet** prove IK, accurate dynamics for purchased motors, object grasping, collision-free task planning, pick-and-place, robot-to-printer control, machine assembly or physical safety. The browser 2D and MuJoCo 3D viewers are separate, not synchronized. Headless CI cannot prove graphical display on your machine.

## Failure behavior

Python unavailable, missing package wheels, install errors, failed deterministic tests or MuJoCo physics errors cause nonzero exit and no READY claim. Ollama absent is expected and nonfatal. To distinguish graphical/GPU issues from core simulation errors, use --headless; the HTML 2D viewer remains available without Python. No other project worker/CDP or AIBridge queue is modified; worker_enabled stays 0.

Virtual environment readiness is only stage one. Physical machine, AI training, GPU optimization and hardware safety review remain explicitly future work.
