#!/usr/bin/env python3
"""
Test 10: mapa de las 16 regiones del diagrama de Venn de (H, R, S3P, P).

Para cada k, enumera una órbita por clase G y clasifica en cuál de las
2^4 = 16 regiones cae, según cuatro propiedades Booleanas:

  H  : palíndromo estricto (w = reverse(w))
  R  : 3-fold screw (σ(w) = rot^m(w) para algún 3-ciclo σ y m ≥ 1)
  S  : S3-palindrómica (∃ σ ∈ S3: σ(w) = reverse(w))
  P  : periódica (w = u^n, n ≥ 2)

Predicciones lógicas:
  - H  ⇒ S3P    (σ = id). Así que H ∧ ¬S3P debe ser SIEMPRE vacía.
  - H ∧ P es la celda "periódica palindrómica" estricta (⊂ PP).
  - R ⊆ S3P bajo la definición estándar (Test 5). Si aparece R ∧ ¬S3P,
    es una contradicción empírica que vale la pena investigar.
"""

from collections import Counter
from common import (
    is_3fold_screw, is_periodic, is_s3_palindromic,
    is_strict_palindrome, chain_to_word, load_canonical,
)


def classify_region(w):
    """Devuelve la 4-tupla (H, R, S, P) de la palabra."""
    return (
        is_strict_palindrome(w),
        is_3fold_screw(w),
        is_s3_palindromic(w),
        is_periodic(w),
    )


def label(region):
    """Etiqueta legible: H·R·S·P, etc."""
    h, r, s, p = region
    parts = []
    parts.append("H" if h else "¬H")
    parts.append("R" if r else "¬R")
    parts.append("S" if s else "¬S")
    parts.append("P" if p else "¬P")
    return "·".join(parts)


if __name__ == "__main__":
    print("=" * 90)
    print("TEST 10 — Diagrama de Venn de (H, R, S3P, P)")
    print("=" * 90)
    print()
    print("H = palíndromo estricto, R = 3-fold screw,")
    print("S = S3-palindrómica,   P = periódica")
    print()

    for k in range(2, 12):
        chains = load_canonical(1, k)
        counts = Counter()
        for ch in chains:
            w = chain_to_word(ch)
            counts[classify_region(w)] += 1

        print(f"\n── k = {k}  ({len(chains)} órbitas) ──")
        # Ordenar por la tupla (con F < T)
        for region in sorted(counts, key=lambda r: tuple(int(x) for x in r)):
            print(f"  {label(region):<20}: {counts[region]:>5}")

        # Verificaciones lógicas
        bad = [(r, n) for r, n in counts.items()
               if r[0] and not r[2]]  # H ∧ ¬S3P
        if bad:
            print(f"  ⚠ IMPOSIBLE: H∧¬S3P = {bad} (bug lógico)")

        r_s = [(r, n) for r, n in counts.items() if r[1] and not r[2]]
        if r_s:
            print(f"  ℹ R∧¬S3P no vacía: {r_s}  (¡contradice Test 5!)")

    # ── Resumen: regiones activas por k ──────────────────────────
    print()
    print("=" * 90)
    print("RESUMEN — regiones activas por k")
    print("=" * 90)
    print()
    print(f"{'región':<22}" + "".join(f"k={k:<3}" for k in range(2, 12)))
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
        (False, True, False, True),   # esperado vacío (R⊆S3P)
        (False, True, False, False),  # esperado vacío
        (False, False, False, True),  # Pp puro (AABAAB, etc.)
        (False, False, False, False), # Ap
    ]
    for region in all_regions:
        row = f"{label(region):<22}"
        for k in range(2, 12):
            chains = load_canonical(1, k)
            present = any(classify_region(chain_to_word(ch)) == region
                          for ch in chains)
            row += "✓  " if present else "·  "
        print(row)

    print()
    print("Leyenda: ✓ = región no vacía en ese k; · = vacía.")
