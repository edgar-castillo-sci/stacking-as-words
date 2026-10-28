#!/usr/bin/env python3
"""
Generate versioned summary tables for the stacking-as-words repository.

Reads the canonical chains in ./data/ (or $SW_DATA_DIR) and writes:

  data/summary/class_counts_pl.tsv          (option 1, k = 2..K)
  data/summary/class_counts_options_2_8.tsv (options 2..8, all k present)
  data/summary/Nprime_pl.tsv                (N'(d) for option 1, d = 2..K)

The output is small (a few KB) and is meant to be committed as evidence.
It can be regenerated with `python3 experiments/dump_summary.py`.

Requires caugjam v0.1.0 if the canonical data is not already cached.
"""

import glob
import os
import re
import sys
from pathlib import Path

from sw.common import (
    classify, chain_to_word, divisors, load_canonical, moebius,
)


def data_roots():
    env_dir = os.environ.get("SW_DATA_DIR")
    roots = []
    if env_dir:
        roots.append(env_dir)
    here = Path(__file__).resolve().parent.parent
    roots.append(str(here / "data"))
    return roots


def discover_levels(option):
    """Sorted list of k values for which canonical data exists."""
    levels = set()
    for root in data_roots():
        if option == 1:
            pattern = os.path.join(root, "n*")
        else:
            pattern = os.path.join(root, f"opt{option}", "n*")
        for path in glob.glob(pattern):
            m = re.search(r"n(\d+)$", path)
            if m and os.path.isfile(os.path.join(path, "canonicas.txt")):
                levels.add(int(m.group(1)))
    return sorted(levels)


def cell_counts(option, k):
    """Return (n_orbits, {PP: n, Pp: n, pP: n, Ap: n})."""
    chains = load_canonical(option, k)
    counts = {"PP": 0, "Pp": 0, "pP": 0, "Ap": 0}
    for ch in chains:
        w = chain_to_word(ch, convention="star_or_plus0")
        counts[classify(w)] += 1
    return len(chains), counts


def n_prime_pl(k_max):
    """N'(d) for PL, computed by Moebius inversion of A'(d)."""
    A = {1: 0}
    for d in range(2, k_max + 1):
        _, c = cell_counts(1, d)
        A[d] = c["Pp"] + c["Ap"]
    N = {}
    for d in range(2, k_max + 1):
        N[d] = sum(moebius(d // e) * A[e] for e in divisors(d) if e >= 2)
    return N


def write_tsv(path, header, rows):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w") as f:
        f.write("\t".join(header) + "\n")
        for row in rows:
            f.write("\t".join(str(x) for x in row) + "\n")
    n = len(rows)
    print(f"  wrote {n} rows to {path.relative_to(path.parent.parent.parent)}")


def main():
    here = Path(__file__).resolve().parent.parent
    out = here / "data" / "summary"
    out.mkdir(parents=True, exist_ok=True)

    print("Discovered levels:")
    for option in range(1, 9):
        levels = discover_levels(option)
        print(f"  option {option}: k = {levels}")

    # -- class_counts_pl.tsv ---------------------------------------------
    levels_pl = discover_levels(1)
    if not levels_pl:
        print("ERROR: no PL canonical data found under data/n*/", file=sys.stderr)
        return 1

    rows = []
    for k in levels_pl:
        n, c = cell_counts(1, k)
        rows.append((k, n, c["PP"], c["Pp"], c["pP"], c["Ap"]))
    write_tsv(
        out / "class_counts_pl.tsv",
        ["k", "n_orbits", "PP", "Pp", "pP", "Ap"],
        rows,
    )

    # -- class_counts_options_2_8.tsv ------------------------------------
    rows = []
    for option in range(2, 9):
        for k in discover_levels(option):
            n, c = cell_counts(option, k)
            rows.append((option, k, n, c["PP"], c["Pp"], c["pP"], c["Ap"]))
    write_tsv(
        out / "class_counts_options_2_8.tsv",
        ["option", "k", "n_orbits", "PP", "Pp", "pP", "Ap"],
        rows,
    )

    # -- Nprime_pl.tsv ---------------------------------------------------
    N = n_prime_pl(max(levels_pl))
    rows = [(d, N[d]) for d in sorted(N)]
    write_tsv(
        out / "Nprime_pl.tsv",
        ["d", "N_prime"],
        rows,
    )

    print()
    print("Done.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
