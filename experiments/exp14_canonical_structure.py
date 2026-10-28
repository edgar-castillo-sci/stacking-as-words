#!/usr/bin/env python3
"""
Test 14: structure of the canonical words.

The words in data/n*/canonicas.txt are kappa(a), the minimum of the
G-orbit of chain a. This test analyzes their structure as words:

  1. Do they always start with 'A'?
  2. Distribution of the first/last character.
  3. Is pi_k(kappa(a)) the lex-min of the G-orbit of pi_k(a)?
  4. Growth of |canonical(k)| (Burnside validation).
  5. Cell distribution (must match Test 3).
"""

from collections import Counter

from sw.common import S3, apply_perm, classify, chain_to_word, load_canonical


def orbit_words(w):
    """The 6 images of w under S3 plus their reversals (G-orbit on words)."""
    orbit = set()
    for p in S3:
        wp = apply_perm(w, p)
        orbit.add(wp)
        orbit.add(wp[::-1])
    return orbit


if __name__ == "__main__":
    print("=" * 100)
    print("TEST 14 - Structure of canonical words")
    print("=" * 100)
    print()

    for k in range(2, 9):
        chains = load_canonical(1, k)
        words = [chain_to_word(ch, convention="star_or_plus0") for ch in chains]

        first = Counter(w[0] for w in words)
        last = Counter(w[-1] for w in words)
        cells = Counter(classify(w) for w in words)

        n_min_word = sum(1 for w in words if w == min(orbit_words(w)))
        n_starts_A = first.get("A", 0)

        print(f"\n-- k = {k}  (|canonical| = {len(chains)}) --")
        print(f"  first char: {dict(first)}")
        print(f"  last  char: {dict(last)}")
        print(f"  start with A: {n_starts_A}/{len(words)}"
              f"  {'OK' if n_starts_A == len(words) else 'FAIL'}")
        label = "OK (commutes)" if n_min_word == len(words) else "differs (no commute)"
        print(f"  pi(kappa(a)) = min_word of G-orbit: {n_min_word}/{len(words)}"
              f"  {label}")
        print(f"  cells: {dict(cells)}")
