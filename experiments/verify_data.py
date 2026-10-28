#!/usr/bin/env python3
"""
Verify the versioned summary tables in data/summary/ against expected
values.

Two modes:

  python3 experiments/verify_data.py
      Load the committed .tsv files and check them against the expected
      values from the paper (fast: < 1 s, no caugJAM needed).

  python3 experiments/verify_data.py --regenerate
      Recompute the summary tables with caugJAM (slow: a few minutes at
      high k), then compare against the committed .tsv. Exits non-zero
      if any value differs.
"""

import argparse
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
SUMMARY = REPO / "data" / "summary"

# Expected values from the paper (Tables 2 and Appendix A).
EXPECTED_PP_PL = {
    3: 0, 4: 0, 5: 0, 6: 1, 7: 0, 8: 4, 9: 1, 10: 16,
    11: 0, 12: 56, 13: 0, 14: 169, 15: 17,
}
EXPECTED_NPRIME_PL = {
    3: 1, 4: 4, 5: 16, 6: 51, 7: 169, 8: 516, 9: 1599,
    10: 4824, 11: 14641, 12: 43988, 13: 132496, 14: 397683,
    15: 1194632,
}


def read_tsv(path):
    with path.open() as f:
        header = f.readline().rstrip("\n").split("\t")
        rows = [line.rstrip("\n").split("\t") for line in f if line.strip()]
    return header, rows


def verify_files_present():
    missing = []
    for name in ("class_counts_pl.tsv", "class_counts_options_2_8.tsv", "Nprime_pl.tsv"):
        if not (SUMMARY / name).exists():
            missing.append(name)
    return missing


def verify_class_counts_pl():
    """Check that (a) PP/Pp/pP/Ap sum to n_orbits, (b) Pp matches the paper."""
    header, rows = read_tsv(SUMMARY / "class_counts_pl.tsv")
    idx = {name: i for i, name in enumerate(header)}
    failures = []
    for row in rows:
        k = int(row[idx["k"]])
        n = int(row[idx["n_orbits"]])
        pp = int(row[idx["PP"]])
        pu = int(row[idx["Pp"]])
        pa = int(row[idx["pP"]])
        ap = int(row[idx["Ap"]])
        if pp + pu + pa + ap != n:
            failures.append(f"k={k}: PP+Pp+pP+Ap={pp+pu+pa+ap} != n_orbits={n}")
        if k in EXPECTED_PP_PL and pu != EXPECTED_PP_PL[k]:
            failures.append(f"k={k}: Pp={pu} != expected {EXPECTED_PP_PL[k]}")
    return failures


def verify_nprime():
    """Check N'(d) against Appendix A of the paper."""
    header, rows = read_tsv(SUMMARY / "Nprime_pl.tsv")
    idx = {name: i for i, name in enumerate(header)}
    failures = []
    for row in rows:
        d = int(row[idx["d"]])
        n = int(row[idx["N_prime"]])
        if d in EXPECTED_NPRIME_PL and n != EXPECTED_NPRIME_PL[d]:
            failures.append(f"d={d}: N'={n} != expected {EXPECTED_NPRIME_PL[d]}")
    return failures


def verify_options():
    """Check internal consistency for options 2-8."""
    header, rows = read_tsv(SUMMARY / "class_counts_options_2_8.tsv")
    idx = {name: i for i, name in enumerate(header)}
    failures = []
    for row in rows:
        option = int(row[idx["option"]])
        k = int(row[idx["k"]])
        n = int(row[idx["n_orbits"]])
        total = sum(int(row[idx[c]]) for c in ("PP", "Pp", "pP", "Ap"))
        if total != n:
            failures.append(f"option={option}, k={k}: sum={total} != n_orbits={n}")
    return failures


def run_regenerate():
    """Recompute summary tables with caugJAM and diff against the committed ones."""
    import subprocess
    print("Regenerating data/summary/*.tsv with caugJAM...")
    result = subprocess.run(
        [sys.executable, str(REPO / "experiments" / "dump_summary.py")],
        cwd=REPO,
    )
    if result.returncode != 0:
        return ["dump_summary.py failed"]
    return []


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--regenerate", action="store_true",
                        help="Recompute the tables with caugJAM before checking.")
    args = parser.parse_args()

    print("Verifying data/summary/*.tsv ...")
    missing = verify_files_present()
    if missing:
        print(f"ERROR: missing files: {missing}")
        print("Run: python3 experiments/dump_summary.py")
        return 1

    all_failures = []

    all_failures += verify_class_counts_pl()
    all_failures += verify_nprime()
    all_failures += verify_options()

    if args.regenerate:
        all_failures += run_regenerate()

    if all_failures:
        print()
        print("FAILURES:")
        for f in all_failures:
            print(f"  {f}")
        return 1

    print()
    print("OK: all checks passed.")
    print("  class_counts_pl.tsv          : sums + Pp values match the paper")
    print("  class_counts_options_2_8.tsv : sums match n_orbits")
    print("  Nprime_pl.tsv                : N'(d) matches Appendix A")
    return 0


if __name__ == "__main__":
    sys.exit(main())
