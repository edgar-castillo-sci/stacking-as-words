#!/usr/bin/env python3
"""
Test 10: map of the 16 regions of the Venn diagram of (H, R, S3P, P).

For each k, enumerate one orbit per G-class and classify into one of the
2^4 = 16 regions, according to four Boolean properties:

  H  : strict palindrome (w = reverse(w))
  R  : 3-fold screw (sigma(w) = rot^m(w) for some 3-cycle sigma and m >= 1)
  S  : S3-palindromic (exists sigma in S3: sigma(w) = reverse(w))
  P  : periodic (w = u^n, n >= 2)

Logical predictions:
  - H  => S3P    (sigma = id). So H and not S3P must always be empty.
  - H and P is the strict "periodic palindromic" cell (subset of PP).
  - R is a subset of S3P under the standard definition (Test 5). If
    R and not S3P appears, it is an empirical contradiction worth
    investigating.
"""

from collections import Counter

from sw.common import (
    is_3fold_screw, is_periodic, is_s3_palindromic,
    is_strict_palindrome, chain_to_word, load_canonical,
)


def classify_region(w):
    """Return the 4-tuple (H, R, S, P) of the word."""
    return (
        is_strict_palindrome(w),
        is_3fold_screw(w),
        is_s3_palindromic(w),
        is_periodic(w),
    )


def label(region):
    """Readable label: H.R.S.P, etc."""
    h, r, s, p = region
    parts = []
    parts.append("H" if h else "!H")
    parts.append("R" if r else "!R")
    parts.append("S" if s else "!S")
    parts.append("P" if p else "!P")
    return ".".join(parts)


if __name__ == "__main__":
    print("=" * 90)
    print("TEST 10 - Venn diagram of (H, R, S3P, P)")
    print("=" * 90)
    print()
    print("H = strict palindrome, R = 3-fold screw,")
    print("S = S3-palindromic,    P = periodic")
    print()

    for k in range(2, 12):
        chains = load_canonical(1, k)
        counts = Counter()
        for ch in chains:
            w = chain_to_word(ch)
            counts[classify_region(w)] += 1

        print(f"\n-- k = {k}  ({len(chains)} orbits) --")
        # Sort by the tuple (False < True)
        for region in sorted(counts, key=lambda r: tuple(int(x) for x in r)):
            print(f"  {label(region):<20}: {counts[region]:>5}")

        # Logical checks
        bad = [(r, n) for r, n in counts.items()
               if r[0] and not r[2]]  # H and not S3P
        if bad:
            print(f"  IMPOSSIBLE: H and not S3P = {bad} (logic bug)")

        r_s = [(r, n) for r, n in counts.items() if r[1] and not r[2]]
        if r_s:
            print(f"  note: R and not S3P nonempty: {r_s}  (contradicts Test 5!)")

    # -- Summary: active regions per k ----------------------------------
    print()
    print("=" * 90)
    print("SUMMARY - active regions per k")
    print("=" * 90)
    print()
    print(f"{'region':<22}" + "".join(f"k={k:<3}" for k in range(2, 12)))
    print("-" * 90)

    all_regions = [
        (True, True, True, True),
        (True, True, True, False),
        (True, False, True, True),
        (True, False, True, False),
        (False, True, True, True),
        (False, True, True, False),
        (False, False, True, True),
        (False, False, True, False),
        (False, True, False, True),   # expected empty (R subset S3P)
        (False, True, False, False),  # expected empty
        (False, False, False, True),  # pure Pp (AABAAB, etc.)
        (False, False, False, False), # Ap
    ]
    for region in all_regions:
        row = f"{label(region):<22}"
        for k in range(2, 12):
            chains = load_canonical(1, k)
            present = any(classify_region(chain_to_word(ch)) == region
                          for ch in chains)
            row += "yes " if present else ".   "
        print(row)

    print()
    print("Legend: 'yes' = region nonempty at that k; '.' = empty.")
