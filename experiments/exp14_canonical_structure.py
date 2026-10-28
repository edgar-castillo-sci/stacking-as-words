#!/usr/bin/env python3
"""
Test 14: estructura de las palabras canónicas.

Las palabras que están en datos/n*/canonicas.txt son κ(a), el mínimo
de la órbita G de la cadena a. Este test analiza su estructura como
palabras:

  1. ¿Siempre empiezan con 'A'?
  2. Distribución del primer/último carácter.
  3. ¿π_k(κ(a)) es el lex-min de la órbita G de π_k(a)?
  4. Crecimiento de |canónicas(k)| (validación de Burnside).
  5. Distribución de celdas (debe coincidir con Test 3).
"""

from collections import Counter
from sw.common import (
    classify, chain_to_word, load_canonical,
)


def orbit_words(w):
    """Las 6 imágenes de w bajo S3 más sus reversos (órbita de G en palabras)."""
    from common import S3, apply_perm
    orbit = set()
    for p in S3:
        wp = apply_perm(w, p)
        orbit.add(wp)
        orbit.add(wp[::-1])
    return orbit


if __name__ == "__main__":
    print("=" * 100)
    print("TEST 14 — Estructura de las palabras canónicas")
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

        print(f"\n── k = {k}  (|canónicas| = {len(chains)}) ──")
        print(f"  primer carácter: {dict(first)}")
        print(f"  último carácter: {dict(last)}")
        print(f"  empiezan con A:  {n_starts_A}/{len(words)}"
              f"  {'✓' if n_starts_A == len(words) else '✗'}")
        label = "✓ (comuta)" if n_min_word == len(words) else "≠ (no comuta)"
        print(f"  π(κ(a)) = min_word órbita G: {n_min_word}/{len(words)}"
              f"  {label}")
        print(f"  celdas: {dict(cells)}")
