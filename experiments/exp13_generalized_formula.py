#!/usr/bin/env python3
"""
Test 13: universal formula for |Pp(k)| across the 8 options.

Extends Test 11 (option 1) to all options. For each option:
  A'(d) = |Pp(d)| + |Ap(d)|
  N'(d) = sum_{e|d} mu(d/e) A'(e)
  |Pp(k)| = sum_{d|k, 3<=d<k} N'(d)
and compare with the actual value.

Requires Test 12 to have run (to have canonical data for 5-8 on disk).
If not, generates and caches it.
"""

from sw.common import (
    classify, chain_to_word, divisors, load_canonical, moebius,
)

OPTIONS = {
    1: 15, 2: 9, 3: 9, 4: 6,
    5: 9, 6: 9, 7: 6, 8: 6,
}

CELLS = ["PP", "Pp", "pP", "Ap"]


def compute_cells(option, k):
    """Return {cell: count} for the given option and k."""
    chains = load_canonical(option, k)
    counts = {c: 0 for c in CELLS}
    for ch in chains:
        w = chain_to_word(ch, convention="star_or_plus0")
        counts[classify(w)] += 1
    return counts


def compute_A(N_max, option):
    """A'(d) = |Pp(d)| + |Ap(d)| for d = 1..N_max."""
    A = {1: 0}
    for d in range(2, N_max + 1):
        try:
            c = compute_cells(option, d)
        except Exception:
            A[d] = None
            continue
        A[d] = c["Pp"] + c["Ap"]
    return A


def compute_N(A, N_max):
    """N'(d) by Moebius inversion."""
    N = {}
    for d in range(1, N_max + 1):
        if A[d] is None:
            N[d] = None
            continue
        vals = []
        ok = True
        for e in divisors(d):
            if A[e] is None:
                ok = False
                break
            vals.append(moebius(d // e) * A[e])
        N[d] = sum(vals) if ok else None
    return N


def predict_Pp(N, k):
    ds = [d for d in divisors(k) if 3 <= d < k]
    if any(N[d] is None for d in ds):
        return None
    return sum(N[d] for d in ds)


if __name__ == "__main__":
    print("=" * 100)
    print("TEST 13 - Universal formula for |Pp(k)| across the 8 options")
    print("=" * 100)
    print()

    for option, k_max in OPTIONS.items():
        print(f"\n{'=' * 100}")
        print(f"OPTION {option} (k_max = {k_max})")
        print("=" * 100)

        A = compute_A(k_max, option)
        N = compute_N(A, k_max)

        print(f"\n  A'(d) = |Pp(d)| + |Ap(d)|:")
        for d in sorted(A):
            if A[d] is not None:
                print(f"    A'({d:>2}) = {A[d]:>8}")

        print(f"\n  N'(d) = Moebius inverse:")
        for d in sorted(N):
            if N[d] is not None:
                print(f"    N'({d:>2}) = {N[d]:>8}")

        print(f"\n  Comparison |Pp(k)| predicted vs actual:")
        print(f"  {'k':>3} | {'predicted':>10} | {'actual':>8} | {'match':>6}")
        print("  " + "-" * 40)
        all_ok = True
        for k in range(2, k_max + 1):
            pred = predict_Pp(N, k)
            try:
                real = compute_cells(option, k)["Pp"]
            except Exception:
                real = None
            if pred is None or real is None:
                print(f"  {k:>3} | {'?':>10} | {'?':>8} |   ?")
                continue
            match = "OK" if pred == real else "FAIL"
            if pred != real:
                all_ok = False
            print(f"  {k:>3} | {pred:>10} | {real:>8} | {match:>6}")

        print(f"\n  -> {'OK: formula confirmed' if all_ok else 'FAIL: formula fails'}")
