# Safety boundaries

Currently safe-to-run baseline: analytic computation and offline generation of a JSONL dataset or ASCII STL. No hardware or GUI side effects beyond explicit output file creation.

Before any physical actuation:
- Separate AI planner from deterministic motion controller and hardwired/independent safety layer.
- Document workspace limits, torque/load budget, pinch points, fixtures, accessible power-disconnect and E-stop; enclosure and interlocks when needed.
- Start with no-load/read-only telemetry, then low-speed constrained movement and gradual calibrated load. Validate collision and emergency stop with a competent on-site operator.
- Enforce power/current/thermal monitoring. Treat battery pack assembly, powered cutting/drilling, hot tools and soldering as separate high-risk stations with their own qualified procedures and safeguards.
- Disallow unsupervised operations that the station cannot reliably detect, abort and recover.
- Never treat simulation PASS or AI confidence as physical safety approval.

Future full autonomy is conditional on supported devices and validated safeguards, not unrestricted operation.
