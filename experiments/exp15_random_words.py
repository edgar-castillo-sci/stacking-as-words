#!/usr/bin/env python3
"""
Test 15: probability of each cell for random words.

Draw N uniform samples from {A,B,C}^k for k = 2..20 and report the
fraction in each cell. Compare with the orbit distribution (Test 7):
they agree for "generic" cells (Ap) but differ for structured cells
(PP, Pp, pP) because small orbits overweight those cells.

No pruning dependency: pure combinatorics, fast.
"""

import random

from sw.common import classify

CELLS = ["PP", "Pp", "pP", "Ap"]
N_SAMPLES = 100_000


def random_word(k, rng):
    return "".join(rng.choice("ABC") for _ in range(k))


if __name__ == "__main__":
    rng = random.Random(42)

    print("=" * 100)
    print(f"TEST 15 - Cell distribution for {N_SAMPLES:,} random words")
    print("=" * 100)
    print()
    print(f"{'k':>3} | " + " | ".join(f"P({c})" for c in CELLS)
          + " | P(S3P) | P(per)")
    print("-" * 90)

    for k in range(2, 21):
        counts = {c: 0 for c in CELLS}
        for _ in range(N_SAMPLES):
            w = random_word(k, rng)
            counts[classify(w)] += 1
        fracs = {c: counts[c] / N_SAMPLES for c in CELLS}
        p_s3p = fracs["PP"] + fracs["pP"]
        p_per = fracs["PP"] + fracs["Pp"]
        print(f"{k:>3} | " +
              " | ".join(f"{fracs[c]:>6.3f}" for c in CELLS) +
              f" | {p_s3p:>7.3f} | {p_per:>6.3f}")

    print()
    print("=" * 100)
    print("READING")
    print("=" * 100)
    print("""
- P(Ap) -> 1, as in Test 7.
- P(S3P) ~ 6 * 3^{-ceil(k/2)} / 3^k = 6 * 3^{-floor(k/2)}.
- P(per) ~ O(3^{-k/2}) (dominated by period k/2).
- For large k, both decay exponentially.
- Compare with Test 7: structured cells (PP, pP) are overrepresented in
  orbits (because they have larger stabilizers).
""")
