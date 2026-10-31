"""Offline-only AIRobotFactory commands: no external machine actuation."""
import argparse
import json

from .cad import export_coupon_stl
from .simulation import export_workspace_jsonl


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="AIRobotFactory offline experiments")
    commands = parser.add_subparsers(dest="command", required=True)
    dataset = commands.add_parser("dataset", help="Export 2-link synthetic workspace JSONL")
    dataset.add_argument("--output", required=True)
    dataset.add_argument("--link1", type=float, default=120.0)
    dataset.add_argument("--link2", type=float, default=90.0)
    cube = commands.add_parser("coupon", help="Export a 3D-print calibration cube ASCII STL")
    cube.add_argument("--output", required=True)
    cube.add_argument("--size", type=float, default=20.0)
    workcell = commands.add_parser("workcell", help="Run headless 6-axis physics simulation")
    workcell.add_argument("--output", required=True)
    workcell.add_argument("--steps", type=int, default=700)
    commands.add_parser("ai-status", help="Check optional local Ollama model names without changing it")
    intent = commands.add_parser("ai-propose", help="Validate a virtual-only Ollama proposal (no execution)")
    intent.add_argument("--model", required=True)
    intent.add_argument("--text", required=True)
    args = parser.parse_args(argv)
    if args.command == "dataset":
        count = export_workspace_jsonl(args.output, args.link1, args.link2)
        print(f"created {count} synthetic samples: {args.output}")
    elif args.command == "coupon":
        path = export_coupon_stl(args.output, args.size)
        print(f"created calibration STL: {path}")
    elif args.command == "workcell":
        from .workcell import save_demo
        print(json.dumps(save_demo(args.output, args.steps), indent=2))
    elif args.command == "ai-status":
        from .local_ai import detect_ollama
        print(json.dumps(detect_ollama(), indent=2))
    else:
        from .local_ai import ask_ollama
        print(json.dumps(ask_ollama(args.model, args.text), indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
