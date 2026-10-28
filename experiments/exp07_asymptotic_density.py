#!/usr/bin/env python3
"""
Test 7: asymptotic density per cell.

For each k, report the fraction of orbits in each cell.
Prediction: the fraction of 'Ap' (aperiodic) tends to 1 as k grows.
"""

from sw.common import classify, chain_to_word, load_canonical

CELLS = ["PP", "Pp", "pP", "Ap"]


if __name__ == "__main__":
    print("=" * 100)
    print("TEST 7 - Asymptotic density per cell (option 1)")
    print("=" * 100)
    print()
    print(f"{'k':>3} | {'orb':>6} | " + " | ".join(f"{c:>6}" for c in CELLS) + " | Ap/%")
    print("-" * 100)

    for k in range(2, 12):
        try:
            chains = load_canonical(1, k)
        except FileNotFoundError:
            continue
        cells = {c: 0 for c in CELLS}
        for ch in chains:
            cells[classify(chain_to_word(ch))] += 1
        n = len(chains)
        fracs = {c: cells[c] / n for c in CELLS}
        ap_pct = 100 * fracs["Ap"]
        print(f"{k:>3} | {n:>6} | " +
              " | ".join(f"{fracs[c]:>6.3f}" for c in CELLS) +
              f" | {ap_pct:>6.2f}")

    print()
    print("Prediction: Ap -> 1 exponentially in k.")
    print("The pattern is informative as a coarse summary only for small/medium k.")
