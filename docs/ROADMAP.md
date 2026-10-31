# Roadmap: simulation-first AI robot factory

The ambition is a fully automated fabrication cycle after the owner assembles the first robot. It is not a claim that one robot can fabricate arbitrary machines or manufacture purchased components from raw materials.

| Phase | Deliverable | Gate |
| --- | --- | --- |
| 0 — Computational baseline | 2-link FK/IK, offline dataset, CI | Deterministic tests on Windows and Linux |
| 1 — Printable experiments | Size coupons, tolerances, candidate gripper/link fixtures | Real prints measured; failures recorded; no invented precision |
| 2 — Local AI research | Dataset registry, evaluation baseline, optional local fine-tuning | Reproducibility, held-out variants, safety audit |
| 3 — Virtual workcell | Robot description (URDF/MJCF), 6-DOF kinematics, collisions, tool changer, assembly fixtures | Verified simulation tasks, collision-free paths, independently checked dynamics |
| 4 — First physical robot | Owner builds it once; encoders, position limits, isolation, safe-stop, guards | Budget and staged physical acceptance; read-only telemetry first |
| 5 — Assisted fabrication | 3D printer and a bounded gripper/screwdriver workcell | Closed-loop inspection, recoverable failure, controlled tool station |
| 6 — Autonomous product pilot | Design + fabricate + assemble + test a low-voltage mini vacuum | No manual step within a fully provisioned workcell; electrical and thermal safety validation |
| 7 — Expansion | More stations, electronics assembly, robot upgrades | Each new station independently validated, funding approved |

**Autonomy definition:** automation is confined to supplied stock, prequalified components, known manufacturing capabilities, and a guarded workcell. Shipping, restocking, sourcing, payment and hazardous fabrication are not silently assumed. A reproducible demo must record every external/manual intervention.

Low-cost-first rule: do not buy expensive actuators to compensate for unproven software. Start with simulation; validate dimensional coupons when printer access exists; buy high-torque hardware only after mechanical load/stiffness/budget calculations.
