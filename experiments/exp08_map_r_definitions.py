#!/usr/bin/env python3
"""
Test 8: map of definitions of R.

The paper claims that S3P is "incomparable with R". Test 5 showed that
under the standard definition (3-cycle + rotation), R is a subset of S3P
for k <= 8.

This test explores several plausible definitions of R and checks which
of them give R \\ S3P nonempty (i.e., which preserve the incomparability).
"""

from itertools import product

from sw.common import S3, THREE_CYCLES, apply_perm, is_s3_palindromic


def all_words(k):
    for tup in product("ABC", repeat=k):
        yield "".join(tup)


def rot(w, m):
    return w if m == 0 else w[m % len(w):] + w[:m % len(w)]


def rev(w):
    return w[::-1]


def R_standard(w):
    """3-cycle + rotation (definition from Test 5)."""
    k = len(w)
    for s in THREE_CYCLES:
        for m in range(k):
            if apply_perm(w, s) == rot(w, m):
                return True
    return False


def R_nontrivial(w):
    """Like R_standard but excluding m=0."""
    k = len(w)
    for s in THREE_CYCLES:
        for m in range(1, k):
            if apply_perm(w, s) == rot(w, m):
                return True
    return False


def R_mirror(w):
    """3-cycle + rotation + mirror: sigma(w) = reverse(rot^m(w))."""
    k = len(w)
    for s in THREE_CYCLES:
        for m in range(k):
            if apply_perm(w, s) == rev(rot(w, m)):
                return True
    return False


def R_any_sigma(w):
    """Any sigma in S3 + rotation (not just 3-cycles)."""
    k = len(w)
    for s in S3:
        for m in range(k):
            if apply_perm(w, s) == rot(w, m):
                return True
    return False


def R_period_pow3(w):
    """Period d with k/d a power of 3 > 1."""
    k = len(w)
    for d in range(1, k):
        if k % d != 0:
            continue
        m = k // d
        if m < 2:
            continue
        mm = m
        while mm % 3 == 0:
            mm //= 3
        if mm == 1:
            if w == w[:d] * m:
                return True
    return False


DEFS = {
    "R_standard":    R_standard,
    "R_nontrivial":  R_nontrivial,
    "R_mirror":      R_mirror,
    "R_any_sigma":   R_any_sigma,
    "R_period_pow3": R_period_pow3,
}


if __name__ == "__main__":
    print("=" * 100)
    print("TEST 8 - Map of definitions of R")
    print("=" * 100)
    print()

    for k in range(2, 9):
        words = list(all_words(k))
        s3p = {w for w in words if is_s3_palindromic(w)}
        print(f"\n-- k = {k}  (|words| = {len(words)}, |S3P| = {len(s3p)}) --")
        print(f"{'definition':>18} | {'|R|':>5} | {'|RnS3P|':>8} | "
              f"{'|R\\S3P|':>8} | {'|S3P\\R|':>8}")
        print("-" * 70)
        for name, f in DEFS.items():
            r = {w for w in words if f(w)}
            inter = r & s3p
            r_only = r - s3p
            s_only = s3p - r
            flag = "<" if r_only else " "
            print(f"{name:>18} | {len(r):>5} | {len(inter):>8} | "
                  f"{len(r_only):>8} {flag} | {len(s_only):>8}")

    print()
    print("=" * 100)
    print("READING")
    print("=" * 100)
    print("""
- '|R\\S3P| > 0' (marked with <) => R is not a subset of S3P, i.e., there
  is incomparability.
- If NO definition gives R\\S3P > 0, the paper should change
  "incomparable with R" to "weaker than R".
- If some definition (likely R_mirror or R_any_sigma) gives R\\S3P > 0,
  that is the "correct" definition to ask Jessica about.
""")
