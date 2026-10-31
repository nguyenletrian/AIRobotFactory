"""One-run, repeatable, simulation-only environment bootstrap (Python 3.10-3.13).
Never registers a Bridge worker or controls physical hardware.
"""
import argparse
import json
import os
from pathlib import Path
import subprocess
import sys
import time
import venv
import webbrowser

ROOT = Path(__file__).resolve().parents[1]
VENV = ROOT / ".venv"
VENV_PYTHON = VENV / ("Scripts/python.exe" if os.name == "nt" else "bin/python")
STATUS = ROOT / "artifacts" / "environment_report.json"


def run(args, label):
    print("[AIRobotFactory]", label, flush=True)
    result = subprocess.run([str(a) for a in args], cwd=ROOT, check=False)
    if result.returncode:
        raise RuntimeError(f"{label}: failed with exit code {result.returncode}")


def installed():
    return subprocess.run(
        [str(VENV_PYTHON), "-c", "import mujoco,airobotfactory; print(mujoco.__version__)"],
        cwd=ROOT, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=False
    ).returncode == 0


def prepare(allow_install=True):
    if not (3, 10) <= sys.version_info[:2] < (3, 14) or sys.maxsize <= 2**32:
        raise RuntimeError("Install 64-bit Python 3.10-3.13; Python 3.12 preferred")
    if not VENV_PYTHON.exists():
        if not allow_install:
            raise RuntimeError("Missing .venv; rerun without --skip-install")
        print("[AIRobotFactory] Creating isolated .venv", flush=True)
        venv.create(VENV, with_pip=True)
    if not installed():
        if not allow_install:
            raise RuntimeError("MuJoCo/project missing in existing venv; installation disabled")
        run([VENV_PYTHON, "-m", "pip", "install", "-e", ".[sim]"],
            "Install project and MuJoCo into isolated .venv")
    if not installed():
        raise RuntimeError("MuJoCo could not be imported after install")


def create_evidence():
    cli = [VENV_PYTHON, "-m", "airobotfactory"]
    run([VENV_PYTHON, "-m", "unittest", "discover", "-s", "tests", "-v"],
        "Run offline Python/MuJoCo unit tests")
    outputs = ROOT / "artifacts"
    outputs.mkdir(parents=True, exist_ok=True)
    for action, filename in (("dataset", "workspace.jsonl"), ("coupon", "cube20.stl")):
        destination = outputs / filename
        if destination.exists():
            if destination.is_symlink() or not destination.is_file():
                raise RuntimeError(f"Refusing unusual generated artifact path {destination}")
            print("[AIRobotFactory] Preserve", filename, flush=True)
        else:
            run([*cli, action, "--output", destination], f"Generate {filename}")
    stamp = time.strftime("%Y%m%d-%H%M%S", time.localtime())
    output = outputs / f"workcell_{stamp}_{os.getpid()}.json"
    run([*cli, "workcell", "--output", output], "Run virtual 6-axis physics test")
    probe = subprocess.run([*map(str, cli), "ai-status"], cwd=ROOT, text=True,
                           capture_output=True, timeout=10, check=False)
    if probe.returncode:
        raise RuntimeError("Ollama read-only probe failed: " + probe.stderr[-200:])
    ai = json.loads(probe.stdout)
    version = subprocess.check_output([str(VENV_PYTHON), "-c", "import mujoco; print(mujoco.__version__)"], cwd=ROOT, text=True).strip()
    result = {
        "mujoco_version": version,
        "status": "simulation_ready_headless",
        "model": "simulations/mujoco/workcell_6dof.xml",
        "workcell_report": str(output.relative_to(ROOT)),
        "local_ai": ai,
        "physical_actuation_enabled": False,
        "bridge_worker_modified": False,
        "gui_tested": False,
    }
    if STATUS.is_symlink():
        raise RuntimeError("Refuse environment report symlink")
    STATUS.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print("[AIRobotFactory] Saved", output, flush=True)
    print("[AIRobotFactory] Local Ollama:", "detected" if ai["reachable"] else "not found (optional)")
    return result


def launch():
    html = ROOT / "visualizer" / "index.html"
    if html.is_file():
        webbrowser.open(html.as_uri())
    scene = ROOT / "simulations" / "mujoco" / "workcell_6dof.xml"
    print("[AIRobotFactory] Launching MuJoCo 6-axis GUI", flush=True)
    subprocess.Popen([str(VENV_PYTHON), "-m", "mujoco.viewer", f"--mjcf={scene}"], cwd=ROOT)


def main(argv=None):
    parser = argparse.ArgumentParser(description="AIRobotFactory one-run offline simulation")
    parser.add_argument("--headless", action="store_true", help="Skip browser/MuJoCo GUI")
    parser.add_argument("--skip-install", action="store_true", help="Require already-installed .venv")
    args = parser.parse_args(argv)
    try:
        prepare(not args.skip_install)
        create_evidence()
        if not args.headless:
            launch()
        print("[AIRobotFactory] READY: simulation-only; no hardware connected", flush=True)
        return 0
    except (OSError, RuntimeError, subprocess.TimeoutExpired, ValueError) as exc:
        print("[AIRobotFactory] SETUP FAILED:", exc, file=sys.stderr, flush=True)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
