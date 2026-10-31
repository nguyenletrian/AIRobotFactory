# AIRobotFactory — Bridge/Architect guide

## Authority and scope
Read the current AIBrigde/GUIDE.md and relevant normative guide/ARCHITECT.md, guide/TASK_WORKFLOW.md, guide/WORKFLOW_STATE_MODEL.md, guide/RUNTIME.md and guide/GIT_RECOVERY.md **before** publishing tasks, editing authoritative workflow state or restarting a worker. The AIBrigde runtime is shared infrastructure; this repository owns the robotics application, models, experiments, TaskSource and goals.

Project identity: system_id=airobotfactory; project_id=AIRobotFactory; worker_id=AIRobotFactory-architect. Authoritative task source: this repo main/bridgeTask.json. Proposed Windows checkout: D:/AIRobotFactory. Project manifest: .aibridge/project.json. Provider CDP port is **unassigned** until Manager/profile/Edge ownership inspection proves a dedicated port. Never assume 9222/9223/9224/9225/9226 is available.

## Owner-approved goal (2026-10-31)
Long-term fully autonomous AI-directed fabrication of small devices (example: mini vacuum), after owner manually builds the initial robot. Near-term goal is software simulation, printable test geometry, local-model data and evaluation. Hardware is gated on available funding and measured evidence.

## Worker safety
- Initial bridgeTask.json uses worker_enabled=0 and tasks=[]. This is intentional, not an online-worker claim.
- Only after Manager confirms registration, exact worker ID, repo/branch/TaskSource binding, isolated CDP delivery and local worktree should Architect publish the first read-only verification:test_script task with full identity and permissions. Then enable dispatch deliberately.
- Do not guess a delivery port or borrow another worker's queue, browser session, TaskSource or Edge profile.
- Architect implements and tests. Bridge executes owner-machine code via registered allowed capabilities. Inspect exact result, record evidence and ACK **only after review**; do not duplicate execution or claim PASS from a pending task.
- Routine local Git sync must use the correct registered worker and terminal:repo_pull_ff capability, when verified, instead of requesting owner PowerShell commands.
- No task may buy parts, control motors, start printers, solder, heat, cut, energize power tools or move a physical robot in this stage.
- No silent secrets, destructive commands, force push, unverified live telemetry or invented successful training.

## Implementation quality
Python 3.10+; standard-library computational baseline, tests for every public function. Treat synthetic 2-link results as educational ground truth only. Keep physical interfaces fail-closed and separate from planner. Review bounded branches and CI, record exact status in bridgeGoals.json. Hardware integration requires explicit safety gates and human acceptance before autonomous operation.
