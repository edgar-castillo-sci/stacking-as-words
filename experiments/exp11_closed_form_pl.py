#!/usr/bin/env python3
"""
Test 11: combinatorial formula for |Pp(k)|_G.

Conjecture derived from Test 3:

  |Pp(k)|_G = sum_{d | k, 3 <= d < k} N'(d)

where N'(d) is computed by Moebius inversion from

  A'(d) = |Pp(d)|_G + |Ap(d)|_G   (G-orbits of non-S3P words)

and

  A'(d) = sum_{e | d} N'(e)   =>   N'(d) = sum_{e | d} mu(d/e) A'(e).

Conceptual basis: w = u^m is S3P iff u is S3P (the primitive root
preserves the property), and the "effective period" of w is |u|.

We verify the conjecture for k = 2..12 (12 is the new prediction: if
Test 3 extended to k=12 gives |Pp(12)|_G = 56, the formula is confirmed).
"""

from sw.common import (
    classify, chain_to_word, divisors, is_s3_palindromic,
    load_canonical, moebius,
)


def compute_A_prime(k_max):
    """A'(d) = |Pp(d)|_G + |Ap(d)|_G, for d = 1..k_max."""
    A = {}
    for d in range(1, k_max + 1):
        if d == 1:
            A[1] = 0
            continue
        chains = load_canonical(1, d)
        A[d] = sum(
            1 for ch in chains
            if not is_s3_palindromic(chain_to_word(ch))
        )
    return A


def compute_N_prime(A, k_max):
    N = {}
    for d in range(1, k_max + 1):
        N[d] = sum(moebius(d // e) * A[e] for e in divisors(d))
    return N


def predict_Pp(N, k):
    """|Pp(k)|_G = sum_{d | k, 3 <= d < k} N'(d)."""
    return sum(N[d] for d in divisors(k) if 3 <= d < k)


def actual_Pp(k):
    chains = load_canonical(1, k)
    return sum(1 for ch in chains
               if classify(chain_to_word(ch)) == "Pp")


if __name__ == "__main__":
    K_MAX = 12
    print("=" * 80)
    print(f"TEST 11 - formula |Pp(k)|_G = sum_(d|k, 3<=d<k) N'(d)  (k_max = {K_MAX})")
    print("=" * 80)
    print()

    print("Step 1: A'(d) = |Pp(d)|_G + |Ap(d)|_G  (G-orbits of non-S3P)")
    A = compute_A_prime(K_MAX)
    for d in sorted(A):
        print(f"  A'({d:>2}) = {A[d]:>7}")

    print()
    print("Step 2: N'(d) by Moebius inversion")
    N = compute_N_prime(A, K_MAX)
    for d in sorted(N):
        print(f"  N'({d:>2}) = {N[d]:>7}")

    print()
    print("Step 3: compare actual vs predicted |Pp(k)|_G")
    print()
    print(f"{'k':>3} | {'predicted':>10} | {'actual':>7} | {'match':>7} | divisors d")
    print("-" * 70)
    all_ok = True
    for k in range(2, K_MAX + 1):
        pred = predict_Pp(N, k)
        real = actual_Pp(k)
        ds = [d for d in divisors(k) if 3 <= d < k]
        match = "OK" if pred == real else "FAIL"
        if pred != real:
            all_ok = False
        print(f"{k:>3} | {pred:>10} | {real:>7} | {match:>7} | {ds}")

    print()
    print("=" * 80)
    if all_ok:
        print("OK: formula confirmed for all k <= 12.")
    else:
        print("FAIL: formula fails for some k. Investigate.")
    print("=" * 80)
    print()

    # -- Extrapolated predictions for k = 13..24 -------------------------
    print("BONUS - predicted |Pp(k)|_G for k = 13..24")
    print("(valid if the formula holds; require N'(d) for d | k, d >= 13")
    print(" -> not computed here; see 'pending' below)")
    print()
    print("Note: predicting k=16 requires N'(4) and N'(8) (already known).")
    print("Predicting k=18 requires N'(3), N'(6), N'(9). N'(9) requires A'(9).")
    print("Predicting k=24 requires N'(3), N'(4), N'(6), N'(8), N'(12).")
    print()
    print("Concrete predictions:")
    for k, ds in [(13, []), (14, [7]), (15, [3, 5]), (16, [4, 8]),
                  (18, [3, 6, 9]), (20, [4, 5, 10]), (21, [3, 7]),
                  (22, [11]), (24, [3, 4, 6, 8, 12])]:
        if all(d in N for d in ds):
            pred = sum(N[d] for d in ds)
            print(f"  k={k:>2}: {pred:>10}   (d in {ds})")
        else:
            print(f"  k={k:>2}: pending (missing N' for d in {ds})")
