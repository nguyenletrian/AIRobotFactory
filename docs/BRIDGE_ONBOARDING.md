# Dedicated AIBridge worker onboarding (not yet performed)

Manifest: .aibridge/project.json.
Exact project binding:
- system_id: airobotfactory
- project_id: AIRobotFactory
- worker_id: AIRobotFactory-architect
- repo: https://github.com/nguyenletrian/AIRobotFactory.git
- branch: main
- proposed checkout: D:/AIRobotFactory
- authoritative TaskSource: main/bridgeTask.json
- execution target: bridge-runtime loopback port 0, as established by Manager
- browser/CDP delivery target: **TBD by verified Manager/Edge ownership**, never copied from another worker

Required preflight owned by AIBridge Manager:
1. Confirm checkout and current Git commit, no unexpected dirty files, correct repo origin and branch.
2. Register a distinct worker profile and task-source identity; verify it against Manager registry and worker lease.
3. Allocate/check isolated Edge profile and free CDP port; verify browser ownership and current ChatGPT conversation. Do not attach to another worker.
4. Confirm WORKER_LISTENING TaskSource and worker identity by live runtime evidence. Do not infer online status from a manifest.
5. Architect publishes a unique read-only verification:test_script task with the **verified** delivery target, exact permissions and accepted route schema, then deliberately flips worker_enabled from 0 to 1.
6. Review Windows test result and exact Git TaskSource revision before ACK. A failure remains failed; no replay of an ambiguous result.

Until the manager-side steps are verified, keep worker_enabled=0, tasks=[], force_restart.enabled=false. No local registry/Edge config, running worker, test result, CDP port or physical equipment is established by GitHub changes alone.
