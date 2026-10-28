#!/usr/bin/env python3
"""
Test 5: quantitative refinement of Ramsdell.

For the PERIODIC words (the ones corresponding to Ramsdell's polytypes),
classify each one by:
  H  : strict palindrome        (Ramsdell)
  R  : 3-fold screw symmetry    (Ramsdell)
  S3P: S3-palindromic           (our notion)

Question: among the S3P, how many are H? how many are R? how many neither?

If there are "S3P but neither H nor R", then S3P is strictly finer than (H U R).
"""

from sw.common import (
    chain_to_word, is_3fold_screw, is_periodic,
    is_s3_palindromic, is_strict_palindrome, load_canonical,
)


def summarize(k):
    """For a level k, classify the periodic words by (H, R)."""
    chains = load_canonical(1, k)
    out = {
        "total": len(chains),
        "periodic": 0,
        "H": 0, "R": 0, "S3P": 0,
        "H_and_R": 0,
        "S3P_only": 0,     # S3P but neither H nor R  -> genuine refinement
        "R_only": 0,       # R but not S3P            -> does it exist? (Ramsdell says yes)
        "H_only": 0,       # H but not S3P            -> impossible (H => S3P)
        "examples_S3P_only": [],
        "examples_R_only": [],
    }
    for ch in chains:
        w = chain_to_word(ch)
        if not is_periodic(w):
            continue
        out["periodic"] += 1
        H = is_strict_palindrome(w)
        R = is_3fold_screw(w)
        S = is_s3_palindromic(w)
        out["H"] += H
        out["R"] += R
        out["S3P"] += S
        if H and R:
            out["H_and_R"] += 1
        if S and not H and not R:
            out["S3P_only"] += 1
            if len(out["examples_S3P_only"]) < 3:
                out["examples_S3P_only"].append(w)
        if R and not S:
            out["R_only"] += 1
            if len(out["examples_R_only"]) < 3:
                out["examples_R_only"].append(w)
        if H and not S:
            out["H_only"] += 1
    return out


if __name__ == "__main__":
    print("=" * 100)
    print("TEST 5 - Ramsdell refinement (periodic words, option 1)")
    print("=" * 100)
    print()
    print("H  : strict palindrome (Ramsdell)")
    print("R  : 3-fold screw symmetry (Ramsdell)")
    print("S3P: S3-palindromic (our notion)")
    print()
    print(f"{'k':>3} | {'per.':>7} | {'H':>3} | {'R':>3} | {'S3P':>4} | "
          f"{'HnR':>4} | {'S3P-only':>9} | {'R-only':>6} | {'H-only':>6}")
    print("-" * 100)

    results = {}
    for k in range(2, 12):
        try:
            r = summarize(k)
        except FileNotFoundError:
            continue
        results[k] = r
        print(f"{k:>3} | {r['periodic']:>7} | {r['H']:>3} | {r['R']:>3} | "
              f"{r['S3P']:>4} | {r['H_and_R']:>4} | "
              f"{r['S3P_only']:>9} | {r['R_only']:>6} | {r['H_only']:>6}")

    print()
    print("=" * 100)
    print("EXAMPLES (periodic words)")
    print("=" * 100)
    for k, r in results.items():
        print(f"\nk = {k}")
        if r["examples_S3P_only"]:
            print(f"  S3P but neither H nor R (genuine refinement):")
            for w in r["examples_S3P_only"]:
                print(f"    {w}")
        if r["examples_R_only"]:
            print(f"  R but not S3P (contradicts 'weak S3P superset R'):")
            for w in r["examples_R_only"]:
                print(f"    {w}")

    print()
    print("=" * 100)
    print("READING")
    print("=" * 100)
    print("""
- If 'S3P-only' > 0 for some k, then S3P does NOT reduce to (H U R):
  it captures words that Ramsdell would not classify as H or as R.
- If 'R-only' > 0, then S3P and R are incomparable (as the paper claims).
- 'H-only' must always be 0: every strict palindrome is S3P with sigma = id.
""")
