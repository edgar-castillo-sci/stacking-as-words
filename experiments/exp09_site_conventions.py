#!/usr/bin/env python3
"""
Test 9: scenario analysis for the distinguished-site convention.

For options 1-8, we try several conventions and check whether they are
S3-equivariant:  pi(sigma . r) = sigma . pi(r)  for every row r and sigma in S3.

Options 6 and 8 (1T, no +0) are the tricky ones.
"""

from collections import Counter

from sw.common import S3, apply_perm
from caugjam import rows_for_option


def letter_position_plus0(row):
    """The +0 is the distinguished site."""
    for pos, tok in enumerate(row):
        if tok == "+0":
            return pos
    return None


def letter_position_star(row):
    """The *x is the distinguished site. None if absent."""
    for pos, tok in enumerate(row):
        if tok.startswith("*"):
            return pos
    return None


def letter_position_first_star_or_plus0(row):
    """Look for *x first; otherwise +0."""
    p = letter_position_star(row)
    if p is not None:
        return p
    return letter_position_plus0(row)


def letter_position_rarest(row):
    """The token that does not repeat (the rarest one)."""
    c = Counter(row)
    rarest = min(c, key=lambda t: (c[t], t))
    return row.index(rarest)


CONVENTIONS = {
    "std (+0)":       letter_position_plus0,
    "star (*x)":      letter_position_star,
    "star_or_plus0":  letter_position_first_star_or_plus0,
    "rarest":         letter_position_rarest,
}


def permute_row(row, sigma):
    """Apply sigma to the COLUMNS (positions) of the row."""
    mp = dict(zip("ABC", sigma))
    inv = {v: i for i, v in enumerate("ABC")}
    new_row = [None, None, None]
    for i, tok in enumerate(row):
        new_letter = mp["ABC"[i]]
        new_i = inv[new_letter]
        new_row[new_i] = tok
    return tuple(new_row)


def check_equivariance(option, convention):
    """Verify pi(sigma.r) = sigma.pi(r) for all rows r and sigma in S3."""
    rows = rows_for_option(option)
    fails = []
    for r in rows:
        r = tuple(r)
        p = convention(r)
        if p is None:
            fails.append(("no-letter", r))
            continue
        sigma_p = "ABC"[p]
        for sigma in S3:
            r_perm = permute_row(r, sigma)
            p_after = convention(r_perm)
            if p_after is None:
                fails.append(("no-letter-after", r, sigma, r_perm))
                continue
            sigma_p_str = apply_perm(sigma_p, sigma)
            if "ABC"[p_after] != sigma_p_str:
                fails.append((r, sigma, sigma_p_str, r_perm, "ABC"[p_after]))
    return fails


if __name__ == "__main__":
    print("=" * 100)
    print("TEST 9 - Scenario analysis for the distinguished-site convention")
    print("=" * 100)
    print()
    print("We verify  pi(sigma.r) = sigma.pi(r)  for every row r and sigma in S3.")
    print("A convention is S3-equivariant if it passes for all rows.")
    print()

    for option in range(1, 9):
        print(f"\n-- Option {option} -----------------------------")
        for name, conv in CONVENTIONS.items():
            fails = check_equivariance(option, conv)
            if not fails:
                print(f"  {name:>16}: OK, equivariant")
            else:
                print(f"  {name:>16}: FAIL, {len(fails)} failures")
                for f in fails[:2]:
                    print(f"                   {f}")
