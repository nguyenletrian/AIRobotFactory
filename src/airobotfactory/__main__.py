"""Run strictly offline AIRobotFactory experiments."""
import argparse

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
    args = parser.parse_args(argv)
    if args.command == "dataset":
        count = export_workspace_jsonl(args.output, args.link1, args.link2)
        print(f"created {count} synthetic samples: {args.output}")
    else:
        path = export_coupon_stl(args.output, args.size)
        print(f"created calibration STL: {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
