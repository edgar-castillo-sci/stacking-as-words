#!/usr/bin/env python3
"""
Test 16: structure of cell transitions under fibration.

Deepens Test 6:
  - Which transitions (parent -> child) are impossible (matrix zeros)?
  - Does the matrix stabilize for large k?
  - Conditional distribution P(child | parent).
  - Any empty rows/columns?

Data: data/fibration/fib_nk_nk+1.tsv (or $SW_DATA_DIR/fibration/...).
"""

from collections import Counter

from sw.common import chain_to_word, classify, load_fibration

CELLS = ["PP", "Pp", "pP", "Ap"]


def transition_matrix(n, option=1):
    pairs = load_fibration(option, n)
    if pairs is None:
        return None
    mat = Counter()
    for parent, child in pairs:
        cp = classify(chain_to_word(parent, convention="star_or_plus0"))
        cc = classify(chain_to_word(child, convention="star_or_plus0"))
        mat[(cp, cc)] += 1
    return mat


if __name__ == "__main__":
    print("=" * 100)
    print("TEST 16 - Forbidden transitions and structure of the fibration")
    print("=" * 100)
    print()

    matrices = {}
    for n in range(1, 8):
        mat = transition_matrix(n)
        if mat is not None:
            matrices[n] = mat

    if not matrices:
        print("No fibration data found. Generate it with caugJAM's")
        print("scripts/fibration.py and place the .tsv files under")
        print("data/fibration/ (or set $SW_DATA_DIR).")
        raise SystemExit(0)

    # -- 1. Which cells appear as PARENT / CHILD? ------------------------
    print("Cells present as PARENT / CHILD per n:")
    print(f"{'n->n+1':>8} | {'parents':>40} | {'children':>40}")
    print("-" * 100)
    for n, mat in matrices.items():
        parents = sorted({cp for (cp, cc) in mat})
        children = sorted({cc for (cp, cc) in mat})
        print(f"{n}->{n+1:<3} | {', '.join(parents):>40} | "
              f"{', '.join(children):>40}")

    # -- 2. Forbidden transitions (structural zeros) --------------------
    print()
    print("Transitions (parent -> child) that NEVER occur for n <= 7:")
    all_pairs = {(cp, cc) for cp in CELLS for cc in CELLS}
    forbidden = all_pairs - {p for mat in matrices.values() for p in mat}
    if forbidden:
        for cp, cc in sorted(forbidden):
            print(f"  {cp} -> {cc}")
    else:
        print("  (none)")

    # -- 3. Conditional distribution P(child | parent) ------------------
    print()
    print("Conditional distribution P(child | parent), aggregated over n <= 7:")
    agg = Counter()
    for mat in matrices.values():
        agg.update(mat)
    row_totals = Counter()
    for (cp, cc), v in agg.items():
        row_totals[cp] += v

    print(f"{'parent':>6} | " + " | ".join(f"{c:>6}" for c in CELLS) + " | total")
    print("-" * 60)
    for cp in CELLS:
        if row_totals[cp] == 0:
            continue
        row = []
        for cc in CELLS:
            v = agg.get((cp, cc), 0)
            row.append(f"{v / row_totals[cp]:>6.3f}")
        print(f"{cp:>6} | " + " | ".join(row) + f" | {row_totals[cp]:>5}")

    # -- 4. Does the distribution stabilize between n and n+1? ---------
    print()
    print("Comparison P(child | parent) between consecutive n:")
    for n in range(2, 7):
        if n not in matrices or n + 1 not in matrices:
            continue

        def cond(mat):
            tot = Counter()
            for (cp, cc), v in mat.items():
                tot[cp] += v
            out = {}
            for cp in CELLS:
                if tot[cp] == 0:
                    out[cp] = {cc: None for cc in CELLS}
                else:
                    out[cp] = {cc: mat.get((cp, cc), 0) / tot[cp]
                               for cc in CELLS}
            return out

        c1, c2 = cond(matrices[n]), cond(matrices[n + 1])
        same_count = sum(
            1 for cp in CELLS for cc in CELLS
            if c1[cp][cc] is not None and c2[cp][cc] is not None
            and abs(c1[cp][cc] - c2[cp][cc]) < 0.05
        )
        total_count = sum(
            1 for cp in CELLS for cc in CELLS
            if c1[cp][cc] is not None and c2[cp][cc] is not None
        )
        print(f"  n={n} vs n={n+1}: {same_count}/{total_count} entries"
              f" within +/- 0.05")

    print()
    print("=" * 100)
    print("READING")
    print("=" * 100)
    print("""
- Forbidden transitions are "structural zeros": they suggest fibration
  constraints worth documenting.
- The conditional distribution shows which cells are "stable" under
  stacking and which are "transient".
- If the matrix stabilizes for large n, there is an interesting
  asymptotic structure for the companion paper (augmentation).
""")
