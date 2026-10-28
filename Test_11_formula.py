#!/usr/bin/env python3
"""
Test 11: fórmula combinatoria para |Pp(k)|_G.

Conjetura derivada de Test 3:

  |Pp(k)|_G = Σ_{d | k, 3 ≤ d < k} N'(d)

donde N'(d) se calcula por inversión de Möbius a partir de

  A'(d) = |Pp(d)|_G + |Ap(d)|_G   (órbitas G de palabras no-S3P)

y

  A'(d) = Σ_{e | d} N'(e)   ⇒   N'(d) = Σ_{e | d} μ(d/e) A'(e).

Base conceptual: w = u^m es S3P ⇔ u es S3P (el raíz primitivo
preserva la propiedad), y el "período efectivo" de w es |u|.

Verificamos la conjetura para k = 2..12 (12 es la predicción nueva:
si Test 3 extendido a k=12 da |Pp(12)|_G = 56, la fórmula queda
confirmada).
"""

from collections import Counter
from common import (
    classify, chain_to_word, load_canonical,
)


# ── Möbius y divisores ───────────────────────────────────────────────
def moebius(n):
    if n == 1:
        return 1
    result = 1
    p = 2
    while p * p <= n:
        if n % p == 0:
            n //= p
            if n % p == 0:
                return 0
            result = -result
        p += 1
    if n > 1:
        result = -result
    return result


def divisors(n):
    return [d for d in range(1, n + 1) if n % d == 0]


# ── A'(d) por conteo directo ────────────────────────────────────────
def compute_A_prime(k_max):
    """A'(d) = |Pp(d)|_G + |Ap(d)|_G, para d = 1..k_max."""
    A = {}
    for d in range(1, k_max + 1):
        if d == 1:
            A[1] = 0
            continue
        chains = load_canonical(1, d)
        count = 0
        for ch in chains:
            w = chain_to_word(ch)
            if not __import__("common").is_s3_palindromic(w):
                count += 1
        A[d] = count
    return A


# ── N'(d) por Möbius ────────────────────────────────────────────────
def compute_N_prime(A, k_max):
    N = {}
    for d in range(1, k_max + 1):
        N[d] = sum(moebius(d // e) * A[e] for e in divisors(d))
    return N


# ── |Pp(k)|_G por la fórmula ────────────────────────────────────────
def predict_Pp(N, k):
    """|Pp(k)|_G = Σ_{d | k, 3 ≤ d < k} N'(d)."""
    return sum(N[d] for d in divisors(k) if 3 <= d < k)


# ── |Pp(k)|_G real ──────────────────────────────────────────────────
def actual_Pp(k):
    chains = load_canonical(1, k)
    return sum(1 for ch in chains
               if classify(chain_to_word(ch)) == "Pp")


# ── Main ────────────────────────────────────────────────────────────
if __name__ == "__main__":
    K_MAX = 12
    print("=" * 80)
    print(f"TEST 11 — Fórmula |Pp(k)|_G = Σ_{{d|k, 3≤d<k}} N'(d)   (k_max = {K_MAX})")
    print("=" * 80)
    print()

    print("Paso 1: A'(d) = |Pp(d)|_G + |Ap(d)|_G  (órbitas G de no-S3P)")
    A = compute_A_prime(K_MAX)
    for d in sorted(A):
        print(f"  A'({d:>2}) = {A[d]:>7}")

    print()
    print("Paso 2: N'(d) por inversión de Möbius")
    N = compute_N_prime(A, K_MAX)
    for d in sorted(N):
        print(f"  N'({d:>2}) = {N[d]:>7}")

    print()
    print("Paso 3: comparar |Pp(k)|_G real vs predicho")
    print()
    print(f"{'k':>3} | {'predicho':>10} | {'real':>7} | {'match':>7} | divisores d")
    print("-" * 70)
    all_ok = True
    for k in range(2, K_MAX + 1):
        pred = predict_Pp(N, k)
        real = actual_Pp(k)
        ds = [d for d in divisors(k) if 3 <= d < k]
        match = "✓" if pred == real else "✗"
        if pred != real:
            all_ok = False
        print(f"{k:>3} | {pred:>10} | {real:>7} | {match:>7} | {ds}")

    print()
    print("=" * 80)
    if all_ok:
        print("✓ Fórmula confirmada para todo k ≤ 12.")
    else:
        print("✗ La fórmula falla en algunos k. Investigar.")
    print("=" * 80)
    print()

    # ── Predicciones "extrapoladas" para k = 13..24 ───────────────────
    print("BONUS — predicciones |Pp(k)|_G para k = 13..24")
    print("(válidas si la fórmula se cumple; requieren N'(d) para d | k, d ≥ 13")
    print("→ no calculadas aquí; ver 'pendiente' abajo)")
    print()
    print("Nota: para predecir k=16 se necesita N'(4) y N'(8) (ya tenemos).")
    print("Para predecir k=18 se necesita N'(3), N'(6), N'(9). N'(9) requiere A'(9).")
    print("Para predecir k=24 se necesita N'(3), N'(4), N'(6), N'(8), N'(12).")
    print()
    print("Predicciones concretas:")
    for k, ds in [(13, []), (14, [7]), (15, [3, 5]), (16, [4, 8]),
                  (18, [3, 6, 9]), (20, [4, 5, 10]), (21, [3, 7]),
                  (22, [11]), (24, [3, 4, 6, 8, 12])]:
        if all(d in N for d in ds):
            pred = sum(N[d] for d in ds)
            print(f"  k={k:>2}: {pred:>10}   (d ∈ {ds})")
        else:
            print(f"  k={k:>2}: pendiente (falta N' para d ∈ {ds})")
