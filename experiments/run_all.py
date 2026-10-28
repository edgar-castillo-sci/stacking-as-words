#!/usr/bin/env python3
"""Run all experiments in sequence, with a dependency report at the start.

This is the "pipeline" entry point. It prints the versions of the
dependencies (caugJam, canonJam, numpy), runs each experiment, and
reports pass/fail at the end. Output is also written to outputs/<name>.txt.

Usage:
  python3 experiments/run_all.py
  python3 experiments/run_all.py --deps     # print deps, exit
  python3 experiments/run_all.py --list     # list experiments, exit
  python3 experiments/run_all.py --no-save  # do not write outputs/
"""

import argparse
import subprocess
import sys
from pathlib import Path

from sw.provenance import format_deps

HERE = Path(__file__).resolve().parent
REPO = HERE.parent
OUTPUTS = REPO / "outputs"
EXPERIMENTS = sorted(HERE.glob("exp*.py"))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--deps", action="store_true",
                        help="Print dependency report and exit")
    parser.add_argument("--list", action="store_true",
                        help="List experiments and exit")
    parser.add_argument("--no-save", action="store_true",
                        help="Do not write outputs/<name>.txt")
    args = parser.parse_args()

    if args.list:
        for exp in EXPERIMENTS:
            print(f"  {exp.name}")
        return 0

    if args.deps:
        print(format_deps())
        return 0

    print(format_deps())
    print()
    print(f"Running {len(EXPERIMENTS)} experiments...")
    print()

    OUTPUTS.mkdir(exist_ok=True)
    failed = []
    for exp in EXPERIMENTS:
        print(f"=== {exp.name} ===")
        result = subprocess.run(
            [sys.executable, str(exp)],
            cwd=REPO,
            capture_output=True,
            text=True,
        )
        sys.stdout.write(result.stdout)
        if result.stderr:
            sys.stderr.write(result.stderr)
        if not args.no_save:
            out = OUTPUTS / (exp.stem + "_output.txt")
            out.write_text(result.stdout)
            print(f"  -> saved to {out.relative_to(REPO)}")
        if result.returncode != 0:
            failed.append((exp.name, result.returncode))
        print()

    if failed:
        print("FAILED experiments:")
        for name, rc in failed:
            print(f"  {name}  (exit {rc})")
        return 1

    print(f"All {len(EXPERIMENTS)} experiments passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
