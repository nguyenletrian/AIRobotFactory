"""Local-only, opt-in Ollama proposal reader; never executes model plans."""
import json
import math
import urllib.error
import urllib.request

ENDPOINT = "http://127.0.0.1:11434"
ALLOWED_TASKS = frozenset({"inspect_virtual_part", "preview_joint_pose", "preview_gripper"})


def validate_plan(proposal):
    if not isinstance(proposal, dict) or set(proposal) != {"task", "parameters"}:
        raise ValueError("Plan requires exactly task and parameters")
    task, p = proposal["task"], proposal["parameters"]
    if task not in ALLOWED_TASKS or not isinstance(p, dict):
        raise ValueError("Unsupported virtual task")
    if task == "inspect_virtual_part":
        if p:
            raise ValueError("Inspect takes no parameters")
    elif task == "preview_joint_pose":
        if set(p) != {"degrees"} or not isinstance(p["degrees"], list) or len(p["degrees"]) != 6:
            raise ValueError("Pose needs exactly six angles")
        limits = (170, 95, 140, 170, 110, 170)
        for v, limit in zip(p["degrees"], limits):
            if isinstance(v, bool) or not isinstance(v, (float, int)) or not math.isfinite(v) or abs(v) > limit:
                raise ValueError("Pose outside virtual joint limits")
    else:
        if set(p) != {"opening"} or isinstance(p["opening"], bool) or not isinstance(p["opening"], (float, int)) or not 0 <= p["opening"] <= 1:
            raise ValueError("Opening must be 0..1")
    return {"task": task, "parameters": p, "mode": "simulation_preview_only"}


def detect_ollama(timeout=1.0):
    """Query only localhost model names; neither starts Ollama nor downloads models."""
    try:
        with urllib.request.urlopen(ENDPOINT + "/api/tags", timeout=timeout) as response:
            names = json.load(response).get("models", [])
        return {"reachable": True, "models": sorted(m.get("name", "") for m in names if isinstance(m, dict))}
    except (OSError, ValueError, TypeError, urllib.error.URLError):
        return {"reachable": False, "models": []}


def ask_ollama(model, task_description, timeout=30.0):
    """Opt-in model proposal, strict schema validation; no side-effect execution."""
    if (not isinstance(model, str) or not model or len(model) > 120 or "://" in model
            or model.startswith("/") or not all(ch.isalnum() or ch in "-_:/. " for ch in model)
            or " " in model):
        raise ValueError("Invalid local model identifier")
    if not isinstance(task_description, str) or not 1 <= len(task_description) <= 700:
        raise ValueError("Description must be 1..700 characters")
    prompt = ("Respond only with JSON containing task: one of inspect_virtual_part, "
              "preview_joint_pose, preview_gripper; parameters: object. For pose, degrees array "
              "of six finite joint angles; for gripper, opening from 0 to 1. This is simulation "
              "planning only. Do not provide commands or hardware instructions. Request: " + task_description)
    payload = json.dumps({"model": model, "prompt": prompt, "format": "json", "stream": False,
                          "options": {"temperature": 0}}).encode("utf-8")
    request = urllib.request.Request(ENDPOINT + "/api/generate", payload, method="POST",
                                     headers={"Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            raw = response.read(65537)
        if len(raw) > 65536:
            raise ValueError("Model reply exceeds limit")
        return validate_plan(json.loads(json.loads(raw).get("response")))
    except (OSError, ValueError, TypeError, json.JSONDecodeError) as exc:
        raise RuntimeError("Local model unavailable or virtual plan invalid") from exc
