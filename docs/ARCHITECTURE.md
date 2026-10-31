# Architecture and evidence boundaries

Control plane: AIBridge Architect goal + authoritative AIRobotFactory bridgeGoals.json/bridgeTask.json. Runtime plane: separately registered worker, Windows machine. Simulation/data plane: pure offline Python package, never imports AIBridge transport internals.

Planned (not implemented):
- **Planner:** local model proposes design and task intents. Model output is untrusted, schema validated, non-executable until policy approval.
- **CAD:** parametric mechanisms, fixtures, tolerances, STL/STEP revision tracking.
- **Kinematics & physics:** analytical sanity checks then MuJoCo/URDF-based collision and dynamics; simulation results are not physical performance claims.
- **Manufacturing stations:** printer, camera QC, kitted parts, gripper, screwdriver, inspection and later electronics processes via allowlisted adapters.
- **Independent safety controller:** limit switches, interlocked enclosure, over-current limits, speed/force caps, external E-stop. The AI cannot disable these.
- **Experiment registry:** design revision, printer material/settings, measurement, simulated baseline, test evidence, failure reason and next change.

Implemented in this bootstrap: deterministic 2D two-link analytical model; 20 mm STL cube exporter; JSONL synthesis; CLI; unit tests. No motor/serial/ROS/USB/network integration.

Every test report must identify its evidence class: analytic/unit, GitHub CI, simulated physics, owner-machine test, or real physical test. Never promote one class to the next without corresponding evidence.
