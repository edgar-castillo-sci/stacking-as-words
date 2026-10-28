#!/usr/bin/env python3
"""
Test 15: probabilidad de cada celda para palabras aleatorias.

Toma N muestras uniformes de {A,B,C}^k para k = 2..20 y reporta la
fracción en cada celda. Compara con la distribución de órbitas
(Test 7): son parecidas para celdas "genéricas" (Ap), pero distintas
para celdas estructuradas (PP, Pp, pP) porque las órbitas pequeñas
sobre-pesan esas celdas.

Sin dependencias de poda: todo es combinatoria directa, rápido.
"""

import random
from common import classify, is_periodic, is_s3_palindromic

CELLS = ["PP", "Pp", "pP", "Ap"]
N_SAMPLES = 100_000


def random_word(k, rng):
    return "".join(rng.choice("ABC") for _ in range(k))


if __name__ == "__main__":
    rng = random.Random(42)

    print("=" * 100)
    print(f"TEST 15 — Distribución de celdas para {N_SAMPLES:,} palabras aleatorias")
    print("=" * 100)
    print()
    print(f"{'k':>3} | " + " | ".join(f"P({c})" for c in CELLS) + " | P(S3P)"
          " | P(per)"
          )
    print("-" * 90)

    for k in range(2, 21):
        counts = {c: 0 for c in CELLS}
        for _ in range(N_SAMPLES):
            w = random_word(k, rng)
            counts[classify(w)] += 1
        fracs = {c: counts[c] / N_SAMPLES for c in CELLS}
        p_s3p = fracs["PP"] + fracs["pP"]
        p_per = fracs["PP"] + fracs["Pp"]
        print(f"{k:>3} | " +
              " | ".join(f"{fracs[c]:>6.3f}" for c in CELLS) +
              f" | {p_s3p:>7.3f} | {p_per:>6.3f}")

    print()
    print("=" * 100)
    print("LECTURA")
    print("=" * 100)
    print("""
- P(Ap) → 1, como en Test 7.
- P(S3P) ~ 6·3^{ceil(k/2)} / 3^k = 6·3^{-floor(k/2)}.
- P(per) ~ O(3^{-k/2}) (dominado por período k/2).
- Para k grande, ambos decaen exponencialmente.
- Comparar con Test 7: las celdas estructuradas (PP, pP) aparecen
  sobrerrepresentadas en órbitas (porque tienen estabilizadores grandes).
""")
