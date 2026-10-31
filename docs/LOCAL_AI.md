# Local AI research path

The existing local code model can first assist with code generation, planning and explanations. It does **not** automatically possess robotic manipulation skills or safe physical control.

Stage A: generate deterministic analytics and simple synthetic examples:

    python -m airobotfactory dataset --output artifacts/workspace.jsonl

Rows describe a two-link **planar** arm at known joint angles. The dataset is a deterministic teacher for evaluating reasoning/data pipelines, **not** a real-robot demonstration or trained model.

Stage B: store dataset version, geometry, units, seed (when stochastic), generation script SHA, and provenance. Keep measured data separate from synthetic data. Split test sets by geometry/design and new configurations to prevent near-duplicate leakage.

Stage C: benchmark local model inference against the analytical baseline. Score Cartesian-position error in millimeters, unreachable-target detection and valid action/schema rate. Compare to an explicit no-AI baseline; training is optional, and cannot be claimed without a saved run, weights, environment, and held-out evaluation.

Stage D: when simulation is mature, create collision-aware task traces in a physics environment. Only after verified guardrails and practical robot access can teleoperation demonstrations support imitation learning.

Any model-suggested physical commands must pass deterministic validation, policy approval and independent device safety interlocks. No autonomous network ordering, payments or hazardous manufacturing in initial scope.
