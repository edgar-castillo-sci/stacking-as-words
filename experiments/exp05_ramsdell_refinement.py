#!/usr/bin/env python3
"""
Test 5: refinamiento cuantitativo de Ramsdell.

Para las palabras PERIÓDICAS (las que corresponden a politipos de Ramsdell),
clasifica cada una por:
  H  : palíndromo estricto        (Ramsdell)
  R  : simetría 3-fold helicoidal (Ramsdell)
  S3P: S3-palindrómica            (nuestra noción)

Pregunta: entre las S3P, ¿cuántas son H? ¿cuántas R? ¿cuántas ni una ni otra?

Si hay "S3P pero ni H ni R", S3P es estrictamente más fina que (H ∪ R).
"""

import sys
from collections import Counter, defaultdict

from sw.common import (
    classify, chain_to_word, is_3fold_screw, is_periodic,
    is_s3_palindromic, is_strict_palindrome, load_canonical,
)


def resumen(k):
    """Para un nivel k, clasifica las palabras periódicas por (H, R)."""
    chains = load_canonical(1, k)
    out = {
        "total": len(chains),
        "periodic": 0,
        "H": 0, "R": 0, "S3P": 0,
        "H_and_R": 0,
        "S3P_only": 0,     # S3P pero ni H ni R  → refinamiento genuino
        "R_only": 0,       # R pero no S3P       → ¿existe? (Ramsdell dice sí)
        "H_only": 0,       # H pero no S3P       → imposible (H ⇒ S3P)
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
    print("TEST 5 — Refinamiento de Ramsdell (palabras periódicas, opción 1)")
    print("=" * 100)
    print()
    print("H  : palíndromo estricto (Ramsdell)")
    print("R  : simetría 3-fold helicoidal (Ramsdell)")
    print("S3P: S3-palindrómica (nuestra noción)")
    print()
    print(f"{'k':>3} | {'periód':>7} | {'H':>3} | {'R':>3} | {'S3P':>4} | "
          f"{'H∩R':>4} | {'S3P-only':>9} | {'R-only':>6} | {'H-only':>6}")
    print("-" * 100)

    resultados = {}
    for k in range(2, 12):
        try:
            r = resumen(k)
        except FileNotFoundError:
            continue
        resultados[k] = r
        print(f"{k:>3} | {r['periodic']:>7} | {r['H']:>3} | {r['R']:>3} | "
              f"{r['S3P']:>4} | {r['H_and_R']:>4} | "
              f"{r['S3P_only']:>9} | {r['R_only']:>6} | {r['H_only']:>6}")

    print()
    print("=" * 100)
    print("EJEMPLOS (palabras periódicas)")
    print("=" * 100)
    for k, r in resultados.items():
        print(f"\nk = {k}")
        if r["examples_S3P_only"]:
            print(f"  S3P pero ni H ni R (refinamiento genuino):")
            for w in r["examples_S3P_only"]:
                print(f"    {w}")
        if r["examples_R_only"]:
            print(f"  R pero no S3P (contradice 'S3P débil ⊃ R'):")
            for w in r["examples_R_only"]:
                print(f"    {w}")

    print()
    print("=" * 100)
    print("LECTURA")
    print("=" * 100)
    print("""
- Si 'S3P-only' > 0 en algún k, entonces S3P NO se reduce a (H ∪ R):
  captura palabras que Ramsdell no clasificaría como H ni como R.
- Si 'R-only' > 0, entonces S3P y R son incomparables (como dice el paper).
- 'H-only' debe ser siempre 0: todo palíndromo estricto es S3P con σ = id.
""")
